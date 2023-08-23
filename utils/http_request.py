"""This module sends HTTP request to a server."""
from abc import ABC, abstractmethod
import requests
import json
from typing import Optional


class HttpRequest(ABC):
    def __init__(self, url: str, headers: Optional[str] = None) -> None:
        self.url = url
        self.headers = headers

    @abstractmethod
    def request(self) -> dict:
        """Sends HTTP request to a server."""
        pass

    def convertDict(self, res: requests.Response) -> dict:
        if res.status_code != 200:
            res.raise_for_status()

        return json.loads(res.text)


class Get(HttpRequest):
    def __init__(self, url: str, headers: Optional[str] = None):
        super().__init__(url, headers)

    def request(self) -> dict:
        res = requests.get(self.url, headers=self.headers)
        json_data = self.convertDict(res)

        return json_data

# post impl here