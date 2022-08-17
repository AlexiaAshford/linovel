from HttpUtil import *


class XbookbenAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id):
        return etree.HTML(get("https://www.xbookben.net/txt/{}.html".format(book_id)))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url, retry: int = 0):
        response = get(api_url="https://www.xbookben.net" + chapter_url, retry=5)
        if isinstance(response, str):
            return etree.HTML(response)
        else:
            if retry <= 10:
                return XbookbenAPI.get_chapter_info_by_chapter_id(chapter_url, retry + 1)
            return print("get chapter info failed, chapter_url is {}".format(chapter_url))


class LinovelAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return etree.HTML(get("https://www.linovel.net/book/{}.html".format(book_id)))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str, retry: int = 0):
        response = get(api_url="https://www.linovel.net" + chapter_url, retry=5)
        if isinstance(response, str):
            return etree.HTML(response)
        else:
            if retry <= 10:
                return LinovelAPI.get_chapter_info_by_chapter_id(chapter_url, retry + 1)
            return print("get chapter info failed, chapter_url is {}".format(chapter_url))

    @staticmethod
    def get_book_info_by_keyword(keyword: str):
        return etree.HTML(get(api_url="https://www.linovel.net/search/", params={"kw": keyword}))


class DingdianAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id):
        return etree.HTML(get("https://www.ddyueshu.com/{}".format(book_id)))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url):
        return etree.HTML(get(api_url='https://www.ddyueshu.com' + chapter_url, retry=5, gbk=True))
