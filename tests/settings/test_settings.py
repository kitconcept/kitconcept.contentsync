from kitconcept.contentsync.settings import get_settings


def test_get_settings_default():
    from kitconcept.contentsync.clients.keycloak import KeycloakClient
    from kitconcept.contentsync.clients.plone import PloneClient
    from kitconcept.contentsync.settings import SyncSettings
    from kitconcept.contentsync.sync.person import PersonSyncer

    settings = get_settings()
    assert isinstance(settings, SyncSettings)
    assert settings.debug is False
    assert settings.sync is PersonSyncer
    assert isinstance(settings.src, KeycloakClient)
    assert isinstance(settings.dst, PloneClient)
