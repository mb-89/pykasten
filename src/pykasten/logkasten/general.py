"""Snippets and recipes that have to do with logging."""

import logging
import sys
import tempfile
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class pkLogger(logging.getLoggerClass()):
    """A modified root logger."""

    def __init__(self, name):
        super().__init__(name)
        self.fmt = "%(relativeCreated)08.0d / %(levelname)-4s / %(src)s / %(message)s"
        self.tfmt = "%Y-%m-%d %H:%M:%S"
        self.hdl_dict = {}

    def log(self, lvl, src, message):
        """Log a message."""
        if isinstance(lvl, str):
            lvl = logging.getLevelNamesMapping().get(lvl.upper(), logging.INFO)
        super().log(lvl, message, extra={"src": src})


setup_done = False


def getLogger() -> pkLogger:
    """Get the logger object."""
    global setup_done
    if not setup_done:
        setup_done = True
        logging.setLoggerClass(pkLogger)
        log = logging.getLogger(__name__)
        logging.addLevelName(logging.DEBUG, "DBG")
        logging.addLevelName(logging.ERROR, "ERR")
        logging.addLevelName(logging.WARNING, "WARN")
        logging.addLevelName((logging.WARN + logging.INFO) // 2, "NOTE")
        log.setLevel(logging.DEBUG)

    log = logging.getLogger(__name__)

    return log  # pyright: ignore


def setTimeInMs(val: bool):
    """Set the time format to ms since start."""
    log = getLogger()
    if val:
        fmt = "%(relativeCreated)08.0d / %(levelname)-4s / %(src)s / %(message)s"
    else:
        fmt = "%(asctime)-10s / %(levelname)-4s / %(src)s / %(message)s"
    log.fmt = fmt


def setLvl(lvl):
    """Set log lvl."""
    log = getLogger()
    log.setLevel(lvl)


def setDstStdErr(val: bool):
    """Start or stop logging to stderr."""
    log = getLogger()
    if h := log.hdl_dict.pop("stderr", None):
        log.removeHandler(h)
    if val:
        h = logging.StreamHandler(sys.stderr)
        f = logging.Formatter(log.fmt, log.tfmt)
        h.setFormatter(f)
        log.addHandler(h)
        log.hdl_dict["stderr"] = h


def setDstFile(path: Path, doLog: bool = True, maxAge_min=-1, maxCnt=0):
    """Add a file to the list of destination files, or remove it if doLog is false."""
    log = getLogger()
    ps = str(path)
    if "$TMP" in ps:
        tmpdir = Path(tempfile.gettempdir()) / "python_logs"
        ps = ps.replace("$TMP", str(tmpdir))
        path = Path(ps).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not doLog and (h := log.hdl_dict.pop(path, None)):
        log.log("info", "logkasten", f"stopping logging into {path}")
        log.removeHandler(h)
    if doLog:
        if maxAge_min > 0:
            h = TimedRotatingFileHandler(path, "m", maxAge_min, maxCnt)
        else:
            h = logging.FileHandler(path, mode="w")
        f = logging.Formatter(log.fmt, log.tfmt)
        h.setFormatter(f)
        log.addHandler(h)
        log.hdl_dict[path] = h
        log.log("info", "logkasten", f"started logging into {path}")


def setDstObj(obj, doLog: bool = True):
    """Add any object that can accept messages, or remove it if doLog is false.

    Usually, this means an object that inherits from LogDst, or a class that we
    know and we can attach a logger to.
    """
    fn = getattr(obj, "log_acceptStreamHandler", None)
    if not fn:
        return

    log = getLogger()
    ID = id(obj)
    tp = type(obj)
    if not doLog and (h := log.hdl_dict.pop(ID, None)):
        log.log("info", "logkasten", f"stopping logging into {tp}")
        log.removeHandler(h)
        fn = getattr(obj, "log_removeStreamHandler", None)
        if fn:
            fn(h)

    if not doLog:
        return

    from pykasten.guikasten.misc import Handler_log2qtsig

    h = Handler_log2qtsig()
    f = logging.Formatter(log.fmt, log.tfmt)
    h.setFormatter(f)
    log.addHandler(h)
    log.hdl_dict[ID] = h
    if fn:
        fn(h)
    log.log("info", "logkasten", f"started logging into {tp}")
