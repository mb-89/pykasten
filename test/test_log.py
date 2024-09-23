from pathlib import Path

import pykasten.logkasten as lk
from pykasten.guikasten import mainwindow as mw


def test_logging():
    L = lk.getLogger()

    L.log("info", "some_source","testmsg1")

    lk.setDstStdErr(True)
    

    L.log("info", "some_source","testmsg")

    lk.setDstStdErr(False)
    lk.setTimeInMs(True)

    lk.setDstFile(Path("$TMP")/"log1.txt")

    L.log("warn", "some_source","testmsg")

    lk.setTimeInMs(False)

    lk.setDstFile(Path("$TMP")/"log1.txt", False)

    L.log("err", "some_source","testmsg")

    lk.setDstFile(Path("$TMP")/"log2.txt", maxAge_min = 60, maxCnt=3)

    L.log("dbg", "some_source","testmsg")

    lk.setDstFile(Path("$TMP")/"log2.txt", False)

    win = mw.Win()
    lk.setDstObj(win)

    L.log("note", "some_source","testmsg")

    lk.setDstObj(win,False)

    L.log("fatal", "some_source","testmsg")