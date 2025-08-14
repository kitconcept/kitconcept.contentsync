from kitconcept.contentsync import settings

import pytest


@pytest.fixture
def local_env(test_dir):
    lines = ["SYNC_DEBUG=1", "SYNC_SRC__SERVER_URL=http://sso.localhost"]
    with open(test_dir / ".env", "w") as f:
        for line in lines:
            f.write(f"{line}\n")
    return test_dir


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
