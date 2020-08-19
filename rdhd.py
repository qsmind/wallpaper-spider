# 提供随机的user_agent和headers，目录下必须有user_agent.txt
"""
使用方法：

目录下必须有user_agent.txt

headers = rdhd.headers() #使用随机的headers

rdhd.random_user_agent()

"""
import random
# 返回随机的user_agent字符串
def random_user_agent():
    user_agent = []
    try:
        with open('user_agent.txt', 'r', encoding="utf-8") as f:
            for line in f:
                user_agent.append(line.rstrip('\n'))
        x=random.randint(0,len(user_agent)-1)
        return user_agent[x]
    except:
        print("请提供‘user_agent.txt’文件")
        return
        

# 返回随机的headers字典
def headers():
    user_agent=random_user_agent()
    headers = {"User-Agent": user_agent}
    return headers

# print(random_user_agent())
