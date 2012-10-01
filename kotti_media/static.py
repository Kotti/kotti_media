# -*- coding: utf-8 -*-

from fanstatic import Library
from fanstatic import Resource
from js.jquery_form import jquery_form

library = Library('kotti_media', 'static')
kotti_media_js = Resource(
    library,
    'kotti_media.js',
    minified='kotti_media.min.js',
    depends=[jquery_form, ]
)
