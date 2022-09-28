import requests
from config import *
import fake_useragent

__all__ = ["API", "request", "get_book_information_template"]

session = requests.Session()


def request(api_url: str, method: str = "GET", params: dict = None, gbk: bool = False):
    headers = {
        "User-Agent": fake_useragent.UserAgent().random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    if Vars.current_book_type == "popo":
        if Vars.cfg.data['popo_cookie'] == "":
            print("popo cookie is empty,you need to set it in config.json")
        else:
            headers["cookie"] = Vars.cfg.data['popo_cookie']
    if method == "GET":
        response = session.request(url=api_url, method="GET", params=params, headers=headers)
    else:
        response = session.request(url=api_url, method=method, data=params, headers=headers)

    if gbk is True:
        response.encoding = 'gbk'
    else:
        response.encoding = 'utf-8'
    if response.status_code == 200:
        return response


def get_book_information_template(book_id: str):  # return book info json
    book_id = book_id if "_" in book_id else re.findall(r"\d+", book_id)[-1]  # del book url suffix
    if Vars.current_book_api is None:
        return print("current book api is None, you need to set up web")
    else:
        current_book_info_html = Vars.current_book_api.get_book_info_by_book_id(book_id)  # get book info html

    book_img = current_book_info_html.xpath(Vars.current_book_rule.book_img)
    book_name = current_book_info_html.xpath(Vars.current_book_rule.book_name)
    book_author = current_book_info_html.xpath(Vars.current_book_rule.book_author)
    book_state = current_book_info_html.xpath(Vars.current_book_rule.book_state)
    book_label = current_book_info_html.xpath(Vars.current_book_rule.book_label)
    last_chapter_title = current_book_info_html.xpath(Vars.current_book_rule.last_chapter_title)
    book_words = current_book_info_html.xpath(Vars.current_book_rule.book_words)
    book_update_time = current_book_info_html.xpath(Vars.current_book_rule.book_update_time)
    book_intro = current_book_info_html.xpath(Vars.current_book_rule.book_intro)

    if Vars.current_book_type == "sfacg":
        catalogue = Vars.current_book_api.get_catalogue_info_by_book_id(book_id)
        chapter_url_list = [i for i in catalogue.xpath(Vars.current_book_rule.chapter_url_list)]
    elif Vars.current_book_type == "popo":
        catalogue = Vars.current_book_api.get_catalogue_info_by_book_id(book_id)
        chapter_url_list = [i for i in catalogue.xpath(Vars.current_book_rule.chapter_url_list)]
    else:
        chapter_url_list = [i for i in current_book_info_html.xpath(Vars.current_book_rule.chapter_url_list)]
        if Vars.current_book_type == "Dingdian":
            chapter_url_list = chapter_url_list[6:]  # del first 6 chapter, because the first 6 chapter is not ordered
    if not chapter_url_list:
        print("目录请求失败")
    return {
        "bookId": book_id,
        "bookName": book_name[0] if len(book_name) > 0 else None,
        "authorName": book_author[0] if book_author else None,
        "bookCoverUrl": book_img[0] if book_img else None,
        "bookWords": book_words[0] if book_words else None,
        "bookTag": book_label[0] if book_label else None,
        "bookIntro": book_intro[0] if book_intro else None,
        "bookStatus": book_state[0] if book_state else None,
        "lastChapterTitle": last_chapter_title[0] if last_chapter_title else None,
        "bookUptime": book_update_time[0] if book_update_time else None,
        "chapUrl": chapter_url_list,
    }
