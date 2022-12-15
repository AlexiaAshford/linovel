import random
import requests
from lxml import etree
from config import *
from tenacity import *
from lib import log
session = requests.Session()
try:
    fake_useragent_list = json.loads(open("./lib/utils/fake_useragent_0.1.11.json", "r", encoding="utf-8").read())
except Exception as error:
    print("fake_useragent_list error: {}".format(error))
    fake_useragent_list = json.loads(open("./fake_useragent_0.1.11.json", "r", encoding="utf-8").read())


def get(api_url: str, method: str = "GET", params: dict = None, re_type: str = "html"):
    try:
        response = request(method=method, api_url=api_url, gbk=Vars.current_source.gbk_encoding, params=params)
        if re_type == "html":
            return etree.HTML(str(response.text))
        elif re_type == "json":
            return response.json()
        elif re_type == "text":
            return response.text
        elif re_type == "content":
            return response.content
    except Exception as e:
        log.logger("response is None, api_url is {}\t\terror:{}".format(api_url, e))


@retry(stop=stop_after_attempt(4))
def request(api_url: str, method: str = "GET", params: dict = None, gbk: bool = False):
    headers = {
        "User-Agent": random.choice(fake_useragent_list.get("browsers").get("chrome")),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    if Vars.current_book_type == "https://www.popo.tw":
        if Vars.cfg.data.popo_cookie == "":
            print("popo cookie is empty,you need to set it in config.json")
        else:
            headers["cookie"] = Vars.cfg.data.popo_cookie
    if method == "GET":
        response = session.request(url=api_url, method="GET", params=params, headers=headers)
    else:
        response = session.request(url=api_url, method=method, data=params, headers=headers)
    if gbk is True:
        response.encoding = 'gbk'
    else:
        response.encoding = 'utf-8'
    if response.status_code == 200:
        return response
