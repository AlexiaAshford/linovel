import json
import os
import re


def update_config():
    Vars.cfg.load()
    change_config = False
    if not isinstance(Vars.cfg.data.get('max_thread'), int):
        Vars.cfg.data['max_thread'] = 16
        change_config = True
    if not isinstance(Vars.cfg.data.get('popo_cookie'), str):
        Vars.cfg.data['popo_cookie'] = ""
        change_config = True
    if not isinstance(Vars.cfg.data.get('config_path'), str):
        Vars.cfg.data['config_path'] = "./Cache/"
        change_config = True
    if not isinstance(Vars.cfg.data.get('out_path'), str):
        Vars.cfg.data['out_path'] = "./downloads/"
        change_config = True
    if change_config:
        Vars.cfg.save()


class Config:
    file_path = None
    dir_path = None
    data = None

    def __init__(self, file_path, dir_path):
        self.file_path = file_path
        self.dir_path = dir_path
        if not os.path.isdir(self.dir_path):
            os.makedirs(self.dir_path)
        if '.txt' in file_path:
            open(self.file_path, 'w').close()
        self.data = {}

    def load(self):
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                self.data = json.load(f) or {}
        except FileNotFoundError:
            try:
                open(self.file_path, 'w', encoding="utf-8").close()
            except Exception as error:
                print('[错误]', error, '创建配置文件时出错')
        except Exception as error:
            print('[错误]', error, '读取配置文件时出错')

    def save(self):
        try:
            with open(self.file_path, 'w', encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print('[错误]', e)
            print('保存配置文件时出错')


class Vars:
    cfg = Config(os.getcwd() + '/config.json', os.getcwd())
    current_book = None
    current_epub = None
    current_book_type = None
    current_book_gbk = False
    current_book_classify_name = None
    current_book_rule = None
    current_book_api = None
    current_book_rul_rule = None


class Msg:
    book_type_dict = {
        '0': 'https://www.linovel.net', '1': 'https://www.ddyueshu.com', '2': 'https://www.xbookben.net',
        '3': 'https://book.sfacg.com', '4': 'https://www.linovelib.com', '5': 'https://www.qbtr.cc',
        '6': 'http://www.trxs.cc', '7': 'https://www.popo.tw', '8': 'http://www.80zw.net',
        '9': 'https://www.qu-la.com', '10': 'https://www.52dus.cc/',
    }
    gbk_book_type = [
        'https://www.ddyueshu.com', 'https://www.qu-la.com', 'https://www.qbtr.cc', 'http://www.trxs.cc',
        'http://www.80zw.net',
    ]


class Current:
    pass


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
