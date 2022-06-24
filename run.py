import api
import book


def shell_download_book():
    book_info = api.get_book_info("111000")
    if book_info is not None:
        download = book.Book(book_info)
        download.init_content_config()
        download.download_book()
        download.save_content_json()
        download.merge_text_file()


if __name__ == '__main__':
    shell_download_book()
