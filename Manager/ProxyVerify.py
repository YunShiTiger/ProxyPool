# -*- coding: utf-8 -*-
# !/usr/bin/env python

import threading
from Manager.ProxyManager import ProxyManager
from ProxyGetter.getFreeProxy import GetFreeProxy
from Log.LogManager import log
from Util.GetConfig import config
from Util.utilFunction import validUsefulProxy

class ProxyVerify(ProxyManager):

    def verify(self, proxy):
        result = False

        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf8')

        proxies = {"http": "http://{proxy}".format(proxy=proxy)}
        try:
            r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
            if r.status_code == 200:
                result = True
                log.debug("verify proxy [{proxy}] pass".format(proxy=proxy)
            else:
                result = False
                log.debug("verify proxy [{proxy}] fail".format(proxy=proxy)

        except Exception as e:
            log.debug("verify proxy [{proxy}] exception: {error}".format(proxy=proxy, error=e)
            result = False

        return result

class ProxyVerifyRaw(ProxyManager):

    def run(self):

        raw_proxy_item = self.getSampleRawProxy()

        thread_id = threading.currentThread().ident
        log.info("thread_id:{thread_id}, Start ValidProxy `raw_proxy_queue`".format(thread_id=thread_id))

        total = 0
        succ = 0
        fail = 0

        remaining_proxies = self.getAll()
        while raw_proxy_item:
            raw_proxy = raw_proxy_item.get('proxy')
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf8')

            if (raw_proxy not in remaining_proxies) and self.verify(raw_proxy):
                self.saveUsefulProxy(raw_proxy)
                self.deleteRawProxy(raw_proxy)
                remaining_proxies.append(raw_proxy)

                succ = succ + 1
                log.debug('ProxyVerifyRaw: %s validation pass' % raw_proxy)
            else:
                self.rawProxyVailFail(raw_proxy)

                fail = fail + 1
                log.debug('ProxyVerifyRaw: %s validation fail' % raw_proxy)
            total = total + 1
            raw_proxy_item = self.getSampleRawProxy()

        log.info('thread_id:{thread_id}, ValidProxy Complete `raw_proxy_queue`, total:{total}, succ:{succ}, fail:{fail}'.format(thread_id=thread_id, total=total, succ=succ, fail=fail))

class ProxyVerifyUseful(ProxyManager):

    def __init__(self):
        self.queue = Queue()

    def resetQueue():
        self.queue.clear()
        proxys = self.getAllUsefulProxy()
        for proxy in proxys:
            self.queue.put(proxy)

    def run(self):

        thread_id = threading.currentThread().ident
        log.info("thread_id:{thread_id} useful_proxy proxy check start".format(thread_id=thread_id))

        total = 0
        succ = 0
        fail = 0
        while self.queue.qsize():
            proxy = self.queue.get()
            if self.verify(proxy):
                self.usefulProxyVaildSucc(proxy)
                succ = succ + 1
                log.debug("ProxyVerifyUseful: {proxy} validation pass".format(proxy=proxy))
            else:
                self.usefulProxyVaildFail(proxy)
                fail = fail + 1
                log.debug("ProxyVerifyUseful: {proxy} validation fail".format(proxy=proxy))

            self.queue.task_done()
            self.usefulProxyVaildTotal(proxy)
            total = total + 1
        
        log.info('thread_id:{thread_id} proxy check end, total:{total}, succ:{succ}, fail:{fail}'.format(thread_id=thread_id, total=total, succ=succ, fail=fail))
