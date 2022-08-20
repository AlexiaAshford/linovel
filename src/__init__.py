import constant
import requests
from config import *
from tenacity import *
import fake_useragent

__all__ = [
    "API",
    "request",
    "get_book_information",
]

session = requests.Session()


@retry(stop=stop_after_attempt(5))
def request(api_url: str, method: str = "GET", params: dict = None, gbk: bool = False):
    headers = {
        "User-Agent": fake_useragent.UserAgent().random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
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
    else:
        raise Exception("[error] status code is not 200, status code is {}".format(response.status_code))


def get_book_information(book_id: str):  # return book info json
    book_id = book_id if "_" in book_id else re.findall(r"\d+", book_id)[-1]  # del book url suffix
    current_book_info_html = Vars.current_book_api.get_book_info_by_book_id(book_id)  # get book info html
    book_img = current_book_info_html.xpath(Vars.current_book_rule.book_img)
    book_name = current_book_info_html.xpath(Vars.current_book_rule.book_name)
    book_author = current_book_info_html.xpath(Vars.current_book_rule.book_author)
    book_state = current_book_info_html.xpath(Vars.current_book_rule.book_state)
    book_label = current_book_info_html.xpath(Vars.current_book_rule.book_label)
    last_chapter_title = current_book_info_html.xpath(Vars.current_book_rule.last_chapter_title)
    book_words = current_book_info_html.xpath(Vars.current_book_rule.book_words)
    book_update_time = current_book_info_html.xpath(Vars.current_book_rule.book_update_time)
    if Vars.current_book_type == "sfacg":
        catalogue = Vars.current_book_api.get_catalogue_info_by_book_id(book_id)
        chapter_url_list = [i for i in catalogue.xpath(Vars.current_book_rule.chapter_url_list)]
    elif Vars.current_book_type == "Dingdian":
        chapter_url_list = [i for i in current_book_info_html.xpath(Vars.current_book_rule.chapter_url_list)][6:]
    else:
        chapter_url_list = [i for i in current_book_info_html.xpath(Vars.current_book_rule.chapter_url_list)]

    return constant.json.book_json(
        book_id=book_id,
        book_name=book_name[0] if len(book_name) > 0 else None,
        book_words=book_words[0] if book_words else None,
        cover_url=book_img[0] if book_img else None,
        author_name=book_author[0] if book_author else None,
        book_status=book_state[0] if book_state else None,
        book_tag=book_label[0] if book_label else None,
        last_chapter_title=last_chapter_title[0] if last_chapter_title else None,
        book_uptime=book_update_time[0] if book_update_time else None,
        chapter_url_list=chapter_url_list if chapter_url_list else []
    )
