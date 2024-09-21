"""Snippets and recipes that dont fit in a dedicated module."""

from itertools import zip_longest


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
