import base64
import datetime
import hashlib
import hmac
import secrets
from urllib.parse import urlencode, urljoin, urlsplit

from requests import Session
from requests.auth import AuthBase

ENCODING = "utf-8"
ONSHAPE_BASE_URL = "https://cad.onshape.com/api/"


class OnshapeAuth(AuthBase):
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def __call__(self, r):
        date_string = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        nonce = secrets.token_urlsafe(32)
        [url, _, query] = r.path_url.partition("?")
        hmac_payload = "\n".join(
            [
                r.method,
                nonce,
                date_string,
                r.headers.get("Content-Type", "application/json"),
                url,
                query,
                "",
            ]
        ).lower()
        hmac_signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode(ENCODING),
                hmac_payload.encode(ENCODING),
                digestmod=hashlib.sha256,
            ).digest()
        ).decode(ENCODING)

        r.headers.update(
            {
                "Date": date_string,
                "On-Nonce": nonce,
                "Authorization": f"On {self.access_key}:HmacSHA256:{hmac_signature}",
            }
        )

        return r


class OnshapeSession(Session):
    def __init__(self, access_key, secret_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth = OnshapeAuth(access_key, secret_key)
        self.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/vnd.onshape.v1+json",
            }
        )

    def request(self, method, url, *args, **kwargs):
        url = urljoin(ONSHAPE_BASE_URL, url)
        return super().request(method, url, *args, **kwargs)
