# -*- coding: utf-8 -*-

"""
Contagra API Class
"""

__title__ = "contagra-api"
__version__ = "1.0.0"
__author__ = "Contagra"
__license__ = "MIT"

import requests
from requests import request
from json import dumps as jsonencode
from time import time
from contagra.oauth import OAuth
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode


class API(object):
    """ API Class """

    def __init__(self, url, username, api_key, **kwargs):
        self.url = url
        self.username = username
        self.api_key = api_key
        self.api = kwargs.get("api", "rest")
        self.path = kwargs.get("path", "api")
        self.version = kwargs.get("version", "v1")
        self.is_ssl = self.__is_ssl()
        self.timeout = kwargs.get("timeout", 5)
        self.verify_ssl = kwargs.get("verify_ssl", True)
        self.query_string_auth = kwargs.get("query_string_auth", False)
        self.user_agent = kwargs.get("user_agent", f"Contagra-Python-REST-API/{__version__}")

    def __is_ssl(self):
        """ Check if url use HTTPS """
        return self.url.startswith("https")

    def __get_url(self, endpoint):
        """ Get URL for requests """
        url = self.url
        api = self.api

        if url.endswith("/") is False:
            url = f"{url}/"

        return f"{url}{api}/{self.version}/{endpoint}"

    def __get_oauth_url(self, url, **kwargs):
        """ Generate oAuth1.0a URL """
        oauth = OAuth(
            url=url,
            username=self.username,
            api_key=self.api_key,
            api=self.api,
            version=self.version,
        )

        return oauth.get_oauth_url()

    def __request(self, method, endpoint, data, params=None, **kwargs):
        """ Do requests """
        if params is None:
            params = {}

        # Get OAuth Token
        oauth_url = self.__get_oauth_url(self.url, path=self.path, **kwargs)
        #token = requests.get(oauth_url, verify=self.verify_ssl)
        token = requests.get(oauth_url, verify=self.verify_ssl).json()["access_token"]

        url = self.__get_url(endpoint)
        auth = None

        headers = {
            "user-agent": f"{self.user_agent}",
            "accept": "application/json",
            "Access-Token": token
        }

        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"

        if data is not None:
            data = jsonencode(data, ensure_ascii=False).encode('utf-8')
            headers["content-type"] = "application/json;charset=utf-8"

        return request(
            method=method,
            url=url,
            verify=self.verify_ssl,
            auth=auth,
            params=params,
            data=data,
            timeout=self.timeout,
            headers=headers,
            **kwargs
        )

    def get(self, endpoint, **kwargs):
        """ Get requests """
        return self.__request("GET", endpoint, None, **kwargs)

    def post(self, endpoint, data, **kwargs):
        """ POST requests """
        return self.__request("POST", endpoint, data, **kwargs)

    def put(self, endpoint, data, **kwargs):
        """ PUT requests """
        return self.__request("PUT", endpoint, data, **kwargs)

    def delete(self, endpoint, **kwargs):
        """ DELETE requests """
        return self.__request("DELETE", endpoint, None, **kwargs)

    def options(self, endpoint, **kwargs):
        """ OPTIONS requests """
        return self.__request("OPTIONS", endpoint, None, **kwargs)
