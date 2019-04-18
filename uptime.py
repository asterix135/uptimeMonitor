import time
from monitor import UptimeMonitor

json_url_file = 'urllist.json'
monitor = UptimeMonitor(json_url_file)

while True:
    monitor.check_all_sites()
    time.sleep(300)
