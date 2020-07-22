import common.parser
import os
from locust import HttpUser, task, between


def get_tests():
    p = common.parser.Parser()
    p.parse(os.getcwd() + "/access.log")
    return p.reqDict


class MyUser(HttpUser):
    min_wait = 100
    max_wait = 120
    tasks = get_tests()
