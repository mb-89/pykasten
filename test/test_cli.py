import pytest

from pykasten import _cli


@pytest.mark.smoke
def test_cli_basics():
    """Check that basic cli usage doesnt crash."""
    _cli.run()
    _cli.run("-h")
    _cli.run("--version")
    _cli.run("repeat")
