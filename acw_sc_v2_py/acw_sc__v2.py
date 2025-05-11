import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s (%(filename)s:%(lineno)d) %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

from requests.adapters import HTTPAdapter
from requests import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from http.cookies import SimpleCookie

class AcwScV2Adapter(HTTPAdapter):
    ACW_SC__V2_COOKIE_VALUE = None

    def __init__(self, *args, acw_sc_v2_solver_url="https://acw-sc-v2.authu.online/", **kwargs):
        super(AcwScV2Adapter, self).__init__(*args, **kwargs)
        self.acw_sc_v2_solver_url = acw_sc_v2_solver_url

    def _generate_cookie(self, html):
        return requests.post(self.acw_sc_v2_solver_url, data={"data": html}).text.strip()

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
            logger.info(f"cookie set {cookie_name}={AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE}")
            first_request.cookies[cookie_name] = AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE
        # try to detect anti spam
        response = super(AcwScV2Adapter, self).send(first_request.prepare(), **kwargs)
        if cookie_name in response.text:
            # anti spam is triggered
            logger.info("detected anti spam is triggered")
            # generate cookie
            AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE = self._generate_cookie(response.text)
            logger.info(f"cookie generated {cookie_name}={AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE}")
            # create new request
            second_request = self._recreate_request(request)
            # set cookie
            second_request.cookies[cookie_name] = AcwScV2Adapter.ACW_SC__V2_COOKIE_VALUE
            # resend the origin request
            logger.info("resending the origin request")
            return super(AcwScV2Adapter, self).send(second_request.prepare(), **kwargs)
        else:
            # anti spam is not triggered
            logger.info("anti spam is not triggered")
            return response