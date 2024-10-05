"""Logging stuff that has gui dependencies."""

import collections
import re
from functools import partial
from pathlib import Path

from pykasten import logkasten as lk
from pykasten import recipekasten as rk
from pykasten.guikasten import dk
from pykasten.guikasten import exec as gkexec
from pykasten.guikasten import pg, qt
from pykasten.guikasten import widgets as gkw

qtw = qt.QtWidgets
qtg = qt.QtGui

N = 2**12


class LogDock(dk):
    """Dock that shows log messages."""

    sig_WriteTxt = qt.QtCore.Signal()

    def __init__(self, logfile: None | Path):
        log2file = logfile is not None
        if log2file:
            super().__init__(f"Log (last {N} entries, rest see logfile)")
        else:
            super().__init__("Log")
        self.constructed = False

        self.txtbuf = collections.deque(maxlen=N if log2file else None)
        self.filtRE = ""
        self.logfile = logfile
        if log2file:
            self.logfile = lk.setDstFile(logfile, True)

        self.writeProxy = pg.SignalProxy(
            self.sig_WriteTxt, delay=0.25, rateLimit=4, slot=self.printTxtBuf
        )
        self.busy = False

        # self.startDBGtimer()

    def startDBGtimer(self):  # pragma: no cover
        self.dbgidx = 0
        self.dbgtimer = qt.QtCore.QTimer()
        t = self.dbgtimer
        t.setInterval(100)
        msg = lk.getLogger().msg

        def fn():
            msg("info", "dbg", f"blabla {self.dbgidx}")
            self.dbgidx += 1

        t.timeout.connect(fn)
        t.start()

    def construct(self):
        """Construct the gui."""
        if self.constructed:
            return

        w = gkw.Widget()
        la = w.qla
        self.addWidget(w)

        self.txt = qtw.QPlainTextEdit()
        self.txt.setLineWrapMode(qtw.QPlainTextEdit.LineWrapMode.NoWrap)
        sp = qtw.QSizePolicy.Expanding  # type: ignore
        self.txt.setSizePolicy(sp, sp)
        f = self.txt.font()
        f.setFamily("Courier New")
        self.txt.setFont(f)

        self.filt = qtw.QLineEdit()
        self.filt.setPlaceholderText("filter w/ regex on <return>")
        self.filt.returnPressed.connect(self.setFiltRE)
        self.clear = qtw.QPushButton("clear")
        self.clear.clicked.connect(self.clearTxtBuf)

        la.addWidget(self.txt, 0, 0, 4, 3)
        la.addWidget(self.filt, 0, 3, 1, 1)
        la.addWidget(self.clear, 1, 3, 1, 1)

        if self.logfile is not None:
            b = qtw.QPushButton("open logfile")
            p = partial(rk.startfile, str(self.logfile))
            b.clicked.connect(p)
            la.addWidget(b, 2, 3, 1, 1)

        la.setColumnStretch(0, 5)
        la.setColumnStretch(1, 1)

        self.setStretch(y=0.3)
        qt.QtCore.QTimer.singleShot(0, lambda: self.setHidden(True))
        la.addItem(
            qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding),  # type: ignore
            4,
            1,
        )
        self.constructed = True

    def exec(self, parent):
        """Run the gui."""
        self.construct()
        parent.addDock(self, "bottom")
        parent.show()
        gkexec()

    def log(self, msg):
        """Log a message."""
        self.txtbuf.appendleft(msg)
        self.sig_WriteTxt.emit()

    def clearTxtBuf(self):
        self.txtbuf.clear()
        self.sig_WriteTxt.emit()

    def setFiltRE(self):
        self.filtRE = self.filt.text()
        self.sig_WriteTxt.emit()

    def printTxtBuf(self):
        if self.busy:
            return
        self.busy = True
        if not self.filtRE:
            self.txt.setPlainText("\n".join(self.txtbuf))
        else:
            self.txt.setPlainText(
                "\n".join(
                    x for x in self.txtbuf if re.findall(self.filtRE, x, re.IGNORECASE)
                )
            )
        self.busy = False
