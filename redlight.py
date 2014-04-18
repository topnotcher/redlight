#!/usr/bin/env python
import urllib2
import urllib
import base64
import json
import argparse

parser = argparse.ArgumentParser(description='Push a notification to the red light')
parser.add_argument('-k', '--key', type=str, required=True, help="key for the service. host/service normally")
parser.add_argument('-s', '--state', type=str, required=True, help="The state (CRITICAL|WARNING|OK|UNKNOWN etc)")
args = parser.parse_args()

notify_url = 'http://10.1.96.38'
data = {'key':args.key, 'state':args.state}

url = notify_url+'/?%s'% (urllib.urlencode(data))
urllib2.urlopen(url)
