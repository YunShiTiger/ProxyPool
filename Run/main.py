# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')

import time
from multiprocessing import Process

from Log import LogManager
from Api.ProxyApi import run as ProxyApiRun
from Schedule.ProxyValidSchedule import run as ValidRun
from Schedule.ProxyRefreshSchedule import run as RefreshRun

def showTime():
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    content = "{newline}{symbol} ProxyPool Start, date:{date} {symbol}{newline}".format(newline="\n", symbol="-"*50, date=date)
    print(content)

def main(test=False):
    showTime()
    LogManager.Init()

    p_list = list()

    p1 = Process(target=ProxyApiRun, name='ProxyApiRun')
    p_list.append(p1)
    p2 = Process(target=ValidRun, name='ValidRun')
    p_list.append(p2)
    p3 = Process(target=RefreshRun, name='RefreshRun')
    p_list.append(p3)

    for p in p_list:
        p.daemon = True
        p.start()

    if test:
        time.sleep(5)
        sys.exit(0)
    else:
        for p in p_list:
            p.join()

if __name__ == '__main__':
    main()