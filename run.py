from shell import *
from config import *


def update_config():
    Vars.cfg.load()
    if not isinstance(Vars.cfg.data.get('downloaded_book_id_list'), dict):
        Vars.cfg.data['downloaded_book_id_list'] = {"Linovel": [], "Dingdian": [], "Xbookben": []}
    if not isinstance(Vars.cfg.data.get('max_thread'), int):
        Vars.cfg.data['max_thread'] = 16
    if not isinstance(Vars.cfg.data.get('app_type_list'), list):
        Vars.cfg.data['app_type_list'] = ["Linovel", "Dingdian", "Xbookben"]
    if not isinstance(Vars.cfg.data.get('config_path'), str):
        Vars.cfg.data['config_path'] = "./Cache/"
    if not isinstance(Vars.cfg.data.get('out_path'), str):
        Vars.cfg.data['out_path'] = "./downloads/"
    if not isinstance(Vars.cfg.data.get('user_agent'), dict):
        Vars.cfg.data['user_agent'] = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/89.0.4389.114 Safari/537.36 "
        }
    Vars.cfg.save()


def downloaded_update_book(app_type_name: str):
    if app_type_name in Vars.cfg.data['app_type_list']:
        if len(Vars.cfg.data['downloaded_book_id_list'][app_type_name]) != 0:
            [start_download_book(book_id) for book_id in Vars.cfg.data.get('downloaded_book_id_list')]
        else:
            print("[warning] downloaded_book_id_list is empty, please download book first")
    else:
        print("[error] app_type_name not found, app_type_name:", app_type_name)


def command():
    import argparse
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
    args, shell_cmd = command(), False

    if args.app:
        set_up_app_type(current_book_type=args.app[0])
    else:
        set_up_app_type(current_book_type="Linovel")

    if args.bookid:
        get_book_info(args.bookid[0])
        shell_cmd = True

    if args.name:
        get_search_list(args.book_name)
        shell_cmd = True

    if args.update is True:
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
                    get_book_info(inputs[1])
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
