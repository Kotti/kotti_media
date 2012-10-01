# -*- coding: utf-8 -*-

import logging
from colander import Boolean
from colander import Float
from colander import Integer
from colander import MappingSchema
from colander import SchemaNode
from deform import Button
from deform import ValidationFailure
from copy import copy
from deform import Form
from js.mediaelement import mediaelementandplayer
from json import dumps
from kotti.resources import Document
from kotti.security import has_permission
from kotti_media.resources import Audio
from kotti_media.resources import Video
from kotti_media.static import kotti_media_js
from pyramid.i18n import TranslationStringFactory
from pyramid.url import resource_url
from pyramid.response import Response
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

    defaultVideoWidth = SchemaNode(Integer(), title=_("Default video width"))
    defaultVideoHeight = SchemaNode(Integer(), title=_("Default video height"))
    videoWidth = SchemaNode(Integer(), title=_("Video width"))
    videoHeight = SchemaNode(Integer(), title=_("Video height"))
    audioWidth = SchemaNode(Integer(), title=_("Audio width"))
    audioHeight = SchemaNode(Integer(), title=_("Audio height"))
    startVolume = SchemaNode(Float(), title=_("Start volume"))
    loop = SchemaNode(Boolean(), title=_("Loop"))
    enableAutosize = SchemaNode(Boolean(), title=_("Enable autosize"))
    # features
    alwaysShowControls = SchemaNode(Boolean(), title=_("Always show controls"))
    iPadUseNativeControls = SchemaNode(Boolean(), title=_("Use native controls on iPad"))
    iPhoneUseNativeControls = SchemaNode(Boolean(), title=_("Use native controls on iPhone"))
    AndroidUseNativeControls = SchemaNode(Boolean(), title=_("Use native controls on Android"))
    alwaysShowHours = SchemaNode(Boolean(), title=_("Always show hours"))
    showTimecodeFrameCount = SchemaNode(Boolean(), title=_("Show timecode frame count"))
    framesPerSecond = SchemaNode(Integer(), title=_("Frames per second"))
    enableKeyboard = SchemaNode(Boolean(), title=_("Enable keyboard"))
    pauseOtherPlayers = SchemaNode(Boolean(), title=_("Pause other players"))
    # keyActions


@view_defaults(permission='view')
class BaseView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

        if has_permission("edit", self.context, self.request):
            kotti_media_js.need()

    def make_url(self, t, context=None):

        if context is None:
            context = self.context

        file = getattr(context, "%s_file" % t)

        if file is None:
            return None
        else:
            if file.data:
                if t == 'poster':
                    return resource_url(file, self.request, "image")
                else:
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

    @view_config(name="player_options")
    def player_options(self):

        schema = PlayerOptionsSchema()
        action = self.request.resource_url(self.context)
        if not action.endswith('/'):  # pragma: no cover
            # don't know ho to test this in unit tests.
            # don't feel like setting up a browser test for this.
            action += '/'
        action += 'player_options'
        form = Form(
            schema,
            action=action,
            buttons=(
                Button(name='save', title=_("Save")),
            )
        )
        post = self.request.POST
        if "save" not in post:
            return Response(form.render(self.options))

        try:
            validated = form.validate(post.items())
        except ValidationFailure, e:
            return Response(e.render())

        self.context.annotations.update(validated)

        result = form.render(self.options)
        result += "<script>edit_player_options_success = true;$('.modal').modal('hide');window.location.reload();</script>"
        return Response(result)


@view_defaults(context=Audio,
               permission='view')
class AudioView(BaseView):

    @view_config(name='view',
                 renderer='kotti_media:templates/audio-view.pt')
    def view(self):

        return {
            "can_edit_player_options": has_permission("edit", self.context, self.request),
        }

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

        return {
            "can_edit_player_options": has_permission("edit", self.context, self.request),
        }

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
            "can_edit_player_options": has_permission("edit", self.context, self.request),
        }

        return result


def includeme(config):

    import forms

    forms.includeme(config)
    config.scan("kotti_media")
