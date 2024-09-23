"""Tests for the recipe collection."""

from pykasten import recipekasten as rk


def test_recipes_basics():

    #grouper
    input = (1,2,3,4)
    output_expected = ((1,2),(3,4))
    output = tuple(rk.grouper(input,2))
    assert (output == output_expected)