import argparse
import src
import book
from config import *


def set_up_app_type(current_book_type: str = "Linovel"):  # set up app type and book type
    if current_book_type == "Linovel" or current_book_type == "l":
        Vars.current_book_type = "Linovel"
    elif current_book_type == "Dingdian" or current_book_type == "d":
        Vars.current_book_type = "Dingdian"
    elif current_book_type == "Xbookben" or current_book_type == "x":
        Vars.current_book_type = "Xbookben"
    # elif Vars.current_book_type == "BiquPavilion" or current_book_type == "b":
    #     Vars.current_book_type = "BiquPavilion"
    else:
        Vars.current_book_type = "Linovel"
        print("[error] app type not found, app type:", current_book_type)


def get_search_list(search_keyword: str):
    if Vars.current_book_type == "Linovel":
        search_response = src.BookAPI.LinovelAPI.get_book_info_by_keyword(search_keyword)
    elif Vars.current_book_type == "Xbookben":
        search_response = src.BookAPI.XbookbenAPI.get_book_info_by_keyword(search_keyword)
    else:
        raise Exception("[error] current book type not found, current book type:", Vars.current_book_type)
    if len(search_response) > 0:
        print("[info] start search book, book_id_list length:", len(search_response))
        for book_id in search_response:
            start_download_book(src.get_book_information(book_id))
    else:
        print("[warning] search result is empty, search keyword:", search_keyword)


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
        start_download_book(src.get_book_information(book_id))


def downloaded_update_book(app_type_name: str):
    if app_type_name in Vars.cfg.data['app_type_list']:
        if len(Vars.cfg.data['downloaded_book_id_list'][app_type_name]) != 0:
            [start_download_book(book_id) for book_id in Vars.cfg.data.get('downloaded_book_id_list')]
        else:
            print("[warning] downloaded_book_id_list is empty, please download book first")
    else:
        print("[error] app_type_name not found, app_type_name:", app_type_name)


def command() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Downloader for Linovel and Dingdian')
    parser.add_argument('-u', '--update', help='update config file', action="store_true")
    parser.add_argument('-s', '--search', help='search book', action="store_true")
    # parser.add_argument('-v', '--version', help='show version', action="store_true")
    parser.add_argument('-i', '--bookid', default=None, nargs=1, help='download book by book id')
    parser.add_argument('-n', '--name', default=None, help='download book by name')
    parser.add_argument('-a', '--app', help='run as app', nargs=1, default=None)
    return parser.parse_args()


if __name__ == '__main__':
    update_config()  # update config file if necessary (for example, add new token)
    args_command = command()
    shell_cmd = False
    set_up_app_type(current_book_type=args_command.app[0]) if args_command.app else set_up_app_type()

    if args_command.bookid is not None and args_command.bookid != "":
        start_download_book(src.get_book_information(args_command.bookid[0]))
        shell_cmd = True

    if args_command.name:
        get_search_list(args_command.book_name)
        shell_cmd = True

    if args_command.update is True:
        for app_type in Vars.cfg.data['app_type_list']:
            downloaded_update_book(app_type)
        shell_cmd = True

    if not shell_cmd:
        print("[info] run as shell")
        print("[info] d | download book by book id")
        print("[info] s | search book")
        print("[info] u | update book")
        print("[info] a | run as app")
        while True:
            inputs = get(">").split(" ")
            if inputs[0] == "d":
                if len(inputs) >= 2:
                    start_download_book(src.get_book_information(inputs[1]))
                else:
                    print("[error] please input book id, example: d 12345")

            elif inputs[0] == "s":
                if len(inputs) >= 2:
                    get_search_list(inputs[1])
                else:
                    print("[error] please input book name, example: s 红楼梦")
            elif inputs[0] == "u":
                if len(inputs) >= 2:
                    downloaded_update_book(inputs[1])
                print("download all books in config book_id_list")
                for app_type in Vars.cfg.data['app_type_list']:
                    downloaded_update_book(app_type)
            else:
                print("[error] command not found", inputs[0])
