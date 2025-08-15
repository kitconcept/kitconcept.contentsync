from contextlib import contextmanager

import logging


def dotted_name_for_class(klass: type) -> str:
    """Return the dotted name for a given class."""
    module = klass.__module__
    name = klass.__name__
    return f"{module}.{name}"


def dotted_name_for_object(obj: object) -> str:
    """Return the dotted name for a given object."""
    module = obj.__module__
    klass = obj.__class__
    name = klass.__name__
    return f"{module}.{name}"


def relative_path(path: str, site_url: str) -> str:
    """Return the relative path for a given content."""
    return path.replace(site_url, "")


@contextmanager
def suppress_logging(names: list[str]):
    """Context manager to suppress logging."""
    status = {}
    for name in names:
        logger = logging.getLogger(name)
        status[name] = logger.level
        logger.setLevel(logging.CRITICAL)
    try:
        yield
    finally:
        # Return logging levels to original
        for name in names:
            logger = logging.getLogger(name)
            logger.setLevel(status[name])
