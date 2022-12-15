from config import *
from lib import *

def get_web_url(url: str):
    if url[0] != "/":
        url = "/" + url
    return Vars.current_book_type + url.replace(Vars.current_book_type, "")


class Response:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        if Vars.current_book_type == "https://www.qbtr.cc":
            url = Vars.current_source.url.book_info.format(Vars.current_book_classify_name, book_id)
        elif Vars.current_book_type == "http://www.trxs.cc":
            url = Vars.current_source.url.book_info.format(Vars.current_book_classify_name, book_id)
        elif Vars.current_book_type == "https://www.xbiquge.la":
            url = Vars.current_source.url.book_info.format(book_id[:2], book_id)
        else:
            url = Vars.current_source.url.book_info.format(book_id)
        Vars.current_book_id = book_id
        return lib.utils.get(api_url=url)

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str):
        if Vars.current_book_type == "http://www.80zw.net":
            url = Vars.current_source.url.chapter_info.format(Vars.current_book.book_id, chapter_url)
        elif Vars.current_book_type == "https://www.qb5.la":
            url = Vars.current_source.url.chapter_info.format(Vars.current_book.book_id, chapter_url)
        else:
            url = Vars.current_source.url.chapter_info.format(chapter_url)
        result = lib.utils.get(api_url=url)
        return result

    @staticmethod
    def get_catalogue_info_by_book_id(book_id: str):
        return lib.utils.get(api_url=Vars.current_source.url.catalogue_info.format(book_id))

    @staticmethod
    def get_book_info_by_keyword(method: str, params: dict = None):
        response = lib.utils.get(method=method, params=params, api_url=Vars.current_source.url.search_info)
        # return list(zip(
        #     # response.xpath(Vars.current_book_rule.Search.book_name),
        #     # response.xpath(Vars.current_book_rule.Search.book_id)
        # ))
