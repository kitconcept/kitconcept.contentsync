from kitconcept.contentsync import _types as t

import pytest


@pytest.fixture
def keycloak_user() -> t.KeycloakUser:
    """Fixture for a sample Keycloak user."""
    return {
        "id": "329b236b-1f64-4873-848e-13e6053a869f",
        "username": "dtremea",
        "firstName": "Dorneles",
        "lastName": "Tremea",
        "email": "dtremea@plone.org",
        "emailVerified": False,
        "attributes": {
            "LDAP_ENTRY_DN": ["cn=dtremea,ou=users,dc=plone,dc=org"],
            "phone": ["+555132232323"],
            "mobile": ["+555199992323"],
            "location": ["Garibaldi, Rio Grande do Sul, Brazil"],
            "fullname": ["Dorneles Tremea"],
            "LDAP_ID": ["7e6acb46-0ca4-1040-8b6d-816234385567"],
            "createTimestamp": ["20250813151821Z"],
            "modifyTimestamp": ["20250813151821Z"],
        },
        "origin": "e460c359-ad37-4c1d-b119-e05c2ecdf1bc",
        "createdTimestamp": 1755098439950,
        "enabled": True,
        "totp": False,
        "federationLink": "e460c359-ad37-4c1d-b119-e05c2ecdf1bc",
        "disableableCredentialTypes": [],
        "requiredActions": [],
        "notBefore": 0,
        "access": {"manage": False},
    }


@pytest.fixture
def plone_person() -> t.PlonePerson:
    """Fixture for a sample Plone person."""
    return {
        "@id": "http://plone.org/users/dtremea",
        "@type": "Person",
        "id": "dtremea",
        "first_name": "Dorneles",
        "last_name": "Tremea",
        "title": "Dorneles Tremea",
        "description": "A user from Keycloak",
    }
