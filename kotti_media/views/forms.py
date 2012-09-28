# -*- coding: utf-8 -*-

import logging
from colander import Invalid
from colander import null
from colander import SchemaNode
from colander import String
from deform import FileData
from deform.widget import FileUploadWidget
from kotti.views.edit import DocumentSchema
from kotti.views.edit import make_generic_add
from kotti.views.edit import make_generic_edit
from kotti.views.file import AddFileFormView
from kotti.views.file import EditFileFormView
from kotti.views.file import FileUploadTempStore
from kotti.views.file import set_title_missing
from kotti.views.file import validate_file_size_limit
from kotti.views.form import ContentSchema
from kotti_media.resources import Audio
from kotti_media.resources import ChaptersFile
from kotti_media.resources import M4aFile
from kotti_media.resources import Mp3File
from kotti_media.resources import Mp4File
from kotti_media.resources import OgaFile
from kotti_media.resources import OgvFile
from kotti_media.resources import SubtitlesFile
from kotti_media.resources import Video
from kotti_media.resources import WavFile
from kotti_media.resources import WebmFile
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_media')
log = logging.getLogger(__name__)


class AddMediaFileFormView(AddFileFormView):

    def schema_factory(self):

        tmpstore = FileUploadTempStore(self.request)

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
                    _(u'Either a file or an external URL is required, bot not both')
                )
                exc['file'] = _(u'Must not be supplied if an external URL is supplied')
                exc['external_url'] = _(u'Must not be supplied if a file is supplied')
                raise exc

        class FileSchema(ContentSchema):

            file = SchemaNode(
                FileData(),
                missing=null,
                title=_(u'File'),
                validator=validate_file_size_limit,
                widget=FileUploadWidget(tmpstore),
            )

            external_url = SchemaNode(
                String(),
                missing=null,
                title=_(u'External URL'),
            )

        file_schema = FileSchema(after_bind=set_title_missing,
                                 validator=validator)

        return file_schema.bind(title_missing=u'')

    def save_success(self, appstruct):

        if not appstruct['title']:

            if appstruct['external_url']:
                appstruct['title'] = appstruct['external_url'].split('/')[-1]

            if appstruct['file']:
                appstruct['title'] = appstruct['file']['filename']

        return super(AddFileFormView, self).save_success(appstruct)

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


class EditMediaFileFormView(EditFileFormView):

    def schema_factory(self):

        tmpstore = FileUploadTempStore(self.request)

        def validator(form, value):

            if not value['external_url'] and not value['file'] and not self.context.data:
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
                    _(u'Either a file or an external URL is required, bot not both')
                )
                exc['file'] = _(u'Must not be supplied if an external URL is supplied')
                exc['external_url'] = _(u'Must not be supplied if a file is supplied')
                raise exc

        class FileSchema(ContentSchema):

            file = SchemaNode(
                FileData(),
                missing=null,
                title=_(u'File'),
                validator=validate_file_size_limit,
                widget=FileUploadWidget(tmpstore),
            )

            external_url = SchemaNode(
                String(),
                missing=null,
                title=_(u'External URL'),
            )

        return FileSchema(validator=validator)

    def edit(self, **appstruct):

        EditFileFormView.edit(self, **appstruct)

        if appstruct['external_url']:
            self.context.data = None
            self.context.filename = None
            self.context.mimetype = None
            self.context.size = None
            self.context.external_url = appstruct['external_url']
        else:  # pragma: no cover
            # can't find a way to test this, so maybe we never get here
            # let's still leave it as a safety belt
            self.context.external_url = None


class AddM4aFileFormView(AddMediaFileFormView):

    item_type = _(u"M4aFile")
    item_class = M4aFile


class AddMp3FileFormView(AddMediaFileFormView):

    item_type = _(u"Mp3File")
    item_class = Mp3File


class AddOgaFileFormView(AddMediaFileFormView):

    item_type = _(u"OgaFile")
    item_class = OgaFile


class AddWavFileFormView(AddMediaFileFormView):

    item_type = _(u"WavFile")
    item_class = WavFile


class AddMp4FileFormView(AddMediaFileFormView):

    item_type = _(u"Mp4File")
    item_class = Mp4File


class AddOgvFileFormView(AddMediaFileFormView):

    item_type = _(u"OgvFile")
    item_class = OgvFile


class AddWebmFileFormView(AddMediaFileFormView):

    item_type = _(u"WebmFile")
    item_class = WebmFile


class AddSubtitlesFileFormView(AddMediaFileFormView):

    item_type = _(u"SubtitlesFile")
    item_class = SubtitlesFile


class AddChaptersFileFormView(AddMediaFileFormView):

    item_type = _(u"ChaptersFile")
    item_class = ChaptersFile


def includeme(config):

    # Aaudio/Video add/edit
    for media_type in (Audio, Video, ):
        config.add_view(make_generic_add(DocumentSchema(), media_type),
                                         name=media_type.type_info.add_view,
                                         permission='add',
                                         renderer='kotti:templates/edit/node.pt', )
        config.add_view(make_generic_edit(DocumentSchema()),
                        context=media_type,
                        name='edit',
                        permission='edit',
                        renderer='kotti:templates/edit/node.pt', )

    # File types edit
    for file_type in (M4aFile, Mp3File, OgaFile, WavFile, Mp4File, OgvFile, WebmFile, SubtitlesFile, ChaptersFile):
        config.add_view(EditMediaFileFormView,
                        context=file_type,
                        name='edit',
                        permission='edit',
                        renderer='kotti:templates/edit/node.pt', )
    # M4aFile add
    config.add_view(AddM4aFileFormView,
                    name=M4aFile.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # Mp3File add
    config.add_view(AddMp3FileFormView,
                    name=Mp3File.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # OgaFile add
    config.add_view(AddOgaFileFormView,
                    name=OgaFile.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # WavFile add
    config.add_view(AddWavFileFormView,
                    name=WavFile.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # Mp4File add
    config.add_view(AddMp4FileFormView,
                    name=Mp4File.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # OgvFile add
    config.add_view(AddOgvFileFormView,
                    name=OgvFile.type_info.add_view,
                    permission='add',
                    renderer='kotti:templates/edit/node.pt', )
    # WebmFile add
    config.add_view(AddWebmFileFormView,
                    name=WebmFile.type_info.add_view,
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
