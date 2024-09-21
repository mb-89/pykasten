"""Tests for the recipe collection."""

from pykasten import recipes as rs


def test_recipes_basics():

    #grouper
    input = (1,2,3,4)
    output_expected = ((1,2),(3,4))
    output = tuple(rs.grouper(input,2))
    assert (output == output_expected)