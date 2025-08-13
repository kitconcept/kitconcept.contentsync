from collective.html2blocks._types import BlocksLayout
from collective.html2blocks._types import VoltoBlock
from typing import NotRequired
from typing import TypedDict


PloneItem = TypedDict(
    "PloneItem",
    {
        "@id": str,
        "@type": str,
        "UID": NotRequired[str],
        "id": str,
        "title": NotRequired[str],
        "description": NotRequired[str],
        "creators": NotRequired[list[str]],
        "image": NotRequired[dict[str, str | int]],
        "image_caption": NotRequired[str],
        "language": NotRequired[str],
        "text": NotRequired[dict[str, str]],
        "nav_title": NotRequired[str],
        "query": NotRequired[list],
        "blocks": NotRequired[dict[str, VoltoBlock]],
        "blocks_layout": NotRequired[BlocksLayout],
        "_blocks_": NotRequired[list[VoltoBlock]],
        "exclude_from_nav": NotRequired[bool],
    },
)


class PlonePerson(PloneItem):
    """Plone Person representation.

    Inherits from PloneItem and adds specific fields for a person.
    """

    first_name: str
    last_name: str
    email: NotRequired[str]
