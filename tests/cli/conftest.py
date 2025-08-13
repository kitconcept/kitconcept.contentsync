import pytest


@pytest.fixture(scope="module", autouse=True)
def start_containers(keycloak_config, plone_config):
    """Start containers."""
    yield
