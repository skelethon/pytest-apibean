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
            os.getenv("API_BASE_URL", defaults.base_url),
        ),
        login_path=opts.get(
            "login_path",
            os.getenv("API_LOGIN_PATH", defaults.login_path),
        ),
        username=opts.get(
            "username",
            os.getenv("API_USERNAME", defaults.username),
        ),
        password=opts.get(
            "password",
            os.getenv("API_PASSWORD", defaults.password),
        ),
        timeout=float(
            opts.get(
                "timeout",
                os.getenv("API_TIMEOUT", defaults.timeout),
            )
        ),
        auto_login=bool(opts.get("auto_login", defaults.auto_login)),
    )


settings = load_settings()
