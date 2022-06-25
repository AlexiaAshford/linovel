import time
from lxml import etree
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.114 Safari/537.36 "
}


def get(api_url: str, param: dict = None, retry: int = 0) -> [str, None, int]:
    if retry >= 5:
        time.sleep(retry * 0.5)
        print("retry is {}, sleep time is:[{}] url:{}".format(retry, int(retry * 0.5), api_url))
    response = requests.get("https://www.ddyueshu.com" + api_url, params=param, headers=headers)
    response.encoding = 'gbk'
    if response.status_code == 404:
        return 404
    return response.text if response.status_code == 200 else None


def post(api_url: str, data: dict = None, retry: int = 0, max_retries: int = 3):
    response = requests.post(api_url, data=data, headers=headers)
    response.encoding = 'gbk'
    if response.status_code == 200:
        return response.text
    if retry <= max_retries:
        post(api_url=api_url, data=data, retry=retry + 1, max_retries=max_retries - 1)
    else:
        print("retry is over, status code is {}".format(response.status_code))


def get_book_info(book_id: str, retry: int = 0) -> [dict, None]:  # get book info from url by book_id
    response = get(api_url="/" + book_id, retry=retry)
    if response is not None and isinstance(response, str):  # if the response is not None and is a string
        html_str = etree.HTML(response)  # parse html string to lxml.etree.ElementTree
        book_info = {
            "bookId": book_id,
            "bookName": html_str.xpath('//*[@id="info"]/h1')[0].text,
            "authorName": html_str.xpath('//*[@id="info"]/p[1]')[0].text.split('：')[-1],
            "bookCoverUrl": 'https://www.ddxstxt8.com' + html_str.xpath('//div[@id="fmimg"]/img')[0].get('src'),
            "chapUrl": [url for url in html_str.xpath('//*[@id="list"]/dl/dd[*]/a/@href')]
        }  # get book info from html string and return a dict with book info
        return book_info  # return a dict with book info
    else:
        if retry <= 10 and response != 404:
            return get_book_info(book_id, retry + 1)
        return print("get book info failed, book_id is {}".format(book_id))


def get_chapter_info(chapter_url: str, index: int, content: str = "", retry: int = 0) -> [dict, None]:
    response = get(api_url=chapter_url, retry=retry)
    if response is not None and isinstance(response, str):
        # content_string = etree.HTML(str(response))
        for book in response.split('<div id="content">')[1].split("<script>")[0].split("<br />"):
            if book.strip() == "":
                continue
            if '请记住本书首发域名' in book or '书友大本营' in book:
                continue
            if book is not None and len(book.strip()) != 0:
                content += book.strip() + "\n"
        return {
            "chapterIndex": index,
            "chapter_url": chapter_url,
            "chapterTitle": etree.HTML(str(response)).xpath('//div[@class="bookname"]/h1')[0].text.strip(),
            "chapterContent": content,
            "imageList": "no chapter png"
        }
    else:
        if retry <= 10:
            return get_chapter_info(chapter_url, index, content, retry + 1)
        return print("get chapter info failed, chapter_url is {}".format(chapter_url))
