"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import sqlite3

connection = sqlite3.connect('music163.db', check_same_thread=False)


# 保存歌单
def insert_play_list(title, play_list_id, views, music_type):
    cursor = connection.cursor()
    sql = "INSERT OR IGNORE INTO `play_lists` (`PLAY_LIST_ID`, `TITLE`, `VIEWS`, `MUSIC_TYPE`) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (play_list_id, title, views, music_type))
    connection.commit()


# 保存评论
def insert_comments(music_id, comments, detail):
    cursor = connection.cursor()
    sql = "INSERT OR IGNORE INTO `comments` (`MUSIC_ID`, `COMMENTS`, `DETAILS`) VALUES (?, ?, ?)"
    cursor.execute(sql, (music_id, comments, detail))
    connection.commit()
    update_music_status(music_id)


# 保存音乐
def insert_music_by_play_list(music_id, music_name, play_list_id):
    cursor = connection.cursor()
    sql = "SELECT id from musics where MUSIC_ID=?"
    cursor.execute(sql, (music_id,))
    is_exist = cursor.fetchall()
    if is_exist:
        sql = "INSERT INTO `musics` (`MUSIC_ID`, `MUSIC_NAME`, `PLAY_LIST_ID`) VALUES (?, ?, ?)"
    else:
        sql = "UPDATE `musics` SET `MUSIC_ID`=?, `MUSIC_NAME`=?, `PLAY_LIST_ID`=?"
    cursor.execute(sql, (music_id, music_name, play_list_id))
    connection.commit()
    update_play_list_status(play_list_id)


# 保存音乐
def insert_music(music_id, music_name, album_id):
    cursor = connection.cursor()
    sql = "INSERT OR REPLACE INTO `musics` (`MUSIC_ID`, `MUSIC_NAME`, `ALBUM_ID`) VALUES (?, ?, ?)"
    cursor.execute(sql, (music_id, music_name, album_id))
    connection.commit()
    update_album_status(album_id)


# 保存专辑
def insert_album(album_id, artist_id):
    cursor = connection.cursor()
    sql = "INSERT OR IGNORE INTO `albums` (`ALBUM_ID`, `ARTIST_ID`) VALUES (?, ?)"
    cursor.execute(sql, (album_id, artist_id))
    connection.commit()
    update_artist_status(artist_id)


# 保存歌手
def insert_artist(artist_id, artist_name):
    cursor = connection.cursor()
    sql = "INSERT OR IGNORE INTO `artists` (`ARTIST_ID`, `ARTIST_NAME`) VALUES (?, ?)"
    cursor.execute(sql, (artist_id, artist_name))
    connection.commit()


def update_artist_status(artist_id):
    cursor = connection.cursor()
    sql_update = "UPDATE `artists` set `IS_CRAWL`=1 where `ARTIST_ID`=?"
    cursor.execute(sql_update, (artist_id,))
    connection.commit()


def update_album_status(album_id):
    cursor = connection.cursor()
    sql_update = "UPDATE `albums` set `IS_CRAWL`=1 where `ALBUM_ID`=?"
    cursor.execute(sql_update, (album_id,))
    connection.commit()


def update_music_status(music_id):
    cursor = connection.cursor()
    sql_update = "UPDATE `musics` set `IS_CRAWL`=1 where `MUSIC_ID`=?"
    cursor.execute(sql_update, (music_id,))
    connection.commit()


def update_play_list_status(play_list_id):
    cursor = connection.cursor()
    sql_update = "UPDATE `play_lists` set `IS_CRAWL`=1 where `PLAY_LIST_ID`=?"
    cursor.execute(sql_update, (play_list_id,))
    connection.commit()


def update_play_list_content(play_list_id, creator, play_count, subscribe_count, share_count, commend_count):
    cursor = connection.cursor()
    sql_update = "UPDATE `play_lists` set IS_CRAWL=1, CREATER=?, PLAY_COUNT=?, " \
                 "SUBSCRIBE_COUNT=?, SHARE_COUNT=?, COMMEND_COUNT=? where `PLAY_LIST_ID`=?"
    cursor.execute(sql_update, (play_list_id, creator, play_count, subscribe_count, share_count, commend_count))
    connection.commit()


# 获取所有歌手的 ID
def get_all_artist():
    cursor = connection.cursor()
    sql = "SELECT id, `ARTIST_NAME`,`ARTIST_ID` FROM `artists` WHERE `IS_CRAWL`=0 and id > 20000 ORDER BY ARTIST_ID"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取所有专辑的 ID
def get_all_album():
    cursor = connection.cursor()
    sql = "SELECT `ALBUM_ID` FROM `albums` WHERE `IS_CRAWL`=0 ORDER BY ALBUM_ID"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取前半部分专辑的 ID
def get_left_album():
    cursor = connection.cursor()
    sql = "SELECT `ALBUM_ID` FROM `albums` WHERE `IS_CRAWL`=0 and id > 150000 ORDER BY ALBUM_ID"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取后半部分专辑的 ID
def get_right_album():
    cursor = connection.cursor()
    sql = "SELECT `ALBUM_ID` FROM `albums` WHERE `IS_CRAWL`=0 and id < 150000 ORDER BY ALBUM_ID"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取所有音乐的 ID
def get_all_music():
    cursor = connection.cursor()
    sql = "SELECT DISTINCT(`MUSIC_ID`) FROM `musics` WHERE `IS_CRAWL`=0 ORDER BY MUSIC_ID"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取前一半音乐的 ID
def get_before_music():
    cursor = connection.cursor()
    sql = "SELECT DISTINCT(`MUSIC_ID`) FROM `musics` WHERE `IS_CRAWL`=0 ORDER BY MUSIC_ID LIMIT 0, 800000"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取后一半音乐的 ID
def get_after_music():
    cursor = connection.cursor()
    sql = "SELECT DISTINCT(`MUSIC_ID`) FROM `musics` WHERE `IS_CRAWL`=0 ORDER BY MUSIC_ID LIMIT 800000, 1197429"
    cursor.execute(sql, ())
    return cursor.fetchall()


# 获取所有play_list
def get_all_play_list():
    cursor = connection.cursor()
    sql = "SELECT DISTINCT(`PLAY_LIST_ID`) FROM `play_lists` WHERE `IS_CRAWL`=1"
    cursor.execute(sql, ())
    return cursor.fetchall()


def dis_connect():
    connection.close()
