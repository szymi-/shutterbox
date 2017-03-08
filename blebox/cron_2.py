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
        #self.sunrise = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(minutes=1)
        self.noon = self.sun['noon']
        #self.noon = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(minutes=5)
        #self.sunset = self.sun['sunset']
        self.sunset = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(seconds=10)


    async def is_after(self, time, offset=0, tasks=None, loop=None):
        while True:
            self.now = datetime.datetime.now(self.location.tzinfo)
            event_time = (getattr(self, time) - self.now).total_seconds() + datetime.timedelta(seconds=offset).total_seconds()
            if self.now < getattr(self, time):
                print('Waiting {} seconds for {}.'.format(event_time, time))
                await asyncio.sleep(event_time)
                print('{} at {}'.format(time.capitalize(), datetime.datetime.now(self.location.tzinfo)))
                if tasks:
                    asyncio.gather(*tasks, loop=loop)
            setattr(self, time, self.location.sun(date=datetime.date.today() + datetime.timedelta(days=1))[time])
