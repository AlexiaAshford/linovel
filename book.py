import threading
import LinovelAPI
from config import *


class Book:
    def __init__(self, book_info: dict):
        self.content_config = []
        self.threading_list = []
        self.progress_bar_count = 0
        self.progress_bar_length = 0
        self.book_info = book_info
        self.book_name = LinovelAPI.illegal_strip(book_info['bookName'])
        self.book_id = book_info['bookId']
        self.book_author = book_info['authorName']
        self.cover = book_info['bookCoverUrl']
        self.chapter_url_list = book_info['chapUrl']
        self.save_config_path = os.path.join(Vars.cfg.data['config_path'], self.book_name + ".json")
        self.out_text_path = os.path.join(Vars.cfg.data['out_path'], self.book_name)  # downloads folder
        # create semaphore to prevent multi threading
        self.max_threading = threading.BoundedSemaphore(Vars.cfg.data.get('max_thread'))

    def init_content_config(self):
        if not os.path.exists(Vars.cfg.data['config_path']):  # if Cache folder is not exist, create it
            os.mkdir(Vars.cfg.data['config_path'])
        if not os.path.exists(self.out_text_path):  # if downloads folder is not exist, create it
            os.makedirs(self.out_text_path)
        if os.path.exists(self.save_config_path):
            self.content_config = LinovelAPI.read_text(self.save_config_path, json_load=True)
            if self.content_config is None:
                self.content_config = []
        else:
            self.content_config = []
        show_info = "book name: {}\nauthor: {}\nchapter count: {}\n\n".format(
            self.book_name, self.book_author, len(self.chapter_url_list))
        print(show_info)  # show book name, author and chapter count
        LinovelAPI.write_text(path_name=os.path.join(self.out_text_path, self.book_name + ".txt"), content=show_info)

    def save_content_json(self) -> None:
        try:
            json_info = json.dumps(self.content_config, ensure_ascii=False)
            LinovelAPI.write_text(path_name=self.save_config_path, content=json_info, mode="w")
        except Exception as err:  # if save_config_path is not exist, create it and save content_config
            print("save content json error: {}".format(err))

    def merge_text_file(self) -> None:  # merge all text file into one
        self.content_config.sort(key=lambda x: x.get('chapterIndex'))
        for chapter_info in self.content_config:
            chapter_title = "第{}章: {}\n".format(chapter_info['chapterIndex'], chapter_info['chapterTitle'])
            chapter_content = '\n'.join(["　　" + i for i in chapter_info.get('chapterContent').split("\n")])
            LinovelAPI.write_text(
                path_name=os.path.join(self.out_text_path, self.book_name + ".txt"),
                content=chapter_title + chapter_content + "\n\n\n", mode="a"
            )  # write chapter title and content to text file in downloads folder
        self.content_config.clear()  # clear content_config for next book download

    def test_config_chapter(self, chapter_url: str) -> bool:
        for i in self.content_config:
            if i.get("chapter_url").split("/")[-1] == chapter_url.split("/")[-1]:
                return True
        return False

    def download_book_content(self, chapter_url, index) -> None:
        self.max_threading.acquire()  # acquire semaphore to prevent multi threading
        try:
            chapter_info = LinovelAPI.get_chapter_info(chapter_url, index)
            if isinstance(chapter_info, dict):
                self.content_config.append(chapter_info)
                self.progress_bar(chapter_info['chapterTitle'])
        except Exception as e:
            print("error: {}".format(e), self.save_content_json())
        finally:
            self.max_threading.release()  # release threading semaphore

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
            self.save_content_json()
            self.merge_text_file()
        else:
            print(self.book_name, "is no chapter to download.\n\n")

        if self.book_id not in Vars.cfg.data['downloaded_book_id_list']:
            Vars.cfg.data['downloaded_book_id_list'].append(self.book_id)
            Vars.cfg.save()
        else:
            print("the book {} add book_id update list.\n\n", self.book_name)

    def progress_bar(self, title: str = "") -> None:  # progress bar
        self.progress_bar_count += 1  # increase progress_bar_count
        print("\r{}/{} title:{}".format(
            self.progress_bar_count, self.progress_bar_length, title), end="\r"
        )  # print progress bar and title
