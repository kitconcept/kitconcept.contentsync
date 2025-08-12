def dotted_name_for_object(obj: object) -> str:
    """Return the dotted name for a given object."""
    module = obj.__module__
    cls = obj.__class__.__name__
    return f"{module}.{cls}"


def relative_path(path: str, site_url: str) -> str:
    """Return the relative path for a given content."""
    return path.replace(site_url, "")
