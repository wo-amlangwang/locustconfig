import json
import logging
import urllib.parse as urlparse
from urllib.parse import urlencode

DEFAULT_METHOD_INDEX = 0
DEFAULT_URL_INDEX = 1
HIGH_PRIORITY = 3
MID_PRIORITY = 2
LOW_PRIORITY = 1


def concat_json_string(json_parts, start_index):
    last_index = find_json_end(json_parts, start_index)
    return last_index + 1, " ".join(json_parts[start_index:last_index + 1])
    pass


def find_json_end(json_parts, start_index):
    square_bracket_count = 0
    curly_bracket_count = 0
    index = start_index
    while True:
        for c in json_parts[index]:
            if c == '{':
                curly_bracket_count += 1
            if c == '[':
                square_bracket_count += 1
            if c == '}':
                curly_bracket_count -= 1
            if c == ']':
                square_bracket_count -= 1
        if square_bracket_count == 0 and curly_bracket_count == 0:
            return index
        index += 1
    pass


def get_function(url, header):
    return lambda session: session.client.get(url=url, headers=header)


def post_function(url, header, data):
    return lambda session: session.client.post(url=url, headers=header, data=json.dumps(data))


def append_query(url, querys):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(querys)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


class Parser:
    def __init__(self):
        self.reqDict = {}

    def parse(self, data_file_path):
        f = open(data_file_path, "r")
        lines = f.readlines()
        request_set = set()
        for line in lines:
            request_set.add(line)
        for line in request_set:
            elements = line.split()
            method = elements[DEFAULT_METHOD_INDEX]
            url = elements[DEFAULT_URL_INDEX]
            next_index = DEFAULT_URL_INDEX + 1
            next_index, header = concat_json_string(elements, next_index)
            next_index, query = concat_json_string(elements, next_index)
            _, body = concat_json_string(elements, next_index)
            parsed_header = json.loads(header)
            parsed_query = json.loads(query)
            parsed_body = json.loads(body)
            url = append_query(url, parsed_query)
            if method == "GET":
                self.reqDict[get_function(url, parsed_header)] = HIGH_PRIORITY
            if method == "POST":
                self.reqDict[post_function(url, parsed_header, parsed_body)] = LOW_PRIORITY

