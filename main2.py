# coding:utf-8
import urllib2
from lxml import etree
import urllib


class LadySpidder(object):
    num = 0

    def __init__(self):
        self.key = raw_input('请输入要查询的贴吧')
        kw = {'kw': str(self.key)}
        kw = urllib.urlencode(kw)
        self.url = 'https://tieba.baidu.com/f?' + kw
        print(self.url)
        self.startPage = raw_input('请输入起始页')
        self.endPage = raw_input('请输入终止页')
        self.headers = {
            'Connection': 'keep-alive',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        }

    def etreeHtml(self, url, htmlFormat):
        # 只要这个从直接urlopen（url）变成urlopen（request）就获取不到，这是个问题
        # 进一步得到，request添加headers就获取不到
        # 再次获得只要添加User-Agent就获取不到
        # 相当奇怪
        request = urllib2.Request(url, headers=self.headers)
        html = urllib2.urlopen(request).read()
        tree = etree.HTML(html)
        return tree.xpath(htmlFormat)

    def allocate(self):
        for page in range(int(self.startPage), int(self.endPage) + 1):
            page = (page - 1) * 50
            url = self.url + '&pn=' + str(page)
            # print(url)

            # 获取每个帖子的连接
            htmlFormat = '//a[@class="j_th_tit "]/@href'
            list = self.etreeHtml(url, htmlFormat)
            # print(list)

            for innerPage in list:
                # self.getImg(innerPage)
                print(innerPage)
                self.getAllPage(innerPage)

    # 获取一个帖子的所有页
    def getAllPage(self, url):
        tmpUrl = 'https://tieba.baidu.com' + url
        htmlFormat = '//div[@class="pb_footer"]//span[@class="red"][last()]/text()'

        # 收到的是一个列表，尽管是只有一个
        list = self.etreeHtml(tmpUrl, htmlFormat)
        tmp = list[0]
        # print(tmp)
        for allPageUrl in range(int(tmp)):
            # print('?pn=%s'%str(allPageUrl))
            self.getImg(tmpUrl + '?pn=' + str(allPageUrl))
            # self.getImg()
            # tmpUrl = url + '?pn=' + str(allPageUrl)
            # urllib2.urlopen(tmpUrl)
            # print(allPageUrl)

    # //span[@class="red"][last()]

    # 获取每个帖子第一页的图片
    def getImg(self, innerPage):
        url = innerPage
        print('getImg : %s' % url)
        # print(innerPageUrl)
        htmlFormat = '//img[@class="BDE_Image"]/@src'
        list = self.etreeHtml(url, htmlFormat)
        for imgUrl in list:
            # print(imgUrl)
            self.writeImg(imgUrl)

    def writeImg(self, url):
        fileFormat = url.split('.')[-1]
        # print(fileFormat)
        if fileFormat not in ['jpg', 'png', 'git', 'bmp', 'jpeg']:
            return
        img = urllib2.urlopen(url).read()
        with open('./img/' + str(LadySpidder.num) + '.' + fileFormat, 'wb+') as f:
            f.write(img)
        print('finished!%d' % LadySpidder.num)
        LadySpidder.num += 1

    def main(self):
        self.allocate()


if __name__ == '__main__':
    ladySpidder = LadySpidder()
    ladySpidder.main()
