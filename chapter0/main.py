# 一只爬虫，爬取维基百科全站
# 采用广度优先遍历
import requests
import pyquery
import queue
import re

class Spider:
    def __init__(self):
        # 错误连接
        with open('error.txt', 'r') as f:
            self.crawled_url = set(f.readlines())
        # 已爬取连接
        with open('crawled.txt', 'r') as f:
            crawled_urls = f.readlines()
            for item in crawled_urls:
                self.crawled_url.add(item)

        self.url_queue = queue.Queue()
        self.clear_and_load_queue_log()

    # 打开 url 返回内容,try_time 为错误重试次数
    def open_url(self, url, try_time=2):
        print(url)
        # 设置请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        try:
            re = requests.get(url, headers=headers)
        except Exception:
            if try_time > 0:
                return self.open_url(url, try_time - 1)
            print('网页:', url, '抓取失败')
            return None
        else:
            return re.text

    # 获得一页的数据
    def handle_url_queue(self):
        url = self.url_queue.get()
        # 如果已经爬取过就直接跳过
        if url in self.crawled_url:
            return
        html = self.open_url(url)
        # 如果打开失败则保存然后关闭
        if html is None:
            # 写入失败日志中
            self.write_error_log(url)
            return
        # 处理 html
        try:
            self.handle_html(html)
            self.write_crawled_log(url)
        except Exception as e:
            print(e)
            self.write_error_log(url)

    # 处理
    def handle_html(self, html):
        soup = pyquery.PyQuery(html)
        urls = [x.attr('href') for x in soup('a').items() if
                x.attr('href') is not None and re.match(r'/wiki/.*', x.attr('href'))]
        for item in urls:
            if item not in self.crawled_url:
                self.url_queue.put('https://en.wikipedia.org' + item)
                self.write_queue_log('https://en.wikipedia.org' + item)

    def start(self):
        if self.url_queue.empty():
            self.url_queue.put('https://en.wikipedia.org/wiki/Main_Page')
        while not self.url_queue.empty():
            self.handle_url_queue()

    def write_error_log(self, url):
        with open('error.txt', 'a+') as f:
            f.write(url + '\n')

    def write_crawled_log(self, url):
        self.crawled_url.add(url)
        with open('crawled.txt', 'a+') as f:
            f.write(url + '\n')

    # 保存任务队列，已经爬取的不删除，等待下次爬虫启动后去重
    def write_queue_log(self, url):
        self.url_queue.put(url)
        with open('queue.txt', 'a+') as f:
            f.write(url + '\n')

    # 去重任务队列
    def clear_and_load_queue_log(self):
        result = ''
        with open('queue.txt', 'r') as f:
            for each in f.readlines():
                if each not in self.crawled_url:
                    result += each
                    self.url_queue.put(each)
        with open('queue.txt', 'w+') as f:
            f.write(result)


Spider().start()
