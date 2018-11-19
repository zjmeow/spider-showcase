import requests
import queue
import logging


# 一个爬取论坛贴子的爬虫，贴子的 id 从 1 到 10000
class Spider():
    '''
        爬虫有两种模式，crawl_error为true的时候回去爬取之前爬取失败的连接
        当指定 id 的时候可以从指定 id 开始爬取

    '''

    def __init__(self, id=1, crawl_error=False):
        # 初始化日志
        self.logger = logging.getLogger('spider')
        fh = logging.FileHandler('error.log')
        ch = logging.StreamHandler()
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        # 初始化任务队列
        self.url_queue = queue.Queue()
        # 开启爬取失败文件
        if crawl_error:
            with open('error.log', 'r') as f:
                for url in f.readlines():
                    self.url_queue.put(url)
        else:
            for id in range(id, 1500):
                self.url_queue.put('url' + str(id))

    def open_url(self, url, try_time=2):
        print('正在爬取：' + url)
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

    def crawl(self, url):
        html = self.open_url(url)
        if html is None:
            self.logger.error(url)
        print(html)
