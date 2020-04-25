# coding: utf-8
# date: 2020/04/25
# author: Suqier
# 抓取豆瓣电影TOP250榜单并写入文件
# Copyright © Suqier 2020

import requests
from requests.exceptions import RequestException
import re
import json


class GetDBMovie(object):
    def __init__(self):
        self.BASE_URL = "https://movie.douban.com/top250?start=xxx&filter="
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        }
        # self.cookies = {
        #      'cookies': ''
        # }
        self.pattern = 'class="">(\d+)</em>.*?href="(.*?)">.*?alt="(.*?)".*?src="(.*?)"\sclass="">.*?class="bd">.*?class="">(.*?)&nbsp;&nbsp;&nbsp;(.*?)<br>(.*?)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)</p>.*?"v:average">(.*?)</span>'
        #                        index            home_page      movie_name       img                                      director                actor     year              area             class                   score
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
                'home_page': item[1],
                'movie_name': item[2],
                'img': item[3].strip(),
                'director': item[4].strip()[3:],
                'actor': item[5][3:],
                'year': item[6].strip(),
                'area': item[7],
                'class': item[8].strip(),
                'score': item[9]
            }

    @ staticmethod
    def write_to_file(temp_content):
        with open('result.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(temp_content, ensure_ascii=False) + '\n')
            f.close()

    def get_all(self):
        offset = range(0, 250, 25)
        for i in offset:
            if i == 0:
                url = self.BASE_URL
                url = url[:31]
            else:
                url = self.BASE_URL.replace("xxx", str(i))

            content = self.get_one_page(url)
            for each in self.parse_one_page(content):
                print(each)
                self.write_to_file(each)


if __name__ == '__main__':
    db = GetDBMovie()
    db.get_all()
    print("Done!")
