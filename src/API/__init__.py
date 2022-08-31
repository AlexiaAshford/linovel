import constant
from lxml import etree
from .. import request
from tenacity import *
from config import *


@retry(stop=stop_after_attempt(7), wait=wait_fixed(0.1))
def get(api_url: str, method: str = "GET", gbk: bool = False, params: dict = None, re_type: str = "html"):
    response = request(method=method, api_url=api_url, gbk=gbk, params=params)
    if re_type == "html":
        return etree.HTML(str(response.text))
    elif re_type == "json":
        return response.json()
    elif re_type == "text":
        return response.text
    elif re_type == "content":
        return response.content
    else:
        raise Exception("[error] re_type is not html, json, text, content")


class XbookbenAPI:

    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return get(api_url=constant.url.Site.Xbookben.book_info_by_book_id.format(book_id))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str):
        return get(api_url=constant.url.Site.Xbookben.host + chapter_url)

    @staticmethod
    def get_book_info_by_keyword(keyword: str):
        response = get(
            method="POST", params={"searchkey": keyword},
            api_url=constant.url.Site.Xbookben.book_info_by_keyword
        )
        return list(zip(
            response.xpath(constant.rule.XbookbenRule.Search.book_name),
            response.xpath(constant.rule.XbookbenRule.Search.book_img),
            response.xpath(constant.rule.XbookbenRule.Search.book_id)
        ))


class LinovelAPI:

    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return get(constant.url.Site.Linovel.book_info_by_book_id.format(book_id))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str):
        return get(api_url=constant.url.Site.Linovel.host + chapter_url)

    @staticmethod
    def get_book_info_by_keyword(keyword: str, page: int = 1):
        params = {'kw': keyword} if page < 2 else {
            'kw': keyword, 'page': page, 'sort': 'hot', 'target': 'complex', 'mio': 1, 'ua': 'Mozilla/5.0'}
        response = get(api_url=constant.url.Site.Linovel.book_info_by_keyword, params=params)
        return list(zip(
            response.xpath(constant.rule.LinovelRule.Search.book_img),
            response.xpath(constant.rule.LinovelRule.Search.book_name)
        ))


class DingdianAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return get(api_url=constant.url.Site.Dingdian.host + book_id, gbk=True)

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url):
        return get(api_url=constant.url.Site.Dingdian.host + chapter_url, gbk=True)


class BoluobaoAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return get(api_url=constant.url.Site.Boluobao.book_info_by_book_id.format(book_id))

    @staticmethod
    def get_catalogue_info_by_book_id(book_id: str):
        return get(api_url=constant.url.Site.Boluobao.catalogue_info_by_book_id.format(book_id))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str):
        return get(api_url=constant.url.Site.Boluobao.host + chapter_url)

    @staticmethod
    def get_book_info_by_keyword(keyword: str, page: int = 1):
        params = {'kw': keyword} if page < 2 else {
            'kw': keyword, 'page': page, 'sort': 'hot', 'target': 'complex', 'mio': 1, 'ua': 'Mozilla/5.0'}
        response = get(api_url=constant.url.Site.Boluobao.book_info_by_keyword, params=params)
        return list(zip(
            response.xpath(constant.rule.BoluobaoRule.Search.book_img),
            response.xpath(constant.rule.BoluobaoRule.Search.book_name)
        ))


class BiqugeAPI:

    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return get(api_url=constant.url.Site.Biquge.book_info_by_book_id + book_id, gbk=True)

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str):
        return get(api_url=constant.url.Site.Biquge.host + chapter_url, gbk=True)


class BalingAPI:

    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return get(api_url=constant.url.Site.Baling.book_info_by_book_id + book_id, gbk=True)

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str):
        api_url = constant.url.Site.Baling.book_info_by_chapter_id
        return get(api_url=api_url.format(Vars.current_book.book_id, chapter_url), gbk=True)


def get_chapter_cover(html_string) -> [list, None]:
    img_url_list = [
        img_url.get('src') for img_url in html_string.xpath('//div[@class="article-text"]//img')
    ]
    if isinstance(img_url_list, list) and len(img_url_list) != 0:
        return img_url_list
    else:
        return []
