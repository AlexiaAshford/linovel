from HttpUtil import *


def get_book_info(book_id: str, retry: int = 0) -> [dict, None]:  # get book info from url by book_id
    response = get(api_url="https://www.ddyueshu.com/" + book_id, retry=retry, gbk=True)
    if response is not None and isinstance(response, str):  # if the response is not None and is a string
        html_str = etree.HTML(response)  # parse html string to lxml.etree.ElementTree
        return book_info_json(
            book_id=book_id,
            book_name=html_str.xpath('//*[@id="info"]/h1')[0].text,
            author_name=html_str.xpath('//*[@id="info"]/p[1]')[0].text.split('：')[-1],
            chapter_url_list=[url for url in html_str.xpath('//*[@id="list"]/dl/dd[*]/a/@href')],
            cover_url='https://www.ddxstxt8.com' + html_str.xpath('//div[@id="fmimg"]/img')[0].get('src'),
        )  # return a dict with book info
    else:
        if retry <= 10 and response != 404:
            return get_book_info(book_id, retry + 1)
        return print("get book info failed, book_id is {}".format(book_id))


def get_chapter_info(chapter_url: str, index: int, content: str = "", retry: int = 0) -> [dict, None]:
    response = get(api_url="https://www.ddyueshu.com" + chapter_url, retry=retry, gbk=True)
    if response is not None and isinstance(response, str):
        for book in response.split('<div id="content">')[1].split("<script>")[0].split("<br />"):
            if book.strip() == "":
                continue
            if '请记住本书首发域名' in book or '书友大本营' in book:
                continue
            if book is not None and len(book.strip()) != 0:
                content += book.strip() + "\n"
        return chapter_info_json(
            index=index, url=chapter_url, content=content,
            title=etree.HTML(str(response)).xpath('//div[@class="bookname"]/h1')[0].text.strip()
        )  # get chapter info from html string and return a dict with chapter info

    else:
        if retry <= 10:
            return get_chapter_info(chapter_url, index, content, retry + 1)
        return print("get chapter info failed, chapter_url is {}".format(chapter_url))
