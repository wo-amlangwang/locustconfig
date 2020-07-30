from common.parser import parse
import common.my_fasthttp
from os import getcwd
from locust import task
from locust.contrib.fasthttp import FastHttpUser


def get_tests():
    return parse(getcwd() + "/access.log")


class MyUser(common.my_fasthttp.MyFastHttpUser):
    min_wait = 100
    max_wait = 120
    tasks = get_tests()

    @task(1)
    def health(self):
        self.client.get("/health")
