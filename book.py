import threading
import constant
from config import *
import Epub


class Book:
    def __init__(self, book_info: dict):
        self.content_config = []
        self.threading_list = []
        self.progress_bar_count = 0
        self.progress_bar_length = 0
        self.book_info = book_info
        self.book_id = book_info['bookId']
        self.book_author = book_info['authorName']
        self.cover = book_info['bookCoverUrl']
        self.chapter_url_list = book_info['chapUrl']
        self.max_threading = threading.BoundedSemaphore(Vars.cfg.data.get('max_thread'))

    @property
    def book_name(self) -> str:
        return re.sub(r'[？?*|“《》<>:/]', '', self.book_info['bookName'])

    @property
    def out_text_path(self) -> str:
        return make_dirs(os.path.join(Vars.cfg.data['out_path'], self.book_name))

    @property
    def save_config_path(self) -> str:
        return os.path.join(make_dirs(Vars.cfg.data['config_path']), self.book_name + ".json")

    def init_content_config(self):
        if os.path.exists(self.save_config_path):
            self.content_config = read_text(self.save_config_path, json_load=True)
            if self.content_config is None:
                self.content_config = []
        else:
            self.content_config = []
        Vars.current_epub = Epub.EpubFile()
        Vars.current_epub.save_epub_file = os.path.join(self.out_text_path, self.book_name + '.epub')
        Vars.current_epub.download_cover_and_add_epub()
        write_text(
            path_name=os.path.join(self.out_text_path, self.book_name + ".txt"),
            content=Vars.current_epub.add_the_book_information()
        )  # write book information to text file in downloads folder and show book name, author and chapter count

    def save_content_json(self) -> None:
        try:
            json_info = json.dumps(self.content_config, ensure_ascii=False)
            write_text(path_name=self.save_config_path, content=json_info)
        except Exception as err:  # if save_config_path is not exist, create it and save content_config
            print("save content json error: {}".format(err))
            self.save_content_json()

    def merge_text_file(self) -> None:  # merge all text file into one
        self.content_config.sort(key=lambda x: x.get('chapterIndex'))
        for chapter_info in self.content_config:
            chapter_title = "第{}章: {}\n".format(chapter_info['chapterIndex'], chapter_info['chapterTitle'])
            chapter_content = ["　　" + i for i in chapter_info.get('chapterContent').split("\n")]
            Vars.current_epub.add_chapter_in_epub_file(
                chapter_title=chapter_title,
                content_lines_list=chapter_content,
                serial_number=chapter_info['chapterIndex']
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
        except Exception as err:
            self.save_content_json()  # save content_config if error occur
            print("[error] {} error:{}".format(chapter_url, err))
        finally:
            self.max_threading.release()  # release threading semaphore when threading is finished

    def multi_thread_download_book(self) -> None:
        for index, chapter_url in enumerate(self.chapter_url_list, start=1):
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

        if self.book_id not in Vars.cfg.data['downloaded_book_id_list'][Vars.current_book_type]:
            Vars.cfg.data['downloaded_book_id_list'][Vars.current_book_type].append(self.book_id)
            Vars.cfg.save()

    def progress_bar(self, title: str = "") -> None:  # progress bar
        self.progress_bar_count += 1  # increase progress_bar_count
        print("\r{}/{} title:{}".format(
            self.progress_bar_count, self.progress_bar_length, title), end="\r"
        )  # print progress bar and title


class Chapter:
    def __init__(self, chapter_id: str, index: int):
        self._content = ""
        self.chapter_index = index
        self.chapter_id = chapter_id

    @property
    def chapter_info(self):
        return Vars.current_book_api.get_chapter_info_by_chapter_id(self.chapter_id)

    @property
    def chapter_title(self) -> str:
        chapter_name = self.chapter_info.xpath(Vars.current_book_rule.chapter_title)
        if isinstance(chapter_name, list) and len(chapter_name) != 0:
            return chapter_name[0].strip()
        return chapter_name.strip()

    @property
    def content_html(self):
        return self.chapter_info.xpath(Vars.current_book_rule.chapter_content)

    @property
    def chapter_json(self):
        image_list = []
        return constant.json.chapter_json(
            index=self.chapter_index,
            url=self.chapter_id,
            content=self.content,
            title=self.chapter_title,
            image_list=image_list if image_list is not None else []
        )  # return a dict with chapter info

    @property
    def content(self):
        if Vars.current_book_type == "Linovel":
            for book in self.content_html:
                if book.text is not None and len(book.text.strip()) != 0:
                    self._content += book.text.strip() + "\n"
            return self._content

        elif Vars.current_book_type == "Dingdian":
            for line in self.content_html:
                content_line = str(line).strip()
                if content_line is None or content_line == "":
                    continue
                if '请记住本书首发域名' in content_line or '书友大本营' in content_line:
                    continue
                self._content += content_line + "\n"
            return re.sub(r'&amp;|amp;|lt;|gt;', '', self._content)

        elif Vars.current_book_type == "Xbookben":
            for content_line in self.content_html[0]:
                if content_line.text is not None and len(content_line.text.strip()) != 0:
                    self._content += content_line.text.strip() + "\n"
            return self._content
        elif Vars.current_book_type == "sfacg":
            for content_line in self.content_html:
                if content_line.text is not None and len(content_line.text.strip()) != 0:
                    self._content += content_line.text.strip() + "\n"
            return self._content
