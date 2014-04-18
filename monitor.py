#!/usr/bin/env python2
import RPi.GPIO as gpio
import sys,json
import time
import logging
import urllib2

SHINKEN_URL = 'http://mig.app.security.uri.edu/shinken.php'
LIGHT_GPIO = 2

def setup_sexy_red_police_light():
	gpio.setwarnings(False)
	gpio.setmode(gpio.BCM)
	gpio.setup(LIGHT_GPIO, gpio.OUT)
	disable_sexy_red_police_light()

def flash_sexy_red_police_light():
	toggle_sexy_red_police_light(True);

def disable_sexy_red_police_light():
	toggle_sexy_red_police_light(False)

def toggle_sexy_red_police_light(on):
	gpio.output(LIGHT_GPIO, on)

def service_counts(services):
	# this needs to be edited to reflect the actual values.
	status_map = {
		0: 'ok',
		1: 'warning',
		2: 'critical', 
		3: 'unknown'
	};

	service_status = 1;

	# set default counts to 0.
	statuses = { 'total': 0 }
	for id in status_map:
		statuses[ status_map[id] ] = 0;

	#add the counts 
	for service in services:
		statuses[ status_map[ service[service_status] ] ] += 1;
		statuses['total'] += 1;

	return statuses;	

def monitor():
	data = json.load(urllib2.urlopen(SHINKEN_URL))
	statuses = {}

	for host in data:
		counts = service_counts(host[105])

		for idx in counts:
			if not idx in statuses:
				statuses[idx] = 0
			
			statuses[idx] += counts[idx]


	if statuses['critical'] > 0:
		flash_sexy_red_police_light()
	else:
		disable_sexy_red_police_light()


def main():
	setup_sexy_red_police_light()
	flash_sexy_red_police_light()
	logging.basicConfig(leevl=logging.DEBUG)

	while True:
		try:
			monitor()
		except Exception,e:
			logging.exception(e)
			flash_sexy_red_police_light()
		finally:
			time.sleep(120);

	flash_sexy_red_police_light()

if __name__ == '__main__':
	main()
