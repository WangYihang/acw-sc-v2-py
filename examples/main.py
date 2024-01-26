import time
import requests
import logging

from acw_sc_v2_py import acw_sc__v2


def init():
    # setup logging
    logger = logging.getLogger("acw_sc_v2_py.acw_sc__v2")
    logger.setLevel(logging.DEBUG)
    logger.propagate = True


def handle():
    url = "https://www.beianx.cn/search/ctycdn.com"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Referer": "https://www.beianx.cn/search",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    # create a session
    session = requests.Session()

    # add the following three lines
    adapter = acw_sc__v2.AcwScV2Adapter()
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # send request
    response = session.get(url, headers=headers)
    print(response.text[0:0x40])
    time.sleep(1)

    # send request
    response = session.get(url, headers=headers)
    print(response.text[0:0x40])
    time.sleep(1)

    # send request
    response = session.get(url, headers=headers)
    print(response.text[0:0x40])
    time.sleep(1)

    # send request
    response = session.get(url, headers=headers)
    print(response.text[0:0x40])
    time.sleep(1)


def main():
    init()
    handle()


if __name__ == "__main__":
    main()
