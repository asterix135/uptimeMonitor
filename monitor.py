import json

class UptimeMonitor():
    def __init__(self, json_list_location):
        self.url_list = self.__load_json_list(json_list_location)

    def __load_json_list(self, json_list_location):
        with open(json_list_location) as f:
            location_list = json.load(f)
        return location_list

    def print_url_list(self):
        print(self.url_list)
