#  Copyright (c) 2026 CUJO LLC
import gzip

import pytest
import pytest_html.extras
from _pytest.fixtures import FixtureRequest

from test_step.html_reporting.extras import PassthroughExtras, FileExtras
from test_step.util import ArgumentError


def test_passthrough_extra_text():
    extras = []
    PassthroughExtras(extras).attach_text('test content', 'test name')
    assert extras == [pytest_html.extras.text('test content', 'test name')]


def test_passthrough_extra_file(tmp_path):
    extras = []
    file = tmp_path / 'test_file.txt'
    file.write_text('test content')
    PassthroughExtras(extras).attach_file(file)
    assert extras == [pytest_html.extras.text('test content', 'test_file.txt')]


def test_file_extra_text(tmp_path, request: FixtureRequest):
    extras = []
    report_dir = tmp_path / 'report'
    FileExtras(request.node, extras, report_dir).attach_text('test content', 'test name')
    assert extras == [
        pytest_html.extras.url(
            'extras/tests_test_step_html_reporting_extras_test.py__test_file_extra_text_0_1.txt',
            'test name'
        )
    ]
    stored_file_path = (report_dir / 'extras'
                        / 'tests_test_step_html_reporting_extras_test.py__test_file_extra_text_0_1.txt')
    assert stored_file_path.read_text() == 'test content'


def test_file_extra_text_compressed(tmp_path, request: FixtureRequest):
    extras = []
    report_dir = tmp_path / 'report'
    FileExtras(request.node, extras, report_dir).attach_text('test content', 'test name', True)
    assert extras == [
        pytest_html.extras.url(
            'extras/tests_test_step_html_reporting_extras_test.py__test_file_extra_text_compressed_0_1.txt.gz',
            'test name.gz'
        )
    ]
    stored_file_path = (report_dir / 'extras' / 'tests_test_step_html_reporting_extras_test.'
                                                'py__test_file_extra_text_compressed_0_1.txt.gz')
    with gzip.open(stored_file_path, 'rt') as f:
        assert f.read() == 'test content'


def test_file_extra_file(tmp_path, request: FixtureRequest):
    extras = []
    report_dir = tmp_path / 'report'
    file = tmp_path / 'test_file.txt'
    file.write_text('test content')
    FileExtras(request.node, extras, report_dir).attach_file(file)
    assert extras == [
        pytest_html.extras.url(
            'extras/tests_test_step_html_reporting_extras_test.py__test_file_extra_file_0_1.txt',
            'test_file.txt'
        )
    ]
    stored_file_path = (report_dir / 'extras' /
                        'tests_test_step_html_reporting_extras_test.py__test_file_extra_file_0_1.txt')
    assert stored_file_path.read_text() == 'test content'


def test_file_extra_file_compressed(tmp_path, request: FixtureRequest):
    extras = []
    report_dir = tmp_path / 'report'
    file = tmp_path / 'test_file.txt'
    file.write_text('test content')
    FileExtras(request.node, extras, report_dir).attach_file(file, compress=True)
    assert extras == [
        pytest_html.extras.url(
            'extras/tests_test_step_html_reporting_extras_test.py__test_file_extra_file_compressed_0_1.txt.gz',
            'test_file.txt.gz'
        )
    ]
    stored_file_path = (report_dir / 'extras' / 'tests_test_step_html_reporting_extras_test.'
                                                'py__test_file_extra_file_compressed_0_1.txt.gz')
    with gzip.open(stored_file_path, 'rt') as f:
        assert f.read() == 'test content'


def test_can_not_attach_file_without_extension(tmp_path, request: FixtureRequest):
    extras = []
    report_dir = tmp_path / 'report'
    file = tmp_path / 'test_file'
    file.write_text('test content')
    with pytest.raises(ArgumentError):
        FileExtras(request.node, extras, report_dir).attach_file(file)
