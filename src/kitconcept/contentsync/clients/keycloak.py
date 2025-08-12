from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
from keycloak.exceptions import KeycloakGetError
from kitconcept.contentsync import _types as t
from kitconcept.contentsync import logger
from kitconcept.contentsync.clients import ConnectionClient


class KeycloakClient(ConnectionClient):
    _connection: KeycloakOpenIDConnection
    _client: KeycloakAdmin
    _config: t.KeycloakConfig

    def _init_client(self):
        """Initialize Keycloak client with configuration"""
        config = self._config
        settings = {
            "server_url": config.server_url,
            "client_id": config.client_id,
            "client_secret_key": config.client_secret_key,
            "realm_name": config.realm_name,
            "verify": config.verify,
        }
        self._connection = KeycloakOpenIDConnection(**settings)
        self._client = KeycloakAdmin(connection=self._connection)

    def get_all_users(self) -> list[t.KeycloakUser]:
        """Retrieve all users from Keycloak"""
        try:
            users = self._client.get_users()
        except KeycloakGetError as e:
            logger.error(f"Failed to retrieve users: {e}")
            users = []
        return users

    def get_all_groups(self) -> list[t.KeycloakGroup]:
        """Query keycloak for groups and return group information."""
        client = self._client
        groups_info = client.get_groups({"briefRepresentation": False})
        return groups_info
