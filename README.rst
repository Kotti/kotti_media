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

Note that all development is done on the ``develop`` branch and ``master`` is reserved for "production-ready state".
Therefore make sure to always base your work on the current state of the ``develop`` branch.

This follows the highly recommended `A successful Git branching model`_ pattern, which is implemented by the excellent `gitflow`_ git extension.

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
