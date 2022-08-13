## Blebox shutterbox

Tool for managing external shutters with shutterbox. It adds the ability to tilt the shutters. This functionality in theory is implemented in shutterbox (if you select appropriate mode for shutters), but I don't like the way it works. This tool can be used for example with homeassistant to trigger shutter opening, closing and tilting.

## Example requests

This app can be used with any tool that is able to send http requests. I use bash scripts with curl commands and hook them up to home assistant.

### Tilting shutters

To tilt two shutters with IP addresses 192.168.0.100 and 192.168.0.101, with the shutterbox server (this app) running on localhost:

    curl http://localhost:8000/tilt?host=192.168.0.100&host=192.168.0.101

To tilt shutters, first they have to go down all the way. Then they have to go up for a certain time and then stop. Tilt factor is the amount of time the shutters go up before they stop (in seconds). 

To adjust the tilt factor (in seconds):

    curl http://localhost:8000/tilt?host=192.168.0.100&host=192.168.0.101&tilt_factor=0.5

### Opening shutters

    curl http://localhost:8000/up?host=192.168.0.100&host=192.168.0.101

### Closing shutters

    curl http://localhost:8000/down?host=192.168.0.100&host=192.168.0.101

### Stopping shutters

    curl http://localhost:8000/stop?host=192.168.0.100&host=192.168.0.101