import json
import time
from dataclasses import dataclass

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, Timeout
from urllib3.util.retry import Retry

# ----------------------------
# RequestInstance error
# ----------------------------

@dataclass
class ApiError(Exception):
    status_code: int
    url: str
    message: str
    body_preview: str = ""

    def str(self):
        extra = f"\nResponse preview:\n{self.body_preview}" if self.body_preview else ""
        return f"API error {self.status_code} for {self.url}: {self.message}{extra}"


def pretty(obj):
    """Pretty-print JSON"""
    return json.dumps(obj, ensure_ascii=False, indent=2)


def raise_for_status_with_details(resp):
    if 200 <= resp.status_code < 400:
        return

    try:
        body = pretty(resp.json())[:500]
    except Exception:
        body = (resp.text or "")[:500]

    raise ApiError(
        status_code=resp.status_code,
        url=resp.url,
        message=resp.reason,
        body_preview=body,
    )


# ----------------------------
# API client
# ----------------------------

TIMEOUT = 5
METHODS = {
    "get": "GET",
    "post": "POST"
}

class RequestInstance:
    def __init__(self, base_url, timeout=TIMEOUT, retries=2):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "python-requests-demo/1.0",
        })

        retry = Retry(
            total=retries,
            connect=retries,
            read=retries,
            status=retries,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=(METHODS["get"], METHODS["post"]),
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, subdomain, query={}, params=None):
        query_string = self._generate_query_string(query)
        return self.request(METHODS["get"], f"{subdomain}?{query_string}", params)

    def post(self, subdomain, query={}, params=None, json_body=None):
        query_string = self._generate_query_string(query)
        return self.request(METHODS["post"], f"{subdomain}?{query_string}", params, json_body)
    
    def request(self, method, path, params=None, json_body=None, headers=None):
        url = self.base_url + path
        start = time.time()

        try:
            resp = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_body,
                headers=headers,
                timeout=self.timeout,
            )
        except Timeout as e:
            raise RuntimeError(f"Timeout after {self.timeout}s: {url}") from e
        except RequestException as e:
            raise RuntimeError(f"Network error: {e}") from e

        elapsed_ms = int((time.time() - start) * 1000)
        print(f"[HTTP] {method} {resp.url} -> {resp.status_code} ({elapsed_ms} ms)")

        raise_for_status_with_details(resp)
        return resp.json()

    def _generate_query_string(self, query={}):
        return '&'.join(f"{key}={value}" for key, value in query.items())
    