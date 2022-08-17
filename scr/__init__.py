from scr import rule

from HttpUtil import *

def get_book_information(book_id: str):
    if Vars.current_book_type == "Xbookben":
        book_rule = rule.XbookbenRule
    else:
        raise Exception("[error] app type not found, app type:", Vars.current_book_type)

    book_id = book_id
    response = etree.HTML(get(book_rule.descriptors_url.format(book_id)))
    book_img = response.xpath(book_rule.book_img)[0]
    book_name = response.xpath(book_rule.book_name)[0]
    book_author = response.xpath(book_rule.book_author)[0]
    book_state = response.xpath(book_rule.book_state)[0]
    book_label = response.xpath(book_rule.book_label)[0]
    last_chapter_title = response.xpath(book_rule.last_chapter_title)[0]
    book_words = response.xpath(book_rule.book_words)[0]
    book_update_time = response.xpath(book_rule.book_update_time)[0].strip("——左边按钮目录正序倒序")
    chapter_url_list = ["https://www.xbookben.net" + i for i in response.xpath(book_rule.chapter_url_list)]

    return book_info_json(
        book_id=book_id,
        book_name=book_name,
        book_words=book_words,
        cover_url=book_img,
        author_name=book_author,
        book_status=book_state,
        book_tag=book_label,
        last_chapter_title=last_chapter_title,
        book_uptime=book_update_time,
        chapter_url_list=chapter_url_list
    )
