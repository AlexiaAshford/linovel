from scr import rule, Xbookben, Linovel

from HttpUtil import *


def get_book_information(book_id: str):
    if Vars.current_book_type == "Xbookben":
        book_rule = rule.XbookbenRule

        result_etree = Xbookben.XbookbenAPI.get_book_info_by_book_id(book_id)
    # elif Vars.current_book_type == "Dingdian":
    #     chapter_info = DingdianAPI.get_chapter_info(chapter_url, index)
    elif Vars.current_book_type == "Linovel":
        book_rule = rule.LinovelRule
        result_etree = Linovel.LinovelAPI.get_book_info_by_book_id(book_id)
    else:
        raise Exception("[error] app type not found, app type:", Vars.current_book_type)

    book_id = book_id
    book_img = result_etree.xpath(book_rule.book_img)[0]
    book_name = result_etree.xpath(book_rule.book_name)[0]
    book_author = result_etree.xpath(book_rule.book_author)[0]
    print(result_etree.xpath(book_rule.book_state))
    book_state = result_etree.xpath(book_rule.book_state)[0]
    book_label = result_etree.xpath(book_rule.book_label)[0]
    last_chapter_title = result_etree.xpath(book_rule.last_chapter_title)[0]
    book_words = result_etree.xpath(book_rule.book_words)[0]
    book_update_time = result_etree.xpath(book_rule.book_update_time)[0].strip("——左边按钮目录正序倒序")
    chapter_url_list = [i for i in result_etree.xpath(book_rule.chapter_url_list)]

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
