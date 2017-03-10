# coding: utf-8
import requests
import polling
import asyncio
import logging

from aiohttp import ClientSession

from time import sleep


class ShutterManager:

    def __init__(self, address):
        self.address = address
        self.logger = logging.getLogger('blebox.ShutterManager')

    def __repr__(self):
        return self.address

    def up(self, *args):
        url = 'http://{}/s/u'.format(self.address)
        return self._send_command(url)

    def down(self, *args):
        url = 'http://{}/s/d'.format(self.address)
        return self._send_command(url)

    def stop(self, *args):
        url = 'http://{}/s/s'.format(self.address)
        return self._send_command(url)

    def position(self, position):
        url = 'http://{}/s/p/{}'.format(self.address, position)
        return self._send_command(url)

    def current_position(self, do_async=False):
        url = 'http://{}/api/shutter/state'.format(self.address)
        if do_async == True:
            return self._send_command(url)
        else:
            result = requests.get(url)
            return result.json()['currentPos']['position']

    def is_in_position(self, position):
        try:
            return polling.poll(lambda: self.current_position() == position, step=1, timeout=600)
        except polling.TimeoutException:
            return False
    
    async def tilt(self, *args):
        if not args:
            time = 0.8
        else:
            time = args[0]
        await self.down()
        self.is_in_position(100)
        await self.up()
        await asyncio.sleep(time)
        await self.stop()

    async def _send_command(self, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                try:
                    json = await response.json()
                except Exception as e:
                    self.logger.exception(e)
                return json, response.status
