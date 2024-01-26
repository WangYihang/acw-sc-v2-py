"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = acw_sc_v2_py.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

import logging

from acw_sc_v2_py import __version__

__author__ = "Yihang Wang"
__copyright__ = "Yihang Wang"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from acw_sc_v2_py.skeleton import fib`,
# when using this Python module as a library.

import requests
from requests.adapters import HTTPAdapter
from requests import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from http.cookies import SimpleCookie

class AcwScV2Adapter(HTTPAdapter):
    ACW_SC__V2_COOKIE_VALUE = None

    def _generate_cookie(self, html):
        return requests.post("https://acw-sc-v2.authu.online/", data={"data": html}).text.strip()

    def _parse_cookie(self, cookie):
        simple_cookie = SimpleCookie()
        simple_cookie.load(cookie)
        jar = RequestsCookieJar()
        for key, morsel in simple_cookie.items():
            jar.set(key, morsel.value)
        return jar.get_dict()

    def _recreate_request(self, prepared_request: PreparedRequest):
        """
        Recreates a Request object from a PreparedRequest object.

        :param prepared_request: A PreparedRequest object.
        :return: A new Request object.
        """
        method = prepared_request.method
        url = prepared_request.url
        headers = prepared_request.headers
        body = prepared_request.body
        if "Cookie" in headers:
            cookies = self._parse_cookie(headers["Cookie"])
            del headers["Cookie"]
        else:
            cookies = {}
        return requests.Request(method, url, headers=headers, data=body, cookies=cookies)

    def send(self, request: PreparedRequest, **kwargs) -> Response:
        # create new request
        first_request = self._recreate_request(request)
        # set cookie
        cookie_name = "acw_sc__v2"
        if AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE is not None:
            logging.info(f"cookie set {cookie_name}={AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE}")
            first_request.cookies[cookie_name] = AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE
        # try to detect anti spam
        response = super(AcwScV2Adapter, self).send(first_request.prepare(), **kwargs)
        if cookie_name in response.text:
            # anti spam is triggered
            logging.info("detected anti spam is triggered")
            # generate cookie
            AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE = self._generate_cookie(response.text)
            logging.info(f"cookie generated {cookie_name}={AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE}")
            # create new request
            second_request = self._recreate_request(request)
            # set cookie
            second_request.cookies[cookie_name] = AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE
            # resend the origin request
            logging.info("resending the origin request")
            return super(AcwScV2Adapter, self).send(second_request.prepare(), **kwargs)
        else:
            # anti spam is not triggered
            logging.info("anti spam is not triggered")
            return response

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version=f"acw-sc-v2-py {__version__}",
    )
    parser.add_argument(dest="n", help="n-th Fibonacci number", type=int, metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

setup_logging(logging.INFO)
