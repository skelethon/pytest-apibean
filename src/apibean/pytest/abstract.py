from functools import wraps

import pytest

def abstract_fixture(func):
    """
    Mark a pytest fixture as an abstract (contract) fixture.

    This decorator designates a fixture as a required contract that must be
    implemented by the application under test. It is intended for core
    infrastructure fixtures that pytest-apibean depends on but cannot
    implement itself.

    When an abstract fixture is not overridden by the application, accessing
    it will immediately skip the test session with a clear and explicit
    message indicating that the fixture is missing.

    The decorator also attaches metadata to the wrapped function via the
    ``__apibean_abstract_fixture__`` attribute, allowing pytest-apibean to
    programmatically discover and list abstract fixtures (for example, via
    a custom command-line option).

    Typical use cases include fixtures such as:

    - ``apibean_config`` – application test configuration
    - ``apibean_container`` – dependency injection container
    - ``apibean_db`` – application database backend

    This decorator should only be applied to fixtures that are expected to be
    provided by the application and must not have a default implementation.
    """

    func.__apibean_abstract_fixture__ = True

    @wraps(func)
    def wrapper(*args, **kwargs):
        pytest.skip(f"{func.__name__} fixture not provided by application")
        return func(*args, **kwargs)
    return wrapper
