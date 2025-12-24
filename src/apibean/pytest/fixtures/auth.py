import pytest

@pytest.fixture(scope="function")
def login(apibean_container):
    def _login(username: str, password: str) -> str:
        auth_service = apibean_container.auth_service()
        result = auth_service.login(dict(username=username, password=password))
        return result["access_token"]
    return _login

@pytest.fixture(scope="function")
def deprecated_login(apibean_container):
    """
    Fixture login: trả về một hàm để thực hiện đăng nhập trong test, tạo access_token bằng
    deprecated_secret_key.

    Ví dụ:
        token = login("alice@example.com", "123456")
        headers = {"Authorization": f"Bearer {token}"}
    """
    def _login(username: str, password: str) -> str:
        auth_service = apibean_container.auth_service()
        result = auth_service.deprecated_login(dict(username=username, password=password))
        assert result is not None, f"auth_service.login() failed: { result }"
        return result["access_token"]

    return _login

@pytest.fixture(scope="function")
def delegated_login(apibean_container):
    """
    Fixture delegated_login: trả về một hàm để thực hiện đăng nhập trong test.

    Ví dụ:
        token = login("alice@example.com", "123456", org_slug"")
        headers = {"Authorization": f"Bearer {token}"}
    """
    def _login(username: str, password: str, org_slug: str) -> str:
        org_service = apibean_container.org_service()
        org_id = org_service.get_id_by_slug(org_slug)
        auth_service = apibean_container.auth_service()
        result = auth_service.delegated_login(dict(
            org_slug=org_slug,
            username=username,
            password=password))
        assert result is not None, f"auth_service.delegated_login() failed: { result }"
        return result["access_token"]

    return _login

@pytest.fixture(scope="function")
def root_access_token(login, apibean_config):
    return login(apibean_config.ROOT_USER_EMAIL, apibean_config.ROOT_USER_PASSWORD)

@pytest.fixture(scope="function")
def sync_access_token(login, apibean_config):
    return login(apibean_config.SYNC_USER_EMAIL, apibean_config.SYNC_USER_PASSWORD)

@pytest.fixture(scope="function")
def inject_access_token():
    def _inject_access_token(access_token, headers = None):
        headers = headers or {}
        headers.update({
            "Authorization": f"Bearer {access_token}"
        })
        return headers
    return _inject_access_token
