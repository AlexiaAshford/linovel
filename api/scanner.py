import requests
from lxml import etree
import json

data = {}

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}


def scan(tag, maxrange):
    lasList = []
    for page in range(1, maxrange):
        respond = requests.get("https://www.linovel.net/cat/-1.html?sort=words&sign=-1&page={}".format(page),
                               headers=headers)
        tree = etree.HTML(respond.text)
        for i in tree.xpath('//a[@class="book-name"]'):
            lasList.append(i.get('href').split('/')[-1][:-5])
    data[tag] = lasList
    with open('./{}.json'.format(tag), 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False))
    return 0
