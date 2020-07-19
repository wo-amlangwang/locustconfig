import json
import logging

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
            if c is '{':
                curly_bracket_count += 1
            if c is '[':
                square_bracket_count += 1
            if c is '}':
                curly_bracket_count -= 1
            if c is ']':
                square_bracket_count -= 1
        if square_bracket_count is 0 and curly_bracket_count is 0:
            return index
        index += 1
    pass


def get_function(url, header):
    return lambda session: session.client.get(url=url, headers=header)


def post_function(url, header, data):
    return lambda session: session.client.post(url=url, headers=header, data=json.dumps(data))


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
            next_index, _ = concat_json_string(elements, next_index)
            _, body = concat_json_string(elements, next_index)
            parsed_header = json.loads(header)
            parsed_body = json.loads(body)
            if method == "GET":
                self.reqDict[get_function(url, parsed_header)] = HIGH_PRIORITY
            if method == "POST":
                self.reqDict[post_function(url, parsed_header, parsed_body)] = LOW_PRIORITY
