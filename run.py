import lib
import argparse
import book
from src import *
from config import *
from api import Response


def init_config_book_source():
    book_source_path = "./book_source/{}.json".format(Vars.current_book_type.split(".")[-2])
    if os.path.exists(book_source_path):
        Vars.current_source = model.BookSource(**json.loads(open(book_source_path, "r", encoding="utf-8").read()))
        print("下载源已设置为: {}".format(Vars.current_book_type))
        return True
    else:
        return False


def set_up_app_type(book_type: str):  # set up app type and book type
    if Msg.book_type_dict.get(book_type):
        Vars.current_book_type = Msg.book_type_dict.get(book_type)
        if not init_config_book_source():
            raise Exception("book source not found, please check your book type, book type:", Vars.current_book_type)

        if book_type == "5" or book_type == "6":
            print("index:1\t\t常规小说\nindex:2\t\t同人小说")
            while Vars.current_book_classify_name is None:
                Vars.current_book_classify_name = {"1": "tongren", "2": "changgui"}.get(get(">").strip())
            else:
                print("set up classify name:", Vars.current_book_classify_name)

    else:
        print("[error] book type not found, please input again", book_type)
        for index, book_type in Msg.book_type_dict.items():
            print("index:", index, "\t\tbook type:", book_type)
        print("please input index to select book type, example: 0")
        set_up_app_type(get(">"))


def parse_args_command() -> argparse.Namespace:
    Vars.cfg.load()  # load config and init config
    parser = argparse.ArgumentParser(description='Downloader for Linovel and Dingdian')
    # parser.add_argument('-u', '--update', help='update config file', action="store_true")
    parser.add_argument('-s', '--search', default=None, nargs=1, help='search book')
    parser.add_argument('-i', '--bookid', default=None, nargs=1, help='download book by book id')
    parser.add_argument('-d', '--download', default=None, nargs=1, help='download book by book id')
    parser.add_argument('-n', '--name', default=None, help='download book by name')
    parser.add_argument('-a', '--app', help='run as app', nargs=1, default=None)
    return parser.parse_args()


def get_book_id_by_url(i: str):
    try:
        return i if "_" in i else re.findall(r"\d+", i)[-1]  # del book url suffix
    except Exception as error:
        return print(error)


@lib.time_count
def shell_console(inputs: list):
    if inputs[0] == "d" or inputs[0] == "download":
        book_info_html = Response.get_book_info_by_book_id(get_book_id_by_url(inputs[1]))
        if book_info_html is None:
            print("<error>", "[red]Get book info error, please check your book id.[/red]")
        else:
            init_book_info_template(book_info_html=book_info_html)

            if Vars.current_book.chapter_url_list is None:
                return print("<error>", "[red]Get chapter url list error, please check your book id.[/red]")
            if Vars.current_book.book_name:
                Vars.current_book.book_name = re.sub(r"[/\\:*?\"<>|]", "_", Vars.current_book.book_name)
                make_dirs(Vars.cfg.data.config_path)
                make_dirs(Vars.cfg.data.cover_path)
                make_dirs(os.path.join(Vars.cfg.data.out_path, Vars.current_book.book_name))
                current_book = book.BookConfig()
                current_book.init_content_config()
                current_book.multi_thread_download_book()
            else:
                print("<error>", "[red]Download book error,please check your input app type name.[/red]")

    elif inputs[0] == "s" or inputs[0] == "search":
        response = Response.get_book_info_by_keyword(inputs[1]) if len(inputs) >= 2 else []
        if len(response) > 0:
            for index, i in enumerate(response):
                print("index", index, "\t\tbook name:", i[0])
            print("please input index to download book, example: 0")
            while True:
                index = get(">").strip()
                if index == "q" or index == "quit":
                    break
                if index.isdigit() and int(index) < len(response):
                    book_id = re.findall(r"(\d+)", response[int(index)][1])[0]
                    shell_console(["d", book_id])
                else:
                    print("[error] index not found")
        else:
            print("[warning] search result is empty, search keyword:", inputs[1])
    else:
        print(inputs[0], "command not found, please input again")


if __name__ == '__main__':

    args_command = parse_args_command()
    set_up_app_type(args_command.app[0]) if args_command.app else set_up_app_type("")

    if args_command.bookid:
        shell_console(["d", args_command.bookid[0]])

    elif args_command.download:
        shell_console(["d", args_command.download[0]])

    elif args_command.search:
        shell_console(["s", args_command.search[0]])
    else:
        print("[input]d + book id\t\t\tddownload book by book id")
        print("[input]s + search keyword\t\tsearch book by keyword")
        while True:
            shell_console(get(">").strip().split(" "))
