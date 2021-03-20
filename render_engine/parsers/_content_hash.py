import hashlib
import typing


def _hash_content(route: typing.Any) -> str:
    """create a ``hashlib.sha1`` hash of a pages ``base_content``"""
    m = hashlib.sha1()
    m.update(getattr(route, "base_content", "").encode("utf-8"))
    return m.hexdigest() + "\n"