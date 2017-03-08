# coding: utf-8
import asyncio
import datetime

from random import randint


class cron:


    def __init__(self, location):
        self.location = location
        self.now = datetime.datetime.now(self.location.tzinfo)
        self.sun = self.location.sun()
        #self.sunrise = self.sun['sunrise']
        self.sunrise = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(minutes=1)
        self.noon = self.sun['noon']
        self.sunset = self.sun['sunset']
        self.first_run = {
            'is_after_noon': True,
            'is_after_sunrise': True
        }


    async def is_after_noon(self):
        while True:
            self.now = datetime.datetime.now(self.location.tzinfo)
            if  0 < (self.now - self.noon).total_seconds() < 30:
                print('After noon')
                self.noon = self.location.sun(date=datetime.date.today() + datetime.timedelta(days=1))['noon']
            else:
                print('Before noon')
            await asyncio.sleep(randint(5, 10))

    async def is_after_sunrise(self):
        while True:
            self.now = datetime.datetime.now(self.location.tzinfo)
            if 0 < (self.now - self.sunrise).total_seconds() < 30:
                print('>>>> After Sunrise <<<<')
                self.sunrise = self.location.sun(date=datetime.date.today() + datetime.timedelta(days=1))['sunrise']
            else:
                print('Before sunrise')
            await asyncio.sleep(randint(5, 10))
            
