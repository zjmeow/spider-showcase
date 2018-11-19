import logging
import queue


# 一个自定义的队列类，会记录下队列中的内容
class LogQueue(queue.Queue):
    def __init__(self, logger, file_name):
        super().__init__()
        self.file_name = file_name
        self.logger = logging.getLogger(logger)
        fh = logging.FileHandler(file_name)
        ch = logging.StreamHandler()
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get(self, block=True, timeout=None):
        item = super().get()
        self.delete_first_line()
        return item

    def put(self, item, block=True, timeout=None):
        super().put(self, item)
        self.logger.info(item)

    def delete_first_line(self):
        with open(self.file_name, 'w+') as f:
            pass
        pass

        #
        # # 保存任务队列，已经爬取的不删除，等待下次爬虫启动后去重
        # def write_queue_log(self, content):
        #     with open('queue.txt', 'a+') as f:
        #         f.write(content + '\n')


q = LogQueue('queue', 'queue.log')
q.put('123')
print(q.get())
