import LinovelAPI
import book
from config import *


def shell_download_book(book_id: str):
    book_info = LinovelAPI.get_book_info(book_id)
    if book_info is not None:
        download = book.Book(book_info)
        download.init_content_config()
        download.multi_thread_download_book()


def shell_tag_scanner(max_page: int = 622):
    for page in range(max_page):
        tag_bookid_list = LinovelAPI.get_sort(page)
        for book_id in tag_bookid_list:
            shell_download_book(book_id)


def update_config():
    Vars.cfg.load()
    if Vars.cfg.data.get('downloaded_book_id_list') is None:
        Vars.cfg.data['downloaded_book_id_list'] = []
    if not isinstance(Vars.cfg.data.get('max_thread'), int):
        Vars.cfg.data['max_thread'] = 32
    if not isinstance(Vars.cfg.data.get('save_path'), str):
        Vars.cfg.data['save_path'] = "./Hbooker/"
    if not isinstance(Vars.cfg.data.get('out_path'), str):
        Vars.cfg.data['out_path'] = "./downloads/"
    if not isinstance(Vars.cfg.data.get('common_params'), dict):
        Vars.cfg.data['common_params'] = {
            'login_token': "", 'account': "", 'app_version': '2.9.022', 'device_token': 'ciweimao_'}
    Vars.cfg.save()


if __name__ == '__main__':
    # shell_download_book()
    update_config()
    shell_tag_scanner()
