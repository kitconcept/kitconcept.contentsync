from collective.html2blocks._types import VoltoBlocksInfo
from collective.html2blocks.converter import volto_blocks
from kitconcept.contentsync import _types as t
from kitconcept.contentsync.converter import ItemConverter


class KeycloakPersonConverter(ItemConverter):
    """Converts a Keycloak user to a Plone Person."""

    portal_type: str = "Person"

    base_mapping: tuple[tuple[str, str], ...] = (
        ("id", "username"),
        ("first_name", "firstName"),
        ("last_name", "lastName"),
        ("email", "email"),
    )

    def _field__transition(self, src: t.KeycloakUser) -> str:
        """Define the transition to be applied to the content."""
        return "publish"

    def _field_location(self, src: t.KeycloakUser) -> str:
        """Extracts the location from the user attributes."""
        attrs = src.get("attributes", {}) or {}
        location = attrs.get("location", [""])[0]
        return location

    def _field_title(self, src: t.KeycloakUser) -> str:
        """Constructs the title from the first and last name."""
        first_name = src.get("firstName", "")
        last_name = src.get("lastName", "")
        return f"{last_name}, {first_name}"

    def _blocks_factory_(self, src: t.KeycloakUser) -> VoltoBlocksInfo:
        """Constructs the blocks for the user."""
        attrs = src.get("attributes", {}) or {}
        location = attrs.get("location", [""])[0]
        company = attrs.get("company", [""])[0]
        department = attrs.get("department", [""])[0]
        html = f"""
        <ul>
            <li><strong>Username:</strong> {src["username"]}</li>
            <li><strong>Company:</strong> {company}</li>
            <li><strong>Department:</strong> {department}</li>
            <li><strong>Location:</strong> {location}</li>
        </ul>
        """
        return volto_blocks(html, default_blocks=[{"@type": "title"}])
