from __future__ import annotations

import os
import tomllib
from pathlib import Path
from dataclasses import dataclass


@dataclass(slots=True)
class ApibeanOptions:
    base_url: str = "http://localhost:8000"
    login_path: str = "/auth/login"
    username: str = "admin"
    password: str = "admin"
    timeout: float = 10.0
    auto_login: bool = True
    seed_modules: str = "tests.seeders"
    seed_marker: str = "seed"   # @pytest.mark.seed(...)
    seed_mode: str = "auto"     # auto | explicit | off


_DEFAULTS = ApibeanOptions()


def _load_pyproject_options() -> dict:
    """
    Load [tool.pytest.apibean.options] từ pyproject.toml
    """
    for path in (Path.cwd(), *Path.cwd().parents):
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            with pyproject.open("rb") as f:
                data = tomllib.load(f)
            return (
                data
                .get("tool", {})
                .get("pytest", {})
                .get("apibean", {})
                .get("options", {})
            )
    return {}


def load_settings() -> ApibeanOptions:
    defaults = _DEFAULTS
    opts = _load_pyproject_options()

    return ApibeanOptions(
        base_url=opts.get(
            "base_url",
            os.getenv("APIBEAN_BASE_URL", defaults.base_url),
        ),
        login_path=opts.get(
            "login_path",
            os.getenv("APIBEAN_LOGIN_PATH", defaults.login_path),
        ),
        username=opts.get(
            "username",
            os.getenv("APIBEAN_USERNAME", defaults.username),
        ),
        password=opts.get(
            "password",
            os.getenv("APIBEAN_PASSWORD", defaults.password),
        ),
        timeout=float(
            opts.get(
                "timeout",
                os.getenv("APIBEAN_TIMEOUT", str(defaults.timeout)),
            )
        ),
        auto_login=bool(opts.get("auto_login", defaults.auto_login)),
        seed_modules=opts.get(
            "seed_modules",
            os.getenv("APIBEAN_SEED_MODULES", defaults.seed_modules),
        ),
        seed_marker=opts.get(
            "seed_marker",
            os.getenv("APIBEAN_SEED_MARKER", defaults.seed_marker),
        ),
    )


settings = load_settings()
