import constant
from config import *


class Chapter:
    def __init__(self, chapter_id: str, index: int):
        self.chapter_index = index
        self.chapter_id = chapter_id
        self.next_url = self.chapter_id.replace(".html", "_2.html")
        self.chapter_info = Vars.current_book_api.get_chapter_info_by_chapter_id(chapter_id)

    # @property
    # def chapter_info(self):
    #     return Vars.current_book_api.get_chapter_info_by_chapter_id(self.chapter_id)

    @property
    def chapter_title(self) -> str:
        chapter_name = self.chapter_info.xpath(Vars.current_book_rule.chapter_title)
        if isinstance(chapter_name, list) and len(chapter_name) != 0:
            return chapter_name[0].strip()
        return chapter_name.strip()

    @property
    def content_page_html(self):
        if Vars.current_book_type == "Xbookben":
            next_page = Vars.current_book_api.get_chapter_info_by_chapter_id(self.next_url)
            return self.chapter_info.xpath(Vars.current_book_rule.chapter_content) + \
                   next_page.xpath(Vars.current_book_rule.chapter_content)

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

    # @property
    # def standard_content(self):
    #     return re.sub(r'&amp;|amp;|lt;|gt;', '', self._content)

    @property
    def content(self):
        content_list = [page.strip() for page in self.content_page_html if page is not None and len(page.strip()) != 0]
        return re.sub(r'&amp;|amp;|lt;|gt;', '',  "\n".join(content_list))
