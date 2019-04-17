from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import logging

from time import time

from monitor import UptimeMonitor



def check_page(url):
    try:
        response = urlopen(url, timeout=10).read().decode('utf-8')
    except HTTPError as error:
        logging.error("Data not retrived because %s\nURL: %s", error, url)
    except URLError as error:
        if isinstance(error.reason, socket.timeout):
            logging.error('socket timed out - URL %s', url)
        else:
            logging.error('some other error happened')
    else:
        logging.info('Access successful')

testurl = "http://www.google.ca"

start_time = time()
# check_page(testurl)
end_time = time()

print(f'start1 to end = {end_time - start_time}')

json_url_file = 'urllist.json'

monitor = UptimeMonitor(json_url_file)
monitor.print_url_list()
