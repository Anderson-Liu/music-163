import json
import re

import requests
import sql
from bs4 import BeautifulSoup
from music_163.config import proxies


class MusicByPlayList:
    def __init__(self):
        self.__headers = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }

    def curl_playlist(self, playlist_id):
        # playlist_api = "http://music.163.com/#/playlist?id={}"
        playlist_api = "http://music.163.com/api/playlist/detail?id={}&offset=0&total=true&limit=1001"
        play_detail_url = playlist_api.format(playlist_id)
        try:
            s = requests.session()
            bs = BeautifulSoup(s.get(play_detail_url, headers=self.__headers, proxies=proxies).content,
                               "html.parser")
            playlist = json.loads(bs.text)['result']
            return playlist
        except Exception as e:
            print("抓取歌单页面存在问题：{} 歌单ID：{}".format(e, playlist_id))

    def get_playlist(self, playlist_id):
        playlist = self.curl_playlist(playlist_id)

        print("《" + playlist['name'] + "》")
        author = playlist['creator']['nickname']
        pc = str(playlist['playCount'])
        sc = str(playlist['subscribedCount'])
        rc = str(playlist['shareCount'])
        cc = str(playlist['commentCount'])

        print("维护者：{}  播放：{} 关注：{} 分享：{} 评论：{}".format(author, pc, sc, rc, cc))
        print("描述：{}".format(playlist['description']))
        print("标签：{}".format(",".join(playlist['tags'])))
        sql.update_play_list_content(playlist_id, author, pc, sc, rc, cc)

        for music in playlist['tracks']:
            artists = []
            for s in music['artists']:
                artists.append(s['name'])
            ms = music['name']
            ar = ",".join(artists)
            ab = music['album']['name']
            ab_id = music['album']['id']
            id = music['id']
            print('ID: {}, NAME: {}, ARTIST: {}, ALBUM: {}'.format(id, ms, ar, ab))
            sql.insert_music_by_play_list(id, ms, playlist_id, ab_id)


if __name__ == '__main__':
    playlists = sql.get_all_play_list()
    for list_id in playlists:
        MusicByPlayList().get_playlist(list_id[0])
