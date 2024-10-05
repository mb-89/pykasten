from functools import partial

import pyqtgraph.console

from pykasten.guikasten import dk, getapp, qt
from pykasten.guikasten import widgets as gkw
from pykasten.logkasten import getLogger

rich_console = False
try:
    from qtconsole import inprocess  # type: ignore

    rich_console = True
except (ImportError, NameError):
    pass

msg = getLogger().msg

startup_cmds = [
    "%load_ext autoreload",
    "%autoreload complete",
    "print(console_prompt)",
    "logmsg('info','console','opened interactive console.')",
    "whos",
]


class ConsoleDock(dk):
    def __init__(self, context: dict = {}, prompt="Hello World :D"):
        super().__init__("console")
        self.constructed = False
        context["console_prompt"] = prompt
        context["logmsg"] = msg
        self.context = context
        self.first_time_shown = False

    def construct(self):
        """Construct the gui."""
        if self.constructed:
            return

        w = gkw.Widget()
        la = w.qla
        self.addWidget(w)
        self.rich = rich_console

        if self.rich:
            self.console = JupyterConsoleWidget()
            app = getapp().instance()
            app.aboutToQuit.connect(self.console.shutdown_kernel)  # type: ignore
            kernel = self.console.kernel_manager.kernel  # type: ignore
            kernel.shell.push(self.context)
            self.console.set_default_style("linux")
        else:
            pyqtgraph.console.ConsoleWidget(
                namespace=self.context, text=self.context["console_prompt"]
            )

        # self.setStretch(y=0.3)
        qt.QtCore.QTimer.singleShot(0, lambda: self.setHidden(True))

        la.addWidget(self.console)
        self.constructed = True

    def cmd(self, cmd):
        if not cmd:
            return
        if self.rich:
            self.console.execute(cmd)

    def setHidden(self, h):
        if not self.first_time_shown:
            self.first_time_shown = True
            if self.rich:
                ss = qt.QtCore.QTimer.singleShot
                for idx, cmd in enumerate(startup_cmds):
                    p = partial(self.cmd, cmd)
                    ss(idx * 250, p)
        super().setHidden(h)


class JupyterConsoleWidget(inprocess.QtInProcessRichJupyterWidget):
    def __init__(self):
        super().__init__()

        self.kernel_manager = inprocess.QtInProcessKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()

    def shutdown_kernel(self):
        self.kernel_client.stop_channels()  # type: ignore
        self.kernel_manager.shutdown_kernel()  # type: ignore
