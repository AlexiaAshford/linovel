import src.http_utils
from config import *


def get_web_url(url: str):
    if url[0] != "/":
        url = "/" + url
    return Vars.current_book_type + url.replace(Vars.current_book_type, "")


class Response:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        if Vars.current_book_type == "https://www.qbtr.cc":
            url = Vars.current_book_rul_rule.get("book_info").format(Vars.current_book_classify_name, book_id)
        elif Vars.current_book_type == "http://www.trxs.cc":
            url = Vars.current_book_rul_rule.get("book_info").format(Vars.current_book_classify_name, book_id)
        else:
            url = Vars.current_book_rul_rule.get("book_info").format(book_id)
        return src.http_utils.get(api_url=url, gbk=Vars.current_book_gbk)

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str):
        if Vars.current_book_type == "http://www.80zw.net":
            url = Vars.current_book_rul_rule.get("chapter_info").format(Vars.current_book.book_id, chapter_url)
        else:
            url = Vars.current_book_rul_rule.get("chapter_info").format(chapter_url)
        return src.http_utils.get(api_url=url, gbk=Vars.current_book_gbk)

    @staticmethod
    def get_catalogue_info_by_book_id(book_id: str):
        url = Vars.current_book_rul_rule.get("catalogue_info").format(book_id)
        return src.http_utils.get(api_url=url, gbk=Vars.current_book_gbk)

    @staticmethod
    def get_book_info_by_keyword(method: str, params: dict):
        response = src.http_utils.get(
            method=method, params=params, api_url=Vars.current_book_rul_rule.get("search_info"),
            gbk=Vars.current_book_gbk
        )
        return list(zip(
            response.xpath(Vars.current_book_rule.Search.book_name),
            response.xpath(Vars.current_book_rule.Search.book_id)
        ))


# class ResponseAPI:
#     class Xbookben:
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/txt/{}.html".format(book_id)))
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url: str):
#             return src.http_utils.get(api_url=get_web_url(chapter_url))
#
#         @staticmethod
#         def get_book_info_by_keyword(keyword: str):
#             response = src.http_utils.get(method="POST", params={"searchkey": keyword}, api_url=get_web_url("/search"))
#             return list(zip(
#                 response.xpath(Vars.current_book_rule.Search.book_name),
#                 response.xpath(Vars.current_book_rule.Search.book_id)
#             ))
#
#     class Linovel:
#
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/book/{}.html".format(book_id)))
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url: str):
#             return src.http_utils.get(api_url=get_web_url(chapter_url))
#
#         @staticmethod
#         def get_book_info_by_keyword(keyword: str, page: int = 1):
#             params = {'kw': keyword}
#             if page > 1:
#                 params.update({'page': page, 'sort': 'hot', 'target': 'complex', 'mio': 1, 'ua': 'Mozilla/5.0'})
#             response = src.http_utils.get(api_url=get_web_url("/search/"), params=params)  # get search result page
#             return list(zip(
#                 response.xpath(Vars.current_book_rule.Search.book_img),
#                 response.xpath(Vars.current_book_rule.Search.book_name),
#                 response.xpath(Vars.current_book_rule.Search.book_id)
#             ))
#
#     class Dingdian:
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url(book_id), gbk=True)
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url):
#             return src.http_utils.get(api_url=get_web_url(chapter_url), gbk=True)
#
#     class Boluobao:
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/Novel/{}/".format(book_id)))
#
#         @staticmethod
#         def get_catalogue_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/Novel/{}/MainIndex/".format(book_id)))
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url: str):
#             return src.http_utils.get(api_url=get_web_url(chapter_url))
#
#         @staticmethod
#         def get_book_info_by_keyword(keyword: str):
#             response = src.http_utils.get(params={"Key": keyword, "S": 1, "SS": 0}, api_url="https://s.sfacg.com/")
#             # print(response.xpath(Vars.current_book_rule.Search.book_id))
#             # for i in response.xpath(Vars.current_book_rule.Search.book_id):
#             #     print(i)
#             return list(zip(
#                 response.xpath(Vars.current_book_rule.Search.book_img),
#                 response.xpath(Vars.current_book_rule.Search.book_name),
#                 response.xpath(Vars.current_book_rule.Search.book_id)
#             ))
#
#     class Biquge:
#
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/booktxt/" + book_id), gbk=True)
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url: str):
#             return src.http_utils.get(api_url=get_web_url(chapter_url), gbk=True)
#
#     class Baling:
#
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/article/" + book_id), gbk=True)
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url: str):
#             return src.http_utils.get(
#                 api_url=get_web_url("/article/{}/{}".format(Vars.current_book.book_id, chapter_url)), gbk=True)
#
#     class Qbtr:
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(
#                 api_url=get_web_url("/{}/{}.html".format(Vars.current_book_classify_name, book_id)), gbk=True)
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url: str):
#             return src.http_utils.get(api_url=get_web_url(chapter_url), gbk=True)
#
#     class Trxs:
#
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(
#                 api_url=get_web_url("/{}/{}.html".format(Vars.current_book_classify_name, book_id)), gbk=True)
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url: str):
#             return src.http_utils.get(api_url=get_web_url(chapter_url), gbk=True)
#
#     class Popo:
#
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/books/" + book_id))
#
#         @staticmethod
#         def get_catalogue_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/books/{}/articles".format(book_id)))
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url: str):
#             return src.http_utils.get(api_url=get_web_url(chapter_url))
#
#     class Linovelib:
#
#         @staticmethod
#         def get_book_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/novel/{}.html".format(book_id)))
#
#         @staticmethod
#         def get_catalogue_info_by_book_id(book_id: str):
#             return src.http_utils.get(api_url=get_web_url("/novel/{}/catalog".format(book_id)))
#
#         @staticmethod
#         def get_chapter_info_by_chapter_id(chapter_url: str):
#             return src.http_utils.get(api_url=get_web_url(chapter_url))
