import common.parser
import os
from locust import HttpUser, task, between
from locust.contrib.fasthttp import FastHttpUser


def get_tests():
    p = common.parser.Parser()
    p.parse(os.getcwd() + "/access.log")
    return p.reqDict


class MyUser(FastHttpUser):
    min_wait = 100
    max_wait = 120
    tasks = get_tests()

    @task(1)
    def health(self):
        self.client.get("/health")
