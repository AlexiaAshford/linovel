import json
import os

book_source_list = os.listdir("book_source")
print(book_source_list)

for book_source in book_source_list:
    with open("book_source/" + book_source, "r", encoding="utf-8") as f:
        file = json.loads((f.read()))
        if not file.get("json_page"):
            file["json_page"] = False

        with open("book_source/" + book_source, "w", encoding="utf-8") as w:
            w.write(json.dumps(file, ensure_ascii=False, indent=4))
