import re
from lxml import etree
import src
from tenacity import retry, stop_after_attempt


class XbookbenAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return etree.HTML(src.request(api_url="https://www.xbookben.net/txt/{}.html".format(book_id)))

    @staticmethod
    @retry(stop=stop_after_attempt(7))
    def get_chapter_info_by_chapter_id(chapter_url: str):
        response = etree.HTML(src.request(api_url="https://www.xbookben.net" + chapter_url))

    @staticmethod
    def get_book_info_by_keyword(keyword: str):
        response = etree.HTML(src.request(
            method="POST", api_url="https://www.xbookben.net/search", params={"searchkey": keyword}
        ))
        search_result = list(
            zip(response.xpath('//*[@id="hism"]/a/img/@alt'), response.xpath('//*[@id="hism"]/a/img/@src'),
                response.xpath('//*[@id="hism"]/h3/a/@href'))
        )
        return search_result


class LinovelAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return etree.HTML(src.request("https://www.linovel.net/book/{}.html".format(book_id)))

    @staticmethod
    @retry(stop=stop_after_attempt(7))
    def get_chapter_info_by_chapter_id(chapter_url: str):
        return etree.HTML(src.request(api_url="https://www.linovel.net" + chapter_url))

    @staticmethod
    def get_book_info_by_keyword(keyword: str, page: int = 1):
        """kw: 神
        page: 2
        sort: hot
        target: complex
        mio: 1
        ua: Mozilla/5.0"""
        # params = {''
        response = etree.HTML(src.request(api_url="https://www.linovel.net/search/", params={"kw": keyword}))
        '/html/body/div[4]/div[3]/div[1]/a[1]/div/div[1]/img'
        '/html/body/div[4]/div[3]/div[1]/a[1]'
        search_result = list(
            zip(response.xpath('/html/body/div[4]/div[3]/div[1]/a/div/div/img/@src'),
                response.xpath('/html/body/div[4]/div[3]/div[1]/a/div/div/img/@alt'))
        )
        return search_result


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
