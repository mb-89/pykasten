from pykasten import cli

import pytest

@pytest.mark.smoke
def test_cli_basics():
    """Check that basic cli usage doesnt crash."""
    cli.run()
    cli.run("-h")
    cli.run("--version")
