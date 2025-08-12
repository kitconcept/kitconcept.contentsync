from dataclasses import dataclass
from dynaconf import Dynaconf
from kitconcept.contentsync.clients import ConnectionClient
from kitconcept.contentsync.clients import get_client
from kitconcept.contentsync.sync import ContentSyncer
from pathlib import Path

import importlib


LOCAL_PATH = Path(__file__).parent


@dataclass
class SyncSettings:
    debug: bool
    sync: ContentSyncer
    src: ConnectionClient
    dst: ConnectionClient
    base_dst_folder: str = "/"


def _get_syncer(dotted_name: str) -> ContentSyncer:
    """Dynamically import and return a syncer class."""
    module_name, class_name = dotted_name.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def _get_client(settings) -> ConnectionClient:
    payload = {k.lower(): v for k, v in settings.items()}
    type_ = payload.pop("type", None)
    return get_client(type_, payload)


def get_settings() -> SyncSettings:
    raw_settings = Dynaconf(
        preload=[f"{LOCAL_PATH}/settings.toml"],
        envvar_prefix="contentsync",
        ignore_unknown_envvars=True,
        load_dotenv=True,
    )
    default = raw_settings["default"]
    debug = default["debug"]
    base_dst_folder = default["base_dst_folder"]
    syncer = _get_syncer(default["sync"])
    src = _get_client(raw_settings["src"])
    dst = _get_client(raw_settings["dst"])
    settings = SyncSettings(
        debug=debug, sync=syncer, src=src, dst=dst, base_dst_folder=base_dst_folder
    )
    return settings
