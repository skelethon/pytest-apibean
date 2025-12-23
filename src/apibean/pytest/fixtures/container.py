import pytest

from apibean.pytest.protocols.container import ApibeanTestContainer


@pytest.fixture(scope="session")
def apibean_container() -> ApibeanTestContainer:
    """
    MUST be provided by project
    """
    raise RuntimeError(
        "Project must provide `apibean_container` fixture "
        "that implements ApibeanTestContainer"
    )


@pytest.fixture(autouse=True)
def _container_lifecycle(apibean_container: ApibeanTestContainer):
    apibean_container.wire()
    yield
    apibean_container.unwire()
