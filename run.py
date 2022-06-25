import sys
from shell import *
from config import *


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
    if not isinstance(Vars.cfg.data.get('user_agent'), dict):
        Vars.cfg.data['user_agent'] = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/89.0.4389.114 Safari/537.36 "
        }
    Vars.cfg.save()


def command():
    import argparse
    parser = argparse.ArgumentParser(description='Downloader for Linovel and Dingdian')
    parser.add_argument('-c', '--config', help='config file path', default="./config.json")
    parser.add_argument('-u', '--update', help='update config file', action="store_true")
    parser.add_argument('-d', '--download', help='download book', action="store_true")
    parser.add_argument('-l', '--list', help='list book', action="store_true")
    parser.add_argument('-s', '--search', help='search book', action="store_true")
    parser.add_argument('-v', '--version', help='show version', action="store_true")
    parser.add_argument('-a', '--all', help='download all book', action="store_true")
    parser.add_argument('-i', '--id', help='download book by id', type=int)
    parser.add_argument('-n', '--name', help='download book by name')
    return parser.parse_args()


if __name__ == '__main__':
    # shell_download_book()
    update_config()  # update config file if necessary (for example, add new token)
    if len(sys.argv) >= 3:
        if sys.argv[1] == "linovel":
            shell_linovel(sys.argv[2:])
        if sys.argv[1] == "dingdian":
            shell_dingdian(sys.argv[2:])
    else:
        print("please input command, like: linovel download book_id")
        inputs = get(">").split(" ")
        if inputs[0] == "linovel":
            shell_linovel(inputs[1:])
        if inputs[0] == "dingdian":
            shell_dingdian(inputs[1:])
