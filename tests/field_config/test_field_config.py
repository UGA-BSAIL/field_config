"""
Tests for the `field_config` module.
"""


import pytest
import yaml

from src.field_config import FieldConfig
from .data import EXAMPLE_CONFIG_1


@pytest.fixture
def example_field_1() -> FieldConfig:
    """
    Loads the first example field configuration.

    Returns:
        The field configuration.

    """
    with EXAMPLE_CONFIG_1.open() as config_file:
        config = yaml.safe_load(config_file)
    return FieldConfig.from_yml(config)


def test_field_size(example_field_1: FieldConfig) -> None:
    """
    Tests that it gets the correct size for the field.

    Args:
        example_field_1: The field configuration.

    """
    # Assert.
    assert example_field_1.num_rows == 6
    assert example_field_1.num_plots == 100 * 6


def test_get_plot_num(example_field_1: FieldConfig) -> None:
    """
    Tests that it gets the correct plot number for a given row and column.

    Args:
        example_field_1: The field configuration.

    """
    # Assert.
    assert example_field_1.get_plot_num(2, 6) == 1526
    assert example_field_1.get_plot_num(4, 41) == 1673
    assert example_field_1.get_plot_num(5, 72) == 1742


def test_get_plot_num_row_major(example_field_1: FieldConfig) -> None:
    """
    Tests that it gets the correct plot number using row-major indexing.

    Args:
        example_field_1: The field configuration.

    """
    # Assert.
    assert example_field_1.get_plot_num_row_major(206) == 1526
    assert example_field_1.get_plot_num_row_major(441) == 1673
    assert example_field_1.get_plot_num_row_major(572) == 1742