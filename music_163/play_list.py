# -*- coding: utf-8 -*-
import requests
import sql
from bs4 import BeautifulSoup

from config import proxies


def curl(url, headers):
    try:
        s = requests.session()
        bs = BeautifulSoup(s.get(url, headers=headers, proxies=proxies).content, "html.parser")
        return bs
    except Exception:
        raise


class Playlist:
    __play_url = None
    __headers = None

    def __init__(self):
        self.__headers = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        self.__play_url = "http://music.163.com/discover/playlist/?order=hot&cat={}&limit=35&offset={}"

    def view_capture(self, page, music_type):
        play_url = self.__play_url.format(music_type, page * 35)
        titles = []
        try:
            acmsk = {'class': 'msk'}
            scnb = {'class': 'nb'}
            dcu = {'class': 'u-cover u-cover-1'}
            ucm = {'class': 'm-cvrlst f-cb'}
            s = requests.session()
            bs = BeautifulSoup(s.get(play_url, headers=self.__headers, proxies=proxies).content, "html.parser")
            if bs is None:
                print("Detect page empty when crawl play list: play_list_type：{} page：{}".format(music_type.encode('utf8'), page))
            else:
                lst = bs.find('ul', ucm)
                for play in lst.find_all('div', dcu):
                    title = play.find('a', acmsk)['title']
                    play_list_id = play.find('a', acmsk)['href'].replace("/playlist?id=", "")
                    views = play.find('span', scnb).text.replace('万', '0000')
                    print(title, play_list_id, views)
                    sql.insert_play_list(title, play_list_id, views, music_type)
                return titles
        except Exception as e:
            print("Error when crawl play list：{} play_list_type：{} page：{}".format(e, music_type.encode('utf8'), page))
            raise


if __name__ == '__main__':
    music_type_count_dict = {'吉他': 41, '轻音乐': 37, '钢琴': 41, '器乐': 42}
    for music_type, page_count in music_type_count_dict.items():
        for i in range(page_count):
            Playlist().view_capture(i, music_type)
