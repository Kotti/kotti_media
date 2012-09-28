# -*- coding: utf-8 -*-

import logging
from colander import MappingSchema
from copy import copy
from js.mediaelement import mediaelementandplayer
from json import dumps
from kotti.resources import Document
from kotti.security import has_permission
from kotti_media.resources import Audio
from kotti_media.resources import MediaContentBase
from kotti_media.resources import Video
from pyramid.i18n import TranslationStringFactory
from pyramid.url import resource_url
from pyramid.view import view_config
from pyramid.view import view_defaults

_ = TranslationStringFactory('kotti_media')
log = logging.getLogger(__name__)

default_player_options = {
    "defaultVideoWidth": 480,
    "defaultVideoHeight": 270,
    "videoWidth": -1,
    "videoHeight": -1,
    "audioWidth": 400,
    "audioHeight": 30,
    "startVolume": 1.0,
    "loop": False,
    "enableAutosize": True,
    "features": [
        'playpause',
        'progress',
        'current',
        'duration',
        'fullscreen',
    ],
    "alwaysShowControls": False,
    "iPadUseNativeControls": True,
    "iPhoneUseNativeControls": True,
    "AndroidUseNativeControls": True,
    "alwaysShowHours": False,
    "showTimecodeFrameCount": False,
    "framesPerSecond": 25,
    "enableKeyboard": True,
    "pauseOtherPlayers": True,
    "keyActions": []
}


class PlayerOptionsSchema(MappingSchema):

    pass


@view_defaults(context=MediaContentBase,
               permission='view')
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

    @property
    def options(self):

        options = copy(default_player_options)

        for k in self.context.annotations:
            if k in options:
                options[k] = self.context.annotations[k]

        return options

    @view_config(name='script',
                 renderer='kotti_media:templates/script.pt')
    def script(self):

        mediaelementandplayer.need()

        return {"options": dumps(self.options)}


@view_defaults(context=Audio,
               permission='view')
class AudioView(BaseView):

    @view_config(name='view',
                 renderer='kotti_media:templates/audio-view.pt')
    def view(self):

        return {}

    @view_config(name='element',
                 renderer='kotti_media:templates/audio-element.pt')
    def element(self):

        result = {}

        for t in ("m4a", "mp3", "oga", "wav", "poster"):

            key = "%s_url" % t
            result[key] = self.make_url(t)

        return result


@view_defaults(context=Video,
               permission='view')
class VideoView(BaseView):

    @view_config(name='view',
                 renderer='kotti_media:templates/video-view.pt')
    def view(self):

        return {}

    @view_config(name='element',
                 renderer='kotti_media:templates/video-element.pt')
    def element(self):

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

        media = [c for c in self.context.children \
                 if (c.type in ("audio", "video", )) \
                 and has_permission("view", self.context, self.request)]
        result = {
            "media": media,
        }

        return result


def includeme(config):

    import forms

    forms.includeme(config)
    config.scan("kotti_media")
