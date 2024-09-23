"""Logging stuff that has gui dependencies."""

from pathlib import Path

from pykasten.guikasten import dk
from pykasten.guikasten import exec as gkexec
from pykasten.guikasten import qt


class LogDock(dk):
    """Dock that shows log messages."""

    def __init__(self, logfile: None | Path):
        super().__init__("Log")
        self.constructed = False

    def construct(self):
        """Construct the gui."""
        if self.constructed:
            return

        self.setStretch(y=0.3)
        qt.QtCore.QTimer.singleShot(0, lambda: self.setHidden(True))
        self.constructed = True

    def exec(self, parent):
        """Run the gui."""
        self.construct()
        parent.addDock(self, "bottom")
        parent.show()
        gkexec()

    def log(self, msg):
        """Log a message."""
        print(msg)
