from HttpUtil import *


def get_book_info():
    response = etree.HTML(get("http://www.xxsy.net/info/1588172.html"))[0]
    book_img = response.xpath("//dl[@class='bookprofile']/dt/img/@src")[0]
    book_title = response.xpath("//dl[@class='bookprofile']/dd/div[@class='title']/h1/text()")[0]
    book_author = response.xpath("//dl[@class='bookprofile']/dd/div[@class='title']/span/a/text()")[0]
    book_state = response.xpath("//dl[@class='bookprofile']/dd/p[@class='sub-cols']/span[2]/text()")[0]
    book_label = response.xpath("//dl[@class='bookprofile']/dd/p[@class='sub-tags']//a/text()")
    book_category = response.xpath("//dl[@class='bookprofile']/dd/p[@class='sub-cols']/span[3]/text()")[0]
    book_update_time = response.xpath("//dl[@class='bookprofile']/dd/div[@class='sub-newest']/p/span/text()")[0]
    book_number = response.xpath("//dl[@class='bookprofile']/dd/p[@class='sub-data']/span[1]/em/text()")[0]
    book_detailed = response.xpath("//div[@class='book-profile']/dl/dd//p/text()")

    return book_info_json(
        book_id=book_number,
        book_name=book_title,
        cover_url=book_img,
        author_name=book_author,
        book_status=book_state,
        book_tag=','.join([str(i) for i in book_label]) if book_label else None,
        book_uptime=book_update_time,
        book_intro=','.join([str(i) for i in book_detailed]) if book_detailed else None,
    )
