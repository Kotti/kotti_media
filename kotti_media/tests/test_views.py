# -*- coding: utf-8 -*-

import os

from kotti.resources import Image
from kotti.resources import get_root
from kotti.testing import DummyRequest

from kotti_media.resources import Audio
from kotti_media.resources import ChaptersFile
from kotti_media.resources import M4aFile
from kotti_media.resources import Mp3File
from kotti_media.resources import Mp4File
from kotti_media.resources import OgaFile
from kotti_media.resources import OgvFile
from kotti_media.resources import SubtitlesFile
from kotti_media.resources import Video
from kotti_media.resources import WavFile
from kotti_media.resources import WebmFile
from kotti_media.views import AudioView
from kotti_media.views import MediaFolderView
from kotti_media.views import PlayerOptionsSchema
from kotti_media.views import VideoView
from kotti_media.views import default_player_options

here = os.path.abspath(os.path.dirname(__file__))


def test_audio_view(db_session):

    root = get_root()
    audio = root['audio'] = Audio()

    view = AudioView(audio, DummyRequest()).element()

    assert ('m4a_url' in view) and (view['m4a_url'] is None)
    assert ('mp3_url' in view) and (view['mp3_url'] is None)
    assert ('oga_url' in view) and (view['oga_url'] is None)
    assert ('wav_url' in view) and (view['wav_url'] is None)
    assert ('poster_url' in view) and (view['poster_url'] is None)

    audio['m4a'] = M4aFile()
    audio['mp3'] = Mp3File()
    audio['oga'] = OgaFile()
    audio['wav'] = WavFile()
    audio['poster'] = Image()

    view = AudioView(audio, DummyRequest()).element()
    # import pdb; pdb.set_trace()
    assert ('m4a_url' in view)  # and (view['m4a_url'] is None)
    assert ('mp3_url' in view)  # and (view['mp3_url'] is None)
    assert ('oga_url' in view)  # and (view['oga_url'] is None)
    assert ('wav_url' in view)  # and (view['wav_url'] is None)
    assert ('poster_url' in view)  # and (view['poster_url'] is None)

    audio['m4a'].data = open(os.path.join(here, "distortion.m4a")).read()
    audio['mp3'].data = open(os.path.join(here, "distortion.mp3")).read()
    audio['oga'].data = open(os.path.join(here, "distortion.oga")).read()
    audio['wav'].data = open(os.path.join(here, "distortion.wav")).read()
    audio['poster'].data = open(os.path.join(here, "distortion.png")).read()

    view = AudioView(audio, DummyRequest()).element()

    assert ('m4a_url' in view) and (
        view['m4a_url'] == 'http://example.com/audio/m4a/@@attachment-view')
    assert ('mp3_url' in view) and (
        view['mp3_url'] == 'http://example.com/audio/mp3/@@attachment-view')
    assert ('oga_url' in view) and (
        view['oga_url'] == 'http://example.com/audio/oga/@@attachment-view')
    assert ('wav_url' in view) and (
        view['wav_url'] == 'http://example.com/audio/wav/@@attachment-view')
    assert ('poster_url' in view) and (
        view['poster_url'] == 'http://example.com/audio/poster/image')


def test_video_view(db_session):

    root = get_root()
    video = root['video'] = Video()

    view = VideoView(video, DummyRequest()).element()

    assert ('mp4_url' in view)  # and (view['mp4_url'] is None)
    assert ('ogv_url' in view)  # and (view['ogv_url'] is None)
    assert ('webm_url' in view)  # and (view['webm_url'] is None)
    assert ('subtitles_url' in view)  # and (view['subtitles_url'] is None)
    assert ('chapters_url' in view)  # and (view['chapters_url'] is None)
    assert ('poster_url' in view)  # and (view['poster_url'] is None)

    video['mp4'] = Mp4File()
    video['ogv'] = OgvFile()
    video['webm'] = WebmFile()
    video['subs'] = SubtitlesFile()
    video['chapters'] = ChaptersFile()
    video['poster'] = Image()

    view = VideoView(video, DummyRequest()).element()

    assert ('mp4_url' in view)  # and (view['mp4_url'] is None)
    assert ('ogv_url' in view)  # and (view['ogv_url'] is None)
    assert ('webm_url' in view)  # and (view['webm_url'] is None)
    assert ('subtitles_url' in view)  # and (view['subtitles_url'] is None)
    assert ('chapters_url' in view)  # and (view['chapters_url'] is None)
    assert ('poster_url' in view)  # and (view['poster_url'] is None)

    video['mp4'].data = open(os.path.join(here, "distortion.m4v")).read()
    video['ogv'].data = open(os.path.join(here, "distortion.ogv")).read()
    video['webm'].data = open(os.path.join(here, "distortion.webm")).read()
    video['subs'].data = open(os.path.join(here, "distortion.srt")).read()
    video['chapters'].data = open(os.path.join(here, "distortion.srt")).read()
    video['poster'].data = open(os.path.join(here, "distortion.png")).read()

    view = VideoView(video, DummyRequest()).element()

    assert ('mp4_url' in view) and (
        view['mp4_url'] ==
        'http://example.com/video/mp4/@@attachment-view')
    assert ('ogv_url' in view) and (
        view['ogv_url'] ==
        'http://example.com/video/ogv/@@attachment-view')
    assert ('webm_url' in view) and (
        view['webm_url'] ==
        'http://example.com/video/webm/@@attachment-view')
    assert ('subtitles_url' in view) and (
        view['subtitles_url'] ==
        'http://example.com/video/subs/@@attachment-view')
    assert ('chapters_url' in view) and (
        view['chapters_url'] ==
        'http://example.com/video/chapters/@@attachment-view')
    assert ('poster_url' in view) and (
        view['poster_url'] ==
        'http://example.com/video/poster/image')


def test_media_folder_view(db_session):

    root = get_root()
    audio = root['audio'] = Audio()
    video = root['video'] = Video()
    view = MediaFolderView(root, DummyRequest()).view()

    assert 'media' in view
    assert audio in view['media']
    assert video in view['media']
    assert 'can_edit_player_options' in view


def test_options(db_session):

    root = get_root()
    audio = root['audio'] = Audio()

    options = AudioView(audio, DummyRequest()).options
    assert options == default_player_options

    audio.annotations = {
        "foo": "bar",
    }

    options = AudioView(audio, DummyRequest()).options
    assert options == default_player_options

    audio.annotations = {
        "startVolume": 0.5,
    }

    options = AudioView(audio, DummyRequest()).options
    assert options["startVolume"] == 0.5


def test_player_options(db_session):

    root = get_root()
    audio = root['audio'] = Audio()

    # test GET
    player_options = AudioView(audio, DummyRequest()).player_options()
    assert player_options.body.find("<form") > -1
    assert player_options.body.find(
        'action="http://example.com/audio/player_options"') > -1

    # test POST with missing parameters
    post_request = DummyRequest()
    post_request.POST = {'save': 'save'}
    player_options = AudioView(audio, post_request).player_options()
    assert player_options.body.find("There was a problem with your submission") > -1  # noqa

    # test POST with all parameters
    post_request = DummyRequest()
    post_request.POST = default_player_options
    post_request.POST = PlayerOptionsSchema().serialize(post_request.POST)
    post_request.POST.update({'save': 'save'})
    player_options = AudioView(audio, post_request).player_options()
    assert player_options.body.find("edit_player_options_success = true") > -1
