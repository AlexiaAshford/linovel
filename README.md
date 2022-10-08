# current support Novel-website:

| 站点名称   | 网址                 | 是否正版 | 插图下载 |
|--------|--------------------|------|------|
| 轻之文库   | www.linovel.net    | ✅    | ✅    |
| 顶点小说   | www.booktxt.net    | ❌    | ✅    |
| POPO   | www.popo.tw        | ✅    | ✅    | 
| 菠萝包    | www.book.sfacg.com | ✅    | ✅    |
| 全本小说网  | www.qb5.la         | ❌    | ✅    |  
| 爱读小说   | www.52dus.cc       | ❌    | ✅    |  
| 全本同人小说 | www.qbtr.cc        | ❌    | ❌    | 
| 同人小说网  | www.trxs.cc        | ❌    | ❌    | 
| 哔哩轻小说  | www.linovelib.com  | ❌    | ✅    |  
| 书本网站   | www.xbookben.net   | ❌    | ✅    |

## command line

``` 
  -h, --help            show this help message and exit
  -u, --update          update config file
  -s, --search          search book
  -i BOOKID             --bookid BOOKID  download book by book id
  -n NAME               --name NAME  download book by name
  -a APP                --app APP     run as app

```

## book source
```
{
  "data": {
    "book_img": "",
    "book_name": "",
    "book_author": "",
    "chapter_url_list": "",
    "book_state": "",
    "book_label": "",
    "book_intro": "",
    "last_chapter_title": "",
    "book_words": "",
    "book_update_time": "",
    "chapter_title": "",
    "chapter_content": ""
  },
  "url": {
    "host_site": "",
    "book_info": "",
    "chapter_info": "",
    "search_info": "",
    "catalogue_info": ""
  }
}
```
- book_img: 封面图片
- book_name: 书名
- book_author: 作者
- chapter_url_list: 章节列表
- book_state: 书籍状态
- book_label: 书籍标签
- book_intro: 书籍简介
- last_chapter_title: 最新章节
- book_words: 字数
- book_update_time: 更新时间
- chapter_title: 章节标题
- chapter_content: 章节内容
- host_site: 站点地址
- book_info: 书籍详细地址
- chapter_info: 章节详细地址
- search_info: 搜索地址
- catalogue_info: 目录地址
- book_id: 书籍id