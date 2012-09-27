# -*- coding: utf-8 -*-

import logging
from js.mediaelement import mediaelementandplayer
from kotti_media.resources import Audio
from kotti_media.resources import Video
from pyramid.i18n import TranslationStringFactory
from pyramid.url import resource_url
from pyramid.view import view_config

_ = TranslationStringFactory('kotti_media')
log = logging.getLogger(__name__)


class BaseView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def make_url(self, t):

        file = getattr(self.context, "%s_file" % t)

        if file is None:
            return None
        else:
            if file.external_url:
                return file.external_url
            else:
                return resource_url(file, self.request, "@@attachment-view")


class AudioView(BaseView):

    @view_config(context=Audio,
                 name='view',
                 permission='view',
                 renderer='kotti_media:templates/audio-view.pt')
    def view(self):

        mediaelementandplayer.need()

        result = {}

        for t in ("m4a", "mp3", "oga", "wav", "poster"):

            key = "%s_url" % t
            result[key] = self.make_url(t)

        return result


class VideoView(BaseView):

    @view_config(context=Video,
                 name='view',
                 permission='view',
                 renderer='kotti_media:templates/video-view.pt')
    def view(self):

        mediaelementandplayer.need()

        result = {}

        for t in ("mp4", "ogv", "webm", "subtitles", "chapters", "poster"):

            key = "%s_url" % t
            result[key] = self.make_url(t)

        return result


def includeme(config):

    import forms

    forms.includeme(config)
    config.scan("kotti_media")
