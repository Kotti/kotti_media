# -*- coding: utf-8 -*-

from kotti.resources import Document, File, TypeInfo
from kotti.security import view_permitted
from kotti.util import _, ViewLink
from pprint import pformat
from sqlalchemy import Column, ForeignKey, Integer


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


class WebmFile(File):

    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"WebmFile",
                                                  title=_(u"Video file (*.webm)"),
                                                  add_view="add_webmfile")


class OggFile(File):

    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"OggFile",
                                                  title=_(u"Video file (*.ogg)"),
                                                  add_view="add_oggfile")


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
                                        addable_to=[u"Document"])
