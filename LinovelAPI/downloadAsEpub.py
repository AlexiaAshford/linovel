from ebooklib import epub
import os
import requests


def creat2epub(bookId, bookName, authorName, coverImgUrl, chapterimgList, epubList):
    """

    :param bookId: 书籍的ID，只能为字符串
    :param bookName: 书籍名字，会影响书籍命名
    :param authorName: 作者名字
    :param coverImgUrl: 封面图像的URL链接
    :param chapterimgList: 小说插图的epub.EpubItem对象列表
    :param epubList: 小说文本的epub.EpubItem对象列表
    :return: success
    """
    if not os.path.exists('./novel'):
        os.mkdir('./novel')
    default_style = '''
    body {font-size:100%;}
    p{
        font-family: Auto;
        text-indent: 2em;
    }
    h1{
        font-style: normal;
        font-size: 20px;
        font-family: Auto;
    }      
    '''
    book = epub.EpubBook()
    book.set_identifier(bookId)
    book.set_title(bookName)
    book.set_language('zh-CN')
    book.add_author(authorName)
    imgb = requests.get(coverImgUrl)
    book.set_cover(bookName + '.png', imgb.content)
    default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css",
                                content=default_style)
    book.add_item(default_css)
    u = 0
    ebookList = []
    for img in chapterimgList:
        book.add_item(img)
    for i in epubList:
        title = i.split('</h1>')[0]
        title = title.split('<h1>')[-1]
        print('\t' + title)
        c = epub.EpubHtml(title=title, file_name='chapter_{}'.format(u) + '.xhtml', lang='zh-CN',
                          uid='chapter_{}'.format(u))
        c.content = i
        c.add_item(default_css)
        book.add_item(c)
        ebookList.append(c)
        u += 1
    book.toc = tuple(ebookList)
    book.spine = ['nav']
    book.spine.extend(ebookList)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    style = '''
    body {
        font-family: Auto;
    }
    p{
         font-family: Auto;
         text-indent: 2em;
    }
    h2 {
         text-align: left;
         text-transform: uppercase;
         font-weight: 200;     
    }
    ol {
            list-style-type: none;
    }
    ol > li:first-child {
            margin-top: 0.3em;
    }
    nav[epub|type~='toc'] > ol > li > ol  {
        list-style-type:square;
    }
    nav[epub|type~='toc'] > ol > li > ol > li {
            margin-top: 0.3em;
    }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    epub.write_epub('./novel/' + bookName + '.epub', book, {})
