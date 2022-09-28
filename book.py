import Epub
import threading
import constant
from config import *


class Book:
    def __init__(self, book_info: dict):
        self.book_info = book_info
        self.book_id = book_info['bookId']
        self.cover = book_info.get('bookCoverUrl')
        self.chapter_url_list = book_info['chapUrl']
        self.book_tag = book_info.get('bookTag')
        self.book_intro = book_info.get('bookIntro')
        self.last_chapter_title = book_info.get('lastChapterTitle')

    @property
    def book_name(self) -> str:
        return re.sub(r'[？?*|“《》<>:/]|\r|\n|\s', '', self.book_info['bookName']).strip()

    @property
    def book_author(self) -> str:
        return self.book_info['authorName'].replace('作    者：', '')

    @property
    def book_status(self) -> str:
        return self.book_info['bookStatus'].strip() if isinstance(self.book_info.get('bookStatus'), str) else None

    @property
    def book_words(self) -> str:
        return self.book_info['bookWords'] if isinstance(self.book_info.get('bookWords'), str) else None

    @property
    def out_text_path(self) -> str:
        return make_dirs(os.path.join(Vars.cfg.data['out_path'], self.book_name))

    @property
    def save_config_path(self) -> str:
        return os.path.join(make_dirs(Vars.cfg.data['config_path']), self.book_name + ".json")


class Chapter:
    def __init__(self, chapter_id: str, index: int):
        self.chapter_index = index
        self.chapter_id = chapter_id
        self.next_url = self.chapter_id.replace(".html", "_2.html")
        self.chapter_page = None
        self.image_list = []

    # @property
    # def chapter_info(self):
    #     return Vars.current_book_api.get_chapter_info_by_chapter_id(self.chapter_id)

    @property
    def chapter_title(self) -> str:
        chapter_name = self.chapter_page.xpath(Vars.current_book_rule.chapter_title)
        if isinstance(chapter_name, list) and len(chapter_name) != 0:
            return chapter_name[0].strip()
        return chapter_name.strip()

    @property
    def content_page_html(self):
        if Vars.current_book_type == "Xbookben":
            next_page = Vars.current_book_api.get_chapter_info_by_chapter_id(self.next_url)
            return self.chapter_page.xpath(Vars.current_book_rule.chapter_content) + next_page.xpath(
                Vars.current_book_rule.chapter_content)

        return self.chapter_page.xpath(Vars.current_book_rule.chapter_content)

    @property
    def chapter_json(self):
        self.chapter_page = Vars.current_book_api.get_chapter_info_by_chapter_id(self.chapter_id)
        return constant.json.chapter_json(
            index=self.chapter_index,
            url=self.chapter_id,
            content=self.standard_content,
            title=self.chapter_title,
            image_list=self.image_list if self.image_list is not None else []
        )  # return a dict with chapter info

    @property
    def standard_content(self) -> str:  # return a standard content
        content = "\n".join(self.content)
        for delete_info in [
            "&amp;", "amp;", "lt;", "gt;", "一秒记住【八零中文网 www.80zw.net】，精彩小说无弹窗免费阅读！"
        ]:
            content = re.sub(delete_info, '', content)
        return content

    @property
    def content(self):
        return [page.strip() for page in self.content_page_html if page is not None and len(page.strip()) != 0]


class BookConfig(Book):
    def __init__(self, book_info: dict):
        super().__init__(book_info=book_info)
        self.content_config = []
        self.threading_list = []
        self.progress_bar_count = 0
        self.progress_bar_length = 0
        self.max_threading = threading.BoundedSemaphore(Vars.cfg.data.get('max_thread'))

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
        for chapter_info in self.content_config:
            chapter_title = "第{}章: {}\n".format(chapter_info['chapterIndex'], chapter_info['chapterTitle'])
            chapter_content = ["　　" + i for i in chapter_info.get('chapterContent').split("\n")]
            Vars.current_epub.add_chapter_in_epub_file(
                title=chapter_title, content=chapter_content, index=chapter_info['chapterIndex']
            )
            write_text(
                path_name=os.path.join(self.out_text_path, self.book_name + ".txt"),
                content=chapter_title + '\n'.join(chapter_content) + "\n\n\n", mode="a"
            )  # write chapter title and content to text file in downloads folder
        self.content_config.clear()  # clear content_config for next book download
        Vars.current_epub.out_put_epub_file()

    def test_config_chapter(self, chapter_url: str) -> bool:
        for i in self.content_config:
            if i.get("chapter_url").split("/")[-1] == chapter_url.split("/")[-1]:
                return True
        return False

    def download_book_content(self, chapter_url, index) -> None:
        self.max_threading.acquire()  # acquire semaphore to prevent multi threading
        try:
            chapter_info = Chapter(chapter_id=chapter_url, index=index)
            if isinstance(chapter_info.chapter_json, dict):
                self.content_config.append(chapter_info.chapter_json)
                self.progress_bar(chapter_info.chapter_title)
            else:
                print("chapter_info.chapter_json is not dict", chapter_info.chapter_json)
        except:
            self.save_content_json()  # save content_config if error
        finally:
            self.max_threading.release()  # release threading semaphore when threading is finished

    def multi_thread_download_book(self) -> None:
        for index, chapter_url in enumerate(self.chapter_url_list, start=1):
            if Vars.current_book_type == "sfacg" and "vip/c" in chapter_url:
                print("sfacg vip chapter is images, not support download:{}".format(chapter_url), end="\r")
                continue
            if self.test_config_chapter(chapter_url):
                continue  # chapter already downloaded
            else:
                self.threading_list.append(
                    threading.Thread(target=self.download_book_content, args=(chapter_url, index,))
                )  # create threading to download book content

        if len(self.threading_list) != 0:  # if threading_list is not empty
            self.progress_bar_length = len(self.threading_list)
            for thread in self.threading_list:  # start all thread in threading_list
                thread.start()
            for thread in self.threading_list:  # wait for all threading_list to finish
                thread.join()
            self.threading_list.clear()  # clear threading_list for next chapter
        else:
            print(self.book_name, "is no chapter to download.\n\n")
        self.save_content_json()
        self.merge_text_file()

    def progress_bar(self, title: str = "") -> None:  # progress bar
        self.progress_bar_count += 1  # increase progress_bar_count
        print("\r{}/{} title:{}".format(
            self.progress_bar_count, self.progress_bar_length, title), end="\r"
        )  # print progress bar and title
