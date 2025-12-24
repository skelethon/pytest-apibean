import pytest

@pytest.fixture(scope="session")
def apibean_db():
    pytest.skip("apibean_db not provided")

@pytest.fixture(scope="function", autouse=False)
def apibean_reset_db():
    pytest.skip("apibean_reset_db not provided")
