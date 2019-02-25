#! /usr/bin/env python3
# 
# (c) Artem Ageev.
# This scipt will query Cisco Umbrella activity history
# Umbrella log retention time - 30 days
# API docs: https://docs.umbrella.com/umbrella-api/docs/about-the-umbrella-api

# curl -i -X GET --url "https://reports.api.umbrella.com/v1/organizations/{COMPANY_ID}/destinations/{domain}/activity?limit=100&offset=0" 
# --header 'Authorization: Basic <base_64(key:value)>'

import requests
import json
import logging
import sys
import time 
from datetime import datetime, timedelta

APIKEY = '<your_secret_apikey>'
COMPANY_ID = '<your_id>'

wait_time = 20 #seconds
#search_time_window = 0.5 #days

logPath = 'C:/Temp/'
logFile = 'umbrella'

logging.basicConfig(
    format='%(asctime)s %(levelname)-5s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.INFO,
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(logPath, logFile)),
        logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)

def main(search_time_window, domains):
    TIME_START = datetime.now() - timedelta(days=int(search_time_window))
    TIME_END = datetime.now()
    result = []

    for domain in domains:
        domain = domain.replace("[", "").replace("]", "") #allows you to use escaped domains like domain[.]com
        
        while True:
            data = getHistory(domain, TIME_START, TIME_END)
 #          print(json.dumps(data, indent=4, sort_keys=True))
            if 'statusCode' in data:
                if data['statusCode'] == 408:
                    logger.info('Received 408 reply from Umbrella. Waiting %s seconds to repeat.' % wait_time)
                    time.sleep(wait_time)
            else:
                break

        if 'requests' in data:
            if data['requests']:
                for _ in data['requests']:
#                   print(json.dumps(_, indent=4, sort_keys=True))
                    result.append([_['datetime'], _['internalIp'], _['originLabel'], _['destination'], _['actionTaken']])
     
    for _ in result:
        print(";".join(map(str,_)))

def getHistory(domain, start, end):
    
    start_epoch = int(start.timestamp())
    end_epoch = int(end.timestamp())

    url = ('https://reports.api.umbrella.com/v1/organizations/%s/destinations/%s/activity?limit=100&offset=0&start=%s&end=%s' % (COMPANY_ID, domain, start_epoch, end_epoch))
    logger.info('Getting data from: {0}'.format(url))
    headers = {'Authorization':'Basic %s' % (APIKEY)}
    try:
        r = requests.get(url, headers = headers)
        logger.info("Domain %s queried" % domain)
        return r.json()
    except Exception as exc:
        print(exc)

if __name__ == "__main__":
    if len(sys.argv)>1:
        main(sys.argv[1], sys.argv[2:])
    else:
        days = input("How many days to look back for? (Default and maximum = 30)")
        if days == "":
            days = 30
        domains = []
        exit = False
        while not exit:
            _ = input("Please type domain name. Finish with empty line: ")
            if _:
                domains.append(_)
            else:
                exit = True
        main(days, domains)
