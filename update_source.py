import json
import os

if __name__ == '__main__':
    # read book source file name
    book_source_list = os.listdir("book_source")
    # print(book_source_list)
    print("book_source_list length: ", len(book_source_list))
    for book_source in book_source_list:
        # read book source file content
        with open("book_source/" + book_source, "r", encoding="utf-8") as f:
            file = json.loads((f.read()))
            if not file.get("json_page"):
                file["json_page"] = False  # add json_page key
            # write book source file for update
            with open("book_source/" + book_source, "w", encoding="utf-8") as w:
                w.write(json.dumps(file, ensure_ascii=False, indent=4))
