import constant
from config import *


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
    def standard_content(self):
        delete_list = [
            "&amp;", "amp;", "lt;", "gt;", "一秒记住【八零中文网 www.80zw.net】，精彩小说无弹窗免费阅读！"
        ]
        content = "\n".join(self.content)
        for delete_info in delete_list:
            content = re.sub(delete_info, '', content)
        return content

    @property
    def content(self):
        return [page.strip() for page in self.content_page_html if page is not None and len(page.strip()) != 0]
