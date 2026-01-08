#  Copyright (c) 2026 CUJO LLC
from pathlib import Path

from test_step.steps import step


@step()
def plain_function(*arg, **kwargs):
    pass


@step()
def function_with_return(arg):
    return arg


@step()
def function_with_raise():
    raise AssertionError('exception content')


@step('decorator-step')
def function_with_message(*arg, **kwargs):
    pass


@step('decorator-step')
def function_with_step_decorator_and_nested_with_statement():
    with step('with-step'):
        pass


class SampleClass:
    @step()
    def method(self):
        pass

    @staticmethod
    @step()
    def static_method():
        pass

    def __repr__(self):
        return 'SampleClass()'


def test_plain_step():
    plain_function()


def test_step_with_args():
    plain_function('foo', 'bar', baz='baz')


def test_step_with_return():
    function_with_return('foo')


def test_non_ascii_args():
    plain_function('如果您')


def test_step_with_exception():
    function_with_raise()


def test_step_with_message():
    function_with_message()


def test_method_step():
    SampleClass().method()


def test_static_method_step():
    SampleClass.static_method()


def test_context():
    with step():
        pass


def test_context_with_name():
    with step('foo'):
        pass


def test_context_raise():
    with step():
        raise AssertionError('exception content')


def test_with_single_step():
    with step('step-1'):
        pass


def test_with_multiple_consecutive_steps():
    with step('step-1'):
        pass
    with step('step-2'):
        pass
    with step('step-3'):
        pass


# ruff: noqa: SIM117
def test_with_multiple_consecutive_and_nested_steps():
    with step('step-1'):
        pass
    with step('step-2'):
        with step('step-3'):
            pass


def test_with_with_statement_and_nested_decorator_function():
    with step('with-step'):
        function_with_message()


def test_with_decorator_function_and_nested_with_statement():
    function_with_step_decorator_and_nested_with_statement()


# ruff: noqa: SIM117
def test_nested_with_statement_with_caught_exception():
    try:
        with step('outer-step'):
            with step('step-with-exception'):
                raise ValueError("An error occurred")
    except ValueError:
        pass
    with step('after-exception-step'):
        pass


# ruff: noqa: SIM117
def test_nested_with_statement_with_uncaught_exception():
    with step('outer-step'):
        with step('step-with-exception'):
            raise ValueError("An error occurred")
    with step('after-exception-step'):
        pass


def test_file_extra_file(tmp_path):
    file = tmp_path / 'test_file.txt'
    file.write_text('test content')
    with step('Attach file extra', report_attachments=[Path(file)]):
        pass
