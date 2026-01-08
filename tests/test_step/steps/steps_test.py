#  Copyright (c) 2026 CUJO LLC
import json
import html  # Added for unescaping HTML entities

from tests.test_step.steps.steps_sample_tests import step_tests
from tests.test_step.util import run_pytest, function_test, ReducedTestCase


# parallel=1 makes the test run in a different pytest process,
# which makes it easier to isolate logs at the cost of performance.

def test_header_with_no_message(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_plain_step)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_plain_step.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert 'Enter ---Step - plain_function ---' in test_case.stdout
    assert 'Exit  ---Step - plain_function ---' in test_case.stdout


def test_method(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_method_step)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_method_step.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert 'Enter ---Step - method ---' in test_case.stdout
    assert 'Exit  ---Step - method ---' in test_case.stdout
    assert 'Arguments (SampleClass(),), {}' in test_case.stdout


def test_static_method(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_static_method_step)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_static_method_step.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert 'Enter ---Step - static_method ---' in test_case.stdout
    assert 'Exit  ---Step - static_method ---' in test_case.stdout
    assert 'Arguments (), {}' in test_case.stdout


def test_header_with_message(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_step_with_message)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_step_with_message.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert 'Enter ---Step - decorator-step (function_with_message)---' in test_case.stdout
    assert 'Exit  ---Step - decorator-step (function_with_message)---' in test_case.stdout


def test_empty_args(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_plain_step)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_plain_step.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert 'Arguments (), {}' in test_case.stdout


def test_args(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_step_with_args)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_step_with_args.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert "Arguments ('foo', 'bar'), {'baz': 'baz'}" in test_case.stdout


def test_non_ascii_args(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_non_ascii_args)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_non_ascii_args.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert "Arguments ('如果您',), {}" in test_case.stdout


def test_return_none(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_plain_step)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_plain_step.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert 'Returned: None' in test_case.stdout


def test_return_value(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_step_with_return)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_step_with_return.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert 'Returned: foo' in test_case.stdout


def test_step_with_exception(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_step_with_exception)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_step_with_exception.__name__, "failure")]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert "Raised AssertionError('exception content')" in test_case.stdout


def test_context_header_with_no_message(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_context)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_context.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert 'Enter ---Step---' in test_case.stdout
    assert 'Exit  ---Step---' in test_case.stdout


def test_context_header_with_message(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_context_with_name)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_context_with_name.__name__, None)]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert 'Enter ---Step - foo ---' in test_case.stdout
    assert 'Exit  ---Step - foo ---' in test_case.stdout


def test_context_with_exception(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_context_raise)],
        tmp_dir=tmp_path,
        parallel=1
    ).suite
    assert suite.test_cases == [ReducedTestCase(step_tests.test_context_raise.__name__, "failure")]
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert "Raised AssertionError('exception content')" in test_case.stdout


def test_context_with_extras(tmp_path):
    report_dir = tmp_path / 'report'
    run_pytest(
        args=[function_test(step_tests.test_file_extra_file)],
        tmp_dir=tmp_path,
        parallel=1,
        html_report_dir=report_dir,
        show_steps=True
    )
    stored_file_path = (report_dir / 'extras' /
                        'tests_test_step_steps_steps_sample_tests_step_tests.py__test_file_extra_file_0_1.txt')
    assert stored_file_path.read_text() == 'test content'


def test_context_with_extras_self_contained(tmp_path):
    report_dir = tmp_path
    suite = run_pytest(
        args=[function_test(step_tests.test_file_extra_file), '--self-contained-html'],
        tmp_dir=tmp_path,
        parallel=1,
        html_report_dir=report_dir,
        show_steps=True
    ).suite
    test_case = suite.test_cases[0]
    print(test_case.stdout)
    assert "Attachments not present in report steps because --self-contained-html was used" in test_case.stdout


def test_report_contains_steps_from_test(tmp_path):
    report_dir = tmp_path / 'report'
    report_path = report_dir / 'report.html'
    run_pytest(
        args=[function_test(step_tests.test_with_single_step)],
        tmp_dir=tmp_path,
        show_steps=True,
        html_report_dir=report_dir,
        parallel=1
    )

    data = [{"step": "step-1", "result": "Pass"}]
    expected_json = (json.dumps(data, indent=2)
                     .replace('\n', '\\n')
                     .replace('"', '\\"'))

    html_content = report_path.read_text()
    html_content_unescaped = html.unescape(html_content)
    assert expected_json in html_content_unescaped


def test_report_does_not_contain_steps_from_test_when_plugin_disabled(tmp_path):
    suite = run_pytest(
        args=[function_test(step_tests.test_with_single_step)],
        tmp_dir=tmp_path,
        show_steps=True,
        parallel=1
    ).suite
    test_case = suite.test_cases[0]
    assert "[{'step':" in test_case.stdout


def test_report_contains_multiple_consecutive_steps_from_test(tmp_path):
    report_dir = tmp_path / 'report'
    report_path = report_dir / 'report.html'
    run_pytest(
        args=[function_test(step_tests.test_with_multiple_consecutive_steps)],
        tmp_dir=tmp_path,
        show_steps=True,
        html_report_dir=report_dir,
        parallel=1
    )
    data = [{"step": "step-1", "result": "Pass"}, {"step": "step-2", "result": "Pass"},
            {"step": "step-3", "result": "Pass"}]
    expected_json = (json.dumps(data, indent=2)
                     .replace('\n', '\\n')
                     .replace('"', '\\"'))

    html_content = report_path.read_text()
    html_content_unescaped = html.unescape(html_content)
    assert expected_json in html_content_unescaped


def test_report_contains_multiple_consecutive_and_nested_steps_from_test(tmp_path):
    report_dir = tmp_path / 'report'
    report_path = report_dir / 'report.html'
    run_pytest(
        args=[function_test(step_tests.test_with_multiple_consecutive_and_nested_steps)],
        tmp_dir=tmp_path,
        show_steps=True,
        html_report_dir=report_dir,
        parallel=1
    )
    data = [{'step': 'step-1', 'result': 'Pass'}, {'step': 'step-2', 'result': 'Pass', 'steps':
        [{'step': 'step-3', 'result': 'Pass'}]}]
    expected_json = (json.dumps(data, indent=2)
                     .replace('\n', '\\n')
                     .replace('"', '\\"'))

    html_content = report_path.read_text()
    html_content_unescaped = html.unescape(html_content)
    assert expected_json in html_content_unescaped


def test_report_contains_decorator_step_from_test(tmp_path):
    report_dir = tmp_path / 'report'
    report_path = report_dir / 'report.html'
    run_pytest(
        args=[function_test(step_tests.test_step_with_message)],
        tmp_dir=tmp_path,
        show_steps=True,
        html_report_dir=report_dir,
        parallel=1
    )
    data = [{'step': 'decorator-step', 'result': 'Pass'}]
    expected_json = (json.dumps(data, indent=2)
                     .replace('\n', '\\n')
                     .replace('"', '\\"'))

    html_content = report_path.read_text()
    html_content_unescaped = html.unescape(html_content)
    assert expected_json in html_content_unescaped


def test_report_contains_with_statement_and_nested_decorator_steps_from_test(tmp_path):
    report_dir = tmp_path / 'report'
    report_path = report_dir / 'report.html'
    run_pytest(
        args=[function_test(step_tests.test_with_with_statement_and_nested_decorator_function)],
        tmp_dir=tmp_path,
        show_steps=True,
        html_report_dir=report_dir,
        parallel=1
    )
    data = [{'step': 'with-step', 'result': 'Pass', 'steps': [{'step': 'decorator-step', 'result': 'Pass'}]}]
    expected_json = (json.dumps(data, indent=2)
                     .replace('\n', '\\n')
                     .replace('"', '\\"'))

    html_content = report_path.read_text()
    html_content_unescaped = html.unescape(html_content)
    assert expected_json in html_content_unescaped


def test_report_contains_with_decorator_function_and_nested_with_statement_steps_from_test(tmp_path):
    report_dir = tmp_path / 'report'
    report_path = report_dir / 'report.html'
    run_pytest(
        args=[function_test(step_tests.test_with_decorator_function_and_nested_with_statement)],
        tmp_dir=tmp_path,
        show_steps=True,
        html_report_dir=report_dir,
        parallel=1
    )
    data = [{'step': 'decorator-step', 'result': 'Pass', 'steps': [{'step': 'with-step', 'result': 'Pass'}]}]
    expected_json = (json.dumps(data, indent=2)
                     .replace('\n', '\\n')
                     .replace('"', '\\"'))

    html_content = report_path.read_text()
    html_content_unescaped = html.unescape(html_content)
    assert expected_json in html_content_unescaped


def test_report_contains_with_statement_with_caught_exception_steps_from_test(tmp_path):
    report_dir = tmp_path / 'report'
    report_path = report_dir / 'report.html'
    run_pytest(
        args=[function_test(step_tests.test_nested_with_statement_with_caught_exception)],
        tmp_dir=tmp_path,
        show_steps=True,
        html_report_dir=report_dir,
        parallel=1
    )
    data = [{'step': 'outer-step', 'result': "Raised ValueError('An error occurred')", 'steps':
        [{'step': 'step-with-exception', 'result': "Raised ValueError('An error occurred')"}]},
            {'step': 'after-exception-step', 'result': 'Pass'}]
    expected_json = (json.dumps(data, indent=2)
                     .replace('\n', '\\n')
                     .replace('"', '\\"'))

    html_content = report_path.read_text()
    html_content_unescaped = html.unescape(html_content)
    assert expected_json in html_content_unescaped


def test_report_contains_with_statement_with_uncaught_exception_steps_from_test(tmp_path):
    report_dir = tmp_path / 'report'
    report_path = report_dir / 'report.html'
    run_pytest(
        args=[function_test(step_tests.test_nested_with_statement_with_uncaught_exception), '--show-steps'],
        tmp_dir=tmp_path,
        show_steps=True,
        html_report_dir=report_dir,
        parallel=1
    )
    data = [{'step': 'outer-step', 'result': "Raised ValueError('An error occurred')", 'steps':
        [{'step': 'step-with-exception', 'result': "Raised ValueError('An error occurred')"}]}]
    expected_json = (json.dumps(data, indent=2)
                     .replace('\n', '\\n')
                     .replace('"', '\\"'))

    html_content = report_path.read_text()
    html_content_unescaped = html.unescape(html_content)
    assert expected_json in html_content_unescaped
