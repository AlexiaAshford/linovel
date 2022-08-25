import argparse
import constant
import book
from config import *
from src import API, get_book_information


def set_up_app_type(current_book_type: str = "Linovel"):  # set up app type and book type
    # distribution book type and app type
    if current_book_type == "Xbookben" or current_book_type == "x":
        Vars.current_book_type = "Xbookben"
        Vars.current_book_rule = constant.rule.XbookbenRule
        Vars.current_book_api = API.XbookbenAPI
    elif current_book_type == "Dingdian" or current_book_type == "d":
        Vars.current_book_type = "Dingdian"
        Vars.current_book_rule = constant.rule.DingdianRule
        Vars.current_book_api = API.DingdianAPI
    elif current_book_type == "Linovel" or current_book_type == "l":
        Vars.current_book_type = "Linovel"
        Vars.current_book_rule = constant.rule.LinovelRule
        Vars.current_book_api = API.LinovelAPI
    elif current_book_type == "sfacg" or current_book_type == "s":
        Vars.current_book_type = "sfacg"
        Vars.current_book_rule = constant.rule.BoluobaoRule
        Vars.current_book_api = API.BoluobaoAPI
    elif current_book_type == "Biquge" or current_book_type == "b":
        Vars.current_book_type = "Biquge"
        Vars.current_book_rule = constant.rule.BiqugeRule
        Vars.current_book_api = API.BiqugeAPI
    else:
        raise Exception("[error] app type not found, app type:", Vars.current_book_type)


def get_search_list(search_keyword: str):
    if Vars.current_book_type not in ["Linovel", "Xbookben"]:
        raise Exception("[error] current book type not found, current book type:", Vars.current_book_type)
    search_response = Vars.current_book_api.get_book_info_by_keyword(search_keyword)
    if len(search_response) > 0:
        print("[info] start search book, book_id_list length:", len(search_response))
        for book_id in search_response:
            start_download_book(book_id)
    else:
        print("[warning] search result is empty, search keyword:", search_keyword)


def start_download_book(book_id: str) -> None:
    Vars.current_book = get_book_information(book_id)
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
        start_download_book(book_id)


def shell_console():
    print("[info] run as shell")
    print("[info] d | download book by book id")
    print("[info] s | search book")
    print("[info] u | update book")
    print("[info] a | run as app")
    while True:
        inputs = get(">").split(" ")
        if inputs[0] == "d":
            if len(inputs) >= 2:
                start_download_book(inputs[1])
            else:
                print("[error] please input book id, example: d 12345")

        elif inputs[0] == "s":
            if len(inputs) >= 2:
                get_search_list(inputs[1])
            else:
                print("[error] please input book name, example: s 红楼梦")
        else:
            print("[error] command not found", inputs[0])


def command() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Downloader for Linovel and Dingdian')
    # parser.add_argument('-u', '--update', help='update config file', action="store_true")
    parser.add_argument('-s', '--search', help='search book', action="store_true")
    # parser.add_argument('-v', '--version', help='show version', action="store_true")
    parser.add_argument('-i', '--bookid', default=None, nargs=1, help='download book by book id')
    parser.add_argument('-n', '--name', default=None, help='download book by name')
    parser.add_argument('-a', '--app', help='run as app', nargs=1, default=None)
    return parser.parse_args()


if __name__ == '__main__':
    update_config()  # update config file if necessary (for example, add new token)
    args_command = command()
    shell_open_console = False
    set_up_app_type(current_book_type=args_command.app[0]) if args_command.app else set_up_app_type()

    if args_command.bookid is not None and args_command.bookid != "":
        start_download_book(args_command.bookid[0])
        shell_open_console = True

    if args_command.name:
        get_search_list(args_command.book_name)
        shell_open_console = True

    if not shell_open_console:
        shell_console()
