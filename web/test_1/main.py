# coding: utf-8
# Time: 2020/04/23
# Author: Suqier
# Copyright © Suqier 2020


import time
import requests
from requests.exceptions import RequestException
from contextlib import closing
import json


class GetPhotos(object):

    def __init__(self):
        self.photos_id = []
        self.download_server = "https://unsplash.com/photos/xxx/download"
        self.target = "http://unsplash.com/napi/photos"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                      + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}

    def get_ids(self):
        try:
            response = requests.get(url=self.target, headers=self.headers)
            if response.status_code == 200:
                raw_json = response.text
            else:
                raw_json = response.status_code
        except RequestException:
            return "RequestException!"

        loaded_json = json.loads(raw_json)
        for each in loaded_json:
            id_tmp = each['id']
            self.photos_id.append(id_tmp)

    def download_photo(self, photo_id, filename):
        target = self.download_server.replace('xxx', photo_id)
        with closing(requests.get(url=target, stream=True, headers=self.headers)) as r:
            with open('%d.jpg' % filename, 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()


if __name__ == "__main__":
    gp = GetPhotos()
    print('Start get photo...')
    gp.get_ids()
    print('Downloading...')
    for i in range(len(gp.photos_id)):
        print('%d th photo downloading...'%(i+1))
        gp.download_photo(gp.photos_id[i], (i+1))




