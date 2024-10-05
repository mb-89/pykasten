"""Snippets and recipes that dont fit in a dedicated module."""

import os
import platform
import subprocess
from itertools import zip_longest


def startfile(x):
    try:
        os.startfile(x)
    except BaseException: #doesnt work on linux
        pass

# from https://docs.python.org/3/library/itertools.html#itertools-recipes
# we dont need high coverage here, since itertools tests it already
def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    """Collect data into non-overlapping fixed-length chunks or blocks."""
    # grouper('ABCDEFG', 3, fillvalue='x') → ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') → ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') → ABC DEF
    iterators = [iter(iterable)] * n
    match incomplete:
        case "fill":
            return zip_longest(*iterators, fillvalue=fillvalue)
        case "strict":  # pragma: no cover
            return zip(*iterators, strict=True)
        case "ignore":  # pragma: no cover
            return zip(*iterators)
        case _:  # pragma: no cover
            raise ValueError("Expected fill, strict, or ignore")


def runInNewProcess(cmd):  # pragma: no cover
    """Run the given cmd in a new process, setting all flags so that it detaches."""
    # Testing this is difficult. On dev-pcs (usually windows)
    # the unix path is not reached and on ci/cd servers the windows path is not reached.
    # Therefore: no coverage. just trust me bro
    iswin = platform.system() == "Windows"
    if iswin:
        ng = subprocess.CREATE_NEW_PROCESS_GROUP
        dp = subprocess.DETACHED_PROCESS
        subprocess.Popen(cmd, shell=True, creationflags=ng | dp)
    else:
        subprocess.Popen(cmd, preexec_fn=getattr(os, "setsid", None))
