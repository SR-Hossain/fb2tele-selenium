import requests
from bs4 import BeautifulSoup

from fb2tele.settings import env


class Browser:
    def __init__(self):
        headers_json_in_string_format = env.str('HEADER_WITH_COOKIES')
        self.headers = eval(headers_json_in_string_format)
        self.content = None

    def get_response(self, url: str):
        response = requests.get(url, headers=self.headers)
        return response.status_code

    def get_html_data(self, url: str):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            self.content = BeautifulSoup(response.content, 'html.parser')
        else:
            print("Failed to retrieve content. Status code:", response.status_code)

        return response.status_code
