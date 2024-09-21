import pytest

from pykasten import cli


@pytest.mark.smoke
def test_cli_basics():
    """Check that basic cli usage doesnt crash."""
    cli.run()
    cli.run("-h")
    cli.run("--version")
    cli.run("repeat")
