# -*- coding: utf-8 -*-

import logging
from js.mediaelement import mediaelementandplayer
from kotti.resources import Document
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

    def make_url(self, t, context=None):

        if context is None:
            context = self.context

        file = getattr(context, "%s_file" % t)

        if file is None:
            return None
        else:
            if file.data:
                return resource_url(file, self.request, "@@attachment-view")
            else:
                return getattr(file, "external_url", None)


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


class MediaFolderView(BaseView):

    @view_config(context=Document,
                 name="media_folder_view",
                 permission="view",
                 renderer="kotti_media:templates/media-folder-view.pt")
    def view(self):

        media = [c for c in self.context.children if c.type in (Audio, Video)]
        result = {}

        return result


def includeme(config):

    import forms

    forms.includeme(config)
    config.scan("kotti_media")
