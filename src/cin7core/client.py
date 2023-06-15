import os

from requests import request

from . import errors
from .endpoints import Sale, Webhook


class Cin7Core(object):
    def __init__(self, api_url=None, account_id=None, app_key=None):
        self.api_url = (
            api_url
            or os.environ.get(
                "CIN7CORE_API_URL", "https://inventory.dearsystems.com/ExternalApi/v2"
            )
        ).rstrip("/")

        self.account_id = account_id or os.environ.get("CIN7CORE_ACCOUNT_ID")
        self.app_key = app_key or os.environ.get("CIN7CORE_APP_KEY")

        if not self.account_id:
            raise errors.AuthenticationError(
                "No Cin7 Core API account id. Pass it into client constructor or "
                "set env var CIN7CORE_ACCOUNT_ID"
            )
        if not self.account_id:
            raise errors.AuthenticationError(
                "No Cin7 Core API app key. Pass it into client constructor or "
                "set env var CIN7CORE_APP_KEY"
            )

        self.headers = {
            "Content-Type": "application/json",
            "api-auth-accountid": self.account_id,
            "api-auth-applicationkey": self.app_key,
        }

        # Endpoints
        self.sale = Sale(client=self)
        self.webhook = Webhook(client=self)

    def _request(self, method, resource, data=None, params=None):
        response = request(
            method,
            self.api_url + "/" + resource,
            json=data,
            headers=self.headers,
            params=params,
        )

        if response.status_code == 401:
            raise errors.AuthenticationError(
                message="Authentication failed",
                response=response,
            )

        return response
