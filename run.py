import argparse
import constant
import book
from config import *
from src import API, get_book_information_template


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
    elif current_book_type == "Baling" or current_book_type == "bl":
        Vars.current_book_type = "Baling"
        Vars.current_book_rule = constant.rule.BalingRule
        Vars.current_book_api = API.BalingAPI
    else:
        raise Exception("[error] app type not found, app type:", Vars.current_book_type)


def get_search_list(search_keyword: str):
    if Vars.current_book_type not in ["Linovel", "Xbookben"]:
        raise Exception("[error] current book type not found, current book type:", Vars.current_book_type)
    search_response = Vars.current_book_api.get_book_info_by_keyword(search_keyword)
    if len(search_response) > 0:
        print("[info] start search book, book_id_list length:", len(search_response))
        for book_id in search_response:
            shell_console(["d", book_id])
    else:
        print("[warning] search result is empty, search keyword:", search_keyword)


def start_search_book(book_id_list: list):
    if len(book_id_list) == 0:
        print("[error] book_id_list is empty")
        return
    print("[info] start search book, book_id_list length:", len(book_id_list))
    for book_id in book_id_list:
        shell_console(["d", book_id])


def shell_console(inputs: list):
    if inputs[0] == "d" or inputs[0] == "download":
        Vars.current_book = None if len(inputs) < 2 else get_book_information_template(inputs[1])
        if Vars.current_book is not None:
            Vars.current_book = book.Book(Vars.current_book)
            Vars.current_book.init_content_config()
            Vars.current_book.multi_thread_download_book()
        else:
            print("[error] please input book id, example: d 12345")
    elif inputs[0] == "s" or inputs[0] == "search":
        if len(inputs) >= 2:
            get_search_list(inputs[1])
        else:
            print("[error] please input book name, example: s 红楼梦")
    else:
        print(inputs[0], "command not found, please input again")


def parse_args_command() -> argparse.Namespace:
    update_config()  # update config file if necessary (for example, add new token)
    parser = argparse.ArgumentParser(description='Downloader for Linovel and Dingdian')
    # parser.add_argument('-u', '--update', help='update config file', action="store_true")
    parser.add_argument('-s', '--search', default=None, nargs=1, help='search book')
    # parser.add_argument('-v', '--version', help='show version', action="store_true")
    parser.add_argument('-i', '--bookid', default=None, nargs=1, help='download book by book id')
    parser.add_argument('-n', '--name', default=None, help='download book by name')
    parser.add_argument('-a', '--app', help='run as app', nargs=1, default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args_command = parse_args_command()
    if args_command.app:
        set_up_app_type(current_book_type=args_command.app[0])
    else:
        set_up_app_type()  # default app type is Linovel

    if args_command.bookid is not None and args_command.bookid != "":
        shell_console(["d", args_command.bookid[0]])

    elif args_command.name is not None and args_command.name != "":
        shell_console(["s", args_command.name[0]])

    else:
        print("Welcome to use downloader, please input command")
        while True:
            shell_console(get(">").strip())
