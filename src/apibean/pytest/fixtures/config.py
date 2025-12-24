import pytest

from apibean.pytest.protocols.config import ApibeanTestConfig

@pytest.fixture
def apibean_config() -> ApibeanTestConfig:
    pytest.skip("apibean_config not provided")
