from __future__ import print_function
import os
import json
import requests
from datetime import datetime
from decimal import Decimal
from local_settings import API_URL


def _read_temp():
    with file('/sys/bus/w1/devices/28-001454cef7ff/w1_slave', 'rt') as f:
        lines = f.readlines()
        if lines[0].strip()[-3:] == 'YES':
            ts = lines[1].find('t=')
            tempc = Decimal(lines[1][ts+2:]) / 1000
            tempf = ((tempc * 9) / 5) + 32
            return tempf
    return None


def _send_temp(temp):
    d = json.dumps({'value': float(round(temp,1)), 'at': str(datetime.now()), 'meta': {}})
    requests.put(API_URL, data=d)
    

def main():
    print("begin -- temp send")
    t = _read_temp()
    if t is not None:
        _send_temp(t)
    print("end -- temp send")


if __name__ == "__main__":
    main()
