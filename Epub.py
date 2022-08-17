from ebooklib import epub
from config import *
import requests


def get_cover_image(cover_url: str):
    retry = 0
    while True:
        try:
            response = requests.get(cover_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '})
            if response.status_code == 304 or response.status_code == 200:
                return response.content
            retry += 1
            if retry > 5:
                return None
        except Exception as error:
            retry += 1
            if retry > 5:
                print("get_cover_image", error)
                return None


class EpubFile:
    def __init__(self):
        self.epub = epub.EpubBook()
        self.EpubList = list()
        self.epub.set_language('zh-CN')
        self.save_epub_file = ""
        self.epub.set_identifier(Vars.current_book.book_id)
        self.epub.set_title(Vars.current_book.book_name)
        self.epub.add_author(Vars.current_book.book_author)

    def add_the_book_information(self) -> str:
        intro_ = epub.EpubHtml(title='简介信息', file_name='0000-000000-intro.xhtml', lang='zh-CN')
        intro_.content = '<html><head></head><body><h1>简介</h1>'
        intro_.content += '<p>书籍书名:{}</p> '.format(Vars.current_book.book_name)

        intro_.content += '<p>书籍序号:{}</p>'.format(Vars.current_book.book_id)
        intro_.content += '<p>书籍作者:{}</p>'.format(Vars.current_book.book_author)
        # intro_.content += '<p>最新章节:{}</p><p>系统标签:{}</p>'.format(up_chapter, novel_tag)
        # intro_.content += '<p>简介信息:</p>{}</body></html>'.format(intro)
        intro_.content += '</body></html>'
        self.epub.add_item(intro_)
        self.EpubList.append(intro_)
        book_detailed = re.compile('<[^>]+>').sub(
            "", intro_.content.replace(' ', '').replace('\n', '').
            replace('<p>', "\n").replace('</p>', "\n").replace('\n\n', "\n"))
        print(book_detailed)  # print book detailed information to console
        return book_detailed  # return book detailed information as string

    def download_cover_and_add_epub(self):  # download cover image and add to epub file as cover
        if Vars.current_book_type == "Xbookben":
            book_host = ""
        elif Vars.current_book_type == "Dingdian":
            book_host = "https://www.ddyueshu.com"
        elif Vars.current_book_type == "Linovel":
            book_host = ""
        else:
            book_host = ""
        # print(book_host + Vars.current_book.cover)
        download_png_file = get_cover_image(book_host + Vars.current_book.cover)  # get cover image from url
        if download_png_file is not None:  # if cover image is not None ,then add to epub file
            self.epub.set_cover(Vars.current_book.book_name + '.png', download_png_file)  # add cover image to epub file

    def add_chapter_in_epub_file(self, chapter_title: str, content_lines_list: str, serial_number: str):
        import uuid
        chapter_serial = epub.EpubHtml(
            title=chapter_title,
            file_name=str(serial_number).rjust(4, "0") + '.xhtml',
            lang='zh-CN',
            uid=uuid.uuid4().hex
        )  # create chapter object and set chapter title, file name, language, uid
        chapter_serial.content = '</p>\r\n<p>'.join(content_lines_list)
        self.epub.add_item(chapter_serial)  # add chapter to epub file as item
        self.EpubList.append(chapter_serial)  # add chapter to epub list

    def out_put_epub_file(self):  # save epub file to local
        # the path to save epub file to local
        self.epub.toc = tuple(self.EpubList)
        self.epub.spine = ['nav']  # add spine to epub file as spine
        self.epub.spine.extend(self.EpubList)
        self.epub.add_item(epub.EpubNcx()), self.epub.add_item(epub.EpubNav())
        epub.write_epub(self.save_epub_file, self.epub, {})  # save epub file to out_path directory with book_name.epub
