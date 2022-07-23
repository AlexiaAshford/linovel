from HttpUtil import *


def get_book_info(book_id: str):
    book_id = book_id
    response = etree.HTML(get(f"https://www.xbookben.net/txt/{book_id}.html"))[0]
    book_img = response.xpath('/html/body/div/div[2]/div/div/div[1]/span/img/@src')[0]
    book_title = response.xpath('/html/body/div/div[2]/div/div/div[2]/h1/text()')[0]
    book_author = response.xpath('/html/body/div/div[2]/div/div/div[2]/p/strong[1]/span/text()')[0]
    book_state = response.xpath('/html/body/div/div[2]/div/div/div[2]/p/strong[3]/span/text()')[0]
    book_label = response.xpath('/html/body/div/div[2]/div/div/div[2]/p/strong[2]/span/text()')[0]
    last_chapter_title = response.xpath('//*[@id="Contents"]/div[1]/p/a/text()')[0]
    book_words = response.xpath('/html/body/div/div[2]/div/div/div[2]/p/strong[4]/span/text()')[0]
    book_update_time = response.xpath('//*[@id="Contents"]/div[1]/p/small/text()')[0].strip("——左边按钮目录正序倒序")
    chapter_url_list = ["https://www.xbookben.net" + i for i in response.xpath('//*[@id="chapterList"]/li/a/@href')]

    return book_info_json(book_id=book_id,
                          book_name=book_title,
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
