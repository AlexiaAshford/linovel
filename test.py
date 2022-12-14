import book
from src import *
from config import *


def init_config_book_source():
    import json
    import constant
    book_source_path = "./book_source/{}.json".format(Vars.current_book_type.split(".")[-2])
    if not os.path.exists(book_source_path):
        return False
    # print(book_source_path)
    Vars.current_book_source = json.loads(open(book_source_path, "r", encoding="utf-8").read())
    print(Vars.current_book_source)
    Vars.current_book_api = API.Response
    Vars.current_book_rule = constant.NovelRule()
    print("下载源已设置为: {}".format(Vars.current_book_type))
    return True


if __name__ == '__main__':
    update_config()
    book_id = "6072"
    Vars.current_book_classify_name = "tongren"
    Vars.current_book_type = "http://www.trxs.cc"
    Vars.current_book_gbk = True
    if not init_config_book_source():
        raise Exception("book source not found, please check your book type, book type:", Vars.current_book_type)

    book_info_html = Vars.current_book_api.get_book_info_by_book_id(book_id)
    print("=== book_info_html ===")
    if book_info_html is None:
        print("<error>", "[red]Get book info error, please check your book id.[/red]")
        exit(1)
    init_book_info_template(book_info_html)
    init_chapter_url_list(book_info_html)
    print("=== init_chapter_url_list ===")
    if Vars.current_book.chapter_url_list is None:
        print("<error>", "[red]The chapter list is empty, please check your book id.[/red]")
        exit(1)
    if Vars.current_book.bookName:
        current_book = book.BookConfig()
        current_book.init_content_config()
        current_book.multi_thread_download_book()
    else:
        print("<error>", "[red]Download book error,please check your input app type name.[/red]")
