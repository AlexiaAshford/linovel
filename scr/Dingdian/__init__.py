from HttpUtil import *


class DingdianAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id):
        return etree.HTML(get("https://www.ddyueshu.com/{}".format(book_id)))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url):
        return etree.HTML(get(api_url='https://www.ddyueshu.com' + chapter_url, retry=5, gbk=True))

