from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from socket import timeout
from time import time
from datetime import datetime
import json
import ssl
import os

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
        todays_date = datetime.today().strftime('%Y-%m-%d')
        todays_data = self.__load_daily_json_data(todays_date)
        for url in self._url_list:
            results = self.check_site(url)
            self.__update_todays_data(todays_data, results, url)
        self.__write_daily_json_data(todays_date, todays_data)

    def check_site(self, url):
        start_time = time()
        formatted_start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        site_results = {
            "load_time": 0.0,
            "timeout_errors": 0,
            "other_errors": 0,
            "error_timestamp": None
        }
        try:
            response = urlopen(url, timeout=5, context=ssl.SSLContext()).read()
        except (HTTPError, URLError) as error:
            logging.error(
                'Data not retrieved at %s because %s\nURL: %s',
                formatted_start_time, error, url
            )
            site_results["other_errors"] = 1
            site_results["error_timestamp"] = formatted_start_time
        except timeout:
            logging.error(
                'socket timed out at %s - URL %s',
                formatted_start_time, url
            )
            site_results["timeout_errors"] = 1
            site_results["error_timestamp"] = formatted_start_time
        else:
            logging.info(
                'Access successful at %s - URL %s',
                formatted_start_time, url
            )
        site_results["load_time"] = time() - start_time
        return site_results

    def __update_todays_data(self, todays_data, site_result, url):
        todays_data[url]["times_accessed"] += 1
        todays_data[url]["total_load_time"] += site_result["load_time"]
        todays_data[url]["timeout_errors"] += site_result["timeout_errors"]
        todays_data[url]["other_errors"] += site_result["other_errors"]
        if site_result["error_timestamp"]:
            todays_data[url]["error_timestamps"].append(site_result["error_timestamp"])

    def __load_daily_json_data(self, todays_date):
        todays_json_file = self.__todays_json_file_path(todays_date)
        if os.path.isfile(todays_json_file) and os.access(todays_json_file, os.R_OK):
            with open(todays_json_file) as f:
                todays_data = json.load(f)
            return todays_data
        else:
            return self.__create_new_json_log_data()

    def __create_new_json_log_data(self):
        new_log_data = {}
        for url in self._url_list:
            new_log_data[url] = {
                "times_accessed": 0,
                "total_load_time": 0.0,
                "timeout_errors": 0,
                "other_errors": 0,
                "error_timestamps": []
            }
        return new_log_data

    def __todays_json_file_path(self, todays_date):
        return os.path.join('monitoringStats/', todays_date + '.json')

    def __write_daily_json_data(self, todays_date, todays_data):
        with open(self.__todays_json_file_path(todays_date), 'w') as outfile:
            json.dump(todays_data, outfile)
