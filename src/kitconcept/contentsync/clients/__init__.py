from kitconcept.contentsync import _types as t


class ConnectionClient:
    system: str
    _config: t.ClientConfig

    def __init__(self, config: t.ClientConfig):
        self._config = config
        self._init_client()

    def _init_client(self):
        """Initialize client with configuration."""
        pass

    def test_connection(self) -> bool:
        """Test the client connection to the remote system."""
        return False


def get_client(type_: str, raw_settings: dict) -> ConnectionClient:
    from .keycloak import KeycloakClient
    from .plone import PloneClient

    client_settings: dict[str, tuple[t.ClientConfig, type[ConnectionClient]]] = {
        "keycloak": (t.KeycloakConfig, KeycloakClient),
        "plone": (t.PloneConfig, PloneClient),
    }
    if type_ not in client_settings:
        raise ValueError(f"No client class found for type: {type_}")
    client_config, client_class = client_settings[type_]
    settings = client_config(**raw_settings)
    return client_class(settings)
