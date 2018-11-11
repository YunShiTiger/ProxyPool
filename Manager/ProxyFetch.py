# -*- coding: utf-8 -*-
# !/usr/bin/env python

from Manager.ProxyManager import ProxyManager
from ProxyGetter.getFreeProxy import GetFreeProxy
from Log.LogManager import log
from Util.GetConfig import config
from Util.utilFunction import verifyProxyFormat

class ProxyFetch(ProxyManager):

    def run(self):
        for proxyGetter in config.proxy_getter_functions:
            try:
                log.info("Fetch Proxy Start, func:{func}".format(func=proxyGetter))

                total = 0
                succ = 0
                fail = 0
                for proxy in getattr(GetFreeProxy, proxyGetter.strip())():
                    proxy = proxy.strip()
                    if proxy and verifyProxyFormat(proxy) and not self.checkRawProxyExists(proxy):
                        self.saveRawProxy(proxy)
                        succ = succ + 1
                        log.debug('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
                    else:
                        fail = fail + 1
                        log.error('{func}: fetch proxy {proxy} error'.format(func=proxyGetter, proxy=proxy))

                    total = total + 1
                
                log.info("fetch proxy end, func:{func}, total:{total}, succ:{succ} fail:{fail}".format(func=proxyGetter, total=total, succ=succ, fail=fail))

            except Exception as e:
                log.error("func_name:{func} fetch proxy fail, error:{error}".format(func=proxyGetter, error=e))
                continue
