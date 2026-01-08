#  Copyright (c) 2026 CUJO LLC
from tests.test_step.html_reporting.html_reporting_sample_tests import save_attachments
from tests.test_step.util import run_pytest, function_test, ReducedTestCase


def test_inject_noop_extras_without_html_report(tmp_path):
    suite = run_pytest(
        args=[function_test(save_attachments.test_inject_extras)],
        tmp_dir=tmp_path,
    ).suite
    assert suite.test_cases == [
        ReducedTestCase(save_attachments.test_inject_extras.__name__, None)
    ]
    assert ("Injected extras are <class 'test_step.html_reporting.extras.NoopExtras'>"
            in suite.test_cases[0].stdout)


def test_inject_extras_with_html_report(tmp_path):
    suite = run_pytest(
        args=[function_test(save_attachments.test_inject_extras)],
        tmp_dir=tmp_path,
        html_report_dir=tmp_path / "report"
    ).suite
    assert suite.test_cases == [
        ReducedTestCase(save_attachments.test_inject_extras.__name__, None)
    ]
    assert ("Injected extras are <class 'test_step.html_reporting.extras.FileExtras'>"
            in suite.test_cases[0].stdout)


def test_inject_passthrough_extras_with_self_contained_html_report(tmp_path):
    suite = run_pytest(
        args=[
            function_test(save_attachments.test_inject_extras),
            '--self-contained-html'
        ],
        tmp_dir=tmp_path,
        html_report_dir=tmp_path / "report",
        show_steps=True
    ).suite
    assert suite.test_cases == [
        ReducedTestCase(save_attachments.test_inject_extras.__name__, None)
    ]
    assert ("Injected extras are <class 'test_step.html_reporting.extras.PassthroughExtras'>"
            in suite.test_cases[0].stdout)
