from pykasten.guikasten import qt


class Widget(qt.QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        L = qt.QtWidgets.QGridLayout()
        L.setSpacing(0)
        L.setContentsMargins(0, 0, 0, 0)
        self.qla = L
        self.setLayout(L)
