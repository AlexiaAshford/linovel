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

