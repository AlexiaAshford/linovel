from pydantic import BaseModel
from typing import Optional, List, Union, Any


class BookInfoData(BaseModel):
    book_img: Optional[str] = ""
    book_name: Optional[str] = ""
    book_author: Optional[str] = ""
    book_state: Optional[str] = ""
    book_label: Optional[str] = ""
    book_intro: Optional[str] = ""
    last_chapter_title: Optional[str] = ""
    chapter_url_list: Optional[str] = ""
    book_words: Optional[str] = ""
    book_update_time: Optional[str] = ""
    chapter_title: Optional[str] = ""
    chapter_content: Optional[str] = ""


class BookInfoUrl(BaseModel):
    host_site: Optional[str] = ""
    book_info: Optional[str] = ""
    chapter_info: Optional[str] = ""
    search_info: Optional[str] = ""
    catalogue_info: Optional[str] = ""


class BookSource(BaseModel):
    data: Union[BookInfoData]
    url: Union[BookInfoUrl]
    json_page: bool = False
    gbk_encoding: bool = False


class BookInfo(BaseModel):
    book_name: Optional[str]
    book_author: Optional[str] = None
    book_cover: Optional[str] = None
    book_words: Optional[str] = None
    book_tag: Optional[str] = None
    book_intro: Optional[str] = None
    book_status: Optional[str] = None
    last_chapter_title: Optional[Any] = None
    book_update_time: Optional[str] = None
    chapter_url_list: Optional[List[str]] = None
    book_id: Optional[str] = None
    book_info: Optional[dict] = None
