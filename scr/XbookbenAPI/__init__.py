from HttpUtil import *
from scr import rule


def get_book_info(book_id: str):
    if Vars.current_book_type == "Xbookben":
        book_rule = rule.XbookbenRule
    else:
        raise Exception("[error] app type not found, app type:", Vars.current_book_type)

    if Vars.current_book_type == "Linovel":
        book_rule = rule.LinovelRule
    if Vars.current_book_type == "Dingdian":
        book_rule = rule.DingdianRule
    if Vars.current_book_type == "Xbookben":
        book_rule = rule.XbookbenRule

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


def get_chapter_info(chapter_url: str, index: int, content: str = "", retry: int = 0) -> [dict, None]:
    response = get(api_url=chapter_url, retry=retry)
    if isinstance(response, str):
        html_string_etree = etree.HTML(response)
        chapter_title = html_string_etree.xpath('//*[@id="mlfy_main_text"]/h1/text()')[0].strip()
        content_line_list = html_string_etree.xpath('//*[@id="TextContent"]')[0]
        for content_line in content_line_list:
            if content_line.text is not None and len(content_line.text.strip()) != 0:
                content += content_line.text.strip() + "\n"

        # return a dict with chapter info
        return chapter_info_json(index=index, url=chapter_url, content=content, title=chapter_title)
    else:
        if retry <= 10:
            return get_chapter_info(chapter_url, index, content, retry + 1)
        return print("get chapter info failed, chapter_url is {}".format(chapter_url))
