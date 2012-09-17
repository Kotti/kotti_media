# -*- coding: utf-8 -*-

from kotti import DBSession
from kotti.resources import Document
from kotti.resources import File
from kotti.resources import TypeInfo
from kotti.security import view_permitted
from kotti.util import _
from kotti.util import ViewLink
from kotti.resources import Image
from pprint import pformat
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer


class VideoFileTypeInfo(TypeInfo):

    def addable(self, context, request):
        """Return True if
            - the type described in 'self' may be added  *and*
            - no other child of the same type has already be added
           to 'context'."""

        if view_permitted(context, request, self.add_view):
            addable = context.type_info.name in self.addable_to
            child_type_already_added = self in [c.type_info for c in context.children]
            return addable and not child_type_already_added
        else:
            return False

    def copy(self, **kwargs):

        d = self.__dict__.copy()
        d.update(kwargs)
        return VideoFileTypeInfo(**d)

    def __repr__(self):

        return pformat(self.__dict__)


generic_video_file_type_info = VideoFileTypeInfo(name=u"VideoFile",
                                                 title=_(u"Video file"),
                                                 addable_to=[u"Video", ],
                                                 add_view=None,
                                                 edit_links=[ViewLink('edit', title=_(u'Edit')), ], )


class Mp4File(File):

    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"Mp4File",
                                                  title=_(u"Video file (*.mp4)"),
                                                  add_view="add_mp4file")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(Mp4File, self).__init__(data=data, filename="video.mp4", mimetype="video/mp4", size=size, **kwargs)


class WebmFile(File):

    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"WebmFile",
                                                  title=_(u"Video file (*.webm)"),
                                                  add_view="add_webmfile")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(WebmFile, self).__init__(data=data, filename="video.webm", mimetype="video/webm", size=size, **kwargs)


class OggFile(File):

    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"OggFile",
                                                  title=_(u"Video file (*.ogg)"),
                                                  add_view="add_oggfile")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(OggFile, self).__init__(data=data, filename="video.ogv", mimetype="video/ogg", size=size, **kwargs)


class SubtitlesFile(File):

    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"SubtitlesFile",
                                                  title=_(u"Subtitles file (*.srt)"),
                                                  add_view="add_subtitlesfile")


class ChaptersFile(File):

    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"ChaptersFile",
                                                  title=_(u"Chapters file (*.srt)"),
                                                  add_view="add_chaptersfile")


class Video(Document):

    id = Column(Integer(), ForeignKey('documents.id'), primary_key=True)

    type_info = Document.type_info.copy(name=u"Video",
                                        title=_(u"Video"),
                                        addable_to=[u"Document"],
                                        add_view="add_video", )

    @property
    def mp4_file(self):

        session = DBSession()
        query = session.query(Mp4File).filter(Mp4File.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None

    @property
    def webm_file(self):

        session = DBSession()
        query = session.query(WebmFile).filter(WebmFile.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None

    @property
    def ogg_file(self):

        session = DBSession()
        query = session.query(OggFile).filter(OggFile.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None

    @property
    def subtitles_file(self):

        session = DBSession()
        query = session.query(SubtitlesFile).filter(SubtitlesFile.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None

    @property
    def chapters_file(self):

        session = DBSession()
        query = session.query(ChaptersFile).filter(ChaptersFile.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None

    @property
    def poster_file(self):

        session = DBSession()
        query = session.query(Image).filter(Image.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None


class AudioFileTypeInfo(TypeInfo):

    def addable(self, context, request):
        """Return True if
            - the type described in 'self' may be added  *and*
            - no other child of the same type has already be added
           to 'context'."""

        if view_permitted(context, request, self.add_view):
            addable = context.type_info.name in self.addable_to
            child_type_already_added = self in [c.type_info for c in context.children]
            return addable and not child_type_already_added
        else:
            return False

    def copy(self, **kwargs):

        d = self.__dict__.copy()
        d.update(kwargs)
        return AudioFileTypeInfo(**d)

    def __repr__(self):

        return pformat(self.__dict__)


generic_audio_file_type_info = AudioFileTypeInfo(name=u"AudioFile",
                                                 title=_(u"Audio file"),
                                                 addable_to=[u"Audio", ],
                                                 add_view=None,
                                                 edit_links=[ViewLink('edit', title=_(u'Edit')), ], )


class Mp3File(File):

    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)

    type_info = generic_audio_file_type_info.copy(name=u"Mp3File",
                                                  title=_(u"Audio file (*.mp3)"),
                                                  add_view="add_mp3file")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(Mp3File, self).__init__(data=data, filename="audio.mp3", mimetype="audio/mp3", size=size, **kwargs)


class Audio(Document):

    id = Column(Integer(), ForeignKey('documents.id'), primary_key=True)

    type_info = Document.type_info.copy(name=u"Audio",
                                        title=_(u"Audio"),
                                        addable_to=[u"Document"],
                                        add_view="add_audio", )

    @property
    def mp3_file(self):

        session = DBSession()
        query = session.query(Mp3File).filter(Mp3File.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None

    @property
    def poster_file(self):

        session = DBSession()
        query = session.query(Image).filter(Image.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None
