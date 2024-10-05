from pykasten.guikasten import dk, qt
from pykasten.guikasten import widgets as gkw


class ConsoleDock(dk):
    def __init__(self):
        super().__init__("console")
        self.constructed = False

    def construct(self):
        """Construct the gui."""
        if self.constructed:
            return

        w = gkw.Widget()
        la = w.qla
        self.addWidget(w)

        self.setStretch(y=0.3)
        qt.QtCore.QTimer.singleShot(0, lambda: self.setHidden(True))

        self.constructed = True
