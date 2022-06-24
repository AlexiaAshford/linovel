import time

from LinovelAPI.tool import *
import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.114 Safari/537.36 "
}


def get(api_url: str, param: dict = None, retry: int = 0) -> [str, None]:
    if retry >= 5:
        time.sleep(retry * 0.5)
        print("retry is {}, sleep time is:[{}] url:{}".format(retry, int(retry * 0.5), api_url))
    response = requests.get("https://www.linovel.net" + api_url, params=param, headers=headers)
    return response.text if response.status_code == 200 else None


def post(api_url: str, data: dict = None, retry: int = 0, max_retries: int = 3):
    response = requests.post(api_url, data=data, headers=headers)
    if response.status_code == 200:
        return response.text
    if retry <= max_retries:
        post(api_url=api_url, data=data, retry=retry + 1, max_retries=max_retries - 1)
    else:
        print("retry is over, status code is {}".format(response.status_code))


def get_book_info(book_id: str, retry: int = 0) -> [dict, None]:  # get book info from url by book_id
    response = get(api_url="/book/{}.html#catalog".format(book_id), retry=retry)
    if response is not None and isinstance(response, str):  # if the response is not None and is a string
        html_str = etree.HTML(response)  # parse html string to lxml.etree.ElementTree
        book_info = {
            "bookName": html_str.xpath('//h1[@class="book-title"]')[0].text,
            "authorName": html_str.xpath('//div[@class="author-frame"]//a')[0].text,
            "bookCoverUrl": html_str.xpath('//div[@class="book-cover"]/a')[0].get('href'),
            "chapUrl": [i.get('href') for i in html_str.xpath('//div[@class="chapter"]/a')]
        }  # get book info from html string and return a dict with book info
        return book_info  # return a dict with book info
    else:
        if retry <= 10:
            return get_book_info(book_id, retry + 1)
        return print("get book info failed, book_id is {}".format(book_id))


def get_chapter_info(chapter_url: str, index: int, content: str = "", retry: int = 0) -> [dict, None]:
    response = get(api_url=chapter_url, retry=retry)
    if response is not None and isinstance(response, str):
        content_string = etree.HTML(response)
        for book in content_string.xpath('//div[@class="article-text"]/p'):
            if book.text is not None and len(book.text.strip()) != 0:
                content += book.text.strip() + "\n"
        return {
            "chapterIndex": index,
            "chapter_url": chapter_url,
            "chapterTitle": content_string.xpath('//div[@class="article-title"]')[0].text.strip(),
            "chapterContent": content
        }
    else:
        if retry <= 10:
            return get_chapter_info(chapter_url, index, content, retry + 1)
        return print("get chapter info failed, chapter_url is {}".format(chapter_url))


def get_sort(page: int, retry: int = 0):  # get sort from url by page
    response = get(api_url="/cat/-1.html?sort=words&sign=-1&page={}".format(page), retry=retry)
    if response is not None and isinstance(response, str):
        sort_list = [i.get('href').split('/')[-1][:-5] for i in etree.HTML(response).xpath('//a[@class="book-name"]')]
        if len(sort_list) != 0:
            return sort_list
    else:
        if retry <= 10:
            return get_sort(page, retry + 1)
        return print("get sort failed, page is {}".format(page))
