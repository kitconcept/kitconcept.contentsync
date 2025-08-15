from collections.abc import Generator
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
from kitconcept.contentsync.clients.keycloak import KeycloakClient

import pytest


@pytest.fixture(scope="module")
def keycloak_client(keycloak_config) -> Generator[KeycloakClient, None, None]:
    client = KeycloakClient(config=keycloak_config)
    yield client


@pytest.mark.parametrize(
    "attr, expected_type",
    [
        ("_connection", KeycloakOpenIDConnection),
        ("_client", KeycloakAdmin),
    ],
)
def test_client_initialization(keycloak_config, attr, expected_type):
    client = KeycloakClient(config=keycloak_config)
    assert client is not None
    assert isinstance(client, KeycloakClient)

    assert getattr(client, attr) is not None
    assert isinstance(getattr(client, attr), expected_type)


def test_client_get_groups(keycloak_client):
    groups = keycloak_client.get_groups()
    assert groups is not None
    assert isinstance(groups, list)
    assert len(groups) == 3


def test_client_get_users(keycloak_client):
    users = keycloak_client.get_users()
    assert users is not None
    assert isinstance(users, list)
    assert len(users) == 4
