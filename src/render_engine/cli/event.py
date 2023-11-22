import importlib
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from rich.console import Console
from watchdog.events import FileSystemEvent, RegexMatchingEventHandler
from watchdog.observers import Observer

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


class RegExHandler(RegexMatchingEventHandler):
    """
    Initializes a handler that looks for file changes in a directory (`dir_to_watch`), as
    well as creates a server to serve files in a given directory (`dir_to_serve`). The
    class contains helper methods to manage server events in a thread.

    Meanwhile, the `watch` method uses an instance of this handler class to monitor for file
    changes. The files to be monitored are all files/directories within the `dir_to_watch`,
    which defaults to the project root directory. The `patterns` and `ignore_patterns` are used
    to filter the files to be monitored using regular expressions.

    Params:
        server_address: A tuple of the form (host, port)
        dir_to_serve: The directory to serve
        app: A Site instance
        dir_to_watch: The directory to watch
        patterns: A list of regular expressions to filter files
        ignore_patterns: A list of regular expressions to ignore
    """

    def __init__(
        self,
        server_address: tuple[int, int],
        dir_to_serve: str,
        app: Site,
        module_site: str,
        dir_to_watch: str = ".",
        patterns: [list[str] | None] = None,
        ignore_patterns: [list[str] | None] = None,
        *args,
        **kwargs,
    ):
        self.p = None
        self._server = spawn_server
        self.server_address = server_address
        self.dir_to_serve = (dir_to_serve,)
        self.app = app
        self.module_site = module_site
        self.dir_to_watch = dir_to_watch
        self.patterns = patterns
        self.ignore_patterns = ignore_patterns
        super().__init__(*args, regexes=patterns, ignore_regexes=ignore_patterns, **kwargs)

    def start_server(self):
        console.print(
            f"[bold green]Spawning server on http://{self.server_address[0]}:{self.server_address[1]}[/bold green]"
        )
        self._server = spawn_server(self.server_address, self.dir_to_serve[0])
        self._thread = threading.Thread(target=self._server.serve_forever)
        self._thread.start()

    def stop_server(self):
        console.print("[bold red]Stopping server[/bold red]")
        self._server.shutdown()
        self._thread.join()

    def rebuild(self):
        console.print("[bold purple]Reloading and Rebuilding site...[/bold purple]")
        import_path = self.module_site[0]
        module = importlib.import_module(import_path)
        importlib.reload(module)
        self.app.render()

    def on_any_event(self, event: FileSystemEvent):
        if event.is_directory:
            return None
        self.rebuild()

    def watch(self):
        """
        This function `watch` starts the server on the output path (`dir_to_serve`)
        and monitors the specified directory (`dir_to_watch`) for changes.

        After it starts the server, it "waits" and monitors the directory for
        changes. If a change is detected, the `on_any_event` method is called,
        which will stop the server and rebuild the site before restarting the
        server.

        If a KeyboardInterrupt is raised, it stops the observer and server.
        """

        console.print(f"[yellow]Serving {self.app.output_path}[/yellow]")

        observer = Observer()
        observer.schedule(self, self.dir_to_watch, recursive=True)
        self.start_server()
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("watcher terminated by keystroke")
            observer.stop()
            self.stop_server()
        observer.join()
        console.print("[bold red]FIN![/bold red]")
