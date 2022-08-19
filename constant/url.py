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
        host = "https://www.ddyueshu.com"
