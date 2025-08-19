from collections.abc import Generator
from kitconcept.contentsync import _types as t
from kitconcept.contentsync.clients.plone import PloneClient
from pathlib import Path
from requests.exceptions import ConnectionError as RequestsConnectionError

import pytest
import requests


@pytest.fixture(autouse=True)
def test_dir(monkeypatch, tmp_path) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


def is_responsive(url: str, accepted_codes: tuple[int, ...] = (200,)) -> bool:
    try:
        response = requests.get(url, timeout=5)
    except RequestsConnectionError:
        return False
    return response.status_code in accepted_codes


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """Fixture pointing to the docker-compose file to be used."""
    return Path(str(pytestconfig.rootdir)).resolve() / "docker-compose.yml"


@pytest.fixture(scope="session")
def keycloak_service(docker_ip, docker_services):
    """Ensure that keycloak service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("keycloak", 8080)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=50.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def keycloak_config(keycloak_service) -> t.KeycloakConfig:
    return t.KeycloakConfig(
        server_url=keycloak_service,
        realm_name="plone",
        client_id="plone-admin",
        client_secret_key="12345678",  # noQA: S106, nosec B105
        verify=False,
    )


@pytest.fixture(scope="session")
def plone_service(docker_ip, docker_services):
    """Ensure that plone service is up and responsive."""
    port = docker_services.port_for("plone", 8080)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=50.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def plone_config(plone_service) -> t.PloneConfig:
    site_url = f"{plone_service}/Plone"
    api_url = f"{site_url}/++api++"
    return t.PloneConfig(
        site_url=site_url,
        api_url=api_url,
        basic_auth=None,
        username="admin",
        password="admin",  # noQA: S106, nosec B105
    )


@pytest.fixture(scope="session")
def plone_client(plone_config) -> Generator[PloneClient, None, None]:
    client = PloneClient(config=plone_config)
    yield client


@pytest.fixture(scope="session")
def populate_portal(plone_client) -> None:
    plone_client.authenticate()
    # Create a Document at the root of the portal
    content = plone_client.create_content(
        "/",
        {
            "@id": "/reports",
            "@type": "Document",
            "id": "reports",
            "title": "Reports",
        },
    )
    if content:
        for idx in range(1, 99):
            obj_id = f"report-{idx}"
            plone_client.create_or_update_content(
                {
                    "@id": f"/reports/{obj_id}",
                    "@type": "Document",
                    "id": obj_id,
                    "title": f"Report {idx}",
                },
            )
    return


def pytest_collection_modifyitems(config, items):
    """Mark tests that require docker."""
    for item in items:
        fixtures = item.fixturenames
        if "docker_ip" in fixtures:
            item.add_marker(pytest.mark.docker)
