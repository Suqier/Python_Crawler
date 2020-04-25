# coding: utf-8
# date: 2020/04/25
# author: Suqier
# 抓取猫眼电影TOP100榜单并写入文件
# Copyright © Suqier 2020

import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool


class GetMYMovie(object):
    def __init__(self):
        self.BASE_URL = "https://maoyan.com/board/4"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
            'Host': 'maoyan.com',
            'Referer': 'https://maoyan.com/board',
            'Upgrade-Insecure-Requests': '1'
        }
        # self.cookies = {
        #      'cookies': ''
        # }
        self.pattern = '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)"\salt="(.*?)".*?star">\s(.*?)\s</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i></p>'
        self.proxies = {
            "http": "http://47.113.108.233:8080",
            "https": "http://47.113.108.233:8080"
        }

    def get_one_page(self, url):
        try:
            response = requests.get(url=url, headers=self.headers)    #, cookies=self.cookies, proxies=self.proxies
            print(response.status_code)
            if response.status_code == 200:
                return response.text
            else:
                return str(response.status_code)
        except RequestException:
            return "RequestException: " + url

    def parse_one_page(self, origin_html):
        if len(origin_html) < 50:
            return "Html_Error"
        pattern = re.compile(self.pattern, re.S)
        items = re.findall(pattern, origin_html)
        for item in items:
            yield {
                'index':  item[0],
                'img': item[1],
                'title': item[2],
                'actor': item[3].strip()[3:],
                'time': item[4].strip()[5:],
                'score': item[5] + item[6]
            }

    @ staticmethod
    def write_to_file(temp_content):
        with open('result.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(temp_content, ensure_ascii=False) + '\n')
            f.close()

    def get_all(self):
        offset = range(0, 100, 10)
        for i in offset:
            if i == 0:
                url = self.BASE_URL
            else:
                url = self.BASE_URL + "?offset=" + str(i)

            content = self.get_one_page(url)
            for each in self.parse_one_page(content):
                print(each)
                self.write_to_file(each)


if __name__ == '__main__':
    get_MY = GetMYMovie()
    get_MY.get_all()
    print("Done!")
