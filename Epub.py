from ebooklib import epub
from src import http_utils
from config import *
import uuid


class EpubHtml:
    def __init__(self):
        self.description = ""
        self.html_template = epub.EpubHtml

    def set_description(self):
        self.description = "<html><head></head><body>"
        if Vars.current_book.cover is not None:
            self.description += f'<img src="cover.png" alt="{Vars.current_book.book_name} 封面">'
        if Vars.current_book.book_name is not None:
            self.description += '<h1>书籍书名:{}</h1>'.format(Vars.current_book.book_name)
        if Vars.current_book.book_author is not None:
            self.description += '<h2>书籍作者:{}</h2>\n'.format(Vars.current_book.book_author)
        if Vars.current_book.book_id is not None:
            self.description += '<h3>书籍序号:{}</h3>'.format(Vars.current_book.book_id)
        if Vars.current_book.book_status is not None:
            self.description += '<h4>书籍状态:{}</h4>\n'.format(Vars.current_book.book_status)
        if Vars.current_book.book_words is not None:
            self.description += '<h4>字数信息:</h4>{}\n'.format(Vars.current_book.book_words.replace("字数：", ""))
        if Vars.current_book.last_chapter_title is not None:
            self.description += '<h4>最新章节:{}</h4>\n'.format(Vars.current_book.last_chapter_title)
        if Vars.current_book.book_tag is not None:
            self.description += '<h4>系统标签:{}</h4>\n'.format(Vars.current_book.book_tag)
        if Vars.current_book.book_intro is not None:
            self.description += '<h5>简介信息:</h5>{}\n'.format(Vars.current_book.book_intro)
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
        elif Vars.current_book_type == "https://www.qu-la.com":
            Vars.current_book.cover = "https://www.qu-la.com" + Vars.current_book.cover
        elif Vars.current_book_type == "http://www.trxs.cc":
            Vars.current_book.cover = "http://www.trxs.cc" + Vars.current_book.cover
        elif Vars.current_book_type == "http://www.trxs.cc":
            Vars.current_book.cover = "http://m.bjcan8.com" + Vars.current_book.cover
        cover_file_path = os.path.join(make_dirs("cover"), Vars.current_book.book_name + ".png")
        if not os.path.exists(cover_file_path):
            image_file = http_utils.get(api_url=Vars.current_book.cover, re_type="content")
            if image_file:
                open(cover_file_path, 'wb').write(image_file)
            else:
                print("download cover image failed, can't download the epub cover！")
        if os.path.exists(cover_file_path):
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
