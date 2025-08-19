from kitconcept.contentsync.clients.plone import PloneClient

import pytest
import requests


@pytest.fixture(scope="module")
def person_payload() -> dict:
    return {
        "@type": "Person",
        "id": "john-doe",
        "first_name": "John",
        "last_name": "Doe",
        "title": "John Doe",
        "description": "A person named John Doe",
        "roles": [],
    }


@pytest.mark.parametrize(
    "attr, expected_type",
    [
        ("session", requests.Session),
        ("site_url", str),
        ("api_url", str),
        ("is_authenticated", bool),
    ],
)
def test_client_initialization(plone_config, attr, expected_type):
    client = PloneClient(config=plone_config)
    assert client is not None
    assert isinstance(client, PloneClient)

    assert getattr(client, attr) is not None
    assert isinstance(getattr(client, attr), expected_type)


@pytest.mark.parametrize(
    "endpoint,expected",
    [
        (
            "http://127.0.0.1:8080/Plone/@login",
            "http://127.0.0.1:8080/Plone/++api++/@login",
        ),
        (
            "http://127.0.0.1:8080/Plone/++api++/@login",
            "http://127.0.0.1:8080/Plone/++api++/@login",
        ),
        ("//@login", "http://127.0.0.1:8080/Plone/++api++/@login"),
        ("/@login", "http://127.0.0.1:8080/Plone/++api++/@login"),
        ("@login", "http://127.0.0.1:8080/Plone/++api++/@login"),
        ("foo-bar", "http://127.0.0.1:8080/Plone/++api++/foo-bar"),
    ],
)
def test_client__get_url(plone_client, endpoint, expected):
    url = plone_client._get_url(endpoint)
    assert url == expected


def test_client_content_lifecycle(plone_client, person_payload):
    # Authenticate
    plone_client.authenticate()
    # Create content
    created = plone_client.create_content("/", person_payload)
    assert isinstance(created, dict)
    person_path = created["@id"]
    assert person_path.endswith(person_payload["id"])

    # Read content
    read = plone_client.get_content(person_path)
    assert isinstance(read, dict)
    assert read["@id"] == person_path

    # Update content
    payload = {"id": "jane-doe", "first_name": "Jane"}
    updated = plone_client.update_content(person_path, payload)
    assert updated is True
    read = plone_client.get_content(person_path)
    assert read["first_name"] == "Jane"
    person_path = read["@id"]

    # Search content
    params = {"portal_type": "Person", "getId": "jane-doe"}
    search_results = plone_client.search_content("/", params)
    assert isinstance(search_results, dict)
    assert search_results["items_total"] == 1
    assert "items" in search_results
    assert len(search_results["items"]) == 1
    assert search_results["items"][0]["@id"] == person_path

    # Delete content
    deleted = plone_client.delete_content(person_path)
    assert deleted is True
    with pytest.raises(requests.HTTPError) as excinfo:
        plone_client.get_content(person_path)
    assert excinfo.value.response.status_code == 404


def test_client_search_content(plone_client, populate_portal):
    params = {"portal_type": "Document"}
    search_results = plone_client.search_content("/reports", params)
    assert isinstance(search_results, dict)
    assert search_results["items_total"] == 99
    assert "batching" in search_results
    assert len(search_results["items"]) == 25


def test_client_search_content_expand(plone_client, populate_portal):
    params = {"portal_type": "Document"}
    search_results = plone_client.search_content("/reports", params, expand_batch=True)
    assert isinstance(search_results, dict)
    assert search_results["items_total"] == len(search_results["items"])
    assert "batching" not in search_results
