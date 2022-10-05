import argparse
import book
from src import *
from config import *


def set_up_web():
    import constant
    if Vars.current_book_type == "https://www.ddyueshu.com":
        book_api = API.ResponseAPI.Dingdian
        book_rule = constant.rule.WebRule.DingdianRule
    elif Vars.current_book_type == "https://www.xbookben.net":
        book_api = API.ResponseAPI.Xbookben
        book_rule = constant.rule.WebRule.XbookbenRule
    elif Vars.current_book_type == "https://www.linovel.net":
        book_api = API.ResponseAPI.Linovel
        book_rule = constant.rule.WebRule.LinovelRule
    elif Vars.current_book_type == "https://book.sfacg.com":
        book_api = API.ResponseAPI.Boluobao
        book_rule = constant.rule.WebRule.BoluobaoRule
    elif Vars.current_book_type == "https://www.qu-la.com":
        book_api = API.ResponseAPI.Biquge
        book_rule = constant.rule.WebRule.BiqugeRule
    elif Vars.current_book_type == "http://www.80zw.net":
        book_api = API.ResponseAPI.Baling
        book_rule = constant.rule.WebRule.BalingRule
    elif Vars.current_book_type == "https://www.qbtr.cc":
        book_api = API.ResponseAPI.Qbtr
        book_rule = constant.rule.WebRule.QbtrRule
    elif Vars.current_book_type == "http://trxs.cc":
        book_api = API.ResponseAPI.Trxs
        book_rule = constant.rule.WebRule.TrxsRule
    elif Vars.current_book_type == "https://www.popo.tw":
        book_api = API.ResponseAPI.Popo
        book_rule = constant.rule.WebRule.PopoRule
    elif Vars.current_book_type == "https://www.linovelib.com":
        book_api = API.ResponseAPI.Linovelib
        book_rule = constant.rule.WebRule.LinovelibRule
    else:
        raise "Error: current_book_type is not in Xbookben, Dingdian, Linovel, sfacg, Biquge, Baling"
    return book_api, book_rule


def set_up_app_type(current_book_type: str = "0"):  # set up app type and book type
    book_type_dict = {
        '0': 'https://www.linovel.net', '1': 'https://www.ddyueshu.com', '2': 'https://www.xbookben.net',
        '3': 'https://book.sfacg.com', '4': 'https://www.linovelib.com', '5': 'https://www.qbtr.cc',
        '6': 'http://trxs.cc', '7': 'https://www.popo.tw', '8': 'http://www.80zw.net', '9': 'https://www.qu-la.com'
    }
    if book_type_dict.get(current_book_type):
        if current_book_type == "5" or current_book_type == "6":
            print("index:1\t\t常规小说\nindex:2\t\t同人小说")
            Vars.current_book_classify_name = {"1": "changgui", "2": "tongren"}.get(
                get("please input your classify index:").strip()
            )
        Vars.current_book_type = book_type_dict.get(current_book_type)
        Vars.current_book_api, Vars.current_book_rule = set_up_web()
        print("已设置为", Vars.current_book_type, "小说下载")
        return True

    else:
        print("[error] book type not found, please input again", current_book_type)
        for index, book_type in book_type_dict.items():
            print("index:", index, "\t\tbook type:", book_type)
        print("please input index to select book type, example: 0")
        return False


def parse_args_command() -> argparse.Namespace:
    update_config()  # update config file if necessary (for example, add new token)
    parser = argparse.ArgumentParser(description='Downloader for Linovel and Dingdian')
    # parser.add_argument('-u', '--update', help='update config file', action="store_true")
    parser.add_argument('-s', '--search', default=None, nargs=1, help='search book')
    parser.add_argument('-i', '--bookid', default=None, nargs=1, help='download book by book id')
    parser.add_argument('-d', '--download', default=None, nargs=1, help='download book by book id')
    parser.add_argument('-n', '--name', default=None, help='download book by name')
    parser.add_argument('-a', '--app', help='run as app', nargs=1, default=None)
    return parser.parse_args()


def shell_console(inputs: list):
    if inputs[0] == "d" or inputs[0] == "download":
        Vars.current_book = get_book_information_template(inputs[1])
        if Vars.current_book and Vars.current_book.get("bookName") is not None:
            Vars.current_book = book.BookConfig(Vars.current_book)
            Vars.current_book.init_content_config()
            Vars.current_book.multi_thread_download_book()
        else:
            print("download error,please  check your input app name or book id")
    elif inputs[0] == "s" or inputs[0] == "search":
        response = Vars.current_book_api.get_book_info_by_keyword(inputs[1]) if len(inputs) >= 2 else []
        if len(response) > 0:
            for index, i in enumerate(response):
                print("index", index, "\t\tbook name:", i[1])
            print("please input index to download book, example: 0")
            while True:
                index = get(">").strip()
                if index == "q" or index == "quit":
                    break
                if index.isdigit() and int(index) < len(response):
                    book_id = re.findall(r"(\d+)", response[int(index)][2])[0]
                    shell_console(["d", book_id])
                else:
                    print("[error] index not found")
        else:
            print("[warning] search result is empty, search keyword:", inputs[1])
    else:
        print(inputs[0], "command not found, please input again")


if __name__ == '__main__':
    args_command = parse_args_command()
    if not (set_up_app_type(args_command.app[0]) if args_command.app is not None else set_up_app_type()):
        exit(1)
    if args_command.bookid is not None and args_command.bookid != "":
        shell_console(["d", args_command.bookid[0]])

    elif args_command.download is not None and args_command.download != "":
        shell_console(["d", args_command.download[0]])

    elif args_command.search is not None and args_command.search != "":
        shell_console(["s", args_command.search[0]])
    else:
        print("Welcome to use downloader, please input command")
        while True:
            shell_console(get(">").strip())

    # def input_index():
    #     try:
    #         index = int(input())
    #         if index < len(response):
    #             Vars.current_book = book.Book(response[index])
    #             Vars.current_book.init_content_config()
    #             Vars.current_book.multi_thread_download_book()
    #         else:
    #             print("[error] index out of range, please input again")
    #             input_index()
    #     except ValueError:
    #         print("[error] please input number")
    #         input_index()
