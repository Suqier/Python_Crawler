# coding: UTF-8
# Time: 2020/04/17
# Author: Suqier
# Almost built a frame for Python Web Crawler privately
# Copyright © Suqier 2020


import logging
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s | [line:%(lineno)d] - %(levelname)s: %(message)s')


index_url = "https://www.biqukan.com/38_38836/"  # 小说的目录页
host_url = "https://www.biqukan.com"             # 网站的首页


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            logging.info('200')
            response.encoding = 'gbk'
            return response.text
        else:
            logging.info('Status code error')
            return None
    except RequestException:
        logging.info('RequestException!')
        return None


def parse_page(html):
    if html is None:
        return None
    bf = BeautifulSoup(html, 'lxml')
    texts = bf.find_all('div', id='content')
    return texts[0].text.replace('\xa0'*8, '\n\n')


def parse_index(html):
    bf = BeautifulSoup(html, 'lxml')
    index = bf.find_all('div', class_='listmain')
    a_bf = BeautifulSoup(str(index[0]), 'lxml')
    a = a_bf.find_all('a')
    u_list = []
    n_list = []
    for each in a:
        chapter_url = host_url + each.get('href')
        chapter_name = each.string
        u_list.append(chapter_url)
        n_list.append(chapter_name)
    return n_list, u_list


def write_into_file(list_1):
    i = 0
    for url in list_1:
        response = get_one_page(url)
        txt = parse_page(response)
        if txt is None:
            i += 1
        else:
            with open(str(name_list[i]) + '.txt', 'w', encoding="utf-8") as f:
                f.write(txt)
            i += 1


if __name__ == '__main__':
    logging.info('Start...')                        # 系统提示开始
    index_html = get_one_page(index_url)     # get目录页的HTML
    name_list, url_list = parse_index(index_html)   # 解析目录页的HTML，得出每个章节的标题和链接
    name_list = name_list[12:]                      # 稍微处理一下
    url_list = url_list[12:]                        # 稍微处理一下
    write_into_file(url_list)                       # 下载小说
    logging.info('Done!')                           # 系统提示结束

