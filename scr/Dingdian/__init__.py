from HttpUtil import *


class DingdianAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id):
        return etree.HTML(get("https://www.ddyueshu.com/{}".format(book_id)))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url):
        return etree.HTML(get(api_url='https://www.ddyueshu.com' + chapter_url, retry=5, gbk=True))


def get_chapter_info(chapter_url: str, index: int, content: str = "", retry: int = 0) -> [dict, None]:
    response = DingdianAPI.get_chapter_info_by_chapter_id(chapter_url)
    title = response.xpath('//div[@class="bookname"]/h1/text()')[0].strip()
    for book in response.xpath('//*[@id="content"]/text()'):
        if book.strip() == "":
            continue
        if '请记住本书首发域名' in book or '书友大本营' in book:
            continue
        if book is not None and len(book.strip()) != 0:
            content += book.strip() + "\n"
    return chapter_info_json(index=index, url=chapter_url, content=content, title=title)
