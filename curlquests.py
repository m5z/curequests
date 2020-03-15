import codecs
import html
import shlex

import requests


class Curlquests:
    _COOKIE_PREFIX = 'Cookie: '

    def __init__(self, curl):
        self.curl = curl
        self._parse()

    @staticmethod
    def from_file(filename):
        with codecs.open(filename, 'r', 'utf-8') as f:
            curl = '\n'.join(f.readlines())
        return Curlquests(curl)

    def response(self):
        if self.data:
            return requests.post(self.url, headers=self.headers, cookies=self.cookies, data=self.data)
        else:
            return requests.get(self.url, headers=self.headers, cookies=self.cookies)

    def _parse(self):
        args = shlex.split(self.curl)

        self.url = None
        self.cookies = {}
        self.headers = {}
        self.data = {}

        i = 0
        while i < len(args):
            current = args[i]
            if current == 'curl':
                i += 1
                self.url = args[i]
            elif current == '-H':
                i += 1
                self._parse_header(args[i])
            elif current == '--data':
                i += 1
                self._parse_data(args[i])
            elif current == '--data-binary':
                i += 1
                self.data = args[i]
            i += 1

    def _parse_header(self, header_arg):
        if header_arg.startswith(Curlquests._COOKIE_PREFIX):
            self._populate_cookies(header_arg)
        else:
            self._insert(self.headers, header_arg, ': ')

    def _populate_cookies(self, cookie_arg):
        cookie_str = cookie_arg[len(Curlquests._COOKIE_PREFIX):]
        cookies_list = cookie_str.split('; ')
        for cookie in cookies_list:
            self._insert(self.cookies, cookie, '=')

    def _parse_data(self, data_arg):
        data_items = data_arg.split('&')
        for item in data_items:
            self._insert(self.data, item, '=')

    @staticmethod
    def _insert(dictionary, pair, delimiter):
        delimiter_index = pair.find(delimiter)
        key = pair[:delimiter_index]
        value = pair[delimiter_index + len(delimiter):]
        dictionary[key] = value


if __name__ == '__main__':
    def demo(curl):
        response = Curlquests(curl).response()

        response.encoding = 'utf-8'

        print('command: {}'.format(curl))
        print('response status code: {}'.format(response.status_code))

        response_text = html.unescape(response.text)
        print('response text: {}'.format(response_text))

        print()


    demo(r"curl 'https://postman-echo.com/get?foo1=bar1&foo2=bar2'")

    demo(r"curl 'https://postman-echo.com/post' --data 'This is expected to be sent back as part of response body.'")
