import requests
from lxml import etree
from urllib3 import Retry


class Chapter():
    """
    获取小说详情的对象
    """

    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }

    def get(self, bookId):
        """
        :param bookId: 书籍ID
        :return: 返回三个指，分别是小说每个章节的URL，小说名字，小说封面Url
        """
        s = requests.Session()
        retries = Retry(total=15, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504],
                        raise_on_redirect=True, raise_on_status=True)
        s.mount('http://', requests.adapters.HTTPAdapter(max_retries=retries))
        s.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))
        respond = s.get("https://www.linovel.net/book/{}.html#catalog".format(bookId), headers=self.headers, timeout=10)
        tree = etree.HTML(respond.text)
        try:
            volume = tree.xpath('//div[@class="chapter"]/a')

            bookName = tree.xpath('//h1[@class="book-title"]')[0].text
            authorName = tree.xpath('//div[@class="author-frame"]//a')[0].text
            bookCoverUrl = tree.xpath('//div[@class="book-cover"]/a')[0].get('href')
        except:
            return -1, -1, -1, -1
        linkList = []
        for i in volume:
            link = "https://www.linovel.net{}".format(i.get('href'))
            linkList.append(link)
        return linkList, bookName, authorName, bookCoverUrl


if "__main__" == __name__:
    Test = Chapter()
    print(Test.get("111000"))
