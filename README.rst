.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

============
Python requests.HTTPAdapter for ``acw_sc__v2`` cookie
============

Quick Start
===========

Before using ``acw-sc-v2-py``
-----------------------------

.. code-block:: python

    import requests

    session = requests.Session()

    for i in range(8):
        response = session.get("https://www.example.com/")
        print(response.text)

Usually, you will get blocked after sending 2 consecutive requests to the same website.
The response will be like the following HTML code which requires you to solve a javascript challenge.
If the web page is opened in a browser, the browser will automatically solve the challenge.

.. code-block:: html

    <html><script>
    var arg1='70D9569CD5E5895C84F284A09503B1598C5762A1';
    var _0x4818=['\x63\x73\x4b\x48\x77\x71\x4d\x49,...
    function setCookie(name,value){var expiredate=new Date();...
    function reload(x) {setCookie("acw_sc__v2", x);...
    </script></html>

After using ``acw-sc-v2-py``
----------------------------

.. code-block:: python

    import requests
    # step 1: import
    from acw_sc_v2_py import acw_sc__v2 

    session = requests.Session()

    # step 2: create adapter
    adapter = acw_sc__v2.AcwScV2Adapter()

    # step 3: mount adapter
    session.mont("http://", adapter)
    session.mount("https://", adapter)

    for i in range(8):
        response = session.get("https://www.example.com/")
        print(response.text)

By using ``acw-sc-v2-py``, you will get the normal response.
The ``acw_sc__v2`` will handle the javascript challenge and  automatically update the cookie.

Enable logging
--------------

Prepend the following code to enable detailed log for ``acw-sc-v2-py``.

.. code-block:: python

    import logging
    logger = logging.getLogger("acw_sc_v2_py.acw_sc__v2")
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

    import requests
    from acw_sc_v2_py import acw_sc__v2 

    session = requests.Session()

    adapter = acw_sc__v2.AcwScV2Adapter()
    session.mont("http://", adapter)
    session.mount("https://", adapter)

    for i in range(8):
        response = session.get("https://www.example.com/")
        print(response.text)

The log will be like the following.

.. code-block:: plain

    [2024-01-26 22:01:26] INFO:root:detected anti spam is triggered
    [2024-01-26 22:01:28] INFO:root:cookie generated acw_sc__v2=65b3bb3601fe9ab002c5c1ff58fc71a1115e8322
    [2024-01-26 22:01:28] INFO:root:resending the origin request
    <!DOCTYPE html></html>
    [2024-01-26 22:01:29] INFO:root:cookie set acw_sc__v2=65b3bb3601fe9ab002c5c1ff58fc71a1115e8322
    [2024-01-26 22:01:30] INFO:root:anti spam is not triggered
    <!DOCTYPE html></html>
    ...

.. _pyscaffold-notes:
