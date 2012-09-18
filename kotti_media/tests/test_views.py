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
from kotti_media.views import AudioView
from kotti_media.views import VideoView


class ViewsTests(UnitTestBase):

    def test_audio_view(self):

        root = get_root()
        audio = root['audio'] = Audio()

        view = AudioView(audio, DummyRequest()).view()

        assert ('mp3_url' in view) and (view['mp3_url'] is None)
        assert ('poster_url' in view) and (view['poster_url'] is None)

        audio['mp3'] = Mp3File()
        audio['poster'] = Image()

        view = AudioView(audio, DummyRequest()).view()

        assert ('mp3_url' in view) and (view['mp3_url'] == 'http://example.com/audio/mp3/@@attachment-view')
        assert ('poster_url' in view) and (view['poster_url'] == 'http://example.com/audio/poster/@@attachment-view')

    def test_video_view(self):

        root = get_root()
        video = root['video'] = Video()

        view = VideoView(video, DummyRequest()).view()

        assert ('chapters_url' in view) and (view['chapters_url'] is None)
        assert ('mp4_url' in view) and (view['mp4_url'] is None)
        assert ('ogg_url' in view) and (view['ogg_url'] is None)
        assert ('poster_url' in view) and (view['poster_url'] is None)
        assert ('subtitles_url' in view) and (view['subtitles_url'] is None)
        assert ('webm_url' in view) and (view['webm_url'] is None)

        video['chapters'] = ChaptersFile()
        video['mp4'] = Mp4File()
        video['ogg'] = OggFile()
        video['poster'] = Image()
        video['subs'] = SubtitlesFile()
        video['webm'] = WebmFile()

        view = VideoView(video, DummyRequest()).view()

        assert ('chapters_url' in view) and (view['chapters_url'] == 'http://example.com/video/chapters/@@attachment-view')
        assert ('mp4_url' in view) and (view['mp4_url'] == 'http://example.com/video/mp4/@@attachment-view')
        assert ('ogg_url' in view) and (view['ogg_url'] == 'http://example.com/video/ogg/@@attachment-view')
        assert ('poster_url' in view) and (view['poster_url'] == 'http://example.com/video/poster/@@attachment-view')
        assert ('subtitles_url' in view) and (view['subtitles_url'] == 'http://example.com/video/subs/@@attachment-view')
        assert ('webm_url' in view) and (view['webm_url'] == 'http://example.com/video/webm/@@attachment-view')
