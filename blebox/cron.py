#,coding: utf-8
import asyncio
import datetime
import logging
import os

from random import randint


class Cron:

    def __init__(self, location):
        self.location = location
        self.now = datetime.datetime.now(self.location.tzinfo)
        self.sun = self.location.sun()
        self.sunrise = self.sun['sunrise']
        #self.sunrise = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(seconds=(60*15)+30)
        self.noon = self.sun['noon']
        #self.noon = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(seconds=70)
        self.sunset = self.sun['sunset']
        #self.sunset = datetime.datetime.now(self.location.tzinfo) + datetime.timedelta(seconds=30)
        self.logger = logging.getLogger('blebox.cron')


    async def is_after(self, time, offset, tasks, *args):
        while True:
            try:
                self.now = datetime.datetime.now(self.location.tzinfo)
                seconds_to_event = (getattr(self, time) - self.now).total_seconds() + datetime.timedelta(seconds=offset).total_seconds()
                if self.now < getattr(self, time):
                    self.logger.info('Pending tasks: {}'.format(tasks))
                    self.logger.info('Task delayed by {}. Waiting for <{} {} {}>.'.format(self.seconds_to_time(seconds_to_event), self.seconds_to_time(abs(offset)), self.before_or_after(offset), time))
                    await asyncio.sleep(seconds_to_event)
                    self.logger.info('<{} {} {}> at {}'.format(self.seconds_to_time(abs(offset)), self.before_or_after(offset), time, datetime.datetime.now(self.location.tzinfo)))
                    for task in tasks:
                        self.ping(task.__self__)
                    if args:
                        coroutines = [i(*args) for i in tasks]
                    else:
                        coroutines = [i() for i in tasks]
                    
                    self.logger.info('Executing {}'.format(tasks))
                    result = await asyncio.gather(*coroutines, return_exceptions=True)
                    errors = [e[1] for e in result if e[1] > 200]
                    if errors:
                        self.logger.warning('Unexpected status codes: {}'.format(errors))
                        self.logger.warning(result)
                    else:
                        self.logger.info(result)
                setattr(self, time, self.location.sun(date=datetime.date.today() + datetime.timedelta(days=1))[time])
            except Exception as e:
                self.logger.exception(e)

    async def run_at(self, seconds, tasks, *args):
        event_time = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=seconds)
        while True:
            try:
                self.now = datetime.datetime.now()
                seconds_to_event = (event_time - self.now).total_seconds()
                if self.now < event_time:
                    self.logger.info('Pending tasks: {}'.format(tasks))
                    self.logger.info('Task delayed by {}. Waiting for <{}>.'.format(self.seconds_to_time(seconds_to_event), self.seconds_to_time(seconds)))
                    await asyncio.sleep(seconds_to_event)
                    self.logger.info('<{}> executed at {}'.format(self.seconds_to_time(seconds), datetime.datetime.now()))
                    for task in tasks:
                        self.ping(task.__self__)
                    if args:
                        coroutines = [i(*args) for i in tasks]
                    else:
                        coroutines = [i() for i in tasks]
                    self.logger.info('Executing {}'.format(tasks))
                    result = await asyncio.gather(*coroutines, return_exceptions=True)
                    errors = [e[1] for e in result if e[1] > 200]
                    if errors:
                        self.logger.warning('Unexpected status codes: {}'.format(errors))
                        self.logger.warning(result)
                    else:
                        self.logger.info(result)
                event_time += datetime.timedelta(days=1)
            except Exception as e:
                self.logger.exception(e)

    def ping(self, address):
        ping = os.system("ping -c 2 {} > /dev/null".format(address))
        if ping == 0:
            self.logger.info('Ping successful for {}'.format(address))
        else:
            self.logger.warning('Ping unsuccessful for {}'.format(address))

    @staticmethod
    def before_or_after(seconds):
        if seconds > 0:
            return 'after'
        else:
            return 'before'

    @staticmethod
    def seconds_to_time(seconds):
        seconds = int(seconds)
        min, sec = divmod(seconds, 60)
        h, min = divmod(min, 60)
        output = ''
        if sec > 0:
            output = "{:02d}s".format(sec)
        if min > 0:
            output = "{:02d}m{}".format(min, output)
        if h > 0:
            output = "{:02d}h{}".format(h, output)
        return output


