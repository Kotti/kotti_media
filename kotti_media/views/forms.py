# -*- coding: utf-8 -*-

import logging

from colander import Invalid
from colander import SchemaNode
from colander import String
from colander import null
from deform import FileData
from deform.widget import FileUploadWidget
from kotti.views.edit import DocumentSchema
from kotti.views.edit.content import DocumentAddForm
from kotti.views.edit.content import DocumentEditForm
from kotti.views.edit.content import FileAddForm
from kotti.views.edit.content import FileEditForm
from kotti.views.form import FileUploadTempStore
from kotti.views.form import validate_file_size_limit
from kotti.views.edit.content import ContentSchema
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config

from kotti_media.resources import Audio
from kotti_media.resources import ChaptersFile
from kotti_media.resources import M4aFile
from kotti_media.resources import MediaContentBase
from kotti_media.resources import MediaFile
from kotti_media.resources import Mp3File
from kotti_media.resources import Mp4File
from kotti_media.resources import OgaFile
from kotti_media.resources import OgvFile
from kotti_media.resources import SubtitlesFile
from kotti_media.resources import Video
from kotti_media.resources import WavFile
from kotti_media.resources import WebmFile

_ = TranslationStringFactory('kotti_media')
log = logging.getLogger(__name__)


def MediaFileSchema(tmpstore, title_missing=None):
    class MediaFileSchema(ContentSchema):
        file = SchemaNode(
            FileData(),
            missing=null,
            title=_(u'File'),
            widget=FileUploadWidget(tmpstore),
            validator=validate_file_size_limit
        )
        external_url = SchemaNode(
            String(),
            missing=null,
            title=_(u'External URL'),
        )

    def set_title_missing(node, kw):
        if title_missing is not None:
            node['title'].missing = title_missing

    def validator(form, value):

        if not value['external_url'] and not value['file']:
            exc = Invalid(
                form,
                _(u'Either a file or an external URL is required')
            )
            exc['file'] = _(u'Required if no external URL is supplied')
            exc['external_url'] = _(u'Required if no file is supplied')
            raise exc

        if value['external_url'] and value['file']:
            exc = Invalid(
                form,
                _(u'Either a file or an external URL is required, bot not '
                  u'both')
            )
            exc['file'] = _(
                u'Must not be supplied if an external URL is supplied')
            exc['external_url'] = _(
                u'Must not be supplied if a file is supplied')
            raise exc

    return MediaFileSchema(after_bind=set_title_missing, validator=validator)


#############
# Add forms #
#############

@view_config(name=Audio.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt')
class AudioAddForm(DocumentAddForm):

    schema_factory = DocumentSchema
    add = Audio
    item_type = _(u"Audio")


@view_config(name=Video.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt')
class VideoAddForm(DocumentAddForm):

    schema_factory = DocumentSchema
    add = Video
    item_type = _(u"Video")


class MediaFileAddForm(FileAddForm):

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return MediaFileSchema(tmpstore, title_missing=null)

    def save_success(self, appstruct):

        if not appstruct['title']:

            if appstruct['external_url']:
                appstruct['title'] = appstruct['external_url'].split('/')[-1]

            if appstruct['file']:
                appstruct['title'] = appstruct['file']['filename']

        return super(FileAddForm, self).save_success(appstruct)

    def add(self, **appstruct):

        image = self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            tags=appstruct['tags'], )

        if appstruct['external_url']:
            image.external_url = appstruct['external_url']

        if appstruct['file']:
            buf = appstruct['file']['fp'].read()
            image.data = buf
            image.filename = appstruct['file']['filename']
            image.mimetype = appstruct['file']['mimetype']
            image.size = len(buf)

        return image


@view_config(name=M4aFile.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class M4aFileAddForm(MediaFileAddForm):

    item_type = _(u"M4aFile")
    item_class = M4aFile


@view_config(name=Mp3File.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class Mp3FileAddForm(MediaFileAddForm):

    item_type = _(u"Mp3File")
    item_class = Mp3File


@view_config(name=OgaFile.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class OgaFileAddForm(MediaFileAddForm):

    item_type = _(u"OgaFile")
    item_class = OgaFile


@view_config(name=WavFile.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class WavFileAddForm(MediaFileAddForm):

    item_type = _(u"WavFile")
    item_class = WavFile


@view_config(name=Mp4File.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class Mp4FileAddForm(MediaFileAddForm):

    item_type = _(u"Mp4File")
    item_class = Mp4File


@view_config(name=OgvFile.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class OgvFileAddForm(MediaFileAddForm):

    item_type = _(u"OgvFile")
    item_class = OgvFile


@view_config(name=WebmFile.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class WebmFileAddForm(MediaFileAddForm):

    item_type = _(u"WebmFile")
    item_class = WebmFile


@view_config(name=SubtitlesFile.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class SubtitlesFileAddForm(MediaFileAddForm):

    item_type = _(u"SubtitlesFile")
    item_class = SubtitlesFile


@view_config(name=ChaptersFile.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt',)
class ChaptersFileAddForm(MediaFileAddForm):

    item_type = _(u"ChaptersFile")
    item_class = ChaptersFile


##############
# Edit forms #
##############

@view_config(name='edit',
             context=MediaContentBase, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class MediaContainerEditForm(DocumentEditForm):
    pass


@view_config(name='edit',
             context=MediaFile, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class MediaFileEditForm(FileEditForm):

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return MediaFileSchema(tmpstore)

    def edit(self, **appstruct):

        FileEditForm.edit(self, **appstruct)

        if appstruct['external_url']:
            self.context.data = None
            self.context.filename = None
            self.context.mimetype = None
            self.context.size = None
            self.context.external_url = appstruct['external_url']
        else:  # pragma: no cover
            # can't find a way to test this, so maybe we never get here.  let's
            # still leave it as a safety belt.
            self.context.external_url = None
