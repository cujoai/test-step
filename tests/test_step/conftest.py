#  Copyright (c) 2026 CUJO LLC
import logging.config

from _pytest.config import hookimpl
from _pytest.nodes import Item

from test_step.logging import default_log_config

logging.config.dictConfig(default_log_config)
logger = logging.getLogger(__name__)


@hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: Item):
    outcome = yield
    config = item.config
    if not config.getoption("--show-steps"):
        return

    report = outcome.get_result()
    if getattr(report, 'steps', None):
        logger.info(report.steps)
