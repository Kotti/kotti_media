# -*- coding: utf-8 -*-

from kotti.resources import get_root
from kotti.resources import Image
from kotti.testing import DummyRequest
from kotti.testing import UnitTestBase
from kotti_media.resources import Audio
from kotti_media.resources import ChaptersFile
from kotti_media.resources import Mp3File
from kotti_media.resources import Mp4File
from kotti_media.resources import OggFile
from kotti_media.resources import SubtitlesFile
from kotti_media.resources import Video
from kotti_media.resources import WebmFile


class ResourcesTests(UnitTestBase):

    def test_audio(self):

        root = get_root()
        audio = Audio()
        assert audio.type_info.addable(root, DummyRequest()) is True
        root['audio'] = audio

        mp3 = Mp3File()
        poster = Image()

        assert audio.mp3_file is None
        assert audio.poster_file is None
        # there is no child of type Mp3File yet, the UI should present the add link
        assert mp3.type_info.addable(audio, DummyRequest()) is True

        audio['mp3'] = mp3
        audio['poster'] = poster

        assert audio.mp3_file is not None
        assert audio.poster_file is not None
        # the add link must not be shown, because there is already a child of type Mp3File
        assert mp3.type_info.addable(audio, DummyRequest()) is False

    def test_video(self):

        root = get_root()
        video = Video()
        assert video.type_info.addable(root, DummyRequest()) is True
        root['video'] = video

        chapters = ChaptersFile()
        mp4 = Mp4File()
        ogg = OggFile()
        poster = Image()
        subtitles = SubtitlesFile()
        webm = WebmFile()

        assert video.chapters_file is None
        assert video.mp4_file is None
        assert video.ogg_file is None
        assert video.poster_file is None
        assert video.subtitles_file is None
        assert video.webm_file is None

        assert chapters.type_info.addable(video, DummyRequest()) is True
        assert mp4.type_info.addable(video, DummyRequest()) is True
        assert ogg.type_info.addable(video, DummyRequest()) is True
        assert subtitles.type_info.addable(video, DummyRequest()) is True
        assert webm.type_info.addable(video, DummyRequest()) is True

        video['chapters'] = chapters
        video['mp4'] = mp4
        video['ogg'] = ogg
        video['poster'] = poster
        video['subtitles'] = subtitles
        video['webm'] = webm

        assert video.chapters_file is not None
        assert video.mp4_file is not None
        assert video.ogg_file is not None
        assert video.poster_file is not None
        assert video.subtitles_file is not None
        assert video.webm_file is not None

        assert chapters.type_info.addable(video, DummyRequest()) is False
        assert mp4.type_info.addable(video, DummyRequest()) is False
        assert ogg.type_info.addable(video, DummyRequest()) is False
        assert subtitles.type_info.addable(video, DummyRequest()) is False
        assert webm.type_info.addable(video, DummyRequest()) is False
