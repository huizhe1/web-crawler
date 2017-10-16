# web-crawler
糗事百科爬虫（python）

此文代码部分依照[该博文](http://cuiqingcai.com/990.html)编写

### 网页下载器

~~~python
def pageDownload(self ,url):
        try:
            response = requests.get(url, headers=self.header)
            if 200 == response.status_code:
                self.html = response.content.decode(encoding='utf-8')
            else:
                return None
        except:
            return None
~~~

这里采用第三方库requests 对网页进行下载，判断其是否响应成功，指定编码格式

url为拼接好的糗事百科路径地址

### 数据获取

~~~python
def getContent(self):
        """正则获取数据"""
        pattern = re.compile('<h2>.*?(.*?)</h2>.*?<div.*?content">.*?<span>(.*?)</span>.*?<div.*?'+
                             'thumb.*?<a.*?>(.*?)</a>.*?<div class="stats.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern, self.html)
        self.addStorys(items)
~~~

这里的正则简单的说明一下：

- .*? 是一个固定的搭配，.和*代表可以匹配任意无限多个字符，加上？表示使用非贪婪模式进行匹配，也就是我们会尽可能短地做匹配，以后我们还会大量用到 .*? 的搭配。
- (.*?)代表一个分组，在这个正则表达式中我们匹配了四个分组，在后面的遍历items中，item[0]就代表第一个(.*?)所指代的内容，item[1]就代表第二个(.*?)所指代的内容，以此类推。
- re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符。

这里的正则对应[糗事百科](http://www.qiushibaike.com/hot/page/1)的页面内容，具体根据该页面，按F12 进行数据的匹配

这样就能获取作者，文本内容，图片信息和点赞数

### addStorys函数

~~~python
def addStorys(self, items):
        """数据存入storys"""
        for item in items:
            haveImg = re.search('<img', item[2])
            if not haveImg:
                self.storys.append({
                    "author": self.trip_content(item[0]),
                    "content": self.trip_content(item[1]),
                    "stats": self.trip_content(item[3])
                })

            # else:
            #     self.storys.append({
            #         "author": self.trip_content(item[0]),
            #         "content": self.trip_content(item[1]),
            #         "img": self.trip_content(item[2]),
            #         "stats": self.trip_content(item[3])
            #     })
~~~

这里我将数据存入一个列表中，注释部分为包含图片信息的数据，依据个人喜爱，自行添加

#### trip_content函数

~~~python
def trip_content(self, content):
        """正则去除空格"""
        remove_trip = re.compile('\n')
        return remove_trip.sub('',content)
~~~

这个函数主要是去除数据中的换行字符，返回去除后的数据

