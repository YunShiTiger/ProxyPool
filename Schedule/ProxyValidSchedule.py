# -*- coding: utf-8 -*-

import sys
import time

try:
    from Queue import Queue  # py3
except:
    from queue import Queue  # py2

from Schedule.ProxyCheck import ProxyCheck
from Manager.ProxyManager import ProxyManager
from Log.LogManager import log
from Config.ConfigManager import config


class ProxyValidSchedule(ProxyManager, object):
    def __init__(self):
        ProxyManager.__init__(self)
        self.queue = Queue()
        self.proxy_item = dict()

    def __validProxy(self, threads=config.BASE.verify_useful_proxy_thread):
        """
        验证useful_proxy代理
        :param threads: 线程数
        :return:
        """
        thread_list = list()
        for index in range(threads):
            thread_list.append(ProxyCheck(self.queue, self.proxy_item))

        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
            thread.join()

    def main(self):
        self.putQueue()
        while True:
            if not self.queue.empty():
                log.info("Start Valid useful_proxy proxy")
                self.__validProxy()
            else:
                log.info('Valid Complete, Sleep 5 Min!')
                time.sleep(60 * config.BASE.verify_useful_proxy_interval)
                self.putQueue()

    def putQueue(self):
        self.db.changeTable(self.useful_proxy_queue)
        self.proxy_item = self.db.getAll()
        for item in self.proxy_item:
            self.queue.put(item)


def run():
    p = ProxyValidSchedule()
    p.main()


if __name__ == '__main__':
    p = ProxyValidSchedule()
    p.main()
