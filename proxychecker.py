#!/usr/bin/python2

import argparse
from sockshandler import SocksiPyHandler
import urllib2
from collections import namedtuple
import os
import re
import socks

Proxy = namedtuple('Proxy', 'proto, host, port, username, password')

scheme_mapping = {
  'socks5': socks.PROXY_TYPE_SOCKS5,
  'socks4': socks.PROXY_TYPE_SOCKS4,
  'http': socks.PROXY_TYPE_HTTP
}

def parse_proxy_file(fname):
    """Parses a proxy file

    The format should be like the following:

        socks5 23.212.45.13:1080 username:password
        socks4 23.212.45.13:80 username:password
        http 23.212.45.13:80

        If username and password aren't provided, GoogleScraper assumes
        that the proxy doesn't need auth credentials.

    Args:
        fname: The file name where to look for proxies.

    Returns:
        The parsed proxies.

    Raises:
        ValueError if no file with the path fname could be found.
    """
    proxies = []
    path = os.path.join(os.getcwd(), fname)
    if os.path.exists(path):
        with open(path, 'r') as pf:
            for line in pf.readlines():
                proxies.append(parse_proxy(line))
        return proxies
    else:
        raise ValueError('No such file/directory')


def parse_proxy(line):
  """Parses proxies from a string.
  
  Args:
    contents: The string that should be parsed.
    
  Returns:
    The parsed proxy.
  """
  proxy = None
  
  if not (line.strip().startswith('#') or line.strip().startswith('//')):
      tokens = line.replace('\n', '').split(' ')
      try:
          proto = tokens[0]
          host, port = tokens[1].split(':')
      except:
          raise Exception('Invalid proxy format.')
      if len(tokens) == 3:
          username, password = tokens[2].split(':')
          proxy = Proxy(proto=proto, host=host, port=port, username=username, password=password)
      else:
          proxy = Proxy(proto=proto, host=host, port=port, username='', password='')
  return proxy
  
def check_proxy(proxy, p=False):
    """Checks the status of the proxy object.
    
    Args:
      proxy: A proxy to check.
      p: A boolean variable that indicates whether to print or return the value.
      
    Returns: The status of the proxy. If there was a failure,
            the reason is given back to the caller as an exception string.
    """
  
    if isinstance(proxy, dict):
      proxy = Proxy(proto=proxy['proto'], host=proxy['host'], port=proxy['port'], username=proxy['username'], password=proxy['password'])
      
    try:
      opener = urllib2.build_opener(SocksiPyHandler(scheme_mapping[proxy.proto], proxy.host, int(proxy.port)))
      opener.open("http://httpbin.org/ip").read()
    except socks.ProxyConnectionError as e:
      if p:
        print '{} is \033[91m offline \033[0m'.format(proxy)
      else:
        return ('offline', str(e))
    else:
      if p:
        print '{} is \033[91m online \033[0m'.format(proxy)
      else:
        return 'online'
        
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-p', '--proxy', help='A proxy to check. Example: "socks4 localhost:1080 user pass"')
  group.add_argument('-f', '--proxy-file', help='The proxy file to check. Format: "proto host:port username password". Example: "socks5 localhost:9050 user pass"')
  args = parser.parse_args()
  
  proxies = []
  
  if args.proxy_file:
    proxies = parse_proxy_file(args.proxy_file)
  elif args.proxy:
    proxies = [parse_proxy(args.proxy)]
    
  for proxy in proxies:
    check_proxy(proxy, True)
