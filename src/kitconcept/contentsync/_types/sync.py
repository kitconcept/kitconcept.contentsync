from dataclasses import dataclass


@dataclass
class ContentSyncerReport:
    """Report for the content synchronization process."""

    total_src_items: int
    created_items: int
    updated_items: int
    deleted_items: int
    errors: list[str]
