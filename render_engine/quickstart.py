from pathlib import Path
import typer


def _main(output_dir: str="output", static_dir: str="static", content_path: str="content"):
    # Create Folders
    # Test Folders Created
    # Test Folders Do Not Overwrite
    # Test Folders Do Not Error if exists already
    Path(output_dir).mkdir(exist_ok=True)
    Path(content).mkdir(exist_ok=True)
    Path(static).mkdir(exist_ok=True)

if __name__ == "__main__":

    _main()
