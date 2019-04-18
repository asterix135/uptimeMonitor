import time
from datetime import datetime
from monitor import UptimeMonitor

json_url_file = 'urllist.json'
monitor = UptimeMonitor(json_url_file)

while True:
    print(f"Site check at {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    monitor.check_all_sites()
    time.sleep(300)
