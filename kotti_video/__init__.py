# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)


def kotti_configure(settings):

    settings['kotti.includes'] += ' kotti_video.views'
    settings['kotti.available_types'] += ' kotti_video.resources.Video'
