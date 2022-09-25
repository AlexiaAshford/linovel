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


class ResponseAPI:
    @staticmethod
    def set_up_web(current_book_type: str):
        if current_book_type == "Dingdian" or current_book_type == "d":
            book_api = ResponseAPI.Dingdian
        elif current_book_type == "Xbookben" or current_book_type == "x":
            book_api = ResponseAPI.Xbookben
        elif current_book_type == "Linovel" or current_book_type == "l":
            book_api = ResponseAPI.Linovel
        elif current_book_type == "sfacg" or current_book_type == "s":
            book_api = ResponseAPI.Boluobao
        elif current_book_type == "Biquge" or current_book_type == "b":
            book_api = ResponseAPI.Biquge
        elif current_book_type == "Baling" or current_book_type == "bl":
            book_api = ResponseAPI.Baling
        elif current_book_type == "Qbtr" or current_book_type == "q":
            book_api = ResponseAPI.Qbtr
        elif current_book_type == "Trxs" or current_book_type == "t":
            book_api = ResponseAPI.Trxs
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
