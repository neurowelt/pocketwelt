from typing import Dict

import pytest

from pocketwelt import BaseConfig


class TestConfig(BaseConfig):
    __test__ = False
    weight_x: float
    weight_y: float
    description: str
    logs: Dict[str, str]


def test_good_construction() -> None:
    """
    Test creating a `BaseConfig` instance.
    """
    test = TestConfig(
        weight_x=1.0,
        weight_y=2.3,
        description="Test configuration",
        logs={"log #1": "initialization"},
    )

    assert test.weight_x == 1.0
    assert test.weight_y == 2.3
    assert test.description == "Test configuration"
    assert test.logs == {"log #1": "initialization"}


def test_wrong_construction() -> None:
    """
    Test wrong creations of a `BaseConfig` instance.
    """
    with pytest.raises(AttributeError) as attr_err:
        TestConfig(wrong_arg=1.0)
    assert "variable named `wrong_arg`" in str(attr_err.value)

    with pytest.raises(TypeError) as typ_err:
        TestConfig(weight_x="1.0")
    assert "`weight_x` should be of type `float`" in str(typ_err.value)

    with pytest.raises(ValueError) as val_err:
        TestConfig(weight_x=1.0, weight_y=2.3, logs={"log #1": "initialization"})
    assert "missing: description" in str(val_err.value)
