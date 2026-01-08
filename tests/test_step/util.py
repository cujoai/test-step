#  Copyright (c) 2026 CUJO LLC
import os
from contextlib import contextmanager
from itertools import chain
from pathlib import Path
from textwrap import dedent
from typing import Any, NamedTuple
from collections.abc import Mapping

import pytest
from junitparser import TestSuite, JUnitXml


def create_config(tmp_dir: Path, config: str) -> Path:
    config_path = tmp_dir / "config.yml"
    config_path.write_text(dedent(config))
    return config_path


class ReducedTestCase(NamedTuple):
    name: str
    result: str | None
    stdout: str = ""

    def __eq__(self, other):
        return self.name == other.name and self.result == other.result

    def __hash__(self):
        return hash((self.name, self.result))


class ReducedTestSuite:
    def __init__(self, xml: TestSuite):
        self.tests = xml.tests
        self.errors = xml.errors
        self.failures = xml.failures
        self.xml = xml
        # First result works well enough, we don't care all that much about correctness in test internals
        # noinspection PyProtectedMember
        self.test_cases = [
            ReducedTestCase(
                name=tc.name,
                result=tc.result[0]._tag if tc.result else None,
                stdout=f'{tc.system_out or ""}\n{tc.system_err or ""}'
            )
            for tc
            in chain.from_iterable(xml)
        ]


class PytestResult:
    def __init__(self, suite: ReducedTestSuite):
        self.suite = suite


def run_pytest(
        args: list[Any],
        tmp_dir: Path,
        parallel: int | None = None,
        keyword: str | None = None,
        show_steps=False,
        html_report_dir: Path | None = None
) -> PytestResult:
    xml_path = tmp_dir / "junit.xml"
    full_args = args.copy()
    if parallel:
        full_args.append(f'-n {parallel}')
    if keyword:
        full_args.append(f'-k {keyword}')
    if show_steps:
        full_args.append('--show-steps')
    if html_report_dir:
        full_args.append(f'--html={html_report_dir / "report.html"}')

    full_args.append(f'--junitxml={xml_path}')
    pytest.main(
        args=full_args
    )
    return PytestResult(ReducedTestSuite(JUnitXml.fromfile(xml_path)))


def function_test(func) -> str:
    return f"{func.__code__.co_filename}::{func.__name__}"


@contextmanager
def temp_env(new_env: Mapping[str, str | None]) -> None:
    """
    Update environment for the duration of the context manager with new values.

    Non-None values are set. Keys with None values are removed from the existing environment
    """
    old_env = os.environ.copy()
    for k, v in new_env.items():
        if v is not None:
            os.environ[k] = v
        else:
            os.environ.pop(k, None)
    try:
        yield
    finally:
        os.environ = old_env  # noqa: B003
