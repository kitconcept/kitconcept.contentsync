from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
from keycloak.exceptions import KeycloakGetError
from kitconcept.contentsync import _types as t
from kitconcept.contentsync import logger
from kitconcept.contentsync.clients import ConnectionClient
from kitconcept.contentsync.utils import dotted_name_for_object


class KeycloakClient(ConnectionClient):
    system = "Keycloak"
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

    def get_users(self, query: dict | None = None) -> list[t.KeycloakUser]:
        """Query keycloak for users and return user information."""
        try:
            users = self._client.get_users(query)
        except KeycloakGetError as e:
            logger.error(f"Failed to retrieve users: {e}")
            users = []
        return users

    def get_groups(self, query: dict | None = None) -> list[t.KeycloakGroup]:
        """Query keycloak for groups and return group information."""
        query = query if query else {}
        if "briefRepresentation" not in query:
            query["briefRepresentation"] = False
        client = self._client
        groups_info = client.get_groups(query=query)
        return groups_info

    def __repr__(self) -> str:
        """Return a string representation of the KeycloakClient."""
        return (
            "\n"
            f" - {self.system} ({dotted_name_for_object(self)})\n"
            f" - Server: {self._config.server_url}\n"
            f" - Client ID: {self._config.client_id}\n"
            f" - Realm: {self._config.realm_name}\n"
        )
