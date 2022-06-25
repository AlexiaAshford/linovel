import sys

import LinovelAPI
import book
from config import *


def shell_download_book(book_id: str):
    book_info = LinovelAPI.get_book_info(book_id)
    if book_info is not None:
        download = book.Book(book_info)
        download.init_content_config()
        download.multi_thread_download_book()


def shell_tag_scanner(tag_name: str = "", max_page: int = 622):
    for page in range(max_page):
        tag_bookid_list = LinovelAPI.get_sort(page)
        for book_id in tag_bookid_list:
            shell_download_book(book_id)


def update_config():
    Vars.cfg.load()
    if Vars.cfg.data.get('downloaded_book_id_list') is None:
        Vars.cfg.data['downloaded_book_id_list'] = []
    if not isinstance(Vars.cfg.data.get('max_thread'), int):
        Vars.cfg.data['max_thread'] = 16
    if not isinstance(Vars.cfg.data.get('config_path'), str):
        Vars.cfg.data['config_path'] = "./Cache/"
    if not isinstance(Vars.cfg.data.get('out_path'), str):
        Vars.cfg.data['out_path'] = "./downloads/"
    Vars.cfg.save()


def shell_main(inputs: list):
    choice = inputs[0].lower()
    if choice == "d" or choice == "download":
        if len(inputs) >= 2:
            shell_download_book(inputs[1])
        else:
            print("please input book_id, like: linovel download book_id")
    elif choice == "t" or choice == "tag":
        if len(inputs) >= 2:
            shell_tag_scanner(tag_name=inputs[1])
        else:
            shell_tag_scanner()


if __name__ == '__main__':
    # shell_download_book()
    update_config()
    print(sys.argv)
    if len(sys.argv) >= 2:
        shell_main(sys.argv[1:])
    else:
        shell_main(inputs=get(">").split(" "))
