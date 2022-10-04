from ebooklib import epub
from config import *
import requests
import uuid


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


class EpubHtml:
    def __init__(self):
        self.description = ""
        self.html_template = epub.EpubHtml

    def set_description(self):
        self.description = "<html><head></head><body>\n<h1>小说简介</h1>"
        if Vars.current_book.book_name is not None:
            self.description += '<p>书籍书名:{}</p>'.format(Vars.current_book.book_name)
        if Vars.current_book.book_id is not None:
            self.description += '<p>书籍序号:{}</p>'.format(Vars.current_book.book_id)
        if Vars.current_book.book_author is not None:
            self.description += '<p>书籍作者:{}</p>\n'.format(Vars.current_book.book_author)
        if Vars.current_book.book_status is not None:
            self.description += '<p>书籍状态:{}</p>\n'.format(Vars.current_book.book_status)
        if Vars.current_book.book_words is not None:
            self.description += '<p>字数信息:</p>{}\n'.format(Vars.current_book.book_words.replace("字数：", ""))
        if Vars.current_book.last_chapter_title is not None:
            self.description += '<p>最新章节:{}</p>\n'.format(Vars.current_book.last_chapter_title)
        if Vars.current_book.book_tag is not None:
            self.description += '<p>系统标签:{}</p>\n'.format(Vars.current_book.book_tag)
        if Vars.current_book.book_intro is not None:
            self.description += '<p>简介信息:</p>{}\n'.format(Vars.current_book.book_intro)
        self.description += '</body></html>'
        data_template = self.html_template(
            title='小说简介', file_name='0000-000000-intro.xhtml', lang='zh-CN'
        )
        data_template.content = self.description
        return data_template

    def set_chapter(self, chapter_title: str, content: str, serial_number: str):
        chapter = self.html_template(
            title=chapter_title, file_name=str(serial_number).rjust(4, "0") + '.xhtml', lang='zh-CN',
            uid=uuid.uuid4().hex
        )  # create chapter object and set chapter title, file name, language, uid
        chapter.content = '</p>\r\n<p>'.join(content)
        return chapter


class EpubFile(epub.EpubBook):
    def __init__(self):
        super().__init__()
        self.toc = []
        self.EpubList = list()
        self.template = EpubHtml()

    def set_epub_book_info(self):
        self.set_language('zh-CN')  # set epub file language
        self.set_identifier(Vars.current_book.book_id)
        self.set_title(Vars.current_book.book_name)
        self.add_author(Vars.current_book.book_author)
        if Vars.current_book.cover:
            Vars.current_epub.download_cover_and_add_epub()
        else:
            print("cover is None, can't download the epub cover！")
        description = self.template.set_description()
        book_detailed = re.sub(r"\n+", "\n", re.sub('<[^>]+>|<p>|</p>', "\n", description.content).strip())
        write_text(
            path_name=os.path.join(Vars.current_book.out_text_path, Vars.current_book.book_name + ".txt"),
            content=book_detailed + "\n\n"
        )  # write book information to text file in downloads folder and show book name, author and chapter count
        print(book_detailed)  # print book detailed information to console
        self.add_item(description)
        self.EpubList.append(description)

    def download_cover_and_add_epub(self):  # download cover image and add to epub file as cover
        if Vars.current_book_type == "https://www.ddyueshu.com":
            Vars.current_book.cover = "https://www.ddyueshu.com" + Vars.current_book.cover
        elif Vars.current_book_type == "Biquge":
            Vars.current_book.cover = "https://www.qu-la.com" + Vars.current_book.cover
        elif Vars.current_book_type == "Trxs":
            Vars.current_book.cover = "http://trxs.cc" + Vars.current_book.cover
        cover_file_path = os.path.join(make_dirs("cover"), Vars.current_book.book_name + ".png")
        if not os.path.exists(cover_file_path):
            open(cover_file_path, 'wb').write(get_cover_image(Vars.current_book.cover))
        cover_image = open(cover_file_path, 'rb').read()
        if cover_image is not None:  # if cover image is not None ,then add to epub file
            self.set_cover("cover.png", cover_image)  # add cover image to epub file
        else:
            self.download_cover_and_add_epub()

    def add_chapter_in_epub_file(self, **kwargs):
        chapter_serial = self.template.set_chapter(
            kwargs.get("title"), kwargs.get("content"), kwargs.get("index"))
        self.add_item(chapter_serial)  # add chapter to epub file as item
        self.EpubList.append(chapter_serial)  # add chapter to epub list

    def out_put_epub_file(self):  # save epub file to local
        # the path to save epub file to local
        self.toc = tuple(self.EpubList)
        self.spine.extend(self.EpubList)
        self.add_item(epub.EpubNcx()), self.add_item(epub.EpubNav())
        save_epub_file = os.path.join(Vars.current_book.out_text_path, Vars.current_book.book_name + '.epub')
        epub.write_epub(save_epub_file, self)  # save epub file to out_path directory with book_name.epub
