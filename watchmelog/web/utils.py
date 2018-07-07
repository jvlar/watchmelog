from typing import Dict

from apistar import http


def redirect(uri: str, headers: Dict = None) -> http.Response:
    if not headers:
        headers = {}
    headers.update({"Location": uri})
    return http.Response("", status_code=302, headers=headers)
