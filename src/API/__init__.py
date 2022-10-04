import constant
from lxml import etree
from .. import request
from config import *
import logging

# Creating and Configuring Logger

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    filename="logfile.log",
    filemode="w",
    format=Log_Format,
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


class ResponseAPI:
    @staticmethod
    def set_up_web( ):
        if Vars.current_book_type == "Dingdian":
            book_api = ResponseAPI.Dingdian
        elif Vars.current_book_type == "Xbookben":
            book_api = ResponseAPI.Xbookben
        elif Vars.current_book_type == "Linovel":
            book_api = ResponseAPI.Linovel
        elif Vars.current_book_type == "sfacg":
            book_api = ResponseAPI.Boluobao
        elif Vars.current_book_type == "Biquge":
            book_api = ResponseAPI.Biquge
        elif Vars.current_book_type == "Baling":
            book_api = ResponseAPI.Baling
        elif Vars.current_book_type == "Qbtr":
            book_api = ResponseAPI.Qbtr
        elif Vars.current_book_type == "Trxs":
            book_api = ResponseAPI.Trxs
        elif Vars.current_book_type == "popo":
            book_api = ResponseAPI.Popo
        elif Vars.current_book_type == "bilibili":
            book_api = ResponseAPI.Linovelib
        else:
            raise "Error: current_book_type is not in Xbookben, Dingdian, Linovel, sfacg, Biquge, Baling"
        return book_api

    class Xbookben:
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
                response.xpath(Vars.current_book_rule.Search.book_img),
                response.xpath(Vars.current_book_rule.Search.book_name),
                response.xpath(Vars.current_book_rule.Search.book_id)
            ))

    class Linovel:

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
                response.xpath(Vars.current_book_rule.Search.book_img),
                response.xpath(Vars.current_book_rule.Search.book_name),
                response.xpath(Vars.current_book_rule.Search.book_id)
            ))

    class Dingdian:
        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=constant.url.Site.Dingdian.host + book_id, gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url):
            return get(api_url=constant.url.Site.Dingdian.host + chapter_url, gbk=True)

    class Boluobao:
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
        def get_book_info_by_keyword(keyword: str):
            response = get(params={"Key": keyword, "S": 1, "SS": 0},
                           api_url=constant.url.Site.Boluobao.book_info_by_keyword)
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
            return get(api_url=constant.url.Site.Biquge.book_info_by_book_id + book_id, gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=constant.url.Site.Biquge.host + chapter_url, gbk=True)

    class Baling:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=constant.url.Site.Baling.book_info_by_book_id + book_id, gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            api_url = constant.url.Site.Baling.book_info_by_chapter_id
            return get(api_url=api_url.format(Vars.current_book.book_id, chapter_url), gbk=True)

    class Qbtr:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=constant.url.Site.Qbtr.book_info_by_book_id.format(book_id), gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=constant.url.Site.Qbtr.host + chapter_url, gbk=True)

    class Trxs:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=constant.url.Site.Trxs.book_info_by_book_id.format(book_id), gbk=True)

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=constant.url.Site.Trxs.host + chapter_url, gbk=True)

    class Popo:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=constant.url.Site.Popo.book_info_by_book_id + book_id)

        @staticmethod
        def get_catalogue_info_by_book_id(book_id: str):
            return get(api_url=constant.url.Site.Popo.catalogue_info_by_book_id.format(book_id))

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=constant.url.Site.Popo.host + chapter_url)

    class Linovelib:

        @staticmethod
        def get_book_info_by_book_id(book_id: str):
            return get(api_url=constant.url.Site.Linovelib.book_info_by_book_id.format(book_id))

        @staticmethod
        def get_catalogue_info_by_book_id(book_id: str):
            return get(api_url=constant.url.Site.Linovelib.catalogue_info_by_book_id.format(book_id))

        @staticmethod
        def get_chapter_info_by_chapter_id(chapter_url: str):
            return get(api_url=constant.url.Site.Linovelib.host + chapter_url)
