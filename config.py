import json
import os
import re
from rich import print
from lib import model
from typing import Union


class Config:
    file_path = None
    dir_path = None

    def __init__(self, file_path, dir_path):
        self.file_path = file_path
        self.dir_path = dir_path
        if not os.path.isdir(self.dir_path):
            os.makedirs(self.dir_path)
        if '.txt' in file_path:
            open(self.file_path, 'w').close()
        self.data_config = {}

    @property
    def data(self):
        return model.AccountConfig(**self.data_config)

    def update(self):
        change_config = False
        if not isinstance(self.data_config.get('max_thread'), int):
            self.data_config['max_thread'] = 16
            change_config = True
        if not isinstance(self.data_config.get('popo_cookie'), str):
            self.data_config['popo_cookie'] = ""
            change_config = True
        if self.data_config.get('config_path') == "" or \
                not isinstance(self.data_config.get('config_path'), str):
            self.data_config['config_path'] = "./cache/"
            change_config = True
        if self.data_config.get('out_path') == "" or \
                not isinstance(self.data_config.get('out_path'), str):
            self.data_config['out_path'] = "./downloads/"
            change_config = True
        if self.data_config.get('cover_path') == "" or \
                not isinstance(self.data_config.get('cover_path'), str):
            self.data_config['cover_path'] = "./cache/cover/"
            change_config = True
        if change_config:
            self.save()

    def load(self) -> bool:
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                self.data_config = json.load(f) or {}
                self.update()
                return True
        except FileNotFoundError:
            try:
                print("配置文件不存在，正在创建配置文件")
                with open(self.file_path, 'w', encoding="utf-8") as f:
                    f.write("{}")
                self.load()
            except Exception as error:
                print('[错误]', error, '创建配置文件时出错')

        except Exception as error:
            print('[错误]', error, '读取配置文件时出错')
            print(self.data_config)
        return False

    def save(self):
        try:
            with open(self.file_path, 'w', encoding="utf-8") as f:
                json.dump(self.data_config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print('[错误]', e)
            print('保存配置文件时出错')


class Vars:
    cfg = Config(os.getcwd() + '/config.json', os.getcwd())
    current_book: Union[model.BookInfo] = None
    current_book_id = None
    current_epub = None
    current_book_type = None
    current_book_classify_name = None
    current_source: Union[model.BookSource] = None


class Msg:
    book_type_dict = {
        '0': 'https://www.linovel.net', '1': 'https://www.ddyueshu.com', '2': 'https://www.xbookben.net',
        '3': 'https://book.sfacg.com', '4': 'https://www.linovelib.com', '5': 'https://www.qbtr.cc',
        '6': 'http://www.trxs.cc', '7': 'https://www.popo.tw', '8': 'http://www.80zw.net',
        '9': 'https://www.qu-la.com', '10': 'https://www.52dus.cc/', '11': 'https://www.qb5.la',
        '12': 'https://www.xbiquge.la', '13': 'http://m.bjcan8.com',
    }
    del_chapter_advertisement_list = [
        "&amp;", "amp;", "lt;", "gt;", "一秒记住【八零中文网 www.80zw.net】，精彩小说无弹窗免费阅读！", "顶点小说手机",
        "<br>", "<br/>", "<br />", "<p>", "</p>", "<div>", "</div>", "<span>", "</span>", "<strong>",
        "</strong>", "<b>", "</b>", "<i>", "</i>", "最新章节！", "全本小说网 www.qb5.la，最快更新", "最新章节免费阅读！",
        "ddyueshu.com"
    ]


def get_id(url: str) -> str:
    result = re.compile(r'(\d+)').findall(url)
    if len(result) > 0:
        return result[-1]
    print("[warning] get bookid failed", url)


def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def make_dirs(file_path: str) -> str:
    file_path = os.path.join(os.getcwd(), file_path)
    if not os.path.exists(file_path):  # if Cache folder is not exist, create it
        os.makedirs(file_path)
    return file_path


def write_text(path_name: str, content: str = "", mode: str = "w"):
    try:
        with open(path_name, mode, encoding="utf-8", newline="") as f:
            f.write(content)
    except Exception as err:
        print("error: {}".format(err))


def read_text(path_name: str, json_load: bool = False) -> [dict, str]:
    import json
    try:
        with open(path_name, "r", encoding="utf-8") as f:
            if not json_load:
                return f.read()
            return json.loads(f.read())
    except Exception as err:
        print("read_text error: {}".format(err))
