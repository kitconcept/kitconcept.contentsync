from kitconcept.contentsync import _types as t
from kitconcept.contentsync.clients.keycloak import KeycloakClient
from kitconcept.contentsync.clients.plone import PloneClient
from kitconcept.contentsync.sync import ContentSyncer
from kitconcept.contentsync.utils import relative_path


class PersonSyncer(ContentSyncer):
    src_client: KeycloakClient
    dst_client: PloneClient

    def get_src_items(
        self, query: dict | None = None, transform: bool = True
    ) -> dict[str, t.PlonePerson | t.KeycloakUser]:
        src_items = self.src_client.get_users(query=query)
        if not transform:
            return {item["id"]: item for item in src_items}
        converted = [self.converter(item) for item in src_items]
        return {item["@id"]: item for item in converted}

    def get_dst_items(self) -> set[str]:
        params = {"portal_type": "Person", "sort_on": "sortable_title"}
        # Get all Person items
        response = self.dst_client.search_content(
            path="/", params=params, expand_batch=True
        )
        site_url = self.dst_site_url
        existing_item_ids = {item["@id"] for item in response.get("items", [])}
        return {relative_path(item, site_url) for item in existing_item_ids}
