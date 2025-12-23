import pytest

from apibean.pytest.protocols.config import ApibeanTestConfig

@pytest.fixture
def apibean_config() -> ApibeanTestConfig:
    pytest.skip("configs not provided")
