import re
import src
from lxml import etree
from tenacity import retry, stop_after_attempt


class XbookbenAPI:
    xbookben_host = "https://www.xbookben.net"
    book_info_by_book_id = "/txt/{}.html"
    book_info_by_keyword = "/search"

    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return etree.HTML(
            src.request(api_url=XbookbenAPI.xbookben_host + XbookbenAPI.book_info_by_book_id.format(book_id))
        )

    @staticmethod
    @retry(stop=stop_after_attempt(7))
    def get_chapter_info_by_chapter_id(chapter_url: str):
        return etree.HTML(src.request(api_url=XbookbenAPI.xbookben_host + chapter_url))

    @staticmethod
    def get_book_info_by_keyword(keyword: str):
        response = etree.HTML(src.request(
            method="POST", params={"searchkey": keyword},
            api_url=XbookbenAPI.xbookben_host + XbookbenAPI.book_info_by_keyword
        ))
        return list(zip(
            response.xpath(constant.rule.XbookbenRule.Search.book_name),
            response.xpath(constant.rule.XbookbenRule.Search.book_img),
            response.xpath(constant.rule.XbookbenRule.Search.book_id)
        ))


class LinovelAPI:
    linovel_host = "https://www.linovel.net"
    book_info_by_book_id = "/book/{}.html"
    book_info_by_keyword = "/search/"

    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return etree.HTML(src.request(LinovelAPI.linovel_host + LinovelAPI.book_info_by_book_id.format(book_id)))

    @staticmethod
    @retry(stop=stop_after_attempt(7))
    def get_chapter_info_by_chapter_id(chapter_url: str):
        return etree.HTML(src.request(api_url=LinovelAPI.linovel_host + chapter_url))

    @staticmethod
    def get_book_info_by_keyword(keyword: str, page: int = 1):
        params = {'kw': keyword} if page < 2 else {'kw': keyword, 'page': page, 'sort': 'hot', 'target': 'complex',
                                                   'mio': 1, 'ua': 'Mozilla/5.0'}
        response = src.request(api_url=LinovelAPI.linovel_host + LinovelAPI.book_info_by_keyword, params=params)
        return list(zip(
            etree.HTML(response).xpath(constant.rule.LinovelRule.Search.book_img),
            etree.HTML(response).xpath(constant.rule.LinovelRule.Search.book_name)
        ))


class DingdianAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return etree.HTML(src.request("https://www.ddyueshu.com/{}".format(book_id), gbk=True))

    @staticmethod
    @retry(stop=stop_after_attempt(7))
    def get_chapter_info_by_chapter_id(chapter_url):
        return etree.HTML(src.request(api_url='https://www.ddyueshu.com' + chapter_url, gbk=True))


class BiquPavilionAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id: str) -> [dict, None]:  # get book info from url by book_id
        response = src.request("https://infosxs.pigqq.com/BookFiles/Html/{}/info.html".format(book_id))
        if response is not None and isinstance(response, dict):  # if the response is not None and is a dict
            return response.get("data")  # get book info from response dict


def get_sort(tag_name: str, page: int, retry: int = 0):  # get sort from url by page
    params = {"sort": "words", "sign": "-1", "page": page}
    response = src.request(api_url="https://www.linovel.net/cat/-1.html", params=params)
    if isinstance(response, str):
        sort_html_list = etree.HTML(response).xpath('//a[@class="book-name"]')
        sort_info_list = [i.get('href').split('/')[-1][:-5] for i in sort_html_list]
        if sort_info_list and len(sort_info_list) != 0:
            return sort_info_list
    else:
        if retry <= 10:
            return get_sort(tag_name, page, retry + 1)
        return print("get sort failed, page is {}".format(page))


def search_book(book_name: str) -> [list, None]:
    response = src.request(api_url="https://www.linovel.net/search/", params={"kw": book_name})
    if response is not None and isinstance(response, str):
        html_str = response.split('<div class="rank-book-list">')[1]
        book_id_list = re.findall(r'<a href="/book/(\d+).html"', str(html_str))
        if len(book_id_list) != 0:
            return book_id_list
        else:
            return []
        # print(book_id)


def get_chapter_cover(html_string: [str, etree.ElementTree]) -> [list, None]:
    img_url_list = [
        img_url.get('src') for img_url in html_string.xpath('//div[@class="article-text"]//img')
    ]
    if isinstance(img_url_list, list) and len(img_url_list) != 0:
        return img_url_list
    else:
        return []
