# -*- coding: utf-8 -*-

import logging
from kotti.util import _
from kotti.views.edit import DocumentSchema
from kotti.views.edit import make_generic_add
from kotti.views.edit import make_generic_edit
from kotti.views.file import AddFileFormView
from kotti.views.file import EditFileFormView
from kotti_media.resources import ChaptersFile
from kotti_media.resources import Mp4File
from kotti_media.resources import OggFile
from kotti_media.resources import SubtitlesFile
from kotti_media.resources import Video
from kotti_media.resources import WebmFile
from pyramid.url import resource_url
from pyramid.view import view_config

log = logging.getLogger(__name__)


class BaseView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request


class VideoView(BaseView):

    @view_config(context=Video,
                 name='view',
                 permission='view',
                 renderer='templates/video-view.pt')
    def view(self):
        result = {}
        for t in ("mp4", "webm", "ogg", "subtitles", "chapters", "poster"):
            key = "%s_url" % t
            file = getattr(self.context, "%s_file" % t)
            if file is None:
                result[key] = None
            else:
                result[key] = resource_url(file, self.request, "@@attachment-view")

        return result


class AddMp4FileFormView(AddFileFormView):

    item_type = _(u"Mp4File")
    item_class = Mp4File


class AddWebmFileFormView(AddFileFormView):

    item_type = _(u"WebmFile")
    item_class = WebmFile


class AddOggFileFormView(AddFileFormView):

    item_type = _(u"OggFile")
    item_class = OggFile


class AddSubtitlesFileFormView(AddFileFormView):

    item_type = _(u"SubtitlesFile")
    item_class = SubtitlesFile


class AddChaptersFileFormView(AddFileFormView):

    item_type = _(u"ChaptersFile")
    item_class = ChaptersFile


def includeme(config):

    config.add_static_view('static-kotti_media', 'kotti_media:static')
    config.scan("kotti_media")

    # Video add/edit
    config.add_view(make_generic_add(DocumentSchema(), Video),
                                     name=Video.type_info.add_view,
                                     permission='add',
                                     renderer='kotti:templates/edit/node.pt', )
    config.add_view(make_generic_edit(DocumentSchema()),
                    context=Video,
                    name='edit',
                    permission='edit',
                    renderer='kotti:templates/edit/node.pt', )

    # VideoFile types edit
    for file_type in (Mp4File, WebmFile, OggFile, SubtitlesFile, ChaptersFile):
        config.add_view(EditFileFormView,
                        context=file_type,
                        name='edit',
                        permission='edit',
                        renderer='kotti:templates/edit/node.pt', )
    # Mp4File add
    config.add_view(AddMp4FileFormView,
                    name=Mp4File.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # WebmFile add
    config.add_view(AddWebmFileFormView,
                    name=WebmFile.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # OggFile add
    config.add_view(AddOggFileFormView,
                    name=OggFile.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # SubtitlesFile add
    config.add_view(AddSubtitlesFileFormView,
                    name=SubtitlesFile.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # ChaptersFile add
    config.add_view(AddChaptersFileFormView,
                    name=ChaptersFile.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
