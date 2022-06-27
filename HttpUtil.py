import time
import requests
from config import *
from lxml import etree


def get(api_url: str, params: dict = None, retry: int = 0, gbk: bool = False) -> [str, None, int]:
    if retry >= 5:
        time.sleep(retry * 0.5)
        print("retry is {}, sleep time is:[{}] url:{}".format(retry, int(retry * 0.5), api_url))
    response = requests.get(api_url, params=params, headers=Vars.cfg.data['user_agent'])
    if gbk:
        response.encoding = 'gbk'
    if response.status_code == 404 or response.status_code == 500:
        return 404
    return response.text if response.status_code == 200 else None


def post(api_url: str, data: dict = None, retry: int = 0, max_retries: int = 3):
    response = requests.post(api_url, data=data, headers=Vars.cfg.data['user_agent'])
    response.encoding = 'gbk'
    if response.status_code == 200:
        return response.text
    if retry <= max_retries:
        post(api_url=api_url, data=data, retry=retry + 1, max_retries=max_retries - 1)
    else:
        print("retry is over, status code is {}".format(response.status_code))
