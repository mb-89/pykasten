"""Utility to browse, execute and test python code examples."""

from pathlib import Path


class ExampleBrowser:
    """Main Class for the example browser."""

    def __init__(self, exampledir: Path, docudir: Path | None = None):
        self.exampledir = exampledir
        self.docudir = docudir

    def showGui(self, parentWidget=None):
        """Show the Examplebrowser."""
        from pykasten.examplebrowser import gui

        g = gui.Gui(self)
        title = "pykasten examples"
        g.exec(parent=parentWidget, title=title)


def runExample(src: Path | str, args: dict = {}) -> int:
    """Run a given example."""
    print(src)
    print(args)
    return -1
