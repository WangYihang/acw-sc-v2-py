# Python requests.HTTPAdapter for `acw_sc__v2`

`acw_sc__v2` is a cookie used by some websites to prevent crawlers.
When the website detects that the request is sent by a crawler, it returns a javascript challenge. The crawler needs to solve the challenge and resend the request with the cookie set to the challenge value.
This project provides a Python requests.HTTPAdapter to resolve the challenge automatically.

## Usage

```bash
pip install acw-sc-v2-py
```

```bash
# start acw_sc_v2_solver
git clone https://github.com/WangYihang/acw-sc-v2.js.git
cd acw-sc-v2.js
npm install
node app.js
```

```python
import requests

session = requests.Session()

# add the following code to your original requests code
from acw_sc_v2_py import acw_sc__v2 
adapter = acw_sc__v2.AcwScV2Adapter(acw_sc_v2_solver_url="http://localhost:3000/")
session.mount("http://", adapter)
session.mount("https://", adapter)

response = session.get("https://www.example.com/")
print(response.text)
```

## Use Case

### Before using `acw-sc-v2-py`

``` python
import requests

session = requests.Session()

for i in range(8):
    response = session.get("https://www.example.com/")
    print(response.text)
```

Usually, you will get blocked after sending 2 consecutive requests to
the same website. The response will be like the following HTML code
which requires you to solve a javascript challenge. If the web page is
opened in a browser, the browser will automatically solve the challenge.

``` html
<html><script>
var arg1='70D9569CD5E5895C84F284A09503B1598C5762A1';
var _0x4818=['\x63\x73\x4b\x48\x77\x71\x4d\x49,...
function setCookie(name,value){var expiredate=new Date();...
function reload(x) {setCookie("acw_sc__v2", x);...
</script></html>
```

### After using `acw-sc-v2-py`

``` python
import requests
# step 1: import
from acw_sc_v2_py import acw_sc__v2 

session = requests.Session()

# step 2: create adapter
adapter = acw_sc__v2.AcwScV2Adapter()

# step 3: mount adapter
session.mount("http://", adapter)
session.mount("https://", adapter)

for i in range(8):
    response = session.get("https://www.example.com/")
    print(response.text)
```

By using `acw-sc-v2-py`, you will get the normal response. The
`acw_sc__v2` will handle the javascript challenge and automatically
update the cookie.

### Enable logging

Prepend the following code to enable detailed log for `acw-sc-v2-py`.

``` python
import logging
logger = logging.getLogger("acw_sc_v2_py.acw_sc__v2")
logger.setLevel(logging.DEBUG)
logger.propagate = True

import requests
from acw_sc_v2_py import acw_sc__v2 

session = requests.Session()

adapter = acw_sc__v2.AcwScV2Adapter()
session.mount("http://", adapter)
session.mount("https://", adapter)

for i in range(8):
    response = session.get("https://www.example.com/")
    print(response.text)
```

The log will be like the following.

``` plain
[2024-01-26 22:01:26] INFO:root:detected anti spam is triggered
[2024-01-26 22:01:28] INFO:root:cookie generated acw_sc__v2=65b3bb3601fe9ab002c5c1ff58fc71a1115e8322
[2024-01-26 22:01:28] INFO:root:resending the origin request
<!DOCTYPE html></html>
[2024-01-26 22:01:29] INFO:root:cookie set acw_sc__v2=65b3bb3601fe9ab002c5c1ff58fc71a1115e8322
[2024-01-26 22:01:30] INFO:root:anti spam is not triggered
<!DOCTYPE html></html>
...
```

## References

* NodeJS version for Server API ([acw-sc-v2.js](https://github.com/WangYihang/acw-sc-v2.js))
* GoLang version for client code ([acw-sc-v2-go](https://github.com/WangYihang/acw-sc-v2-go))
