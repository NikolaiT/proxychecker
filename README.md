## Proxychecker


#### Installation

`sudo pip install proxychecker`


#### Usage

```python
from proxychecker import check_proxy, Proxy

proxy = Proxy(proto='socks5', host='localhost', port='9050', username='', password='')

print check_proxy(proxy)
```
