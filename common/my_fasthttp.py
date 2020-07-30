from locust.contrib.fasthttp import FastHttpUser, FastHttpSession
from locust.env import Environment
import logging

logger = logging.getLogger(__name__)


class MyFastHttpUser(FastHttpUser):

    def __init__(self, environment):
        super().__init__(environment)

        self.client = MyFastHttpSession(
            self.environment,
            base_url=self.host,
            network_timeout=self.network_timeout,
            connection_timeout=self.connection_timeout,
            max_redirects=self.max_redirects,
            max_retries=self.max_retries,
            insecure=self.insecure,
        )


class MyFastHttpSession(FastHttpSession):

    def __init__(self, environment: Environment, base_url: str, insecure=True, **kwargs):
        super().__init__(environment, base_url, insecure, **kwargs)

    def delete(self, path, **kwargs):
        return super().request("DELETE", path, **kwargs)

    def get(self, path, **kwargs):
        """Sends a GET request"""
        logger.info(1)
        return super().request("GET", path, **kwargs)

    def head(self, path, **kwargs):
        """Sends a HEAD request"""
        return super().request("HEAD", path, **kwargs)

    def options(self, path, **kwargs):
        """Sends a OPTIONS request"""
        return super().request("OPTIONS", path, **kwargs)

    def patch(self, path, data=None, **kwargs):
        """Sends a POST request"""
        return super().request("PATCH", path, data=data, **kwargs)

    def post(self, path, data=None, **kwargs):
        """Sends a POST request"""
        return super().request("POST", path, data=data, **kwargs)

    def put(self, path, data=None, **kwargs):
        """Sends a PUT request"""
        return super().request("PUT", path, data=data, **kwargs)
