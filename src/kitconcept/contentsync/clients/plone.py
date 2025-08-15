from kitconcept.contentsync import _types as t
from kitconcept.contentsync import logger
from kitconcept.contentsync.clients import ConnectionClient
from kitconcept.contentsync.utils import dotted_name_for_object
from requests.auth import HTTPBasicAuth
from typing import Any
from urllib.parse import urljoin

import requests


class PloneClient(ConnectionClient):
    """Base client for Plone REST API operations"""

    system = "Plone"

    _config: t.PloneConfig
    session: requests.Session
    site_url: str
    api_url: str
    is_authenticated: bool = False
    base_folder: str = "/"

    def _init_client(self):
        """Initialize HTTP session with authentication and headers"""
        config = self._config
        self.api_url = config.api_url
        self.site_url = config.site_url
        self.base_folder = config.base_folder
        self.session = requests.Session()
        if config.basic_auth:
            self.session.auth = HTTPBasicAuth(
                config.basic_auth["username"],
                config.basic_auth["password"],
            )
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def test_connection(self) -> bool:
        """Test the connection to the Plone."""
        try:
            return self.get_content("/") is not None
        except requests.HTTPError:
            return False

    def authenticate(self):
        """Authenticate user with Plone REST API"""
        url = self._get_url("/@login")
        data = {
            "login": self._config.username,
            "password": self._config.password,
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        token = response.json().get("token")
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            self.is_authenticated = True
        else:
            raise RuntimeError("Authentication failed, no token received.")

    def _get_url(self, endpoint: str) -> str:
        """Build full URL for API endpoint"""
        endpoint = endpoint.lstrip("/")
        return urljoin(self.api_url, endpoint)

    def _relative_url(self, url: str) -> str:
        """Process the URL for API requests."""
        return url.replace(self.site_url, "").lstrip("/")

    def _batching_next_url(self, data: dict[str, str]) -> str | None:
        """Get the next URL for batching requests."""
        if url := data.get("next"):
            return self._relative_url(url)
        return None

    def _make_request(
        self, method: str, endpoint: str, raise_for_status: bool = True, **kwargs
    ) -> requests.Response:
        """Make HTTP request with error handling"""
        url = self._get_url(endpoint)
        try:
            response = self.session.request(method, url, **kwargs)
            if raise_for_status:
                response.raise_for_status()
            return response
        except requests.HTTPError:
            body = response.json()
            logger.error(f"HTTP error occurred: {body}")
            raise
        except requests.RequestException as e:
            logger.error(f"Request failed: {method} {url} - {e}")
            raise

    def get_content(
        self, path: str, params: dict | None = None, raise_for_status: bool = True
    ) -> t.PloneItem | None:
        """Retrieve content item from Plone."""
        params = params or {}
        response = self._make_request(
            "GET", path, raise_for_status=raise_for_status, params=params
        )
        if response.status_code == 200:
            return response.json()
        return None

    def create_content(self, path: str, payload: dict) -> t.PloneItem:
        """Create a new content item in Plone."""
        response = self._make_request("POST", path, json=payload)
        content = response.json()
        logger.info(f"Created content at {content['@id']}")
        return content

    def update_content(self, path: str, payload: dict[str, Any]) -> bool:
        """Update existing content item in Plone."""
        response = self._make_request("PATCH", path, json=payload)
        if response.status_code in (204, 200):
            logger.info(f"Updated content at {path}")
            status = True
        else:
            logger.error(f"Failed to update content at {path}: {response.status_code}")
            status = False
        return status

    def delete_content(self, path: str) -> bool:
        """Delete content item in Plone."""
        response = self._make_request("DELETE", path)
        # DELETE may return 204 No Content, so handle empty response
        if response.status_code == 204:
            logger.info(f"Deleted content at {path}")
            status = True
        else:
            logger.error(f"Failed to delete content at {path}: {response.status_code}")
            status = False
        return status

    def create_or_update_content(self, payload: dict) -> t.PloneItem | None:
        """Create a new content item in Plone."""
        path = payload.get("@id")
        if not path:
            raise ValueError("Content item must have an '@id' field.")
        if self.get_content(path, raise_for_status=False):
            # Should update
            status = self.update_content(path, payload)
            return self.get_content(path) if status else None
        # should create
        path = path.rsplit("/", 1)[0]
        return self.create_content(path, payload)

    def _available_transitions(self, path: str) -> list[str]:
        """Retrieve available transitions for a content item."""
        response = self._make_request("GET", f"{path}/@workflow")
        if response.status_code == 200:
            data = response.json()
            transitions = []
            for transition in data.get("transitions", []):
                id_ = transition["@id"].rsplit("/", 1)[-1]
                transitions.append(id_)
            return transitions
        logger.error(
            f"Failed to retrieve workflow transitions at {path}: {response.status_code}"
        )
        return []

    def transition_content(self, path: str, transition: str) -> bool:
        """Transition content item in Plone."""
        if transition not in self._available_transitions(path):
            logger.error(f"Invalid transition '{transition}' for content at {path}")
            return False
        response = self._make_request("POST", f"{path}/@workflow/{transition}")
        if response.status_code == 200:
            logger.info(f"Transitioned content at {path} to {transition}")
            return True
        logger.error(f"Failed to transition content at {path}: {response.status_code}")
        return False

    def search_content(
        self, path: str, params: dict, expand_batch: bool = False
    ) -> dict:
        """Search for content item in Plone."""
        endpoint = f"{path}/@search"
        response = self._make_request("GET", endpoint, params=params)
        if response.status_code != 200:
            logger.error(
                f"Failed to search content at {endpoint}: {response.status_code}"
            )
            return {}
        result = response.json()
        if expand_batch and (batching := result.pop("batching", None)):
            while batching:
                next_url = self._batching_next_url(batching)
                if not next_url:
                    batching = None
                    break
                response = self._make_request("GET", next_url)
                data = response.json()
                items = data.get("items", [])
                result["items"].extend(items)
                batching = data.pop("batching", None)
        return result

    def __repr__(self) -> str:
        """Return a string representation of the KeycloakClient."""
        return (
            "\n"
            f" - {self.system} ({dotted_name_for_object(self)})\n"
            f" - Site URL: {self.site_url}\n"
            f" - API URL: {self.api_url}\n"
            f" - Username: {self._config.username}\n"
        )
