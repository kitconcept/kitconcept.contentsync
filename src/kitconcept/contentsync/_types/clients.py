from dataclasses import dataclass
from typing import TypedDict


class BasicAuth(TypedDict):
    """Basic authentication credentials for Plone"""

    username: str
    password: str


@dataclass
class ClientConfig:
    """Configuration for a client"""

    __name__ = ""


@dataclass
class PloneConfig(ClientConfig):
    """Configuration for Plone instance"""

    __name__ = "plone"
    site_url: str = ""
    api_url: str = ""
    basic_auth: BasicAuth | None = None
    username: str | None = None
    password: str | None = None


@dataclass
class KeycloakConfig(ClientConfig):
    """Configuration for Keycloak instance"""

    __name__ = "keycloak"
    server_url: str = ""
    realm_name: str = ""
    basic_auth: BasicAuth | None = None
    client_id: str = ""
    client_secret_key: str = ""
    verify: bool = False
