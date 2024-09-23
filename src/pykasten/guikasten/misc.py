"""Misc GUI code snippets."""

import logging

from pykasten.guikasten import qt


class Emitter(qt.QtCore.QObject):
    """We need this for some reason..."""

    sig = qt.QtCore.Signal(logging.LogRecord)


class Handler_log2qtsig(qt.QtCore.QObject, logging.StreamHandler):
    """Mapper for log records to qt signals."""

    def __init__(self):
        super().__init__()
        self.emitter = Emitter()

    def emit(self, logRecord):
        """Emit a logrecord as qt signal."""
        msg = self.format(logRecord)
        self.emitter.sig.emit(msg)
