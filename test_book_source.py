import argparse
import book
from src import *
from config import *


def init_config_book_source():
    import json
    import constant
    book_source_path = "./book_source/{}.json".format(Vars.current_book_type.split(".")[-2])
    if os.path.exists(book_source_path):
        Vars.current_book_source = json.loads(open(book_source_path, "r", encoding="utf-8").read())
        Vars.current_book_api = API.Response
        Vars.current_book_rule = constant.NovelRule()
        print("下载源已设置为: {}".format(Vars.current_book_type))
        return True
    else:
        return False


if __name__ == '__main__':
    book_id = ""
    Vars.current_book_type = ""
    Vars.current_book_gbk = False
    init_config_book_source()
    if not init_config_book_source():
        raise Exception("book source not found, please check your book type, book type:", Vars.current_book_type)

    book_info_html = Vars.current_book_api.get_book_info_by_book_id(book_id)
    if book_info_html is None:
        print("<error>", "[red]Get book info error, please check your book id.[/red]")
    else:
        init_book_info_template(book_info_html=book_info_html)
        init_chapter_url_list(book_info_html=book_info_html)
        if Vars.current_book and Vars.current_book.get("bookName") is not None:
            Vars.current_book = book.BookConfig(Vars.current_book)
            Vars.current_book.init_content_config()
            Vars.current_book.multi_thread_download_book()
        else:
            print("<error>", "[red]Download book error,please check your input app type name.[/red]")
