from dataclasses import dataclass
from dynaconf import Dynaconf
from dynaconf import Validator
from kitconcept.contentsync.clients import ConnectionClient
from kitconcept.contentsync.clients import get_client
from kitconcept.contentsync.converters import ItemConverter
from kitconcept.contentsync.sync import ContentSyncer
from pathlib import Path

import importlib


LOCAL_PATH = Path(__file__).parent


@dataclass
class SyncSettings:
    debug: bool
    sync: ContentSyncer
    item_converter: ItemConverter
    src: ConnectionClient
    dst: ConnectionClient
    base_dst_folder: str = "/"


def _get_syncer(
    syncer_klass: str, converter_klass: str
) -> tuple[ContentSyncer, ItemConverter]:
    """Dynamically import and return a syncer class."""
    module_name, class_name = syncer_klass.rsplit(".", 1)
    module = importlib.import_module(module_name)
    content_syncer = getattr(module, class_name)
    module_name, class_name = converter_klass.rsplit(".", 1)
    module = importlib.import_module(module_name)
    item_converter = getattr(module, class_name)
    return content_syncer, item_converter


def _get_client(settings) -> ConnectionClient:
    payload = {k.lower(): v for k, v in settings.items()}
    type_ = payload.pop("type", None)
    return get_client(type_, payload)


def get_settings() -> SyncSettings:
    raw_settings = Dynaconf(
        preload=[f"{LOCAL_PATH}/settings.toml"],
        envvar_prefix="SYNC",
        ignore_unknown_envvars=True,
        load_dotenv=True,
        validators=[
            Validator("debug", cast=bool, default=False),
        ],
    )
    debug = raw_settings["debug"]
    sync = raw_settings["sync"]
    syncer, item_converter = _get_syncer(sync["klass"], sync["item_converter"])
    src = _get_client(raw_settings["src"])
    dst = _get_client(raw_settings["dst"])
    base_dst_folder = dst.base_folder
    settings = SyncSettings(
        debug=debug,
        sync=syncer,
        item_converter=item_converter,
        src=src,
        dst=dst,
        base_dst_folder=base_dst_folder,
    )
    return settings
