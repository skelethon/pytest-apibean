from dataclasses import asdict

import pytest

from .fixtures.auth import *
from .fixtures.config import *
from .fixtures.container import *
from .fixtures.database import *
from .fixtures.seeds import *


def pytest_addoption(parser):
    parser.addoption(
        "--apibean-show-config",
        action="store_true",
        help="Show apibean pytest configuration",
    )


def pytest_cmdline_main(config):
    if config.getoption("--apibean-show-config"):
        from .settings import settings
        print("\n[pytest-apibean config]")
        for k, v in asdict(settings).items():
            print(f"  {k} = {v}")
        return pytest.ExitCode.OK
