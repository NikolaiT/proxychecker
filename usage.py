from proxychecker import check_proxy, Proxy

proxy = Proxy(proto='socks5', host='localhost', port='9055', username='', password='')

print check_proxy(proxy)
