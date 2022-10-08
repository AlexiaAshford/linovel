from config import *
from . import decodes, API


def init_book_info_template(book_info_html):  # return book info json book info html
    book_img = book_info_html.xpath(Vars.current_book_rule.book_img)
    book_name = book_info_html.xpath(Vars.current_book_rule.book_name)
    book_author = book_info_html.xpath(Vars.current_book_rule.book_author)
    book_state = book_info_html.xpath(Vars.current_book_rule.book_state)
    book_label = book_info_html.xpath(Vars.current_book_rule.book_label)
    last_chapter_title = book_info_html.xpath(Vars.current_book_rule.last_chapter_title)
    book_words = book_info_html.xpath(Vars.current_book_rule.book_words)
    book_update_time = book_info_html.xpath(Vars.current_book_rule.book_update_time)
    book_intro = book_info_html.xpath(Vars.current_book_rule.book_intro)

    Vars.current_book["bookName"] = book_name[0] if len(book_name) > 0 else None
    Vars.current_book["authorName"] = book_author[0] if book_author else None
    Vars.current_book["bookCoverUrl"] = book_img[0] if book_img else None
    Vars.current_book["bookWords"] = book_words[0] if book_words else None
    Vars.current_book["bookTag"] = book_label[0] if book_label else None
    Vars.current_book["bookIntro"] = book_intro[0] if book_intro else None
    Vars.current_book["bookStatus"] = book_state[0] if book_state else None
    Vars.current_book["last_chapter_title"] = last_chapter_title[0] if last_chapter_title else None
    Vars.current_book["book_update_time"] = book_update_time[0] if book_update_time else None


def init_chapter_url_list(book_info_html, max_retry: int = 3):
    if Vars.current_book_source.get("url").get("catalogue_info") != "":
        catalogue = Vars.current_book_api.get_catalogue_info_by_book_id(Vars.current_book["bookId"])
        if Vars.current_book_type == "https://www.linovelib.com":
            chapter_url_list = [i for i in catalogue.xpath(Vars.current_book_rule.chapter_url_list) if "novel" in i]
        else:
            chapter_url_list = [i for i in catalogue.xpath(Vars.current_book_rule.chapter_url_list)]
    else:
        chapter_url_list = [i for i in book_info_html.xpath(Vars.current_book_rule.chapter_url_list)]
        if Vars.current_book_type == "https://www.ddyueshu.com":
            chapter_url_list = chapter_url_list[6:]  # del first 6 chapter, because the first 6 chapter is not ordered

    if not chapter_url_list:
        if max_retry >= 0:
            return init_chapter_url_list(book_info_html, max_retry - 1)
        else:
            return print("retry 3 times, but still empty, book_id is {}".format(Vars.current_book["bookId"]))
    Vars.current_book["chapter_url_list"] = chapter_url_list
