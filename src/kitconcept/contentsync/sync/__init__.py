from kitconcept.contentsync import _types as t
from kitconcept.contentsync.clients.keycloak import KeycloakClient
from kitconcept.contentsync.clients.plone import PloneClient
from kitconcept.contentsync.converters import ItemConverter


class ContentSyncer:
    src_client: KeycloakClient | PloneClient
    dst_client: PloneClient
    dst_site_url: str
    converter: ItemConverter

    def __init__(
        self,
        item_converter: type[ItemConverter],
        src_client: KeycloakClient | PloneClient,
        dst_client: PloneClient,
        base_dst_folder: str,
    ):
        self.src_client = src_client
        self.dst_client = dst_client
        self.converter = item_converter(base_path=base_dst_folder)
        self.dst_site_url = dst_client.site_url

    def get_src_items(self, transform: bool = True) -> dict[str, dict]:
        """Retrieve items from the source client."""
        return {}

    def get_dst_items(self) -> set[str]:
        """Retrieve item ids from the destination client."""
        return set()

    def group_items(
        self, item_ids: set[str], existing_item_ids: set[str]
    ) -> tuple[set[str], set[str], set[str]]:
        """Group items into create, update, and delete sets."""
        to_create = item_ids - existing_item_ids
        to_update = item_ids & existing_item_ids
        to_delete = existing_item_ids - item_ids
        return to_create, to_update, to_delete

    def _create_item(self, item: dict) -> str:
        """Create a new item in the destination client."""
        path = item.pop("@id")
        parent_path = path.rsplit("/", 1)[0]
        transition = item.pop("_transition", None)
        content = self.dst_client.create_content(parent_path, item)
        if transition:
            self.dst_client.transition_content(path, transition)
        return content["@id"]

    def _update_item(self, item: dict) -> str:
        """Update an existing item in the destination client."""
        path = item.pop("@id")
        transition = item.pop("_transition", None)
        self.dst_client.update_content(path, item)
        if transition:
            self.dst_client.transition_content(path, transition)
        return path

    def _delete_item(self, item: dict) -> str:
        """Delete an existing item in the destination client."""
        path = item.pop("@id")
        self.dst_client.delete_content(path)
        return path

    def dump_contents(self, transform: bool = True) -> dict[str, dict]:
        """Dump contents from the source client."""
        src_items = self.get_src_items(transform)
        return src_items

    def __call__(self) -> t.ContentSyncerReport:
        """Perform the synchronization process."""
        # Get src items
        src_items = self.get_src_items()
        item_ids = set(src_items.keys())

        client = self.dst_client
        client.authenticate()

        # Get existing item ids
        existing_item_ids = self.get_dst_items()
        # Define items to create, update, and delete
        to_create, to_update, to_delete = self.group_items(item_ids, existing_item_ids)
        # Create new items
        for item_id in to_create:
            item = src_items[item_id]
            self._create_item(item)
        # Update existing items
        for item_id in to_update:
            item = src_items[item_id]
            self._update_item(item)
        # Delete removed items
        for item_id in to_delete:
            item = src_items[item_id]
            self._delete_item(item)
        return t.ContentSyncerReport(
            total_src_items=len(src_items),
            created_items=len(to_create),
            updated_items=len(to_update),
            deleted_items=len(to_delete),
            errors=[],
        )
