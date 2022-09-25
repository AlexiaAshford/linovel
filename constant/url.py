class Site:
    class Xbookben:
        host = "https://www.xbookben.net"
        book_info_by_book_id = host + "/txt/{}.html"
        book_info_by_keyword = host + "/search"

    class Linovel:
        host = "https://www.linovel.net"
        book_info_by_book_id = host + "/book/{}.html"
        book_info_by_keyword = host + "/search/"

    class Dingdian:
        host = "https://www.ddyueshu.com/"

    class Boluobao:
        host = "https://book.sfacg.com"
        book_info_by_book_id = host + "/Novel/{}/"
        catalogue_info_by_book_id = host + "/Novel/{}/MainIndex/"
        book_info_by_keyword = "https://s.sfacg.com/"

    class Biquge:
        host = "https://www.qu-la.com"
        book_info_by_book_id = host + "/booktxt/"

    class Baling:
        host = "http://www.80zw.net"
        book_info_by_book_id = host + "/article/"
        book_info_by_chapter_id = host + "/article/{}/{}"

    class Qbtr:
        host = "https://www.qbtr.cc"
        book_info_by_book_id = host + "/changgui/{}.html"  # 书籍信息
