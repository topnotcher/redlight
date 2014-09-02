#!/usr/bin/env python2
import RPi.GPIO as gpio
import time, threading
from flask import Flask, render_template, request,redirect

LIGHT_GPIO = 2
CRITICAL_TIMEOUT = 1800

app = Flask(__name__)

class WatcherThread(threading.Thread):
    def __init__(self,states):
        threading.Thread.__init__(self)
        self.states = states
    def run(self):
        while True:
            time.sleep(30)
            manage_sexy_light(self.states)

class ServiceStates(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.states = {}

    def lock_states(self):
        self.lock.acquire()

    def release_states(self):
        self.lock.release()

    def clear_critical(self,key):
        self.lock_states()

        if key in self.states:
            self.states.pop(key)

        self.release_states()

    def set_critical(self,key):
        self.lock_states()
        self.states[key] = time.time()
        self.release_states()

    def update_state(self,key,state):
        if state in ('CRITICAL','DOWN'):
            self.set_critical(key)
        else:
            self.clear_critical(key)

    def count_critical(self):
        count = 0 
        remove = []
        self.lock_states()
        for key,value in self.states.iteritems():
            if time.time() - value > CRITICAL_TIMEOUT:
                remove.append(key)
            else:
                count += 1

        for key in remove:
            self.states.pop(key)

        self.release_states()
        return count


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

def manage_sexy_light(states):
    if states.count_critical() > 0:
        flash_sexy_red_police_light()
    else:
        disable_sexy_red_police_light()

@app.route('/hilde')
def hilde():
	return redirect('/snafu');

@app.route('/snafu')
def snafu():
	SNAFU_FILE='/tmp/snafu.time'
	if request.args.get('update',None) is not None:
		open(SNAFU_FILE,'w').write(str(int(time.time())))	

	try: 
		incident = int(open(SNAFU_FILE).read())
		days = int((time.time()-incident)/86400)
	except Exception:
		days = 0
	days = str(days)
	
	if request.args.get('get',None) is not None:
		return days
	else:
		return render_template('snafu.html', days=days)

@app.route('/')
def main():
    key = request.args.get('key',None)
    state = request.args.get('state','OK')

    if key is not None:
        states.update_state(key,state)
    
    manage_sexy_light(states)

    return ''


if __name__ == '__main__':
    setup_sexy_red_police_light()
    states = ServiceStates()
    WatcherThread(states).start()
    app.run(host='0.0.0.0')


