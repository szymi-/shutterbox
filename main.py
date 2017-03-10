# -*- encoding: utf-8 -*-
"""shutters
Usage:
    async_shutters.py [options] <shutter_hostname>...

Options:
    -a <action> --action=<action>	Action
    -t <tilt> --tilt=<tilt>         Tilt delay [default: 0.8]
"""
import asyncio
import logging

from time import sleep
from docopt import docopt
from blebox.shutter import ShutterManager

logging.basicConfig(
    filename='/tmp/shutters.log',
    level=logging.DEBUG,
    format='%(levelname)s:%(name)s:%(asctime)s:%(message)s'
)

action_map = {
    'up': 'up',
    'down': 'down',
    'stop': 'stop',
    'tilt': 'down',
    'status': None
}

args = docopt(__doc__)
shutters = []
for shutter in args['<shutter_hostname>']:
    shutters.append(ShutterManager(shutter))
action = args['--action']
tilt = float(args['--tilt'])
loop = asyncio.get_event_loop()

if action not in ['up', 'down', 'stop', 'status', 'tilt']:
    raise Exception('Wrong action specified')

tasks = []

for shutter in shutters:
    if action == 'tilt':
        tasks.append(shutter.tilt(tilt))
    else:
        tasks.append(
            getattr(shutter, action)()
        )

result = loop.run_until_complete(asyncio.gather(*tasks))
logging.info('Action: {}, result: {}'.format(action, result))
