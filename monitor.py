from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from socket import timeout
from time import time
from datetime import datetime
import json
import ssl

import logging

logging.basicConfig(filename="errorlog.log", level=logging.ERROR)

class UptimeMonitor():
    def __init__(self, json_list_location):
        self._url_list = self.__load_json_list(json_list_location)

    def __load_json_list(self, json_list_location):
        with open(json_list_location) as f:
            location_list = json.load(f)
        return location_list

    def print_url_list(self):
        print(self._url_list)

    def url_list(self):
        return(self._url_list)

    def check_all_sites(self):
        for url in self._url_list:
            self.check_site(url)

    def check_site(self, url):
        start_time = time()
        formatted_start_time = datetime.fromtimestamp(time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        try:
            response = urlopen(url, timeout=5, context=ssl.SSLContext()).read()
        except (HTTPError, URLError) as error:
            logging.error(
                'Data not retrieved at %s because %s\nURL: %s',
                formatted_start_time, error, url
            )
        except timeout:
            logging.error(
                'socket timed out at %s - URL %s',
                formatted_start_time, url
            )
        else:
            logging.info(
                'Access successful at %s - URL %s',
                formatted_start_time, url
            )
