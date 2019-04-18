# Uptime Monitor

### Simple python program to monitor uptime & responsiveness of a set of web sites

Essentially, this runs an infinite loop, checking whatever web sites are in urllist.json, and logging results in two ways:

1. Daily summary data in the folder monitoringStats
2. errorlog.log - showing a list of failed attempts

## Setup

1. Requires python 3.6 or higher
2. clone this repo
3. run setup.sh from command line (this will create the monitoringStats directory, and rename sample_urllist.json to urllist.json)
4. update urllist.json with whatever urls you want to check
5. There are no dependencies outside of base python libraries

## To run

From command line:

`python3 uptime.py`
