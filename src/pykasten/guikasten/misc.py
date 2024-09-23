import logging

from pykasten.guikasten import qt


class Emitter(qt.QtCore.QObject):
    sig = qt.QtCore.Signal(logging.LogRecord)

class Handler_log2qtsig(qt.QtCore.QObject, logging.StreamHandler):

    def __init__(self):
        super().__init__()
        self.emitter = Emitter()

    def emit(self, logRecord):
        msg = self.format(logRecord)
        self.emitter.sig.emit(msg)

