import base64
import json
import os
import time

import httpx
from mcp.server.fastmcp import FastMCP

HOST_ONBOARD = "https://backoffice-service-onboarding-t57o3dxfca-nn.a.run.app"
HOST_API = "https://backoffice-service-t57o3dxfca-nn.a.run.app"
HEADERS = {
    "Origin": "https://localhost",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}
GUIDE_FLAGS = {"supports_no_guide_category": "true", "supports_no_guide_city": "true", "supports_collab_guides": "true"}
MIN_INTERVAL = 3.0

mcp = FastMCP("beli")
_http = httpx.Client(timeout=30, headers=HEADERS)
_state = {"access": "", "refresh": os.environ.get("BELI_REFRESH_TOKEN", ""), "last": 0.0}


def _claims(token):
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))


def _expired(token):
    try:
        return _claims(token)["exp"] - 60 <= time.time()
    except Exception:
        return True


def _token():
    if not _expired(_state["access"]):
        return _state["access"]
    if _state["refresh"] and not _expired(_state["refresh"]):
        r = _http.post(f"{HOST_ONBOARD}/api/token/refresh/", json={"refresh": _state["refresh"]})
        if r.status_code == 200:
            _state["access"] = r.json()["access"]
            return _state["access"]
    email, password = os.environ.get("BELI_EMAIL"), os.environ.get("BELI_PASSWORD")
    if not (email and password):
        raise RuntimeError("Set BELI_EMAIL and BELI_PASSWORD (or BELI_REFRESH_TOKEN)")
    r = _http.post(f"{HOST_ONBOARD}/api/token/", json={"email": email, "password": password})
    r.raise_for_status()
    pair = r.json()
    _state["access"], _state["refresh"] = pair["access"], pair["refresh"]
    return _state["access"]


def _user_id():
    return _claims(_token())["user_id"]


def _call(method, path, params=None, body=None, host=HOST_API):
    wait = MIN_INTERVAL - (time.time() - _state["last"])
    if wait > 0:
        time.sleep(wait)
    r = _http.request(method, host + path, params=params, json=body, headers={"Authorization": f"Bearer {_token()}"})
    _state["last"] = time.time()
    if r.status_code == 429:
        raise RuntimeError("Beli rate limited this request (HTTP 429). Wait a minute and retry.")
    if r.status_code >= 400:
        raise RuntimeError(f"Beli returned HTTP {r.status_code}: {r.text[:200]}")
    return r.json() if r.content else {"ok": True}


@mcp.tool()
def whoami() -> dict:
    """Return the signed-in Beli user (id, username, name)."""
    return _call("GET", "/api/user/logged-in/", host=HOST_ONBOARD)


@mcp.tool()
def search_restaurants(term: str, city: str = "Tokyo, Japan") -> dict:
    """Search Beli for restaurants. Returns candidates with a `business` id and address. Check the address, since top hits can be in the wrong city."""
    return _call("GET", "/api/search-app/", params={"term": term, "city": city})


@mcp.tool()
def get_bookmarks(category: str = "RES") -> dict:
    """List the signed-in user's bookmarks. Category RES is restaurants."""
    return _call("GET", "/api/get-bookmark/", params={"user": _user_id(), "category": category})


@mcp.tool()
def add_bookmark(business_id: int) -> dict:
    """Bookmark a restaurant by its Beli business id. Idempotent. This writes to the user's account."""
    return _call("POST", "/api/add-bookmark/", body={"user_id": _user_id(), "business_id": business_id})


@mcp.tool()
def bookmark_status(business_id: int) -> dict:
    """Check whether a restaurant is bookmarked."""
    return _call("GET", f"/api/bookmark-status/{_user_id()}/{business_id}/")


@mcp.tool()
def list_my_guides() -> dict:
    """List the signed-in user's Beli guides with titles, audience and place counts."""
    return _call("GET", "/api/user-guide/", params={"user_id": _user_id(), **GUIDE_FLAGS})


@mcp.tool()
def get_my_guide_items() -> dict:
    """List the places in all of the signed-in user's guides (each item names its guide id)."""
    return _call("GET", "/api/user-guide-items/", params={"user_id": _user_id(), **GUIDE_FLAGS})


@mcp.tool()
def get_guide(guide_id: int) -> dict:
    """Read one guide in full by id."""
    params = {"list_id": guide_id, "viewer": _user_id(), "check_user_access": "false", "playlists_v2": "true", "vguides": "true",
              "supports_no_guide_category": "true", "supports_no_guide_city": "true"}
    return _call("GET", "/api/user-guide-list-view/", params=params)


@mcp.tool()
def referral_link() -> dict:
    """Get the signed-in user's referral link."""
    return _call("GET", "/api/user/user-referral-link/")


@mcp.tool()
def beli_get(path: str, params: dict | None = None) -> dict:
    """Read-only escape hatch: GET any /api/ path from the Beli spec (see beli-api-spec). Use {user} in the path for your user id."""
    if not path.startswith("/api/") or ".." in path:
        raise ValueError("path must start with /api/")
    return _call("GET", path.replace("{user}", _user_id()), params=params)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
