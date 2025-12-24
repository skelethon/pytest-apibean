from typing import Protocol, runtime_checkable

@runtime_checkable
class ApibeanTestConfig(Protocol):
    ROOT_USER_EMAIL: str
    ROOT_USER_PASSWORD: str

    SYNC_USER_EMAIL: str
    SYNC_USER_PASSWORD: str
