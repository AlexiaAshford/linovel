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
    Vars.cfg.save()


if __name__ == '__main__':
    # shell_download_book()
    update_config()
    if len(sys.argv) >= 2:
        shell_linovel(sys.argv[1:])
    else:
        shell_linovel(inputs=get(">").split(" "))
