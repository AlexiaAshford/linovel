import re
from lxml import etree
import src


class XbookbenAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id):
        return etree.HTML(src.request(api_url="https://www.xbookben.net/txt/{}.html".format(book_id)))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url, retry: int = 0):
        response = src.request(api_url="https://www.xbookben.net" + chapter_url)
        if isinstance(response, str):
            return etree.HTML(response)
        else:
            if retry <= 10:
                return XbookbenAPI.get_chapter_info_by_chapter_id(chapter_url, retry + 1)
            return print("get chapter info failed, chapter_url is {}".format(chapter_url))


class LinovelAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return etree.HTML(src.request("https://www.linovel.net/book/{}.html".format(book_id)))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str, retry: int = 0):
        response = src.request(api_url="https://www.linovel.net" + chapter_url)
        if isinstance(response, str):
            return etree.HTML(response)
        else:
            if retry <= 10:
                return LinovelAPI.get_chapter_info_by_chapter_id(chapter_url, retry + 1)
            return print("get chapter info failed, chapter_url is {}".format(chapter_url))

    @staticmethod
    def get_book_info_by_keyword(keyword: str):
        return etree.HTML(src.request(api_url="https://www.linovel.net/search/", params={"kw": keyword}))


class DingdianAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id):
        return etree.HTML(src.request("https://www.ddyueshu.com/{}".format(book_id), gbk=True))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url):
        return etree.HTML(src.request(api_url='https://www.ddyueshu.com' + chapter_url, gbk=True))


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
