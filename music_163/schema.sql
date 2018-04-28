CREATE TABLE `albums` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `ALBUM_ID` varchar(45) NOT NULL
,  `ARTIST_ID` varchar(45) NOT NULL
, IS_CRAWL integer NOT NULL DEFAULT '0',  UNIQUE (`ALBUM_ID`,`ARTIST_ID`)
);
CREATE TABLE `artists` (
  `id` integer NOT NULL DEFAULT '0'
,  `ARTIST_ID` varchar(45) NOT NULL
,  `ARTIST_NAME` text NOT NULL
,  `IS_CRAWL` integer NOT NULL DEFAULT '0'
,  UNIQUE (`ARTIST_ID`)
);
CREATE TABLE `comments` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `MUSIC_ID` varchar(45) NOT NULL
,  `COMMENTS` varchar(45) DEFAULT NULL
,  `DETAILS` varchar(45) DEFAULT NULL
,  UNIQUE (`MUSIC_ID`,`COMMENTS`)
);
CREATE TABLE `musics` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `MUSIC_ID` varchar(45) NOT NULL
,  `MUSIC_NAME` varchar(45) DEFAULT NULL
,  `ALBUM_ID` varchar(45) DEFAULT NULL
, IS_CRAWL integer NOT NULL DEFAULT '0',  UNIQUE (`MUSIC_ID`,`ALBUM_ID`)
);

CREATE TABLE `play_lists` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `PLAY_LIST_ID` varchar(45) NOT NULL
,  `TITLE` text NOT NULL
,  `VIEWS` varchar(45) NOT NULL
,  `MUSIC_TYPE` varchar(45) NOT NULL
, IS_CRAWL integer NOT NULL DEFAULT '0',  UNIQUE (`PLAY_LIST_ID`)
);

alter table musics add PLAY_LIST_ID varchar default NULL;

alter table play_lists add CREATER varchar default NULL;
alter table play_lists add PLAY_COUNT varchar default NULL;
alter table play_lists add SUBSCRIBE_COUNT varchar default NULL;
alter table play_lists add SHARE_COUNT varchar default NULL;
alter table play_lists add COMMEND_COUNT varchar default NULL;



