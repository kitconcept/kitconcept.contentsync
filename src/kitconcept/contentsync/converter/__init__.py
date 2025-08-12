from kitconcept.contentsync import _types as t
from typing import cast


class ItemConverter:
    base_path: str
    base_mapping: tuple[tuple[str, str], ...] = ()
    portal_type: str = "Document"

    def __init__(self, base_path: str):
        self.base_path = base_path.rstrip("/")

    def _local_transformers(self) -> dict[str, str]:
        """Returns a mapping of local transformer functions."""
        prefix = "_field_"
        attrs = [name for name in dir(self) if name.startswith(prefix)]
        return {name[len(prefix) :]: name for name in attrs}

    def __call__(self, src: dict) -> t.PlonePerson:
        """Converts a user to a Plone person."""
        person = cast(t.PlonePerson, {"@type": self.portal_type})
        for key, attr in self.base_mapping:
            person[key] = src.get(attr, "")
        for key, meth_name in self._local_transformers().items():
            person[key] = getattr(self, meth_name)(src)
        if (factory := getattr(self, "_blocks_factory_", None)) and (
            blocks_info := factory(src)
        ):
            person.update(blocks_info)
        person["@id"] = f"{self.base_path}/{person['id']}"
        return person
