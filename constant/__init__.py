from config import *


class NovelRule:
    def __init__(self):
        self.book_img = Vars.current_book_source.get("data")['book_img']
        self.book_name = Vars.current_book_source.get("data")['book_name']
        self.book_author = Vars.current_book_source.get("data")['book_author']
        self.chapter_url_list = Vars.current_book_source.get("data")['chapter_url_list']
        self.book_state = Vars.current_book_source.get("data")['book_state']
        self.book_label = Vars.current_book_source.get("data")['book_label']
        self.book_intro = Vars.current_book_source.get("data")['book_intro']
        self.last_chapter_title = Vars.current_book_source.get("data")['last_chapter_title']
        self.book_words = Vars.current_book_source.get("data")['book_words']
        self.book_update_time = Vars.current_book_source.get("data")['book_update_time']
        self.chapter_title = Vars.current_book_source.get("data")['chapter_title']
        self.chapter_content = Vars.current_book_source.get("data")['chapter_content']


class WebRule:
    class XbookbenRule:
        class Search:
            book_name = '//*[@id="hism"]/a/img/@alt'
            book_id = '//*[@id="hism"]/h3/a/@href'

    class LinovelRule:
        class Search:
            book_name = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@alt'
            book_id = '/html/body/div[4]/div[3]/div[1]/a/@href'

    class BoluobaoRule:
        class Search:
            book_name = '/html/body/form/table[5]/tbody/tr/td/ul[1]/li/strong/a/text()'
            book_id = '/html/body/form/table[5]/tbody/tr/td/ul[1]/li[2]/strong/a'
            '/html/body/form/table[5]/tbody/tr/td/ul[1]/li[2]/strong/a'

    class BiqugeRule:
        class Search:
            book_name = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@alt'
            book_id = '/html/body/div[4]/div[3]/div[1]/a/@href'

    class BalingRule:
        class Search:
            book_name = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@alt'
            book_id = '/html/body/div[4]/div[3]/div[1]/a/@href'
