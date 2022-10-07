from config import *


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
        book_img = '/html/body/div/div[2]/div/div/div[1]/span/img/@src'
        book_name = '/html/body/div/div[2]/div/div/div[2]/h1/text()'
        book_author = '/html/body/div/div[2]/div/div/div[2]/p/strong[1]/span/text()'
        chapter_url_list = '//*[@id="chapterList"]/li/a/@href'
        book_state = '/html/body/div/div[2]/div/div/div[2]/p/strong[3]/span/text()'
        book_label = '/html/body/div/div[2]/div/div/div[2]/p/strong[2]/span/text()'
        book_intro = '/html/body/div/div[2]/div/div/div[2]/div[1]/p/text()'
        last_chapter_title = '//*[@id="Contents"]/div[1]/p/a/text()'
        book_words = '/html/body/div/div[2]/div/div/div[2]/p/strong[4]/span/text()'
        book_update_time = '//*[@id="Contents"]/div[1]/p/small/text()'
        chapter_title = '//*[@id="mlfy_main_text"]/h1/text()'
        chapter_content = '//*[@id="TextContent"]/p/text()'

        # chapter_cover = ''
        class Search:
            book_name = '//*[@id="hism"]/a/img/@alt'
            book_img = '//*[@id="hism"]/a/img/@src'
            book_id = '//*[@id="hism"]/h3/a/@href'

    class DingdianRule:
        book_img = '//*[@id="fmimg"]/img/@src'
        book_name = '//*[@id="info"]/h1/text()'
        book_author = '//*[@id="info"]/p[1]/text()'
        chapter_url_list = '//*[@id="list"]/dl/dd[*]/a/@href'
        book_state = '//*[@id="intro"]/p'  # 没有这个信息
        book_label = '//*[@id="wrapper"]/div[4]/div[1]/text()'
        book_intro = '//*[@id="intro"]/p/text()'
        last_chapter_title = '//*[@id="list"]/dl/dd[1]/a/text()'
        book_words = '//*[@id="intro"]/p'  # 没有这个信息
        book_update_time = '//*[@id="info"]/p[3]/text()'
        chapter_title = '//div[@class="bookname"]/h1/text()'
        chapter_content = '//*[@id="content"]/text()'
        # chapter_cover = ''

    class LinovelRule:
        book_img = '//div[@class="book-cover"]/a/@href'
        book_name = '//h1[@class="book-title"]/text()'
        book_author = '//div[@class="author-frame"]//a/text()'
        chapter_url_list = '//div[@class="chapter"]/a/@href'
        book_state = '/html/body/div[3]/div[2]/div[1]/div[2]/div[3]/span[7]/text()'
        book_label = '/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/a[1]/text()'
        book_intro = '/html/body/div[3]/div[2]/div[1]/div[5]/div[1]/div[2]/div[1]/div/text()'
        last_chapter_title = '/html/body/div[3]/div[2]/div[1]/div[5]/div[2]/div[3]/div[2]'
        book_words = '/html/body/div[3]/div[2]/div[1]/div[2]/div[3]/span[1]/text()'
        book_update_time = '/html/body/div[3]/div[2]/div[1]/div[5]/div[2]/div[3]/div[2]/div[1]/small/text()'
        chapter_title = '//div[@class="article-title"]/text()'
        chapter_content = '//div[@class="article-text"]/p/text()'

        # chapter_cover = ''
        class Search:
            book_name = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@alt'
            book_img = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@src'
            book_id = '/html/body/div[4]/div[3]/div[1]/a/@href'

    class BoluobaoRule:
        book_img = '//*[@id="hasTicket"]/div[1]/div/div[1]/a/img/@src'
        book_name = '/html/body/div[1]/div[4]/div/div[1]/div[1]/a[3]/text()'
        book_author = '/html/body/div[1]/div[5]/div/div[1]/div[2]/div[2]/div[2]/p[1]/text()'
        chapter_url_list = '/html/body/div[1]/div[3]/div/div/ul/li/a/@href'
        book_state = '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/span[2]/text()'
        book_label = '/html/body/div[1]/div[4]/div/div[1]/ul/text()'
        book_intro = '/html/body/div[1]/div[4]/div/div[1]/div[2]/p/text()'
        last_chapter_title = '/html/body/div[1]/div[4]/div/div[1]/div[2]/h3/a/text()'
        book_words = '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/span[2]/text()'
        book_update_time = '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div[2]/span/text()'
        chapter_title = '//*[@id="article"]/div[1]/h1/text()'
        chapter_content = '//*[@id="ChapterBody"]/p/text()'

        # chapter_cover = ''
        class Search:
            book_name = '/html/body/form/table[5]/tbody/tr/td/ul[1]/li/strong/a/text()'
            book_img = '//*[@id="SearchResultList1___ResultList_Cover_0"]/img/@src'
            book_id = '/html/body/form/table[5]/tbody/tr/td/ul[1]/li[2]/strong/a'
            '/html/body/form/table[5]/tbody/tr/td/ul[1]/li[2]/strong/a'

    class BiqugeRule:
        book_img = '//*[@id="fengmian"]/a/img/@src'
        book_name = '//*[@id="list"]/div[1]/div[2]/h1/text()'
        book_author = '//*[@id="list"]/div[1]/div[2]/span/text()'
        chapter_url_list = '//*[@id="list"]/div[3]/ul[2]/li/a/@href'
        book_state = '//*[@id="list"]/div[1]/div[2]/div[1]/span[2]/text()'
        book_label = '/html/body/div[1]/div[4]/div/div[1]/ul/text()'
        book_intro = '//*[@id="list"]/div[1]/div[2]/div[2]/text()'
        last_chapter_title = '//*[@id="list"]/div[2]/p[2]/a/text()'
        book_words = '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/span[2]/text()'
        book_update_time = '//*[@id="list"]/div[2]/p[2]/span/text()'
        chapter_title = '//*[@id="chapter-title"]/h1/text()'
        chapter_content = '//*[@id="txt"]/text()'

        # chapter_cover = ''
        class Search:
            book_name = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@alt'
            book_img = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@src'
            book_id = '/html/body/div[4]/div[3]/div[1]/a/@href'

    class BalingRule:
        book_img = '//*[@id="fmimg"]/img/@src'
        book_name = '//*[@id="info"]/h1/text()'
        book_author = '//*[@id="info"]/p[1]/a/text()'
        chapter_url_list = '/html/body/div[4]/div/ul/li/a/@href'
        book_state = '//*[@id="list"]/div[1]/div[2]/div[1]/span[2]/text()'
        book_label = '/html/body/div[1]/div[4]/div/div[1]/ul/text()'
        book_intro = '//*[@id="intro"]/text()'
        last_chapter_title = '//*[@id="list"]/div[2]/p[2]/a/text()'
        book_words = '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/span[2]/text()'
        book_update_time = '//*[@id="info"]/p[3]/text()'
        chapter_title = '//*[@id="content"]/h1/text()'
        chapter_content = '//*[@id="htmlContent"]/text()'

        # chapter_cover = ''
        class Search:
            book_name = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@alt'
            book_img = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@src'
            book_id = '/html/body/div[4]/div[3]/div[1]/a/@href'

    class QbtrRule:
        book_img = '/html/notfound'  # 没有这个信息
        book_name = '/html/body/div[3]/div[2]/div/h1/text()'
        book_author = '/html/body/div[3]/div[2]/div/div[1]/span/text()'
        chapter_url_list = '/html/body/div[3]/div[3]/ul/li/a/@href'
        book_state = '/html/notfound'  # 没有这个信息
        book_label = '/html/notfound'  # 没有这个信息
        book_intro = '/html/body/div[3]/div[2]/div/p/text()'
        last_chapter_title = '//*[@id="list"]/dl/dd[1]/a/text()'
        book_words = '/html/notfound'  # 没有这个信息
        book_update_time = '/html/body/div[3]/div[2]/div/div[1]/text()'
        chapter_title = '//*[@id="readContent_set"]/div[2]/div[1]/h1/text()'
        chapter_content = '//*[@id="readContent_set"]/div[2]/div[2]/p/text()'
        # chapter_cover = ''

    class TrxsRule:
        book_img = '/html/body/div[3]/div[2]/div[1]/img/@src'
        book_name = '/html/body/div[3]/div[2]/div[2]/h1/text()'
        book_author = '/html/body/div[3]/div[2]/div[2]/div[1]/span/a/text()'
        chapter_url_list = '/html/body/div[3]/div[3]/ul/li/a/@href'
        book_state = '/html/notfound'  # 没有这个信息
        book_label = '/html/notfound'  # 没有这个信息
        book_intro = '/html/body/div[3]/div[2]/div[2]/p/text()'
        last_chapter_title = '//*[@id="list"]/dl/dd[1]/a/text()'
        book_words = '/html/notfound'  # 没有这个信息
        book_update_time = '/html/body/div[3]/div[2]/div[2]/div[1]/text()'
        chapter_title = '/html/body/div[3]/div/div[2]/div[1]/h1/text()'
        chapter_content = '/html/body/div[3]/div/div[2]/div[2]/p/text()'
        # chapter_cover = ''

    class PopoRule:
        book_img = '//*[@id="rs"]/@src'
        book_name = '/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/h3/text()'
        book_author = '/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/dl/dd[1]/a/text()'
        chapter_url_list = '//*[@id="w0"]/div/div/div[2]/a/@href'
        book_state = '/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/dl/dd[3]/text()'
        book_label = '/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/dl/dd[2]/span/text()'
        book_intro = '/html/body/div[4]/div[2]/div[1]/div[5]/p/text()'
        last_chapter_title = '/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/dl/dd[3]/span/text()'
        book_words = '/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[2]/table[1]/tbody/tr[3]/td/text()'
        book_update_time = '//*[@id="list"]/div[2]/p[2]/span/text()'
        chapter_title = '//*[@id="readmask"]/div/h2/text()'
        chapter_content = '//*[@id="readmask"]/div/p/text()'

        # chapter_cover = ''
        class Search:
            book_name = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@alt'
            book_img = '/html/body/div[4]/div[3]/div[1]/a/div/div/img/@src'
            book_id = '/html/body/div[4]/div[3]/div[1]/a/@href'

    class LinovelibRule:
        book_img = '/html/body/div[2]/div[3]/div[1]/div[1]/div[1]/img/@src'
        book_name = '/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/h1/text()'
        book_author = '/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/a/text()'
        chapter_url_list = '/html/body/div[2]/div[3]/div[2]/div[2]/div/ul/li/a/@href'
        book_state = '/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/div[1]/a[1]/text()'
        book_label = '/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/dl/dd[2]/span/text()'
        book_intro = '/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/div[3]/p/text()'
        last_chapter_title = '/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/a/text()'
        book_words = '/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/span[2]/i/text()'
        book_update_time = '/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/span[1]/i/text()'
        chapter_title = '//*[@id="mlfy_main_text"]/h1/text()'
        chapter_content = '//*[@id="TextContent"]/p/text()'
