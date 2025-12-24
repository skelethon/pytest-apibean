import pytest

from apibean.pytest.abstract import abstract_fixture

@pytest.fixture(scope="session")
@abstract_fixture
def apibean_db():
    """
    Abstract contract fixture for the application database.

    This fixture defines the database contract required by pytest-apibean.
    It does not provide any implementation and must be explicitly implemented
    by the application under test.

    If the application does not override this fixture, the entire test session
    will be skipped with a clear and explicit message indicating that the
    ``apibean_db`` fixture is missing.

    The object returned by this fixture represents the application's database
    backend and is consumed by core Apibean fixtures such as
    ``apibean_reset_db`` and ``apibean_seed_data``.

    The exact return type is application-specific and intentionally left
    unspecified. It must only satisfy the expectations of the fixtures that
    depend on it.

    This fixture is scoped to the test session to allow the application to
    perform expensive setup (e.g. engine creation, container wiring) once
    per test run.
    """

@pytest.fixture(scope="function")
@abstract_fixture
def apibean_reset_db():
    """
    Reset application database state before each test.

    This fixture is responsible for clearing application data
    while preserving the database schema. It is typically used
    to ensure test isolation between test cases.

    The application must provide an implementation of this fixture.
    """
