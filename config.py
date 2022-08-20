import json
import os
import re


def update_config():
    Vars.cfg.load()
    if not isinstance(Vars.cfg.data.get('max_thread'), int):
        Vars.cfg.data['max_thread'] = 16
    if not isinstance(Vars.cfg.data.get('app_type_list'), list):
        Vars.cfg.data['app_type_list'] = ["Linovel", "Dingdian", "Xbookben", "BiquPavilion", "sfacg"]
    if not isinstance(Vars.cfg.data.get('config_path'), str):
        Vars.cfg.data['config_path'] = "./Cache/"
    if not isinstance(Vars.cfg.data.get('out_path'), str):
        Vars.cfg.data['out_path'] = "./downloads/"
    if not isinstance(Vars.cfg.data.get('user_agent'), dict):
        Vars.cfg.data['user_agent'] = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit"}
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
    current_book_rule = None
    current_book_api = None


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
