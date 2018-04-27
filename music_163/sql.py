"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import sqlite3

connection = sqlite3.connect('music163.db')


# 保存评论
def insert_comments(music_id, comments, detail, connection0):
    cursor = connection0.cursor()
    sql = "INSERT OR IGNORE INTO `comments` (`MUSIC_ID`, `COMMENTS`, `DETAILS`) VALUES (?, ?, ?)"
    cursor.execute(sql, (music_id, comments, detail))
    connection0.commit()


# 保存音乐
def insert_music(music_id, music_name, album_id):
    cursor = connection.cursor()
    sql = "INSERT OR IGNORE INTO `musics` (`MUSIC_ID`, `MUSIC_NAME`, `ALBUM_ID`) VALUES (?, ?, ?)"
    cursor.execute(sql, (music_id, music_name, album_id))
    connection.commit()


# 保存专辑
def insert_album(album_id, artist_id):
    cursor = connection.cursor()
    sql = "INSERT OR IGNORE INTO `albums` (`ALBUM_ID`, `ARTIST_ID`) VALUES (?, ?)"
    cursor.execute(sql, (album_id, artist_id))
    sql_update = "UPDATE `artists` set `IS_CRAWL`=1 where `ARTIST_ID`=?"
    cursor.execute(sql_update, (artist_id,))
    connection.commit()


# 保存歌手
def insert_artist(artist_id, artist_name):
    cursor = connection.cursor()
    sql = "INSERT OR IGNORE INTO `artists` (`ARTIST_ID`, `ARTIST_NAME`) VALUES (?, ?)"
    cursor.execute(sql, (artist_id, artist_name))
    connection.commit()


# 获取所有歌手的 ID
def get_all_artist():
    cursor = connection.cursor()
    sql = "SELECT `ARTIST_NAME`,`ARTIST_ID` FROM `artists` WHERE `IS_CRAWL`=0 ORDER BY ARTIST_ID"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取所有专辑的 ID
def get_all_album():
    cursor = connection.cursor()
    sql = "SELECT `ALBUM_ID` FROM `albums` ORDER BY ALBUM_ID"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取所有音乐的 ID
def get_all_music():
    cursor = connection.cursor()
    sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取前一半音乐的 ID
def get_before_music():
    cursor = connection.cursor()
    sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 0, 800000"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取后一半音乐的 ID
def get_after_music():
    cursor = connection.cursor()
    sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 800000, 1197429"
    cursor.execute(sql, ())
    return cursor.fetchall()


def dis_connect():
    connection.close()
