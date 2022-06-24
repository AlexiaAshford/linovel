import re

import grequests
import requests
from lxml import etree
from urllib3 import Retry

from api import downloadAsEpub
from api import getBookInfo


def illegalStrip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？?\*|“《》<>:/]', '', str(path))
    return path





class LiNovelBot(getBookInfo.Chapter):
    def __init__(self, bookId):
        super().__init__()
        self.bookId = bookId

    def run(self):
        epubList, chapterimgList = [], []
        linkList, bookName, authorName, bookCoverUrl = self.get(self.bookId)
        if linkList == -1:
            print(self.bookId, "获取章节错误")
            return -1
        bookName = illegalStrip(bookName)
        s= 0
        reqList = [grequests.get(i, session=s, headers=self.headers, timeout=10) for i in linkList]
        print('目录解析完毕，正在请求.\/')
        responds = grequests.map(reqList, size=30)
        for i in responds:
            bookTree = etree.HTML(i.text)
            title = bookTree.xpath('//div[@class="article-title"]')[0].text
            epubCodes = '<h1>{}</h1>'.format(title.strip())
            imgCode = ''
            for book in bookTree.xpath('//div[@class="article-text"]/p'):
                if book.text is not None:
                    if len(book.text.strip()) == 0:
                        continue
                    epubCodes += '<p>{}</p>'.format(book.text.strip())
            numb = 0
            for img in bookTree.xpath('//div[@class="article-text"]//img'):
                imgUrl = img.get('src')
                try:
                    imgContent = requests.get(imgUrl, headers=self.headers, timeout=10).content
                except:
                    continue
                chapterimg = downloadAsEpub.epub.EpubItem(
                    file_name="images/" + self.bookId + '_' + str(i.url.split('/')[-1][:-5]) + '_' + str(numb) + '.png',
                    content=imgContent)
                chapterimgList.append(chapterimg)
                imgCode += '<p><img src=' + "images/" + self.bookId + '_' + str(i.url.split('/')[-1][:-5]) + '_' + str(
                    numb) + '.png' + '></p>'
                numb += 1
            epubList.append(epubCodes + imgCode)
        downloadAsEpub.creat2epub(self.bookId, bookName, authorName, bookCoverUrl, chapterimgList, epubList)
