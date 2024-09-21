"""Commandline interface for pykasten."""

import json
import sys
import tempfile
from pathlib import Path

import click

from pykasten import examplebrowser as eb
from pykasten import recipes as rs


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
def examples(name, args):
    """Show example browser or run example (possibly with args)."""
    if name:
        argdict = {}
        if args:
            for kv in args.split(";"):
                for k, v in rs.grouper(kv.split("="), 2):
                    argdict[k.strip()] = v.strip()
        eb.runExample(name, argdict)
    else:
        exdir = (Path(__file__).parent.parent / "examples").resolve()
        docudir = exdir.parent / "doc"
        eb.ExampleBrowser(exdir, docudir).showGui()


@cli.command()
def repeat():
    """Repeat the last cli call (mainly used for debugging)."""


def get_buffered_args():
    """Return the last buffered cli call."""
    path = Path(tempfile.gettempdir()) / "pykasten_argbuf"
    if not path.is_file():
        return ""
    return json.loads(open(path, "r").read())


def set_buffered_args(args):
    """Buffer this cli call."""
    path = Path(tempfile.gettempdir()) / "pykasten_argbuf"
    open(path, "w").write(json.dumps(args))


def run(args=[]):
    """Run the commandline interface. Global entry point."""
    if isinstance(args, str):
        args = args.split()
    if not args:
        args = sys.argv[1:]
    try:
        if args and len(args) > 0 and args[0] == "repeat":
            args = get_buffered_args()
        else:
            set_buffered_args(args)

        cli.main(args=args)

    except SystemExit:
        pass
