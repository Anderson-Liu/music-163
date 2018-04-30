"""
根据歌曲 ID 获得所有的歌曲所对应的评论信息
"""
import base64
import json
import sqlite3
import traceback

import psycopg2
import requests
import simplejson
import sql
import time
import threading

from config import proxies
from getlogging import get_logging

logger = get_logging('kindle')


class Comments(object):
    headers = {
        'Host': 'music.163.com',
        'Connection': 'keep-alive',
        'Content-Length': '484',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cookie': 'JSESSIONID-WYYY=b66d89ed74ae9e94ead89b16e475556e763dd34f95e6ca357d06830a210abc7b685e82318b9d1d5b52ac4f4b9a55024c7a34024fddaee852404ed410933db994dcc0e398f61e670bfeea81105cbe098294e39ac566e1d5aa7232df741870ba1fe96e5cede8372ca587275d35c1a5d1b23a11e274a4c249afba03e20fa2dafb7a16eebdf6%3A1476373826753; _iuqxldmzr_=25; _ntes_nnid=7fa73e96706f26f3ada99abba6c4a6b2,1476372027128; _ntes_nuid=7fa73e96706f26f3ada99abba6c4a6b2; __utma=94650624.748605760.1476372027.1476372027.1476372027.1; __utmb=94650624.4.10.1476372027; __utmc=94650624; __utmz=94650624.1476372027.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }

    params = {
        'csrf_token': ''
    }

    data = {
        'params': 'Ak2s0LoP1GRJYqE3XxJUZVYK9uPEXSTttmAS+8uVLnYRoUt/Xgqdrt/13nr6OYhi75QSTlQ9FcZaWElIwE+oz9qXAu87t2DHj6Auu+2yBJDr+arG+irBbjIvKJGfjgBac+kSm2ePwf4rfuHSKVgQu1cYMdqFVnB+ojBsWopHcexbvLylDIMPulPljAWK6MR8',
        'encSecKey': '8c85d1b6f53bfebaf5258d171f3526c06980cbcaf490d759eac82145ee27198297c152dd95e7ea0f08cfb7281588cdab305946e01b9d84f0b49700f9c2eb6eeced8624b16ce378bccd24341b1b5ad3d84ebd707dbbd18a4f01c2a007cd47de32f28ca395c9715afa134ed9ee321caa7f28ec82b94307d75144f6b5b134a9ce1a'
    }

    # proxies = {'http': 'http://127.0.0.1:10800'}

    def get_comments(self, music_id, flag):
        self.headers['Referer'] = 'http://music.163.com/playlist?id=' + str(music_id)

        if flag:
            r = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id),
                              headers=self.headers, params=self.params, data=self.data, proxies=proxies)
        else:
            r = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id),
                              headers=self.headers, params=self.params, data=self.data)
        return r.json()


if __name__ == '__main__':
    my_comment = Comments()


    def fetch_comment(music_id, retry_count, flag, connection):
        try:
            comments = my_comment.get_comments(music_id, flag)
            print(comments)
            if comments['total'] > 0:
                sql.insert_comments(music_id, comments['total'], str(comments), connection)
        except simplejson.scanner.JSONDecodeError:
            # Set status to already crawled
            sql.update_music_status(music_id)
            pass
        except Exception as e:
            traceback.print_exc()
            time.sleep(60)

    def save_comments(musics, flag):
        retry_count = 0
        # connection = sqlite3.connect('music163.db')
        connection = psycopg2.connect(database='music163')
        for i in musics:
            my_music_id = i[0]
            if '-' in my_music_id:
                my_music_id.replace('-', '')
            logger.info(my_music_id)
            fetch_comment(my_music_id, retry_count, flag, connection)

    music_before = sql.get_before_music()
    music_medium = sql.get_medium_music()
    music_after = sql.get_after_music()
    music_in_play_list = sql.get_music_from_play_list()
    logger.info('Done fetch left and right data.')

    t1 = threading.Thread(target=save_comments, args=(music_before, True))
    t2 = threading.Thread(target=save_comments, args=(music_medium, True))
    t3 = threading.Thread(target=save_comments, args=(music_after, True))
    t4 = threading.Thread(target=save_comments, args=(music_in_play_list, True))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
