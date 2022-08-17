from HttpUtil import *


class XbookbenAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id):
        return etree.HTML(get("https://www.xbookben.net/txt/{}.html".format(book_id)))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url):
        return etree.HTML(get(api_url=chapter_url, retry=5))


def get_chapter_info(chapter_url: str, index: int, content: str = "", retry: int = 0) -> [dict, None]:
    response = get(api_url="https://www.xbookben.net" + chapter_url, retry=retry)
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
