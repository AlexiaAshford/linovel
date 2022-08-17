from HttpUtil import *
from src import rule


def get_book_info(novel_id: str, retry: int = 0) -> [dict, None]:  # get book info from url by book_id
    response = get("https://infosxs.pigqq.com/BookFiles/Html/{}/info.html".format(novel_id), return_type="json")
    if response is not None and isinstance(response, dict):  # if the response is not None and is a dict
        book_info = response.get("data")  # get book info from response dict
        return rule.book_json(
            book_id=book_info["Id"],
            book_name=book_info["Name"],
            author_name=book_info["Author"],
            book_tag=book_info["CName"],
            book_intro=book_info["Desc"],
            book_status=book_info["BookStatus"],
            cover_url=book_info["Img"],
            chapter_url_list=Book.catalogue(book_info["Id"]),
        )  # get book info from html string and return a dict with book info
    else:
        if retry <= 10 and response != 404:
            return get_book_info(novel_id, retry + 1)  # if the response is None or is not a dict, retry
        return print("get book info failed, book_id is {}".format(novel_id))  # if response is not a dict


class Book:

    @staticmethod
    def catalogue(novel_id: str):
        response = get("https://infosxs.pigqq.com/BookFiles/Html/{}/index.html".format(novel_id))
        if response is not None and response.get('info') == 'success':
            print(response.get('data').get('list'))
            return response.get('data').get('list')

    @staticmethod
    def search(book_name: str, page: int = 1):
        params = {"key": book_name, "page": page, "siteid": "app2"}
        response = get("https://souxs.pigqq.com/search.aspx", params=params)
        if response is not None and response.get('info') == 'success':
            return response.get('data')


class Chapter:
    @staticmethod
    def content(book_id: str, chapter_id: str):
        response = get("https://contentxs.pigqq.com/BookFiles/Html/{}/{}.html".format(book_id, chapter_id))
        if response is not None and response.get('info') == 'success':
            return response.get('data')


class Cover:
    @staticmethod
    def download_cover(url: str, params: dict = None) -> bytes:
        response = get(url, params=params)
        if response is not None:
            return response.content
