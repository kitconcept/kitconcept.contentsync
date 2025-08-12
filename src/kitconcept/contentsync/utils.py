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
