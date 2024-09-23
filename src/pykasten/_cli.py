"""Commandline interface for pykasten."""

import json
import sys
import tempfile
from pathlib import Path

import click

from pykasten import examplebrowser as eb
from pykasten import recipekasten as rk


@click.group()
def cli():  # pragma: no cover
    """Commandline interface for pykasten."""
    pass


@cli.command()
@click.option("-n", "--name", type=str, default="", help="pass to run specific example")
@click.option(
    "-a",
    "--args",
    type=str,
    default="",
    help="override of example variables (in the form of $VAR1=$VAL1;$VAR2=VAL2;...)",
)
@click.option(
    "--show/--no-show", default=False, help="pass to show in this process (blocking)"
)
def examples(name, args, show):
    """Show example browser or run example (possibly with args)."""
    if name:
        argdict = {}
        if args:
            for kv in args.split(";"):
                for k, v in rk.grouper(kv.split("="), 2):
                    argdict[k.strip()] = v.strip()
        errno = eb.runExample(name, argdict)
        if errno:
            # try to run a test instead of an example
            try:
                import pytest
            except BaseException:
                return
            testpath = (Path(__file__).parent.parent.parent / "test").resolve()
            pytest.main([str(testpath), "-k", name, "--args", args, "--capture=sys"])
    else:
        newprocess = not show
        show_examples(newprocess)


@cli.command()
@click.option("--nocache", is_flag=True, default=False, help="dont cache this call.")
def repeat():
    """Repeat the last cahced cli call (mainly used for debugging)."""


def get_cache_args() -> list:
    """Return the last cached cli call."""
    path = Path(tempfile.gettempdir()) / "pykasten_argbuf"
    if not path.is_file():
        return []
    return json.loads(open(path, "r").read())


def set_cached_args(args):
    """Cache this cli call."""
    path = Path(tempfile.gettempdir()) / "pykasten_argbuf"
    open(path, "w").write(json.dumps(args))


def run(args: list | str = []):
    """Run the commandline interface. Global entry point."""
    if isinstance(args, str):
        args = args.split()
    if not args:
        args = sys.argv[1:]
    if args and len(args) > 0 and args[0] == "repeat":
        args = get_cache_args()
    elif "--nocache" not in args:
        set_cached_args(args)
    if "--nocache" in args:
        args.remove("--nocache")
    try:
        cli.main(args=args)
    except SystemExit:
        pass


def show_examples(newprocess):
    """Run the example-browser, either in-process or out-of-process."""
    if newprocess:
        interp = Path(sys.executable)
        interp = interp.with_stem("pythonw")

        cmd = [interp, "-m", "pykasten", "examples", "--show", "--nocache"]
        rk.runInNewProcess(cmd)
    else:
        exdir = (Path(__file__).parent.parent / "examples").resolve()
        docudir = exdir.parent / "doc"
        eb.ExampleBrowser(exdir, docudir).showGui()
