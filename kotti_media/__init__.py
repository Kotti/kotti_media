# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)


def kotti_configure(settings):

    settings['kotti.includes'] += ' kotti_media.views'
    settings['kotti.available_types'] += ' kotti_media.resources.Video'
    settings['kotti.available_types'] += ' kotti_media.resources.Mp4File'
    settings['kotti.available_types'] += ' kotti_media.resources.WebmFile'
    settings['kotti.available_types'] += ' kotti_media.resources.OggFile'
    settings['kotti.available_types'] += ' kotti_media.resources.SubtitlesFile'
    settings['kotti.available_types'] += ' kotti_media.resources.ChaptersFile'
    settings['kotti.available_types'] += ' kotti_media.resources.Audio'
    settings['kotti.available_types'] += ' kotti_media.resources.Mp3File'
