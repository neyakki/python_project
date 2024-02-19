from __future__ import annotations

import time

import pytest

from project.mains.main import add


class TestOperations:
    def test_add_1(self) -> None:
        assert add(1, 1) == 101

    def test_add_2(self) -> None:
        time.sleep(10)
        assert add(-1, 1) == 0

    def test_add_3(self) -> None:
        assert add(0, 1) == 2


def test_recursion_depth() -> None:
    with pytest.raises(RuntimeError) as excinfo:

        def f() -> None:
            f()

        f()
    assert "maximum recursion2" in str(excinfo.value)


def test_foo_not_implemented() -> None:
    def foo() -> None:
        raise NotImplementedError

    with pytest.raises(RuntimeError) as excinfo:
        foo()
    assert excinfo.type is RuntimeError
