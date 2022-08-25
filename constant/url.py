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
        book_info_by_keyword = host + "https://s.sfacg.com/?Key={}&S=1&SS=0"

    class Biquge:
        host = "https://www.qu-la.com"
        book_info_by_book_id = host + "/booktxt/"
