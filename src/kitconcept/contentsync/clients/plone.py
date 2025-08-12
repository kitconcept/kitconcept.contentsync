from kitconcept.contentsync import _types as t
from kitconcept.contentsync import logger
from kitconcept.contentsync.clients import ConnectionClient
from requests.auth import HTTPBasicAuth
from typing import Any
from urllib.parse import urljoin

import requests


class PloneClient(ConnectionClient):
    """Base client for Plone REST API operations"""

    _config: t.PloneConfig
    session: requests.Session
    site_url: str
    api_url: str
    is_authenticated: bool = False

    def _init_client(self):
        """Initialize HTTP session with authentication and headers"""
        config = self._config
        self.api_url = config.api_url
        self.site_url = config.site_url
        self.session = requests.Session()
        if config.basic_auth:
            self.session.auth = HTTPBasicAuth(
                config.basic_auth["username"],
                config.basic_auth["password"],
            )
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

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
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.is_authenticated = True

    def _get_url(self, endpoint: str) -> str:
        """Build full URL for API endpoint"""
        return urljoin(self.api_url, endpoint)

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        endpoint = endpoint.lstrip("/")

        url = self._get_url(endpoint)
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.HTTPError:
            body = response.json()
            logger.error(f"HTTP error occurred: {body}")
            raise
        except requests.RequestException as e:
            logger.error(f"Request failed: {method} {url} - {e}")
            raise

    def get_content(self, path: str, params: dict | None = None) -> t.PloneItem | None:
        """Retrieve content item from Plone."""
        params = params or {}
        response = self._make_request("GET", path, params=params)
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
        if self.get_content(path):
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

    def search_content(self, path: str, params: dict) -> dict:
        """Search for content item in Plone."""
        endpoint = f"{path}/@search"
        response = self._make_request("GET", endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to search content at {endpoint}: {response.status_code}")
        return {}
