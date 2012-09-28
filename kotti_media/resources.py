# -*- coding: utf-8 -*-

from kotti import DBSession
from kotti.resources import Document
from kotti.resources import File
from kotti.resources import Image
from kotti.resources import TypeInfo
from kotti.security import view_permitted
from kotti.util import _
from kotti.util import ViewLink
from pprint import pformat
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String


class MediaFileTypeInfo(TypeInfo):

    def addable(self, context, request):
        """Return True if
            - the type described in 'self' may be added  *and*
            - no other child of the same type has already be added
           to 'context'."""

        if view_permitted(context, request, self.add_view):
            addable = context.type_info.name in self.addable_to
            child_type_already_added = self in [c.type_info for c in context.children]
            return addable and not child_type_already_added
        else:  # pragma: no cover (this already tested in Kotti itself)
            return False

    def copy(self, **kwargs):

        d = self.__dict__.copy()
        d.update(kwargs)
        return MediaFileTypeInfo(**d)

    def __repr__(self):  # pragma: no cover

        return pformat(self.__dict__)


generic_video_file_type_info = MediaFileTypeInfo(name=u"VideoFile",
                                                 title=_(u"Video file"),
                                                 addable_to=[u"Video", ],
                                                 add_view=None,
                                                 edit_links=[ViewLink('edit', title=_(u'Edit')), ], )

generic_audio_file_type_info = MediaFileTypeInfo(name=u"AudioFile",
                                                 title=_(u"Audio file"),
                                                 addable_to=[u"Audio", ],
                                                 add_view=None,
                                                 edit_links=[ViewLink('edit', title=_(u'Edit')), ], )


class MediaFile(File):
    """This is an 'abstract' base class for all media files that adds
       an external URL attribute to to files to allow them to be served
       from a CDN instead of storing the file data in Kotti's DB."""

    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)

    external_url = Column(String(1000))


###############
# AUDIO FILES #
###############


class M4aFile(MediaFile):

    id = Column(Integer(), ForeignKey('media_files.id'), primary_key=True)

    type_info = generic_audio_file_type_info.copy(name=u"M4aFile",
                                                  title=_(u"Audio file (*.m4a)"),
                                                  add_view="add_m4afile")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(M4aFile, self).__init__(data=data, filename="audio.m4a", mimetype="audio/mp4", size=size, **kwargs)


class Mp3File(MediaFile):

    id = Column(Integer(), ForeignKey('media_files.id'), primary_key=True)

    type_info = generic_audio_file_type_info.copy(name=u"Mp3File",
                                                  title=_(u"Audio file (*.mp3)"),
                                                  add_view="add_mp3file")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(Mp3File, self).__init__(data=data, filename="audio.mp3", mimetype="audio/mp3", size=size, **kwargs)


class OgaFile(MediaFile):

    id = Column(Integer(), ForeignKey('media_files.id'), primary_key=True)

    type_info = generic_audio_file_type_info.copy(name=u"OgaFile",
                                                  title=_(u"Audio file (*.oga)"),
                                                  add_view="add_ogafile")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(OgaFile, self).__init__(data=data, filename="audio.oga", mimetype="audio/ogg", size=size, **kwargs)


class WavFile(MediaFile):

    id = Column(Integer(), ForeignKey('media_files.id'), primary_key=True)

    type_info = generic_audio_file_type_info.copy(name=u"WavFile",
                                                  title=_(u"Audio file (*.wav)"),
                                                  add_view="add_wavfile")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(WavFile, self).__init__(data=data, filename="audio.wav", mimetype="audio/wav", size=size, **kwargs)


###############
# VIDEO FILES #
###############


class Mp4File(MediaFile):

    id = Column(Integer(), ForeignKey('media_files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"Mp4File",
                                                  title=_(u"Video file (*.mp4)"),
                                                  add_view="add_mp4file")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(Mp4File, self).__init__(data=data, filename="video.mp4", mimetype="video/mp4", size=size, **kwargs)


class OgvFile(MediaFile):

    id = Column(Integer(), ForeignKey('media_files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"OgvFile",
                                                  title=_(u"Video file (*.ogv)"),
                                                  add_view="add_ogvfile")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(OgvFile, self).__init__(data=data, filename="video.ogv", mimetype="video/ogg", size=size, **kwargs)


class WebmFile(MediaFile):

    id = Column(Integer(), ForeignKey('media_files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"WebmFile",
                                                  title=_(u"Video file (*.webm)"),
                                                  add_view="add_webmfile")

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(WebmFile, self).__init__(data=data, filename="video.webm", mimetype="video/webm", size=size, **kwargs)


class SubtitlesFile(MediaFile):

    id = Column(Integer(), ForeignKey('media_files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"SubtitlesFile",
                                                  title=_(u"Subtitles file (*.srt)"),
                                                  add_view="add_subtitlesfile")


class ChaptersFile(MediaFile):

    id = Column(Integer(), ForeignKey('media_files.id'), primary_key=True)

    type_info = generic_video_file_type_info.copy(name=u"ChaptersFile",
                                                  title=_(u"Chapters file (*.srt)"),
                                                  add_view="add_chaptersfile")


##############
# CONTAINERS #
##############


class MediaContentBase(object):

    @property
    def poster_file(self):

        session = DBSession()
        query = session.query(Image).filter(Image.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None


class Audio(Document, MediaContentBase):

    id = Column(Integer(), ForeignKey('documents.id'), primary_key=True)

    type_info = Document.type_info.copy(name=u"Audio",
                                        title=_(u"Audio"),
                                        addable_to=[u"Document"],
                                        add_view="add_audio", )

    @property
    def m4a_file(self):

        session = DBSession()
        query = session.query(M4aFile).filter(M4aFile.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None

    @property
    def mp3_file(self):

        session = DBSession()
        query = session.query(Mp3File).filter(Mp3File.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None

    @property
    def oga_file(self):

        session = DBSession()
        query = session.query(OgaFile).filter(OgaFile.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None

    @property
    def wav_file(self):

        session = DBSession()
        query = session.query(WavFile).filter(WavFile.parent_id == self.id)

        if query.count() > 0:
            return query.first()

        return None


class Video(Document, MediaContentBase):

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
    def ogv_file(self):

        session = DBSession()
        query = session.query(OgvFile).filter(OgvFile.parent_id == self.id)

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
