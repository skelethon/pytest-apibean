import pytest

from apibean.pytest.abstract import abstract_fixture
from apibean.pytest.protocols.container import ApibeanTestContainer

@pytest.fixture(scope="session")
@abstract_fixture
def apibean_container() -> ApibeanTestContainer:
    """
    Abstract contract fixture for the application test container.

    This fixture defines the dependency container contract required by
    pytest-apibean. It represents the application's wired dependency graph
    used during testing.

    The container returned by this fixture is expected to expose application
    services, repositories, and infrastructure components required by
    Apibean test fixtures (for example: authentication services, domain
    services, or repositories).

    This fixture does not provide any default implementation. Applications
    must explicitly override it and return a fully configured test container.

    If the application does not provide an implementation, the entire test
    session will be skipped with a clear message indicating that the
    ``apibean_container`` fixture is missing.

    The exact container type is application-specific but must conform to
    the expectations of fixtures that consume it. Typically, this will be
    a container created using a dependency injection framework (such as
    dependency-injector), but no specific framework is required.

    This fixture is scoped to the test session to allow container wiring
    and expensive initialization to occur only once per test run.
    """
