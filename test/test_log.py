from pathlib import Path

import pykasten.logkasten as lk
from pykasten.guikasten import mainwindow as mw


def test_logging():
    L = lk.getLogger()

    L.msg("info", "some_source","testmsg1")

    lk.setDstStdErr(True)
    

    L.msg("info", "some_source","testmsg")

    lk.setDstStdErr(False)
    lk.setTimeInMs(True)

    lk.setDstFile(Path("$TMP")/"log1.txt")

    L.msg("warn", "some_source","testmsg")

    lk.setTimeInMs(False)

    lk.setDstFile(Path("$TMP")/"log1.txt", False)

    L.msg("err", "some_source","testmsg")

    lk.setDstFile(Path("$TMP")/"log2.txt", maxAge_min = 60, maxCnt=3)

    L.msg("dbg", "some_source","testmsg")

    lk.setDstFile(Path("$TMP")/"log2.txt", False)

    win = mw.Win()
    lk.setDstObj(win)

    L.msg("note", "some_source","testmsg")

    lk.setDstObj(win,False)

    L.msg("fatal", "some_source","testmsg")