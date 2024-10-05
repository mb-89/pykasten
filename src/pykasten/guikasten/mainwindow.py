"""The mainwindow is a class that hosts Docks and provide some infrastructure fns."""

import inspect
import json
from pathlib import Path

import pykasten.logkasten as lk
from pykasten.guikasten import addShortcut, consoleDock, da, getapp, qt
from pykasten.logkasten.gui import LogDock

msg = lk.getLogger().msg


class Win(qt.QtWidgets.QMainWindow):
    """Class for the mainwindow."""

    def __init__(self, title="pykasten mainwindow"):
        super().__init__()
        frame = inspect.currentframe()
        pframe = frame.f_back  # type: ignore
        try:
            pclass = pframe.f_locals["self"].__class__.__name__  # type: ignore
        except BaseException:
            pclass = None
        self.caller = {
            "file": pframe.f_code.co_filename,  # type: ignore
            "fn": pframe.f_code.co_name,  # type: ignore
            "class": pclass,
        }
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
        cd = consoleDock.ConsoleDock()
        self.addDock(ld)
        self.addDock(cd, "top")

        self.resize(800, 600)

        while self._dockList:
            x = self._dockList.pop(0)
            try:
                x[0].construct()
            except AttributeError:
                pass
            self.da.addDock(*x)

        sb = StatusBar(self, dockArea=self.da, logDock=ld, consoleDock=cd)
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
        self.construct()
        h.emitter.sig.connect(self.sb.setText)
        self.loghandlers.append(h)

    def log_removeStreamHandler(self, h):
        """Remove the given handler."""
        self.loghandlers.remove(h)


class StatusBar(qt.QtWidgets.QStatusBar):
    """A statusbar for the main gui."""

    def __init__(self, root, dockArea=None, logDock=None, consoleDock=None):
        super().__init__()
        W = 20

        self.root = root
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
        self.logdock = logDock

        if consoleDock is not None:
            self.b1 = (x := qt.QtWidgets.QPushButton("C"))
            x.setMaximumWidth(W)
            x.setToolTip("console. Press to toggle console [^^]")
            x.setCheckable(True)
            x.clicked.connect((lambda x: consoleDock.setHidden(not x)))
            addShortcut(self, x.click, "^,^", "toggle console widget")
            la.addWidget(self.b1)

        if dockArea is not None:
            self.b3 = (x := qt.QtWidgets.QPushButton("W"))
            x.setMaximumWidth(W)
            x.setMaximumWidth(W)
            x.setToolTip(
                "window layout. Press to reset, shift-press to store [CTRL+W, CTRL+SHIFT+W]"
            )
            x.clicked.connect(lambda x: self.handleWindowLayout(dockArea))
            addShortcut(self, x.click, "Ctrl+W", "reset window layout")
            addShortcut(self, x.click, "Ctrl+Shift+W", "store window layout")
            la.addWidget(self.b3)

        self.addPermanentWidget(w)

        w = qt.QtWidgets.QLabel()
        self.txt = w
        self.addWidget(w, 1)

    def handleWindowLayout(self, dockArea, mode=None):
        mods = getapp().keyboardModifiers()
        c = self.root.caller
        safefile = Path(c["file"]).resolve()
        safefile = safefile.with_stem(
            safefile.stem + f"_{c['class']}_{c['fn']}_guilayout"
        )
        safefile = safefile.with_suffix(".json")
        safefile_override = safefile.with_stem(safefile.stem + "_override")

        if mode is None:
            if mods & qt.QtCore.Qt.ShiftModifier:  # type: ignore
                mode = "store"
            else:
                mode = "restore"
        if mode == "store":
            state = dockArea.saveState()
            statejs = json.dumps(state, indent=4)
            open(safefile_override, "w").write(statejs)
            msg("info", "mainwindow", "stored window state.")
        else:
            if safefile_override.is_file():
                f = safefile_override
            elif safefile.is_file():
                f = safefile
            else:
                f = None
            if f is None:
                return
            state = json.loads(open(f, "r").read())
            dockArea.restoreState(state)
            msg("info", "mainwindow", "restored window state.")

    def setText(self, log):
        """Set the text of the statusbar, usually for logging."""
        txt = log.format()
        self.txt.setText(txt)
        if self.logdock is not None:
            self.logdock.log(txt)
