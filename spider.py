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

# 创建目录
def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

#生产者只请求页面
class producer(threading.Thread):
    def __init__(self,i,page_queue):
        super().__init__()
        self.i = i
        self.page_queue = page_queue
    
    #复写run方法
    def run(self):
        #任务队列不为空就取数据执行
        while True:
            if self.page_queue.empty():
                break
            try:
                q = self.page_queue.get(block=False)
                print(self.i, '开始任务%s======='%(q))
                # url = 'https://careers.tencent.com/tencentcareer/api/post/Query?keyword=python&pageIndex=%s&pageSize=10'%(q)
                url = 'http://spotlight.shijuewuyu.com/?page=%s'%(q)
                html=self.get_html(url)# 获取主页信息
                pic_list = []  # 二维列表，格式：[链接，套图名称,更新时间]
                get_pic_list(html, pic_list)  # 获取套图      
                
                for link in pic_list:  # 爬取单个页面套图
                    j += 1  # 已获取的套图数量
                    html = get_html(link[0])  # 获取网页
                    src=[]
                    length = get_pic_link(html,src)  # 获取图片链接
                    # 将图片链接存入队列
                    for ref in src:
                        response_q.put(ref)    
            except:
                pass
            
    # 获取网页
    def get_html(self,url):
        i=0
        while i<2:
            try:
                # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
                headers = rdhd.headers()  # 使用随机的headers
                r = requests.get(url, headers=headers,timeout=10)
                # print(r.apparent_encoding)
                # r.encoding = r.apparent_encoding
                r.encoding = 'utf-8'
                return r.text
            except:
                i+=1
                print('第{}次超时'.format(i))
                
        headers = rdhd.headers()  # 使用随机的headers
        r = requests.get(url, headers=headers,timeout=10)
        r.encoding = 'utf-8'
        return r.text
        
    # 获取套图
    def get_pic_list(self,html, pic_list):
        try:
            temp = []
            soup = BeautifulSoup(html, "html.parser")
            # print(soup)
            pins = soup.find_all('div','container')
            # print(pins[1])
            for li in pins[1].find_all('li'):
                # temp.append('https://555zui.com/'+li.find('a').get('href'))
                temp.append('https://www.2456cc.com/'+li.find('a').get('href'))
                temp.append(li.find('a').get('title'))
                temp.append(li.find('div','subtitle text-time text-overflow').string)
                pic_list.append(temp)
                temp = []
                # print(pic_list)
        except:
            # print('获取套图失败！')
            return ''

    # 获取每套图片链接
    def get_pic_link(self,html,src):
        soup = BeautifulSoup(html, "html.parser")
        # 获取初始图片链接
        for img in soup.find_all('div', 'container')[1].find_all('img'):
            src.append(img.get('src'))
        # print(src)

        # 获取图片数目
        # pag = soup.find('div', 'pagenavi')
        # length = pag.find_all('span')
        # length=src.split('[')[-1][:-2]
        length=len(src)

        return int(length)

# 消费者
class consumer(threading.Thread):
    def __init__(self,i):
        super().__init__()
        self.i = i
 
    #复写run方法
    def run(self):
        #任务队列不为空就取数据执行
        while True:
            #1.任务队列为空，2生产者进程全部结束
            if response_q.empty() and flag:
                break
 
            try:
                response = response_q.get(block=False)
                self.parse_html(response)
            except:
                pass
            
    def parse_html(self,response):
        job_lst = response['Data']['Posts']
        for job in job_lst:
            name = job['RecruitPostName']
            address = job['LocationName']
            Responsibility = job['Responsibility']
            Responsibility = Responsibility.replace('\n', '').replace('\r', '')
            PostURL = job['PostURL']
 
            info = "工作名称：%s,工作地点：%s，岗位职责：%s，详情：%s" % (name, address, Responsibility, PostURL)
 
            #加锁
            with lock:
                with open("腾讯招聘.txt", 'a', encoding='utf-8') as f:
                    f.write(info + '\n')
                    
    # 下载一套图片
    def get_pic(self,src, length, name,uptime, path, k):
        # 创建套图目录
        name=name+'-'+uptime
        #若目录已存在，则返回
        # if os.path.isdir('{}/{}/{}'.format(path,k, name)):
        #     return
        try:
            create_dir('{}/{}'.format(path, str(name)))
        except :
            print('创建目录失败！')
            return 

        # headers = {
        #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
        #     'Connection': 'Keep-Alive',
        #     'Referer': "http://www.mzitu.com/99566"
        # }

        # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}

        i=1
        for url in src:
            err=0
            while err<3:
                try:
                    # if i < 10:
                    #     url = src[:-6] + '0' + str(i) + '.jpg'
                    # else:
                    #     url = src[:-6] + str(i) + '.jpg'
                    # 使用随机的user_agent
                    headers = {
                        'User-Agent': rdhd.random_user_agent(),
                        'Connection': 'Keep-Alive'
                    }
                    r = requests.get(url, headers=headers,timeout=22)
                    with open('{}/{}/{}'.format(path, name, '00'+str(i)+'_'+url.split('/')[-1]), 'wb') as f:
                        f.write(r.content)

                    print('{}下载成功！'.format(url.split('/')[-1]),'进度：{}/{}'.format(i, length))
                    i+=1
                    time.sleep(1)
                    break
                    # if i==4: #下载图片数量
                    #     break
                except:
                    err+=1
                    print('第',err,'次下载失败！')
                    # continue
 
 
lock = threading.Lock()  #锁
response_q = Queue()     #消费者队列
flag = False             #表示生产者线程是否都结束

if __name__ == '__main__':
    #创建生产者任务队列
    page_queue = Queue()
    for i in range(1,175):
        page_queue.put(i)
 
    #启线程队列
    producer_name = ['p1','p2','p3']
    p_tread = []
    cousumer_name = ['c1','c2','c3']
    c_tread = []
 
    #启动三个生产者线程
    for i in producer_name:
        p_crawl = producer(i,page_queue)
        p_crawl.start()
        p_tread.append(p_crawl)
 
    #启动三个消费者线程
    for j in cousumer_name:
        c_crawl = consumer(j)
        c_crawl.start()
        c_tread.append(c_crawl)
 
 
    #生产者阻塞主线程
    for threadi in p_tread:
        threadi.join()
    #生产者都死了把flag变成True，可以让消费者做判断
    flag = True
 
    #消费者阻塞主线程
    for threadi in c_tread:
        threadi.join()