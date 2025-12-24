import anyio
import importlib
import pytest

from apibean.pytest.settings import settings

@pytest.fixture(scope="function")
def apibean_seed_modules():
    return settings.seed_modules or "tests.seeders"

@pytest.fixture(autouse=False)
def apibean_seed_data(request, apibean_container, apibean_seed_modules):
    """
    Fixture tự động seed dữ liệu dựa trên marker @pytest.mark.seed(...).

    Cho phép:
        @pytest.mark.seed("user.basic", count=3)
        @pytest.mark.seed("user_admin", active=False)
    """

    markers = reversed(list(request.node.iter_markers("seed")))
    if not markers:
        yield
        return

    for marker in markers:
        # args[0] là seed name, kwargs chứa tham số bổ sung
        seed_name = marker.args[0] if marker.args else marker.kwargs.get("name")
        kwargs = marker.kwargs or {}

        if not seed_name:
            raise ValueError("Missing seed name in pytest.mark.seed()")

        try:
            prefix, variant = seed_name.split(".", 1)
        except ValueError as e:
            raise ValueError(f"Invalid seed name: '{seed_name}' (must be in format 'module.variant')") from e

        seeder_module_name = f"{apibean_seed_modules}.{prefix}_seeder"
        seeder_class_name = "".join(part.capitalize() for part in prefix.split("_")) + "Seeder"

        try:
            module = importlib.import_module(seeder_module_name)
            seeder_cls = getattr(module, seeder_class_name)
            seeder = seeder_cls(seed=seed_name, session=None, container=apibean_container, **kwargs)
            if hasattr(seeder, "run_in_anyio_worker") and getattr(seeder, "run_in_anyio_worker"):
                anyio.run(anyio.to_thread.run_sync, seeder.run)
            else:
                seeder.run()
        except (ImportError, AttributeError) as e:
            raise RuntimeError(f"Couldn't load the class [{seeder_class_name}] for '{seed_name}': {e}") from e

    yield

@pytest.fixture(autouse=False)
def apibean_before_reset_db():
    yield

@pytest.fixture(autouse=True)
def apibean_testcase_loop(apibean_before_reset_db, apibean_reset_db, apibean_seed_data):
    yield
