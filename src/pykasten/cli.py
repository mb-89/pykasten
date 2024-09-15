"""Commandline interface for pykasten."""

import sys


def run(args=[]):
    """Run the commandline interface. Global entry point."""
    if not args:
        args = sys.argv[1:]
    print("hello world")
    print(args)
