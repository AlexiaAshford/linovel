from typing import Type
from src import BookAPI
import requests
from config import *
import constant
from tenacity import retry, stop_after_attempt
from fake_useragent import UserAgent


headers = {"user-agent": UserAgent().random}


@retry(stop=stop_after_attempt(5))
def request(api_url: str, method: str = "GET", params: dict = None, gbk: bool = False, return_type: str = "text"):
    if method == "GET":
        response = requests.request(url=api_url, method="GET", params=params, headers=headers)
    else:
        response = requests.request(url=api_url, method=method, data=params, headers=headers)

    if gbk is True:
        response.encoding = 'gbk'
    else:
        response.encoding = 'utf-8'

    if response.status_code == 200:
        if return_type == "json":
            return response.json()
        elif return_type == "text":
            return response.text
        elif return_type == "content":
            return response.content
    else:
        raise Exception("[error] status code is not 200, status code is {}".format(response.status_code))


def get_book_information(book_id: str):
    if Vars.current_book_type == "Xbookben":
        book_rule: Type["constant.rule.XbookbenRule"] = constant.rule.XbookbenRule
        result_etree = BookAPI.XbookbenAPI.get_book_info_by_book_id(book_id)
    elif Vars.current_book_type == "Dingdian":
        book_rule: Type["constant.rule.DingdianRule"] = constant.rule.DingdianRule
        result_etree = BookAPI.DingdianAPI.get_book_info_by_book_id(book_id)
    elif Vars.current_book_type == "Linovel":
        book_rule: Type["constant.rule.LinovelRule"] = constant.rule.LinovelRule
        result_etree = BookAPI.LinovelAPI.get_book_info_by_book_id(book_id)
    elif Vars.current_book_type == "sfacg":
        book_rule: Type["constant.rule.BoluobaoRule"] = constant.rule.BoluobaoRule
        result_etree = BookAPI.BoluobaoAPI.get_book_info_by_book_id(book_id)
    else:
        raise Exception("[error] app type not found, app type:", Vars.current_book_type)

    book_id = book_id
    book_img = result_etree.xpath(book_rule.book_img)
    book_name = result_etree.xpath(book_rule.book_name)
    book_author = result_etree.xpath(book_rule.book_author)
    book_state = result_etree.xpath(book_rule.book_state)
    book_label = result_etree.xpath(book_rule.book_label)
    last_chapter_title = result_etree.xpath(book_rule.last_chapter_title)
    book_words = result_etree.xpath(book_rule.book_words)
    book_update_time = result_etree.xpath(book_rule.book_update_time)
    if Vars.current_book_type == "sfacg":
        catalogue = BookAPI.BoluobaoAPI.get_catalogue_info_by_book_id(book_id)
        chapter_url_list = [i for i in catalogue.xpath(book_rule.chapter_url_list)]
    else:
        chapter_url_list = [i for i in result_etree.xpath(book_rule.chapter_url_list)]

    return constant.json.book_json(
        book_id=book_id,
        book_name=book_name[0] if len(book_name) > 0 else "",
        book_words=book_words[0] if book_words else None,
        cover_url=book_img[0] if book_img else None,
        author_name=book_author[0] if book_author else None,
        book_status=book_state[0] if book_state else None,
        book_tag=book_label[0] if book_label else None,
        last_chapter_title=last_chapter_title[0] if last_chapter_title else None,
        book_uptime=book_update_time[0] if book_update_time else None,
        chapter_url_list=chapter_url_list if chapter_url_list else []
    )
