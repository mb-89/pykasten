from pykasten.guikasten import dk
from pykasten.guikasten import exec as gkexec
from pykasten.guikasten.mainwindow import Win as mw


class Gui(dk):
    def __init__(self, examplebrowser):
        super().__init__("Example browser")
        self.eb = examplebrowser
        self.constructed = False

    def construct(self):
        if self.constructed:
            return

        self.constructed = True

    def exec(self, parent=None, title=""):
        self.construct()
        if parent is None:
            parent = mw(title=title)
        parent.addDock(self, "top")
        parent.show()
        gkexec()
