from scr import rule, Xbookben, Linovel, Dingdian

from HttpUtil import *


def get_book_information(book_id: str):
    if Vars.current_book_type == "Xbookben":
        book_rule = rule.XbookbenRule
        result_etree = Xbookben.XbookbenAPI.get_book_info_by_book_id(book_id)
    elif Vars.current_book_type == "Dingdian":
        book_rule = rule.DingdianRule
        result_etree = Dingdian.DingdianAPI.get_book_info_by_book_id(book_id)
    elif Vars.current_book_type == "Linovel":
        book_rule = rule.LinovelRule
        result_etree = Linovel.LinovelAPI.get_book_info_by_book_id(book_id)
    else:
        raise Exception("[error] app type not found, app type:", Vars.current_book_type)

    book_id = book_id
    book_img = result_etree.xpath(book_rule.book_img)
    book_name = result_etree.xpath(book_rule.book_name)
    book_author = result_etree.xpath(book_rule.book_author)
    book_state = result_etree.xpath(book_rule.book_state)
    book_label = result_etree.xpath(book_rule.book_label)
    last_chapter_title = result_etree.xpath(book_rule.last_chapter_title)
    book_words = result_etree.xpath(book_rule.book_words)
    book_update_time = result_etree.xpath(book_rule.book_update_time)
    chapter_url_list = [i for i in result_etree.xpath(book_rule.chapter_url_list)]

    return book_info_json(
        book_id=book_id,
        book_name=book_name[0] if len(book_name) > 0 else "",
        book_words=book_words[0] if book_words else None,
        cover_url=book_img[0] if book_img else None,
        author_name=book_author[0] if book_author else None,
        book_status=book_state[0] if book_state else None,
        book_tag=book_label[0] if book_label else None,
        last_chapter_title=last_chapter_title[0] if last_chapter_title else None,
        book_uptime=book_update_time[0] if book_update_time else None,
        chapter_url_list=chapter_url_list
    )
