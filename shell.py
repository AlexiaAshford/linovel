import scr
from scr import DingdianAPI, LinovelAPI, BiquPavilionAPI, XbookbenAPI
import book
from config import *


def get_book_info(book_id: str):  # get book info by book id
    if Vars.current_book_type == "Linovel":
        start_download_book(LinovelAPI.get_book_info(book_id))
    elif Vars.current_book_type == "Dingdian":
        start_download_book(DingdianAPI.get_book_info(book_id))
    elif Vars.current_book_type == "BiquPavilion":
        start_download_book(BiquPavilionAPI.get_book_info(book_id))
    elif Vars.current_book_type == "Xbookben":
        start_download_book(scr.get_book_information(book_id))
    else:
        print("[error] app type not found, app type:", Vars.current_book_type)


def set_up_app_type(current_book_type: str):  # set up app type and book type
    if current_book_type == "Linovel" or current_book_type == "l":
        Vars.current_book_type = "Linovel"
    elif current_book_type == "Dingdian" or current_book_type == "d":
        Vars.current_book_type = "Dingdian"
    elif current_book_type == "Xbookben" or current_book_type == "x":
        Vars.current_book_type = "Xbookben"
    elif Vars.current_book_type == "BiquPavilion" or current_book_type == "b":
        Vars.current_book_type = "BiquPavilion"
    else:
        Vars.current_book_type = "Linovel"
        print("[error] app type not found, app type:", current_book_type)


def get_search_list(search_keyword: str):
    if Vars.current_book_type == "Linovel":
        return start_search_book(LinovelAPI.search_book(search_keyword))
    # elif Vars.current_book_type == "Dingdian":
    #     return start_search_book(DingdianAPI.search_book(search_keyword))
    # elif Vars.current_book_type == "BiquPavilion":
    #     return start_search_book(BiquPavilionAPI.search_book(search_keyword))


def start_download_book(book_info_result: dict) -> None:
    Vars.current_book = book_info_result
    if Vars.current_book is not None:
        Vars.current_book = book.Book(Vars.current_book)
        Vars.current_book.init_content_config()
        Vars.current_book.multi_thread_download_book()
    else:
        print("[warning] Vars.current_book is None")


def start_search_book(book_id_list: list):
    if len(book_id_list) == 0:
        print("[error] book_id_list is empty")
        return
    print("[info] start search book, book_id_list length:", len(book_id_list))
    for book_id in book_id_list:
        get_book_info(book_id)


class Dingdian:
    @staticmethod
    def shell_tag_scanner(tag_name: str = "", max_page: int = 622):
        for page in range(max_page):
            tag_bookid_list = LinovelAPI.get_sort(tag_name, page)
            for book_id in tag_bookid_list:
                get_book_info(book_id)


class Linovel:

    @staticmethod
    def shell_tag_scanner(tag_name: str = "", max_page: int = 622):
        for page in range(max_page):
            tag_bookid_list = LinovelAPI.get_sort(tag_name, page)
            for book_id in tag_bookid_list:
                get_book_info(book_id)
