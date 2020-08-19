import os
import time
import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue

import rdhd


# 从首页获取套图链接
# 访问套图链接，获取每张图片链接
# 创建套图目录
# 下载图片到相应目录


# 生产者
class producer(threading.Thread):
    def __init__(self,i,page_queue):
        super().__init__()
        self.i = i
        self.page_queue = page_queue

# 消费者
class consumer(threading.Thread):
    def __init__(self,i):
        super().__init__()
        self.i = i



if __name__ == '__main__':
    pass
    