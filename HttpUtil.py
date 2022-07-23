import time
import requests
from config import *
from lxml import etree


def get(
        api_url: str,
        params: dict = None,
        retry: int = 0,
        gbk: bool = False,
        max_retries: int = 5,
        return_type: str = "text"
) -> [str, dict, int, None]:
    try:
        response = requests.get(api_url, params=params, headers=Vars.cfg.data['user_agent'])
        if gbk:
            response.encoding = 'gbk'
        if response.status_code == 404 or response.status_code == 500:
            return 404
        if response.status_code == 200:
            if return_type == "json":
                return response.json()
            elif return_type == "text":
                return response.text
            elif return_type == "content":
                return response.content
    except (Exception, requests.exceptions.ConnectionError) as error:
        if retry <= max_retries:
            if retry >= 3:
                time.sleep(retry * 0.5)
                print("get error, url is {}".format(api_url))
            if retry == max_retries:
                print("get error: {}".format(error))
            return get(api_url=api_url, params=params, retry=retry + 1, gbk=gbk)


def post(
        api_url: str,
        data: dict = None,
        retry: int = 0,
        gbk: bool = False,
        max_retries: int = 3,
        return_type: str = "json"
) -> [str, dict, int, None]:
    try:
        response = requests.post(api_url, data=data, headers=Vars.cfg.data['user_agent'])
        if gbk:
            response.encoding = 'gbk'
        if response.status_code == 404 or response.status_code == 500:
            return 404
        if response.status_code == 200:
            if return_type == "json":
                return response.json()
            elif return_type == "text":
                return response.text
            elif return_type == "content":
                return response.content
    except (Exception, requests.exceptions.ConnectionError) as error:
        if retry <= max_retries:
            if retry >= 3:
                time.sleep(retry * 0.5)
                print("post error, url is {}".format(api_url))
            if retry == max_retries:
                print("post error: {}".format(error))
            post(api_url=api_url, data=data, retry=retry + 1, gbk=gbk)


def chapter_info_json(index: int, url: str, title: str, content: str, image_list: list = None) -> [dict, None]:
    try:
        return {
            "chapterIndex": index,
            "chapter_url": url,
            "chapterTitle": title,
            "chapterContent": content,
            "imageList": image_list
        }
    except Exception as error:
        print("chapter_info_json", error)


def book_info_json(
        book_id: str = None,
        book_name: str = None,
        author_name: str = None,
        book_tag: str = None,
        book_intro: str = None,
        book_status: str = None,
        cover_url: str = None,
        book_uptime: str = None,
        last_chapter_title: str = None,
        chapter_url_list: list = None,
        book_words: str = None,
) -> [dict, None]:
    try:
        return {
            "bookId": book_id,
            "bookName": book_name,
            "authorName": author_name,
            "bookCoverUrl": cover_url,
            "chapUrl": chapter_url_list,
            "bookWords": book_words,
            "bookTag": book_tag,
            "bookIntro": book_intro,
            "bookStatus": book_status,
            "lastChapterTitle": last_chapter_title,
            "bookUptime": book_uptime
        }
    except Exception as error:
        print("book_info_json", error)
