class NovelRule:
    def __init__(self, novel_rule):
        self.novel_rule = novel_rule
        self.book_img = novel_rule['book_img']
        self.book_name = novel_rule['book_name']
        self.book_author = novel_rule['book_author']
        self.chapter_url_list = novel_rule['chapter_url_list']
        self.book_state = novel_rule['book_state']
        self.book_label = novel_rule['book_label']
        self.book_intro = novel_rule['book_intro']
        self.last_chapter_title = novel_rule['last_chapter_title']
        self.book_words = novel_rule['book_words']
        self.book_update_time = novel_rule['book_update_time']
        self.chapter_title = novel_rule['chapter_title']
        self.chapter_content = novel_rule['chapter_content']


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
