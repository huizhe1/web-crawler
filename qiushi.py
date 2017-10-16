import requests
import bs4
import re

class QSBK:
    """糗事百科爬虫"""
    def __init__(self):
        self.pageIndex = 1
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        }
        self.url = "http://www.qiushibaike.com/hot/page/"
        self.storys = []
        self.pageIndex = 1
        self.enable = True

    def pageDownload(self ,url):
        try:
            response = requests.get(url, headers=self.header)
            if 200 == response.status_code:
                self.html = response.content.decode(encoding='utf-8')
            else:
                return None
        except:
            return None

    def getContent(self):
        """正则获取数据"""
        pattern = re.compile('<h2>.*?(.*?)</h2>.*?<div.*?content">.*?<span>(.*?)</span>.*?<div.*?'+
                             'thumb.*?<a.*?>(.*?)</a>',re.S)
        items = re.findall(pattern, self.html)
        self.addStorys(items)

    def trip_content(self, content):
        """正则去除空格"""
        remove_trip = re.compile('\n')
        return remove_trip.sub('',content)

    def addStorys(self, items):
        """数据存入storys"""
        for item in items:
            haveImg = re.search('<img', item[2])
            if not haveImg:
                self.storys.append({
                    "author": self.trip_content(item[0]),
                    "content": self.trip_content(item[1])
                })

            else:
                self.storys.append({
                    "author": self.trip_content(item[0]),
                    "content": self.trip_content(item[1]),
                    "img": self.trip_content(item[2])
                })

    def getStory(self):
        """打印无图片故事"""
        while self.enable:
            print("按下enter键获取下一个的故事||输入 Q 则不再获取故事")
            text = str(input())
            if "Q" == text.upper():
                self.enable = False
                print('end')
            else:
                if len(self.storys) > 0:
                    print(self.storys.pop())
                else:
                    print('正在获取，请稍后---')
                    self.pageIndex += 1
                    self.getIndex()

    def getIndex(self):
        """获取第X页故事"""
        url = self.url+str(self.pageIndex)
        self.pageDownload(url)
        self.getContent()

qiushi = QSBK()
qiushi.getIndex()
qiushi.getStory()

