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
        description = epub.EpubHtml(title='简介信息', file_name='0000-000000-intro.xhtml', lang='zh-CN')
        description.content = '<html><head></head><body>\n'
        description.content += '<h1>小说简介</h1>\n'
        description.content += '<p>书籍书名:{}</p>\n'.format(Vars.current_book.book_name)
        description.content += '<p>书籍序号:{}</p>\n'.format(Vars.current_book.book_id)
        description.content += '<p>书籍作者:{}</p>\n'.format(Vars.current_book.book_author)
        if Vars.current_book.book_status is not None:
            description.content += '<p>书籍状态:{}</p>\n'.format(Vars.current_book.book_status)
        if Vars.current_book.book_words is not None:
            description.content += '<p>字数信息:</p>{}\n'.format(Vars.current_book.book_words)
        if Vars.current_book.last_chapter_title is not None:
            description.content += '<p>最新章节:{}</p>\n'.format(Vars.current_book.last_chapter_title)
        if Vars.current_book.book_tag is not None:
            description.content += '<p>系统标签:{}</p>\n'.format(Vars.current_book.book_tag)
        if Vars.current_book.book_intro is not None:
            description.content += '<p>简介信息:</p>{}\n'.format(Vars.current_book.book_intro)
        description.content += '</body></html>'
        self.epub.add_item(description)
        self.EpubList.append(description)
        book_detailed = re.sub(r"\n+", "\n", re.sub('<[^>]+>|<p>|</p>', "\n", description.content).strip())
        print(book_detailed)  # print book detailed information to console
        return book_detailed + "\n\n"  # return book detailed information as string

    def download_cover_and_add_epub(self):  # download cover image and add to epub file as cover
        if Vars.current_book_type == "Dingdian":
            Vars.current_book.cover = "https://www.ddyueshu.com" + Vars.current_book.cover
        elif Vars.current_book_type == "Biquge":
            Vars.current_book.cover = "https://www.qu-la.com" + Vars.current_book.cover
        cover_file_path = os.path.join(make_dirs("cover"), Vars.current_book.book_name + ".png")
        if not os.path.exists(cover_file_path):
            open(cover_file_path, 'wb').write(get_cover_image(Vars.current_book.cover))
        cover_image = open(cover_file_path, 'rb').read()
        if cover_image is not None:  # if cover image is not None ,then add to epub file
            self.epub.set_cover("cover.png", cover_image)  # add cover image to epub file
        else:
            self.download_cover_and_add_epub()

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
