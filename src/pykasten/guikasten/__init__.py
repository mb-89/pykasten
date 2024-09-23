"""The guikasten contains snippets and classes used for gui-programming.

It is recommended that you import it dynamically only when you really need it,
since the main packages it relies on (PySide6 and pyqtgraph) are heavy dependencies.
Code outside the gui_kasten should be independent of those.
"""

# isort: skip_file

qt = None
pg = None
dk = None
da = None


class ShortcutKasten:
    """A container for shortcuts."""

    def __init__(self) -> None:
        self.shortcuts = []

    def addShortcut(self, parent, fn, shortcut, descr):
        """Add shortcut to a global list."""
        self.shortcuts.append((parent, fn, shortcut, descr))


def import_deps():
    """Do the heavy importing.

    The idea is that the user imports guikasten on demand, which triggers these imports.
    """
    import PySide6  # noqa: F401
    import pyqtgraph
    from pyqtgraph.dockarea.Dock import Dock
    from pyqtgraph.dockarea.DockArea import DockArea

    global qt, pg, dk, da
    qt = pyqtgraph.Qt
    pg = pyqtgraph

    dk = Dock
    da = DockArea

    app = pg.mkQApp()
    app.sk = ShortcutKasten()  # pyright: ignore


def getapp():
    """Return the current app instance."""
    return pg.mkQApp()  # pyright: ignore


def addShortcut(parent, fn, shortcut, descr):
    """Add a Shortcut to the global collection."""
    getapp().sk.addShortcut(parent, fn, shortcut, descr)  # pyright: ignore


def exec():
    """Execute qt event loop."""
    app = pg.mkQApp()  # pyright: ignore
    for parent, fn, shortcut, descr in app.sk.shortcuts:  # pyright: ignore
        a = qt.QtGui.QAction(parent)  # pyright: ignore
        a.setShortcut(shortcut)
        a.setText(descr)
        a.triggered.connect(fn)
        parent.addAction(a)
    app.exec()


import_deps()
