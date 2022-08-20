import constant
from config import *


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
