# coding: utf-8
import asyncio
import datetime

from random import randint


class Cron:

    def __init__(self, location):
        self.location = location
        self.now = datetime.datetime.now(self.location.tzinfo)
        self.sun = self.location.sun()
        self.sunrise = self.sun['sunrise']
        #self.sunrise = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(seconds=5)
        self.noon = self.sun['noon']
        #self.noon = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(seconds=70)
        self.sunset = self.sun['sunset']
        #self.sunset = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(seconds=140)


    async def is_after(self, time, offset, tasks, *args):
        while True:
            self.now = datetime.datetime.now(self.location.tzinfo)
            seconds_to_event = (getattr(self, time) - self.now).total_seconds() + datetime.timedelta(seconds=offset).total_seconds()
            if self.now < getattr(self, time):
                print('Waiting {} seconds for {}.'.format(seconds_to_event, time))
                await asyncio.sleep(seconds_to_event)
                print('{} at {}'.format(time.capitalize(), datetime.datetime.now(self.location.tzinfo)))
                if args:
                    coroutines = [i(*args) for i in tasks]
                else:
                    coroutines = [i() for i in tasks]
                asyncio.gather(*coroutines)
            setattr(self, time, self.location.sun(date=datetime.date.today() + datetime.timedelta(days=1))[time])

    async def run_at(self, time, tasks, *args):
        event_time = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=time)
        while True:
            self.now = datetime.datetime.now()
            seconds_to_event = (event_time - self.now).total_seconds()
            if self.now < event_time:
                print('Waiting {} seconds for {}.'.format(seconds_to_event, time))
                await asyncio.sleep(seconds_to_event)
                print('{} at {}'.format(time, datetime.datetime.now()))
                if args:
                    coroutines = [i(*args) for i in tasks]
                else:
                    coroutines = [i() for i in tasks]
                asyncio.gather(*coroutines)
            event_time += datetime.timedelta(days=1)
