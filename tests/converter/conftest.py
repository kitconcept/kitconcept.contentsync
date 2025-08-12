from kitconcept.contentsync import _types as t

import pytest


@pytest.fixture
def keycloak_user() -> t.KeycloakUser:
    """Fixture for a sample Keycloak user."""
    return {
        "access": {"manage": False},
        "attributes": {
            "LDAP_ENTRY_DN": ["cn=dtremea,ou=users,dc=plone,dc=org"],
            "LDAP_ID": ["87bbd51e-0b23-1040-8f10-61523cfcb04f"],
            "createTimestamp": ["20250811172241Z"],
            "location": ["Garibaldi, Rio Grande do Sul, Brazil"],
            "modifyTimestamp": ["20250811172241Z"],
        },
        "createdTimestamp": 1754932976002,
        "disableableCredentialTypes": [],
        "email": "dtremea@plone.org",
        "emailVerified": False,
        "enabled": True,
        "federationLink": "e460c359-ad37-4c1d-b119-e05c2ecdf1bc",
        "firstName": "Dorneles",
        "id": "7b10d7b5-dd77-4aa2-8a2a-9945aa06d504",
        "lastName": "Tremea",
        "notBefore": 0,
        "origin": "e460c359-ad37-4c1d-b119-e05c2ecdf1bc",
        "requiredActions": [],
        "totp": False,
        "username": "dtremea",
    }


@pytest.fixture
def plone_person() -> t.PlonePerson:
    """Fixture for a sample Plone person."""
    return {
        "@id": "http://plone.org/users/dtremea",
        "first_name": "Dorneles",
        "last_name": "Tremea",
        "title": "Dorneles Tremea",
        "description": "A user from Keycloak",
    }
