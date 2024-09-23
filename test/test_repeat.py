import sys

import pytest

import pykasten._cli as cli


@pytest.mark.repeat
def test_repeat(pytestconfig):
    """Run this test via 'poe test -m repeat' to test the last command."""
    markers_arg = pytestconfig.getoption('-m')
    tr = sys.gettrace() #if we have a tracer, assume that we are in debug mode and run
    if ("repeat" not in markers_arg) and not tr:
        return
    cli.run("repeat")