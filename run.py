import LinovelAPI
import book


def shell_download_book(book_id: str):
    book_info = LinovelAPI.get_book_info(book_id)
    if book_info is not None:
        download = book.Book(book_info)
        download.init_content_config()
        download.multi_thread_download_book()


def shell_tag_scanner(max_page: int = 622):
    for page in range(max_page):
        tag_bookid_list = LinovelAPI.get_sort(page)
        for book_id in tag_bookid_list:
            shell_download_book(book_id)


if __name__ == '__main__':
    # shell_download_book()
    shell_tag_scanner()
