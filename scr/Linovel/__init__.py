from HttpUtil import *


class LinovelAPI:
    @staticmethod
    def get_book_info_by_book_id(book_id: str):
        return etree.HTML(get("https://www.linovel.net/book/{}.html".format(book_id)))

    @staticmethod
    def get_chapter_info_by_chapter_id(chapter_url: str):
        return etree.HTML(get(api_url="https://www.linovel.net" + chapter_url, retry=5))

    @staticmethod
    def get_book_info_by_keyword(keyword: str):
        return etree.HTML(get(api_url="https://www.linovel.net/search/", params={"kw": keyword}))


def get_chapter_info(chapter_url: str, index: int, content: str = "", retry: int = 0) -> [dict, None]:
    html_string_etree = LinovelAPI.get_chapter_info_by_chapter_id(chapter_url)
    chapter_title = html_string_etree.xpath('//div[@class="article-title"]')[0].text.strip()
    content_text_list = html_string_etree.xpath('//div[@class="article-text"]/p')
    image_list = get_chapter_cover(html_string_etree)  # get chapter cover from html string

    for book in content_text_list:
        if book.text is not None and len(book.text.strip()) != 0:
            content += book.text.strip() + "\n"

    return chapter_info_json(
        index=index, url=chapter_url,
        content=content, title=chapter_title, image_list=image_list
    )  # return a dict with chapter info


def get_sort(tag_name: str, page: int, retry: int = 0):  # get sort from url by page
    params = {"sort": "words", "sign": "-1", "page": page}
    response = get(api_url="https://www.linovel.net/cat/-1.html", params=params, retry=retry)
    if isinstance(response, str):
        sort_html_list = etree.HTML(response).xpath('//a[@class="book-name"]')
        sort_info_list = [i.get('href').split('/')[-1][:-5] for i in sort_html_list]
        if sort_info_list and len(sort_info_list) != 0:
            return sort_info_list
    else:
        if retry <= 10:
            return get_sort(tag_name, page, retry + 1)
        return print("get sort failed, page is {}".format(page))


def search_book(book_name: str) -> [list, None]:
    response = get(api_url="https://www.linovel.net/search/", params={"kw": book_name})
    if response is not None and isinstance(response, str):
        html_str = response.split('<div class="rank-book-list">')[1]
        book_id_list = re.findall(r'<a href="/book/(\d+).html"', str(html_str))
        if len(book_id_list) != 0:
            return book_id_list
        else:
            return []
        # print(book_id)


def get_chapter_cover(html_string: [str, etree.ElementTree]) -> [list, None]:
    img_url_list = [
        img_url.get('src') for img_url in html_string.xpath('//div[@class="article-text"]//img')
    ]
    if isinstance(img_url_list, list) and len(img_url_list) != 0:
        return img_url_list
    else:
        return []
