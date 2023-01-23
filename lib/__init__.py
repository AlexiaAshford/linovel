import time

import lib.utils
from lib.ebooklib import epub
from lib import decodes
from lib import model
from lib import log


# 统计时间的装饰器

def time_count(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("time count: ", end - start)

    return wrapper


# 提取url里id的装饰器

def get_book_id(url):
    def wrapper(func):
        try:
            book_id = url if "_" in url else re.findall(r"\d+", url)[-1]
            func(book_id)
        except Exception as error:
            print(error)

    return wrapper
