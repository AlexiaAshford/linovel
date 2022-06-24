from api import bot
from api import scanner
import json
def init():
    tag = 'all'
    maxrange = 622
    headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            }
    scanner.scan(tag,maxrange)
def downloadAllTags(tag):
    with open('./{}.json'.format(tag),'r') as f:
        downloadList = json.load(f)[tag]
    for i in downloadList[1301:]:
        ilNovelBot = bot.LiNovelBot(i)
        ilNovelBot.run()
        del ilNovelBot

# bookId = "101436"
# ilNovelBot = bot.LiNovelBot(bookId)
# ilNovelBot.run()
