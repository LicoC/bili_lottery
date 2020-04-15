#!/usr/bin/env python
# coding: utf-8

import logging
import time
import json
import csv
import random
import datetime

import requests

headers = {
    'Sec-Fetch-Dest': 'script',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3980.132 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Referer': 'https://space.bilibili.com/171474500/fans/fans',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Cookie':'这里要填你自己的cookie'
}

def main():
    bili_closed_price = 27.480 #B站美股收盘价格
    up_id = 171474500 #我自己的id
    max_page_num = 24
    end_time = 1586894400 # 抽奖截止时间戳 北京时间2020-4-15 04:00 am （美股收盘时间）

    users_map = {}
    users = []

    print("\n北京时间2020-4-15 04:00am B站收盘价格为：{}\n".format(bili_closed_price)) 
    print("评论拉取中... 🚀 🚀 🚀\n")

    #这个接口是「创作中心-互动管理-评论/弹幕管理」那的接口
    #这个接口拉取评论和弹幕会更方便，但这个接口只有up主本人的cookie才能访问
    #有兴趣的小伙伴可以看看怎么拉取别人的视频下的弹幕和评论（小破站可能有限制）
    url_tpl = 'https://member.bilibili.com/x/web/replies?order=ctime&filter=-1&is_hidden=0&type=1&bvid=BV1Wa4y1x7Gb&pn={page_num}&ps=10'
    for i in range(1, max_page_num):
            url = url_tpl.format(page_num=i)
            res = requests.get(url, headers=headers, timeout=3)
            if not res.ok:
                print(res.status_code, res.text)
                continue
            data = json.loads(res.text)
            replies = data.get('data')
            for replier in replies:
                mid = replier.get('mid')
                nickname = replier.get('replier')
                ctime = replier.get('ctime')
                dt = datetime.datetime.strptime(ctime, '%Y-%m-%d %H:%M:%S')
                ctime = int(time.mktime(dt.timetuple()))
                if (mid != up_id and ctime <= end_time):#把我自己的账号过滤掉 并且 小于等于抽奖结束时间
                    users.append(mid)
                    users_map[mid] = nickname                  

    print("弹幕拉取中... 🚀 🚀 🚀\n")

    max_page_num = 4

    url_tpl = 'https://api.bilibili.com/x/v2/dm/search?oid=175307869&type=1&mids=&keyword=&progress_from=&progress_to=&ctime_from=&ctime_to=&modes=&pool=&attrs=&order=ctime&sort=desc&pn={page_num}&ps=50'

    for i in range(1,max_page_num):
        url = url_tpl.format(page_num = i)
        res = requests.get(url, headers=headers, timeout=3)
        if not res.ok:
            print(res.status_code, res.text)
            continue
        data = json.loads(res.text)
        dms = data.get('data').get('result')
        for dm in dms:
            mid = dm.get('mid')
            nickname = dm.get('uname')
            ctime = dm.get('ctime')
            if (mid != up_id and ctime <= end_time):#把我自己的账号过滤掉 并且 小于等于抽奖结束时间
                users.append(mid)
                users_map[mid] = nickname
            
    #将弹幕和评论中的用户去重
    users = list(set(users))
    print("本次累计参与抽奖用户共 {} 人\n".format(len(users)))

    print("正在捞取幸运儿... 🚀 🚀 🚀  看到名字的小伙伴可以在弹幕举个小手 🙋‍♂️ 🙋‍♀️ \n")

    for v in users_map.values():
        print("{}".format(v).ljust(30), end='\r', flush=True)
        time.sleep(0.1)

    
    #在所有用户中随机选取5名
    #随机数种子选择抽奖名单公布前一天的B站股票收盘价格，即：北京时间 2020-4-15 04:00 am 
    
    random.seed(bili_closed_price)
    random.shuffle(users) #打乱列表
    lottery_users = random.sample(users,5) #随机选取5个用户id
    
    for i in range(5,0,-1):
        print("倒计时：{}".format(i), end='\r',flush=True)
        time.sleep(1)

    print("🎉 🎉 🎉 🎉 🎉 恭喜以下 5 名幸运儿 🎉 🎉 🎉 🎉 🎉\n")
    time.sleep(0.5)
    for mid in lottery_users:
        print(users_map[mid])
        time.sleep(0.5)
    print('\n')
    print('请以上朋友私信联系我领取奖品呀~\n')


if __name__ == '__main__':
    main()
