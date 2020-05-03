#!/usr/bin/env /usr/local/bin/python3
# <bitbar.title>Tasmota Switch Devices</bitbar.title>
# <bitbar.author></bitbar.author>
# <bitbar.author.github>ChristianTreutler</bitbar.author.github>
# <bitbar.desc>See status and set state of Tasmota devices</bitbar.desc>
# <bitbar.dependencies>python,requests</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/yogitea/bitbar-plugin-tasmota-switch<bitbar.abouturl>

import sys
import os
import os.path
import subprocess
import time
import argparse
import urllib.parse
import requests

# Define Tasmota switches here:
tasmota_devices = {
#    'NameOfSwitch' : '10.10.10.10',
}

def make_call(prog, *args):
    res = []
    res.append('bash="{0}"'.format(prog))
    for i, arg in enumerate(args):
        res.append('param{0}="{1}"'.format(i + 1, arg))
    return " ".join(res)


def main(device=None, action=None):
    parser = argparse.ArgumentParser(description='tasmota devices')
    parser.add_argument('--device', help='the device id')
    parser.add_argument('--action', help='on or off')

    args = parser.parse_args()

    devices_on = []
    devices_off = []

    if args.device is not None:
        if args.action is not None:
            if args.action == "on":
                r = requests.get(f'http://{tasmota_devices[args.device]}/cm?cmnd=Power%20on')
            elif args.action == "off":
                r = requests.get(f'http://{tasmota_devices[args.device]}/cm?cmnd=Power%20off')

    if not tasmota_devices:
        print('Please define your devices first.')
        return

    for device_name in tasmota_devices.keys():
        r = requests.get(f'http://{tasmota_devices[device_name]}/cm?cmnd=Power')
        data = r.json()
        if data['POWER'] == 'ON':
           devices_on.append(device_name) 
        elif data['POWER'] == 'OFF':
           devices_off.append(device_name)  

    if devices_on:
        print("%d On | color=blue" % (len(devices_on)))
    else:
        print("All Off| color=green")
    print("---")
    print("Your Tasmota switches")
    print("---")
    for device in devices_on:
        text = "{0} - switch off".format(device)
        action = make_call(sys.argv[0], "--device", urllib.parse.quote(device), "--action", "off")
        print("%s|%s terminal=false refresh=true" % (text, action))
    for device in devices_off:
        text = "{0} - switch on".format(device)
        action = make_call(sys.argv[0], "--device", urllib.parse.quote(device), "--action", "on")
        print("%s|%s terminal=false refresh=true" % (text, action))


if __name__ == '__main__':
    main()

