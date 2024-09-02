import importlib
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import watchfiles
from rich.console import Console

from render_engine import Site

console = Console()


def spawn_server(server_address: tuple[str, int], directory: str) -> ThreadingHTTPServer:
    """
        Create and return an instance of ThreadingHTTPServer that serves files
    from the specified directory.

    Params:
        server_address: A tuple of a string and integer representing the server address (host, port).
        directory: A string representing the directory from which the server should serve files.
    """

    class _RequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    def _httpd() -> ThreadingHTTPServer:
        return ThreadingHTTPServer(server_address, _RequestHandler)

    return _httpd()


class ServerEventHandler:
    """
    Initializes a handler that looks for file changes in a directory (`dirs_to_watch`), as
    well as creates a server to serve files in a given directory. The
    class contains helper methods to manage server events in a thread.

    Meanwhile, the `watch` method uses an instance of this handler class to monitor for file
    changes. The files to be monitored are all files/directories within the `dirs_to_watch`,
    which defaults to the project root directory. The `patterns` and `ignore_patterns` are used
    to filter the files to be monitored using regular expressions.

    Params:
        server_address: A tuple of the form (host, port)
        site: A Site instance
        dirs_to_watch: The directories to watch
        patterns: A list of regular expressions to filter files
        ignore_patterns: A list of regular expressions to ignore
    """

    def __init__(
        self,
        server_address: tuple[str, int],
        import_path: str,
        site: Site,
        dirs_to_watch: str | None = None,
        patterns: list[str] | None = None,
        ignore_patterns: list[str] | None = None,
        *args,
        **kwargs,
    ) -> None:
        self.p = None
        self.server_address = server_address
        self.import_path = import_path
        self.site = site
        self.dirs_to_watch = dirs_to_watch
        self.patterns = patterns
        self.ignore_patterns = ignore_patterns

    def start_server(self) -> None:
        if not getattr(self, "server", False):
            console.print(
                f"[bold green]Spawning server on http://{self.server_address[0]}:{self.server_address[1]}[/bold green]"
            )
            self.server = spawn_server(self.server_address, self.site.output_path)
        self._thread = threading.Thread(target=self.server.serve_forever)
        self._thread.start()

    def stop_server(self) -> None:
        console.print("[bold red]Stopping server[/bold red]")
        self.server.shutdown()
        self._thread.join()

    def rebuild(self) -> None:
        console.print("[bold purple]Reloading and Rebuilding site...[/bold purple]")
        module = importlib.import_module(self.import_path)
        importlib.reload(module)
        self.site.render()

    def stop_watcher(self) -> bool:
        """
        logic to stop the watcher.

        By default this code looks for the KeyboardInterrupt
        """

        # return if keyboard interrupt is raised
        try:
            time.sleep(1)
            return False
        except KeyboardInterrupt:
            return True

    def watch(self) -> None:
        """
        This function `watch` starts the server on the output path
        and monitors the specified directories in (`dirs_to_watch`) for changes.

        After it starts the server, it "waits" and monitors the directory for
        changes. If a change is detected, the `on_any_event` method is called,
        which will stop the server and rebuild the site before restarting the
        server.

        If a KeyboardInterrupt is raised, it stops the observer and server.
        """

        console.print(f"[yellow]Serving {self.site.output_path}[/yellow]")
        while not self.stop_watcher():
            if self.dirs_to_watch:
                for _ in watchfiles.watch(*self.dirs_to_watch):
                    self.rebuild()

    def __enter__(self):
        """Starting Context manager for the class"""
        try:
            self._thread.server_close()
        except AttributeError:
            pass
        self.start_server()
        self.watch()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Stopping Context manager for the class"""

        self.stop_server()
        console.print("[bold red]FIN![/bold red]")
        return None
