def chapter_json(index: int, url: str, title: str, content: str, image_list: list = None) -> dict:
    try:
        return {
            "chapterIndex": index,
            "chapter_url": url,
            "chapterTitle": title,
            "chapterContent": content,
            "imageList": image_list
        }
    except Exception as error:
        print("chapter_info_json", error)


def book_json(
        book_id: str = None,
        book_name: str = None,
        author_name: str = None,
        book_tag: str = None,
        book_intro: str = None,
        book_status: str = None,
        cover_url: str = None,
        book_uptime: str = None,
        last_chapter_title: str = None,
        chapter_url_list: list = None,
        book_words: str = None,
) -> [dict, None]:
    try:
        return {
            "bookId": book_id,
            "bookName": book_name,
            "authorName": author_name,
            "bookCoverUrl": cover_url,
            "chapUrl": chapter_url_list,
            "bookWords": book_words,
            "bookTag": book_tag,
            "bookIntro": book_intro,
            "bookStatus": book_status,
            "lastChapterTitle": last_chapter_title,
            "bookUptime": book_uptime
        }
    except Exception as error:
        print("book_info_json", error)
