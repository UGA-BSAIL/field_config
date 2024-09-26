"""
Tests for the `utils` module.
"""

import geopandas as gpd

import pytest

from src.field_config import FieldConfig, label_plots, RowDirection
from .data import EXAMPLE_PLOTS_1


@pytest.fixture
def example_1_plot_shapes() -> gpd.GeoDataFrame:
    """
    Loads the Example 1 plot boundaries.
    """
    return gpd.read_file(EXAMPLE_PLOTS_1)


@pytest.mark.parametrize(
    "row_direction",
    [RowDirection.NORTH_TO_SOUTH, RowDirection.WEST_TO_EAST],
    ids=["N-S", "W-E"],
)
def test_label_plots(
    example_field_1: FieldConfig,
    example_1_plot_shapes: gpd.GeoDataFrame,
    row_direction: RowDirection,
) -> None:
    """
    Tests that `label_plots` works.

    Args:
        example_field_1: The field config to test with.
        example_1_plot_shapes: The shapes of the plots in the field.
        row_direction: The direction of the rows in the plots.

    """
    # Act.
    labeled = list(
        label_plots(
            plot_boundaries=example_1_plot_shapes.geometry,
            field_config=example_field_1,
            row_direction=row_direction,
        )
    )

    # Assert.
    assert len(labeled) == len(example_1_plot_shapes)

    # In this field, the north-western-most plot is 1393.
    assert labeled[0][1] == 1393
    # The south-eastern-most plot is 1729.
    assert labeled[-1][1] == 1729

    plot1, _ = labeled[0]
    plot2, _ = labeled[1]
    if row_direction == RowDirection.NORTH_TO_SOUTH:
        # The plots should be enumerated north-to-south first.
        assert plot1.centroid.y > plot2.centroid.y
        assert (plot1.centroid.y - plot2.centroid.y) > (
            plot2.centroid.x - plot1.centroid.x
        )
    else:
        # The plots should be enumerated west-to-east first.
        assert plot2.centroid.x > plot1.centroid.x
        assert (plot2.centroid.x - plot1.centroid.x) > (
            plot1.centroid.y - plot2.centroid.y
        )
