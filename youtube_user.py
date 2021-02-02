from dataclasses import dataclass
import os
from collections import UserDict
import datetime

from ytmusicapi import YTMusic

__all__ = [
    "YTUser",
    "UsersDB",
]

HEADERS_FOLDER_TEMPLATE = os.path.abspath(
    os.path.join(__file__, "..", "headers", "{tg_id}_headers_auth.json")
)

ID_FOLDER_TEMPLATE = os.path.abspath(
    os.path.join(__file__, "..", "ids", "{tg_id}_youtube_id.json")
)


@dataclass
class YTUser:
    tg_id: int

    @property
    def headers_file_path(self) -> str:
        res = HEADERS_FOLDER_TEMPLATE.format(tg_id=self.tg_id)
        return res

    @property
    def id_file_path(self) -> str:
        res = ID_FOLDER_TEMPLATE.format(tg_id=self.tg_id)
        return res

    @property
    def yt_music_id(self) -> str:
        with open(self.id_file_path, 'r') as f:
            return f.readline()

    @yt_music_id.setter
    def yt_music_id(self, value: str):
        with open(self.id_file_path, 'w') as f:
            f.write(str(value))

    @property
    def has_yt_music_id(self) -> bool:
        try:
            with open(self.id_file_path, 'r') as f:
                f.read(1)
            res = True
        except FileNotFoundError:
            res = False
        return res

    @property
    def has_headers(self) -> bool:
        try:
            with open(self.headers_file_path, 'r') as f:
                f.read(1)
            res = True
        except FileNotFoundError:
            res = False
        return res

    @property
    def youtube_music(self) -> YTMusic:
        inst = YTMusic(self.headers_file_path, self.yt_music_id)
        return inst

    def store_headers(self, headers: str) -> None:
        YTMusic.setup(
            self.headers_file_path,
            headers
        )
        return None

    def copy_playlist(
            self,
            playlist_to_copy: str = "LM",
            limit: int = 1000,
    ) -> str:
        music = self.youtube_music
        liked_music = music.get_playlist(playlist_to_copy, limit=limit)
        tracks = [
            track["videoId"]
            for track in liked_music["tracks"]
        ]

        ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        playist_name = f"Liked Music - Copy ({ts})"

        success = music.create_playlist(
            playist_name,
            "Public copy of a Liked Music Playlist",
            "PUBLIC",
            video_ids=tracks,
        )

        return playist_name if success else "Failed to create playlist"

    def __str__(self):
        res = f"YouTubeMusicUser(tg_id={self.tg_id}, has_youtube_id={self.has_yt_music_id}, has_headers={self.has_headers})"
        return res


class UsersDB(UserDict):
    def __missing__(self, key) -> YTUser:
        return YTUser(key)
