"""Class client for tiko protocol."""
import json
import logging

import requests

_LOGGER = logging.getLogger(__name__)

API_HOST = "https://tiko.ch"
API_ENDPOINT = "/api/v3/graphql/"

class TikoClient(object):
    """The client class."""

    def __init__(
        self, email, password, token=None, session=None, timeout=None
    ):
        """Initialize the client object."""
        self.email = email
        self.password = password
        self.token = token
        self._session = session
        self._timeout = timeout
        
    def login(self):
        """Login to Tiko API."""
        if self._session is None:
            self._session = requests.session()
            self._session.headers.update({"Access-Control-Request-Headers": "content-type,x-tiko-agent", "User-agent":"Mozilla/5.0 (Linux; Android 13; Pixel 4a Build/T1B3.221003.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.126 Mobile Safari/537.36", "Sec-Fetch-Mode": "cors", "X-Requested-With": "ch.be_smart.besmartapp", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-Dest": "empty", "Referer": "http://localhost:8100/", "Accept-Language": "fr-FR,fr;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6"})

        payload = {
    "operationName": "LogIn",
    "variables": {
        "email": self.email,
        "password": self.password,
        "langCode": "fr",
        "retainSession": True
    },
    "query": "mutation LogIn($email: String!, $password: String!, $langCode: String, $retainSession: Boolean) {\n  logIn(\n    input: {email: $email, password: $password, langCode: $langCode, retainSession: $retainSession}\n  ) {\n    settings {\n      client {\n        name\n        __typename\n      }\n      support {\n        serviceActive\n        phone\n        email\n        __typename\n      }\n      __typename\n    }\n    user {\n      id\n      clientCustomerId\n      agreements\n      properties {\n        id\n        allInstalled\n        __typename\n      }\n      inbox(modes: [\"app\"]) {\n        actions {\n          label\n          type\n          value\n          __typename\n        }\n        id\n        lockUser\n        maxNumberOfSkip\n        messageBody\n        messageHeader\n        __typename\n      }\n      __typename\n    }\n    token\n    firstLogin\n    __typename\n  }\n}\n"
}
        self.Request(payload)

    def Request(self, payload):
        req = self._session.post(
            API_HOST + API_ENDPOINT,
            json=payload,
            headers={"content-type": "application/json"},
            timeout=self._timeout,
        )

        response_json = req.json()
        _LOGGER.debug(response_json)

        self.ParseAPI(response_json)

    def ParseAPI(self, json):
        #Handle errors
        if "errors" in json:
            for error in json["errors"]:
                _LOGGER.critical(error["message"])

        return json["data"]
