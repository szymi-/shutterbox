# coding: utf-8
import requests
import polling

from time import sleep

class ShutterManager:

    def __init__(self, ip):
        self.ip = ip

    def up(self):
        url = 'http://{}/s/u'.format(self.ip)
        result = requests.get(url)
        return result

    def down(self):
        url = 'http://{}/s/d'.format(self.ip)
        result = requests.get(url)
        return result

    def stop(self):
        url = 'http://{}/s/s'.format(self.ip)
        result = requests.get(url)
        return result

    def position(self, position):
        url = 'http://{}/s/p/{}'.format(self.ip, position)
        result = requests.get(url)
        return result

    def current_position(self):
        url = 'http://{}/api/shutter/state'.format(self.ip)
        result = requests.get(url)
        return result.json()['currentPos']['position']

    def is_in_position(self, position):
        try:
            return polling.poll(lambda: self.current_position() == position, step=1, timeout=600)
        except polling.TimeoutException:
            return False
    
    def tilt(self, direction='up', time=1):
        if direction == 'up':
            self.up()
        elif direction == 'down':
            self.down()
        sleep(time)
        self.stop()
