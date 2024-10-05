from pyqtgraph.dockarea.Dock import Dock as _D
from pyqtgraph.dockarea.DockArea import DockArea as _DA


class Dock(_D):
    def __init__(
        self,
        name,
        area=None,
        size=(10, 10),
        widget=None,
        hideTitle=False,
        autoOrientation=True,
        label=None,
        **kargs
    ):
        autoOrientation = False
        super().__init__(
            name, area, size, widget, hideTitle, autoOrientation, label, **kargs
        )


class DockArea(_DA):
    pass
