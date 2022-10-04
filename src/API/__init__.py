from lxml import etree
from .. import request
from config import *
import logging

logging.basicConfig(
    filename="logfile.log",
    filemode="w",
    format="%(levelname)s %(asctime)s - %(message)s",
    level=logging.ERROR
)

logger = logging.getLogger()


def get(api_url: str, method: str = "GET", gbk: bool = False, params: dict = None, re_type: str = "html"):
    try:
        response = request(method=method, api_url=api_url, gbk=gbk, params=params)
        if re_type == "html":
            return etree.HTML(str(response.text))
        elif re_type == "json":
            return response.json()
        elif re_type == "text":
            return response.text
        elif re_type == "content":
            return response.content
    except Exception as error:
        logger.error("response is None, api_url is {}\t\terror:{}".format(api_url, error))


class Site:  # 站点类 用于存储站点信息
    class Boluobao:
        host = "https://book.sfacg.com"
        book_info_by_book_id = host + "/Novel/{}/"
        catalogue_info_by_book_id = host + "/Novel/{}/MainIndex/"
        book_info_by_keyword = "https://s.sfacg.com/"

    class Baling:
        host = "http://www.80zw.net"
        book_info_by_book_id = host + "/article/"
        book_info_by_chapter_id = host + "/article/{}/{}"

    class Qbtr:
        host = "https://www.qbtr.cc"
        book_info_by_book_id = host + "/changgui/{}.html"  # 书籍信息

    class Trxs:
        host = "http://trxs.cc"
        book_info_by_book_id = host + "/tongren/{}.html"  # 书籍信息

    class Popo:
        host = "https://www.popo.tw"
        book_info_by_book_id = host + "/books/"  # 书籍信息
        catalogue_info_by_book_id = host + "/books/{}/articles"  # 书籍信息

    class Linovelib:
        host = "https://www.linovelib.com"
        book_info_by_book_id = host + "/novel/{}.html"  # 书籍信息
        catalogue_info_by_book_id = host + "/novel/{}/catalog"  # 书籍信息


def get_web_url(url: str):
    if url[0] != "/":
        url = "/" + url
    return Vars.current_book_type + url.replace(Vars.current_book_type, "")


class ResponseAPI:
    class Xbookben:
        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=get_web_url("/txt/{}.html".format(book_id)))

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=get_web_url(chapter_url))

        @staticmethod
        def get_book_info_by_keyword(keyword: str):
            response = get(method="POST", params={"searchkey": keyword}, api_url=get_web_url("/search"))
            return list(zip(
                response.xpath(Vars.current_book_rule.Search.book_img),
                response.xpath(Vars.current_book_rule.Search.book_name),
                response.xpath(Vars.current_book_rule.Search.book_id)
            ))

    class Linovel:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=get_web_url("/book/{}.html".format(book_id)))

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=get_web_url(chapter_url))

        @staticmethod
        def get_book_info_by_keyword(keyword: str, page: int = 1):
            params = {'kw': keyword}
            if page > 1:
                params.update({'page': page, 'sort': 'hot', 'target': 'complex', 'mio': 1, 'ua': 'Mozilla/5.0'})
            response = get(api_url=get_web_url("/search/"), params=params)  # get search result page
            return list(zip(
                response.xpath(Vars.current_book_rule.Search.book_img),
                response.xpath(Vars.current_book_rule.Search.book_name),
                response.xpath(Vars.current_book_rule.Search.book_id)
            ))

    class Dingdian:
        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=get_web_url(book_id), gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url):
            return get(api_url=get_web_url(chapter_url), gbk=True)

    class Boluobao:
        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=Site.Boluobao.book_info_by_book_id.format(book_id))

        @staticmethod
        def get_catalogue_info_by_book_id(book_id: str):
            return get(api_url=Site.Boluobao.catalogue_info_by_book_id.format(book_id))

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=Site.Boluobao.host + chapter_url)

        @staticmethod
        def get_book_info_by_keyword(keyword: str):
            response = get(params={"Key": keyword, "S": 1, "SS": 0},
                           api_url=Site.Boluobao.book_info_by_keyword)
            print(response.xpath(Vars.current_book_rule.Search.book_id))
            for i in response.xpath(Vars.current_book_rule.Search.book_id):
                print(i)
            return list(zip(
                response.xpath(Vars.current_book_rule.Search.book_img),
                response.xpath(Vars.current_book_rule.Search.book_name),
                response.xpath(Vars.current_book_rule.Search.book_id)
            ))

    class Biquge:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=get_web_url("/booktxt/" + book_id), gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=get_web_url(chapter_url), gbk=True)

    class Baling:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=Site.Baling.book_info_by_book_id + book_id, gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            api_url = Site.Baling.book_info_by_chapter_id
            return get(api_url=api_url.format(Vars.current_book.book_id, chapter_url), gbk=True)

    class Qbtr:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=Site.Qbtr.book_info_by_book_id.format(book_id), gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=Site.Qbtr.host + chapter_url, gbk=True)

    class Trxs:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=Site.Trxs.book_info_by_book_id.format(book_id), gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=Site.Trxs.host + chapter_url, gbk=True)

    class Popo:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=Site.Popo.book_info_by_book_id + book_id)

        @staticmethod
        def get_catalogue_info_by_book_id(book_id: str):
            return get(api_url=Site.Popo.catalogue_info_by_book_id.format(book_id))

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=Site.Popo.host + chapter_url)

    class Linovelib:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=Site.Linovelib.book_info_by_book_id.format(book_id))

        @staticmethod
        def get_catalogue_info_by_book_id(book_id: str):
            return get(api_url=Site.Linovelib.catalogue_info_by_book_id.format(book_id))

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=Site.Linovelib.host + chapter_url)
