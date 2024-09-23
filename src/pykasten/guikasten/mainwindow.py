"""The mainwindow is a class that hosts Docks and provide some infrastructure fns."""

from pathlib import Path

import pykasten.logkasten as lk
from pykasten.guikasten import addShortcut, da, qt
from pykasten.logkasten.gui import LogDock


class Win(qt.QtWidgets.QMainWindow):
    """Class for the mainwindow."""

    def __init__(self, title="pykasten mainwindow"):
        super().__init__()
        self.constructed = False
        self._dockList = []
        self.loghandlers = []
        self.setWindowTitle(title)
        self.title = title

    def construct(self):
        """Construct the gui contents."""
        if self.constructed:
            return

        self.da = da()
        self.setCentralWidget(self.da)

        ld = LogDock(Path("$TMP") / f"{self.title}.log")
        self.addDock(ld)

        self.resize(800, 600)

        while self._dockList:
            x = self._dockList.pop(0)
            try:
                x[0].construct()
            except AttributeError:
                pass
            self.da.addDock(*x)

        sb = StatusBar(logDock=ld)
        self.setStatusBar(sb)
        self.sb = sb

        self.constructed = True

    def show(self):
        """Show the gui."""
        self.construct()

        lk.setDstObj(self)
        lk.setTimeInMs(True)

        super().show()

    def addDock(self, *args):
        """Add a dock to the gui."""
        self._dockList.append(args)

    def log_acceptStreamHandler(self, h):
        """Accept a log streaming handler, map it to qt signals."""
        h.emitter.sig.connect(self.sb.setText)
        self.loghandlers.append(h)

    def log_removeStreamHandler(self, h):
        """Remove the given handler."""
        self.loghandlers.remove(h)


class StatusBar(qt.QtWidgets.QStatusBar):
    """A statusbar for the main gui."""

    def __init__(self, logDock=None):
        super().__init__()
        W = 20

        w = qt.QtWidgets.QWidget()
        la = qt.QtWidgets.QHBoxLayout()
        la.setSpacing(0)
        la.setContentsMargins(0, 0, 0, 0)
        w.setLayout(la)

        if logDock is not None:
            logbut = qt.QtWidgets.QPushButton("L")
            logbut.setMaximumWidth(W)
            logbut.setToolTip("logging. Press to toggle log [CTRL+C]")
            logbut.setCheckable(True)
            logbut.clicked.connect(lambda x: logDock.setHidden(not x))
            la.addWidget(logbut)
            addShortcut(self, logbut.click, "Ctrl+L", "toggle log widget")

        self.b1 = (x := qt.QtWidgets.QPushButton("C"))
        x.setMaximumWidth(W)
        self.b3 = (x := qt.QtWidgets.QPushButton("W"))
        x.setMaximumWidth(W)

        la.addWidget(self.b1)
        la.addWidget(self.b3)

        self.addPermanentWidget(w)

        w = qt.QtWidgets.QLabel()
        self.txt = w
        self.addWidget(w, 1)

    def setText(self, log):
        """Set the text of the statusbar, usually for logging."""
        self.txt.setText(log.format())
