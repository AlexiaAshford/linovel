from HttpUtil import *


def get_book_info(book_id: str):
    response = etree.HTML(get(f"https://www.xbookben.net/txt/{book_id}.html"))[0]
    book_img = response.xpath('/html/body/div/div[2]/div/div/div[1]/span/img/@src')[0]
    book_title = response.xpath('/html/body/div/div[2]/div/div/div[2]/h1/text()')[0]
    book_author = response.xpath('/html/body/div/div[2]/div/div/div[2]/p/strong[1]/span/text()')[0]
    book_state = response.xpath('/html/body/div/div[2]/div/div/div[2]/p/strong[3]/span/text()')[0]
    book_label = response.xpath('/html/body/div/div[2]/div/div/div[2]/p/strong[2]/span/text()')[0]
    last_chapter_title = response.xpath('//*[@id="Contents"]/div[1]/p/a/text()')[0]
    book_number = response.xpath('/html/body/div/div[2]/div/div/div[2]/p/strong[4]/span/text()')[0]
    book_update_time = response.xpath('//*[@id="Contents"]/div[1]/p/small/text()')[0].strip("——左边按钮目录正序倒序")
    chapter_url_list = ["https://www.xbookben.net" + i for i in response.xpath('//*[@id="chapterList"]/li/a/@href')]
    return book_info_json(
        book_id=book_number,
        book_name=book_title,
        cover_url=book_img,
        author_name=book_author,
        book_status=book_state,
        book_tag=book_label,
        last_chapter_title=last_chapter_title,
        book_uptime=book_update_time,
        chapter_url_list=chapter_url_list
    )
