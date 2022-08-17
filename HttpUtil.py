import time
import requests
from config import *
from lxml import etree


def get(
        api_url: str,
        params: dict = None,
        retry: int = 0,
        gbk: bool = False,
        max_retries: int = 5,
        return_type: str = "text"
) -> [str, dict, int, None]:
    try:
        response = requests.get(api_url, params=params, headers=Vars.cfg.data['user_agent'])
        if gbk:
            response.encoding = 'gbk'
        if response.status_code == 404 or response.status_code == 500:
            return 404
        if response.status_code == 200:
            if return_type == "json":
                return response.json()
            elif return_type == "text":
                return response.text
            elif return_type == "content":
                return response.content
    except (Exception, requests.exceptions.ConnectionError) as error:
        if retry <= max_retries:
            if retry >= 3:
                print("get error, url is {}".format(api_url))
            if retry == max_retries:
                print("get error: {}\n{}".format(error, api_url))
            return get(api_url=api_url, params=params, retry=retry + 1, gbk=gbk)

 