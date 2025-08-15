from collections.abc import Generator
from kitconcept.contentsync import settings
from pathlib import Path

import pytest


@pytest.fixture
def local_env(test_dir) -> Generator[Path, None, None]:
    lines = ["SYNC_DEBUG=1", "SYNC_SRC__SERVER_URL=http://sso.localhost"]
    path = test_dir / ".env"
    with open(path, "w") as f:
        for line in lines:
            f.write(f"{line}\n")
    yield test_dir
    # Remove .env file after usage
    path.unlink(missing_ok=True)


def test_get_settings_default(test_dir):
    from kitconcept.contentsync.clients.keycloak import KeycloakClient
    from kitconcept.contentsync.clients.plone import PloneClient
    from kitconcept.contentsync.settings import SyncSettings
    from kitconcept.contentsync.sync.person import PersonSyncer

    config = settings.get_settings()
    assert isinstance(config, SyncSettings)
    assert config.debug is False
    assert config.sync is PersonSyncer
    assert isinstance(config.src, KeycloakClient)
    assert isinstance(config.dst, PloneClient)


def test_get_settings_env_file(local_env):
    from kitconcept.contentsync.settings import SyncSettings

    config = settings.get_settings()
    assert isinstance(config, SyncSettings)
    assert config.debug is True
    assert config.src._config.server_url == "http://sso.localhost"
