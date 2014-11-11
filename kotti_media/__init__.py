# -*- coding: utf-8 -*-

import logging

from kotti import TRUE_VALUES
from kotti.resources import Image

log = logging.getLogger(__name__)


def kotti_configure(settings):

    settings['kotti_media.use_fanstatic'] = settings.get(
        'kotti_media.use_fanstatic', 'true').lower() in TRUE_VALUES
    settings['pyramid.includes'] += ' kotti_media.views'

    settings['kotti.available_types'] += ' kotti_media.resources.Audio'
    settings['kotti.available_types'] += ' kotti_media.resources.M4aFile'
    settings['kotti.available_types'] += ' kotti_media.resources.Mp3File'
    settings['kotti.available_types'] += ' kotti_media.resources.OgaFile'
    settings['kotti.available_types'] += ' kotti_media.resources.WavFile'

    settings['kotti.available_types'] += ' kotti_media.resources.Video'
    settings['kotti.available_types'] += ' kotti_media.resources.ChaptersFile'
    settings['kotti.available_types'] += ' kotti_media.resources.Mp4File'
    settings['kotti.available_types'] += ' kotti_media.resources.OgvFile'
    settings['kotti.available_types'] += ' kotti_media.resources.SubtitlesFile'
    settings['kotti.available_types'] += ' kotti_media.resources.WebmFile'

    Image.type_info.addable_to.append("Audio")
    Image.type_info.addable_to.append("Video")
