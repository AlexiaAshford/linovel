import Epub
import src
from config import *
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


class Chapter:
    def __init__(self, chapter_id: str, index: int):
        self.chapter_index = index
        self.chapter_id = chapter_id
        self.next_url = self.chapter_id.replace(".html", "_2.html")
        self.chapter_page = None
        self.image_list = []

        # def chapter_info(self):

    #     return Vars.current_book_api.get_chapter_info_by_chapter_id(self.chapter_id)

    @property
    def chapter_title(self) -> str:
        chapter_name = self.chapter_page.xpath(Vars.current_source.data.chapter_title)
        if isinstance(chapter_name, list) and len(chapter_name) != 0:
            return chapter_name[0].strip()
        return chapter_name.strip()

    @property
    def content_page_html(self):
        if Vars.current_book_type == "https://www.xbookben.net":
            next_page = Vars.current_book_api.get_chapter_info_by_chapter_id(self.next_url)
            return self.chapter_page.xpath(Vars.current_source.data.chapter_content) + next_page.xpath(
                Vars.current_source.data.chapter_content)

        return self.chapter_page.xpath(Vars.current_source.data.chapter_content)

    @property
    def chapter_json(self):
        self.chapter_page = Vars.current_book_api.get_chapter_info_by_chapter_id(self.chapter_id)
        return {
            "chapterIndex": self.chapter_index,
            "chapter_url": self.chapter_id,
            "chapterTitle": self.chapter_title,
            "chapterContent": self.standard_content,
            "imageList": self.image_list if self.image_list is not None else []
        }

    @property
    def standard_content(self) -> str:  # return a standard content
        content = "\n".join(self.content)  # list to str
        if Vars.current_book_type == "https://www.linovelib.com":
            content = src.decodes.decode_content_text(content)  # decode content text
        for delete_info in Msg.del_chapter_advertisement_list:  # delete chapter advertisement text
            content = re.sub(delete_info, '', content)
        return content

    @property
    def content(self):
        return [page.strip() for page in self.content_page_html if page is not None and len(page.strip()) != 0]


class BookConfig:
    def __init__(self):
        self.content_config = []
        self.threading_list = []

        make_dirs(Vars.cfg.data['config_path'])
        self.save_config_path = os.path.join(Vars.cfg.data['config_path'], Vars.current_book.bookName + ".json")

    def init_content_config(self):
        if os.path.exists(self.save_config_path):
            self.content_config = read_text(self.save_config_path, json_load=True)
            if self.content_config is None:
                self.content_config = []
        else:
            self.content_config = []

        Vars.current_epub = Epub.EpubFile()
        Vars.current_epub.set_epub_book_info()

    def save_content_json(self) -> None:
        try:
            self.content_config.sort(key=lambda x: x.get('chapterIndex'))
            json_info = json.dumps(self.content_config, ensure_ascii=False, indent=4)
            write_text(path_name=self.save_config_path, content=json_info)
        except Exception as err:  # if save_config_path is not exist, create it and save content_config
            print("save content json error: {}".format(err))
            self.save_content_json()

    def merge_text_file(self) -> None:  # merge all text file into one text file
        make_dirs(os.path.join(Vars.cfg.data['out_path'], Vars.current_book.bookName))
        for chapter_info in self.content_config:
            chapter_title = "第{}章: {}\n".format(chapter_info['chapterIndex'], chapter_info['chapterTitle'])
            chapter_content = ["　　" + i for i in chapter_info.get('chapterContent').split("\n")]
            Vars.current_epub.add_chapter_in_epub_file(
                title=chapter_title, content=chapter_content, index=chapter_info['chapterIndex']
            )

            write_text(
                path_name=os.path.join(Vars.cfg.data['out_path'], Vars.current_book.bookName,
                                       Vars.current_book.bookName + ".txt"),
                content=chapter_title + '\n'.join(chapter_content) + "\n\n\n", mode="a"
            )  # write chapter title and content to text file in downloads folder
        self.content_config.clear()  # clear content_config for next book download
        Vars.current_epub.out_put_epub_file()

    def test_config_chapter(self, chapter_url: str) -> bool:
        if not self.content_config:
            return False
        for i in self.content_config:
            if i.get("chapter_url").split("/")[-1] == chapter_url.split("/")[-1]:
                return True
        return False

    def download_book_content(self, chapter_url, index) -> None:
        try:
            chapter_info = Chapter(chapter_id=chapter_url, index=index)
            chapter_info_json = chapter_info.chapter_json
            if isinstance(chapter_info_json, dict):
                self.content_config.append(chapter_info_json)
            else:
                print("chapter_info.chapter_json is not dict", chapter_info_json)
        except Exception as err:
            self.download_book_content(chapter_url=chapter_url, index=index)
            # print("download_book_content error: {}".format(err), end="\r")
            self.save_content_json()  # save content_config if error

    def multi_thread_download_book(self) -> None:
        with ThreadPoolExecutor(max_workers=Vars.cfg.data.get('max_thread')) as executor:
            for index, chapter_url in enumerate(Vars.current_book.chapter_url_list, start=1):
                if Vars.current_book_type == "https://book.sfacg.com" and "vip/c" in chapter_url:
                    continue  # sfacg web vip chapter is images, not support download
                if self.test_config_chapter(chapter_url):
                    continue  # chapter already downloaded
                else:
                    self.threading_list.append(
                        executor.submit(self.download_book_content, chapter_url, index)
                    )
            if len(self.threading_list) != 0:  # if threading_list is not empty
                print("start download book content, length: {}".format(len(self.threading_list)))
                # wait for all threading finished
                for thread in tqdm(self.threading_list, ncols=100, desc='download book content'):
                    thread.result()
            else:
                print(Vars.current_book.bookName, "is no chapter to download.\n\n")

        self.save_content_json()

        self.merge_text_file()

# class Book:
#     def __init__(self, book_info: dict):
#         self.book_info = book_info
#         self.book_id = book_info['bookId']
#         self.cover = book_info.get('bookCoverUrl')
#         self.chapter_url_list = book_info['chapter_url_list']
#         self.book_tag = book_info.get('bookTag')
#         self.last_chapter_title = book_info.get('last_chapter_title')
#
#     @property
#     def book_intro(self) -> str:
#         intro_list = [line for line in self.book_info.get('bookIntro').splitlines() if line.strip()]
#         return re.sub(r' |\r|\s', '', '\n'.join(intro_list))
#
#     @property
#     def book_name(self) -> str:
#         return re.sub(r'[？?*|“《》<>:/]|\r|\n|\s', '', self.book_info['bookName']).strip()
#
#     @property
#     def book_author(self) -> str:
#         return self.book_info['authorName'].replace('作    者：', '')
#
#     @property
#     def book_status(self) -> str:
#         return self.book_info['book_status'].strip() if isinstance(self.book_info.get('book_status'), str) else None
#
#     @property
#     def book_words(self) -> str:
#         return self.book_info['bookWords'] if isinstance(self.book_info.get('bookWords'), str) else None
#
#     @property
#     def out_text_path(self) -> str:
#         return make_dirs(os.path.join(Vars.cfg.data['out_path'], self.book_name))
#
#     @property
#     def save_config_path(self) -> str:
#         return os.path.join(make_dirs(Vars.cfg.data['config_path']), self.book_name + ".json")
