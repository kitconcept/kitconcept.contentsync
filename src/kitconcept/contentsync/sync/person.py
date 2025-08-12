from kitconcept.contentsync import _types as t
from kitconcept.contentsync.clients.keycloak import KeycloakClient
from kitconcept.contentsync.clients.plone import PloneClient
from kitconcept.contentsync.converter.keycloak import KeycloakPersonConverter
from kitconcept.contentsync.sync import ContentSyncer
from kitconcept.contentsync.utils import relative_path


class contentsync(ContentSyncer):
    src_client: KeycloakClient
    dst_client: PloneClient
    item_converter: KeycloakPersonConverter

    def __init__(
        self, src_client: KeycloakClient, dst_client: PloneClient, base_dst_folder: str
    ):
        super().__init__(src_client, dst_client, base_dst_folder)
        converter = KeycloakPersonConverter(base_path=base_dst_folder)
        self.converter = converter

    def get_src_items(self) -> dict[str, t.PlonePerson]:
        src_items = self.src_client.get_all_users()
        converted = [self.converter(item) for item in src_items]
        return {item["@id"]: item for item in converted}

    def get_dst_items(self) -> set[str]:
        params = {"portal_type": "Person", "sort_on": "sortable_title"}
        response = self.dst_client.search_content(path="/", params=params)
        site_url = self.dst_site_url
        existing_item_ids = {item["@id"] for item in response.get("items", [])}
        return {relative_path(item, site_url) for item in existing_item_ids}
