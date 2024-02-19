"""
Набор функций и задач

===================================================
Author: funny-neto-code <na011912@gmail.com>
"""
from __future__ import annotations

import os

from invoke.context import Context
from invoke.tasks import task

DEFAULT_CONFIG_FILE = os.environ.get("CONFIG_FILE", "pyproject.toml")
DEFAULT_REMOVE_FILES = ["dist"]


@task
def check(c: Context) -> None:
    """Проверка проекта"""
    c.run("poetry check", echo=True)


@task(pre=[check])
def lint(
    c: Context,
    file: str = ".",
    config_file: str = DEFAULT_CONFIG_FILE,
    silent: bool = False,
) -> None:
    """Проверка линетром"""
    cmd = f"ruff --config={config_file}"

    if silent is True:
        c.run(f"{cmd} --silent {file}", echo=True)
        return

    c.run(f"{cmd} {file}", echo=True)


@task(pre=[check])
def format(  # noqa: A001
    c: Context,
    file: str = ".",
    config_file: str = DEFAULT_CONFIG_FILE,
    silent: bool = False,
) -> None:
    """Форматирование файлов"""
    cmd_fix = f"ruff --fix --config={config_file}"
    cmd_format = f"ruff format --config={config_file}"

    if silent is True:
        c.run(f"{cmd_fix} --silent {file}", echo=True)
        c.run(f"{cmd_format} --silent {file}", echo=True)
        return

    c.run(f"{cmd_fix} {file}", echo=True)
    c.run(f"{cmd_format} {file}", echo=True)


@task(pre=[check])
def clean(c: Context, extend: str | None = None) -> None:
    """Очистка проекта"""
    _remove_file = DEFAULT_REMOVE_FILES.copy()

    if extend:
        _remove_file.extend(extend)

    c.run(f"rm -rf {' '.join(_remove_file)}", echo=True)
    c.run("find . -name __pycache__ -not -path \"./.venv/*\" -exec rm -rf {} \\;")


@task(pre=[check, clean])
def build(c: Context) -> None:
    """Сборка проекта"""
    c.run("poetry build", echo=True)


@task(name="test")
def run_test(
    c: Context,
    file: str = ".",
    doctest: bool = False,
) -> None:
    """Запусков тестов"""
    cmd = f"coverage run -m pytest -v {file}"

    if doctest:
        c.run(f"{cmd} --doctest-modules --doctest-continue-on-failure", echo=True)

    c.run(cmd, echo=True)


@task(pre=[run_test])
def report(c: Context) -> None:
    """Создание в консоли отчета покрытия кода тестами"""
    c.run("coverage report -m", echo=True)


@task(pre=[run_test])
def lcov(c: Context) -> None:
    """Создание lcov файла"""
    c.run("coverage lcov", echo=True)


@task(pre=[run_test])
def html(c: Context) -> None:
    """Создание HTML отчета покрытия кода тестами"""
    c.run("coverage html", echo=True)
