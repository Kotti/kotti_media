# -*- coding: utf-8 -*-

"""
Created on 2014-11-10
:author: Andreas Kaiser (disko)

This file contains the populator that is used in the development configuration.
"""

import os

import transaction
from kotti.populate import populate as kotti_populate
from kotti.resources import get_root
from kotti.resources import Image

from kotti_media.resources import Audio
# from kotti_media.resources import ChaptersFile
from kotti_media.resources import M4aFile
from kotti_media.resources import Mp3File
from kotti_media.resources import Mp4File
from kotti_media.resources import OgaFile
from kotti_media.resources import OgvFile
from kotti_media.resources import SubtitlesFile
from kotti_media.resources import Video
from kotti_media.resources import WavFile
from kotti_media.resources import WebmFile


lorem = u'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam architecto, voluptatibus explicabo magnam? Hic reprehenderit doloribus modi ipsam blanditiis voluptatibus, placeat error sed, praesentium maiores sit, voluptatum assumenda. Nihil, dolorum!'  # noqa


def data(filetype):

    f = os.path.join(
        os.path.dirname(__file__),
        'tests',
        'distortion.{}'.format(filetype))

    return open(f).read()


def populate():

    kotti_populate()
    transaction.commit()

    root = get_root()

    if 'audio' not in root.keys():

        root['audio'] = audio = Audio(title=u'Audio', body=lorem)

        audio['poster'] = poster = Image(
            title=u"Poster", filename='distortion.png', mimetype='image/png')
        poster.data = data('png')

        audio['m4a'] = m4a = M4aFile(title=u"M4aFile")
        m4a.data = data('m4a')

        audio['mp3'] = mp3 = Mp3File(title=u"Mp3File")
        mp3.data = data('mp3')

        audio['oga'] = oga = OgaFile(title=u"OgaFile")
        oga.data = data('oga')

        audio['wav'] = wav = WavFile(title=u"WavFile")
        wav.data = data('wav')

    if 'video' not in root.keys():

        root['video'] = video = Video(title=u'Video', body=lorem)

        video['poster'] = poster = Image(
            title=u"Poster", filename='distortion.png', mimetype='image/png')
        poster.data = data('png')

        # video['chapters'] = chapters = ChaptersFile(title=u"ChaptersFile")
        # chapters.data = data('chapters')

        video['m4v'] = m4v = Mp4File(title=u"Mp4File")
        m4v.data = data('m4v')

        video['ogv'] = ogv = OgvFile(title=u"OgvFile")
        ogv.data = data('ogv')

        video['srt'] = srt = SubtitlesFile(title=u"SubtitlesFile")
        srt.data = data('srt')

        video['webm'] = webm = WebmFile(title=u"WebmFile")
        webm.data = data('webm')
