from monitor import UptimeMonitor

json_url_file = 'urllist.json'

monitor = UptimeMonitor(json_url_file)
monitor.check_all_sites()
