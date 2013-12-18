===========
kotti_media
===========

This is an extension to the Kotti CMS that allows you to add audio and video to your Kotti site.

`Find out more about Kotti`_

``kotti_media`` uses `MediaElementJS`_ for video and audio views and thus supports native HTML5 playback on all platforms that support this.
Each video can have multiple formats (MP4 (.h264 baseline profile), WebM, Ogg/Theora) to achieve this goal. For audio, supported formats include mp3 and wav.
For older Platforms `MediaElementJS`_ includes a Adobe Flash / MS Silverlight plugin fallback, so that every resopurce can be played on every platform if all supported formats are uploaded.

Compatibility
=============

For Kotti >= 0.7 use the latest release of ``kotti_media``.

For Kotti < 0.7 use the ``kotti_video`` < 0.2.

Setup
=====

To activate the ``kotti_media`` add-on in your Kotti site, you need to add an entry to the ``kotti.configurators`` setting in your Paste Deploy config.
If you don't have a ``kotti.configurators`` option, add one.
The line in your ``[app:main]`` section could then look like this::

  kotti.configurators = kotti_media.kotti_configure

With this, you'll be able to add video and audio items in your site. Video and Audio content types are containers, into which you add specific media file types.

In your settings file, set kotti_media.asset_overrides to a list of asset specifications. This allows you to set up a directory in your package that will mirror kotti_media’s own and that allows you to override kotti_media’s templates on a case by case basis.

Usage
=====

A standard way to use kotti_media is to first creates a Document in your content tree; this document will become the media section of your application. Then you can add childs to your media section by appending audio/video content to it. 
``kotti_media`` comes with a handy `media_folder_view` that can be used to display your 'media section' Document (that is to display every media attached to it). 

Registration is done like this:

.. code-block:: python

    from kotti.resources import Document
    from kotti.util import _

    def includeme(config):

        Document.type_info.add_selectable_default_view("media_folder_view",
                                                       _("Media Folder"))

You will then be able to select that view for your media section Document in the user interface.

Work in progress
================

``kotti_media`` is considered alpha software, not yet suitable for use in production environments.
The current state of the project is in no way feature complete nor API stable.
If you really want to use it in your project(s), make sure to pin the exact version in your requirements.
Not doing so will likely break your project when future releases become available.


Development
===========

Contributions to ``kotti_media`` are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

Testing
-------

|build status|_

``kotti_media`` has 100% test coverage.
Please make sure that you add tests for new features and that all tests pass before submitting pull requests.
Running the test suite is as easy as running ``py.test`` from the source directory (you might need to run ``python setup.py dev`` to have all the test requirements installed in your virtualenv).


.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
.. _Github repository: https://github.com/disko/kotti_media
.. _gitflow: https://github.com/nvie/gitflow
.. _A successful Git branching model: http://nvie.com/posts/a-successful-git-branching-model/
.. _MediaElementJS: http://mediaelementjs.com/
.. |build status| image:: https://secure.travis-ci.org/disko/kotti_media.png?branch=master
.. _build status: http://travis-ci.org/disko/kotti_media
