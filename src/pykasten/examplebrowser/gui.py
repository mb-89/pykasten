"""GUI parts of the examplebrowser."""

from pykasten.guikasten import dk
from pykasten.guikasten import exec as gkexec
from pykasten.guikasten.mainwindow import Win as mw


class Gui(dk):
    """The GUI for the examplebrowser."""

    def __init__(self, examplebrowser):
        super().__init__("Example browser")
        self.eb = examplebrowser
        self.constructed = False

    def construct(self):
        """Construct the gui contents."""
        if self.constructed:
            return

        self.constructed = True

    def exec(self, parent=None, title=""):
        """Execute the GUI, create a parent widget if we have none."""
        self.construct()
        if parent is None:
            parent = mw(title=title)
        parent.addDock(self, "top")
        parent.show()
        gkexec()
