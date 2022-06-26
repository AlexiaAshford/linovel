import LinovelAPI
import DingdianAPI
import book
from config import *


def get_book_info(book_id: str):
    if Vars.current_book_type == "Linovel":
        start_download_book(LinovelAPI.get_book_info(book_id))
    elif Vars.current_book_type == "Dingdian":
        start_download_book(DingdianAPI.get_book_info(book_id))
    else:
        print("[error] app type not found, app type:", Vars.current_book_type)


def set_up_app_type(app_type: str):
    if app_type == "Linovel":
        Vars.current_book_type = "Linovel"
    elif app_type == "Dingdian":
        Vars.current_book_type = "Dingdian"
    else:
        Vars.current_book_type = "Linovel"
        print("[error] app type not found, app type:", app_type)


def get_search_list(search_keyword: str):
    if Vars.current_book_type == "Linovel":
        return start_search_book(LinovelAPI.search_book(search_keyword))
    # elif Vars.current_book_type == "Dingdian":
    #     return Dingdian.get_search_list()


def start_download_book(book_info_result: dict) -> None:
    Vars.current_book = book_info_result
    if Vars.current_book is not None:
        Vars.current_book = book.Book(Vars.current_book, "Linovel")
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


# def shell_linovel(inputs: list):
#     choice = inputs[0].lower()
#     if choice == "d" or choice == "download":
#         if len(inputs) >= 2:
#             Linovel.shell_download_book(inputs[1])
#         else:
#             print("please input book_id, like: linovel download book_id")
#     elif choice == "t" or choice == "tag":
#         if len(inputs) >= 2:
#             Linovel.shell_tag_scanner(tag_name=inputs[1])
#         else:
#             Linovel.shell_tag_scanner()
#
#
# def shell_dingdian(inputs: list):
#     choice = inputs[0].lower()
#     if choice == "d" or choice == "download":
#         if len(inputs) >= 2:
#             Dingdian.shell_download_book(inputs[1])
#         else:
#             print("please input book_id, like: linovel download book_id")
