import pytest

from apibean.pytest.abstract import abstract_fixture
from apibean.pytest.protocols.config import ApibeanTestConfig

@pytest.fixture(scope="function")
@abstract_fixture
def apibean_config() -> ApibeanTestConfig:
    """
    Provide apibean test configuration for the current test.

    This fixture returns an ApibeanTestConfig object that defines
    how the apibean testing lifecycle behaves, including database
    reset strategy, data seeding options, and optional test features.

    The concrete configuration must be supplied by the application
    or test environment.

    The application must provide an implementation of this fixture.
    """
