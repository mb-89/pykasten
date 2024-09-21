"""Utility to browse, execute and test python code examples."""

from pathlib import Path


class ExampleBrowser:
    """Main Class for the example browser."""

    def __init__(self, exampledir: Path, docudir: Path | None = None):
        self.exampledir = exampledir
        self.docudir = docudir

    def showGui(self, parentWidget=None):
        """Show the Examplebrowser."""
        pass


def runExample(src: Path | str, args: dict = {}):
    """Run a given example."""
    print(src)
    print(args)
