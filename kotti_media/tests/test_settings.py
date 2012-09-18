# -*- coding: utf-8 -*-

from kotti.testing import UnitTestBase


class SettingsTest(UnitTestBase):

    def test(self):

        settings = {
            'kotti.includes': '',
            'kotti.available_types': '',
        }

        import kotti_media

        kotti_media.kotti_configure(settings)

        # make sure all the types are available
        assert settings['kotti.available_types'].find('kotti_media.resources.Audio') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.M4aFile') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.Mp3File') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.OgaFile') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.WavFile') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.Video') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.Mp4File') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.OgvFile') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.WebmFile') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.SubtitlesFile') > 0
        assert settings['kotti.available_types'].find('kotti_media.resources.ChaptersFile') > 0

        # make sure all inccludes are available
        assert settings['kotti.includes'].find('kotti_media.views') > 0
