import LinovelAPI
import book
from config import *


class Linovel:
    @staticmethod
    def shell_download_book(book_id: str) -> None:
        Vars.current_book = LinovelAPI.get_book_info(book_id)
        if Vars.current_book is not None:
            Vars.current_book = book.Book(Vars.current_book, "Linovel")
            Vars.current_book.init_content_config()
            Vars.current_book.multi_thread_download_book()
        else:
            print("[warning] book_id not found, book_id:", book_id)

    @staticmethod
    def shell_tag_scanner(tag_name: str = "", max_page: int = 622):
        for page in range(max_page):
            tag_bookid_list = LinovelAPI.get_sort(tag_name, page)
            for book_id in tag_bookid_list:
                Linovel.shell_download_book(book_id)


def shell_linovel(inputs: list):
    choice = inputs[0].lower()
    if choice == "d" or choice == "download":
        if len(inputs) >= 2:
            Linovel.shell_download_book(inputs[1])
        else:
            print("please input book_id, like: linovel download book_id")
    elif choice == "t" or choice == "tag":
        if len(inputs) >= 2:
            Linovel.shell_tag_scanner(tag_name=inputs[1])
        else:
            Linovel.shell_tag_scanner()
