class XbookbenRule:
    descriptors_url = "https://www.xbookben.net/txt/{}.html"
    book_img = '/html/body/div/div[2]/div/div/div[1]/span/img/@src'
    book_name = '/html/body/div/div[2]/div/div/div[2]/h1/text()'
    book_author = '/html/body/div/div[2]/div/div/div[2]/p/strong[1]/span/text()'
    chapter_url_list = '//*[@id="chapterList"]/li/a/@href'
    book_state = '/html/body/div/div[2]/div/div/div[2]/p/strong[3]/span/text()'
    book_label = '/html/body/div/div[2]/div/div/div[2]/p/strong[2]/span/text()'
    last_chapter_title = '//*[@id="Contents"]/div[1]/p/a/text()'
    book_words = '/html/body/div/div[2]/div/div/div[2]/p/strong[4]/span/text()'
    book_update_time = '//*[@id="Contents"]/div[1]/p/small/text()'


class DingdianRule:
    descriptors_url = "https://www.ddyueshu.com/{}"
    book_img = '//div[@id="fmimg"]/img'
    book_name = '//*[@id="info"]/h1'
    book_author = '//*[@id="info"]/p[1]'
    chapter_url_list = '//*[@id="list"]/dl/dd[*]/a/@href'
    book_state = ''
    book_label = ''
    last_chapter_title = ''
    book_words = ''
    book_update_time = ''


class LinovelRule:
    descriptors_url = "https://www.linovel.net/book/{}.html"
    book_img = '//div[@class="book-cover"]/a/@href'
    book_name = '//h1[@class="book-title"]/text()'
    book_author = '//div[@class="author-frame"]//a/text()'
    chapter_url_list = '//div[@class="chapter"]/a/@href'
    book_state = ''
    book_label = ''
    last_chapter_title = ''
    book_words = ''
    book_update_time = ''
