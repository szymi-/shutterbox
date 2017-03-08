# coding: utf-8
import asyncio
import datetime

from random import randint


class cron:


    def __init__(self, dabrowa):
        self.dabrowa = dabrowa
        self.sun = self.dabrowa.sun()
        #self.sunrise = self.sun['sunrise']
        self.sunrise = datetime.datetime.now(self.dabrowa.tzinfo) + datetime.timedelta(minutes=1)
        self.noon = self.sun['noon']
        self.sunset = self.sun['sunset']
        self.now = datetime.datetime.now(self.dabrowa.tzinfo)
        self.first_run = {
            'is_after_noon': True,
            'is_after_sunrise': True
        }


    async def is_after_noon(self):
        while True:
            self.now = datetime.datetime.now(self.dabrowa.tzinfo)
            await asyncio.sleep(
            if  0 < (self.now - self.noon).total_seconds() < 30:
                print('After noon') # do stuff here
                self.noon = self.dabrowa.sun(date=datetime.date.today() + datetime.timedelta(days=1))['noon']
            else:
                print('Before noon')
            await asyncio.sleep(randint(5, 10))

    async def is_after_sunrise(self):
        while True:
            self.now = datetime.datetime.now(self.dabrowa.tzinfo)
            if 0 < (self.now - self.sunrise).total_seconds() < 30:
                print('>>>> After Sunrise <<<<') # do stuff here
                self.sunrise = self.dabrowa.sun(date=datetime.date.today() + datetime.timedelta(days=1))['sunrise']
            else:
                print('Before sunrise')
            await asyncio.sleep(randint(5, 10))
            
