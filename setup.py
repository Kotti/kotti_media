from setuptools import setup, find_packages
import os

version = '0.4'

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''
try:
    TODO = open(os.path.join(here, 'TODO.txt')).read()
except IOError:
    TODO = ''
try:
    AUTHORS = open(os.path.join(here, 'AUTHORS.txt')).read()
except IOError:
    AUTHORS = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    CHANGES = ''

development_requires = [
    'minify',
]
install_requires = [
    'Kotti>=0.7',
    'js.jquery_form',
    'js.mediaelement',
]
tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-pep8',
    'pytest-xdist',
    'WebTest',
    'wsgi_intercept',
    'zope.testbrowser',
]

setup(
    name='kotti_media',
    version=version,
    description='Add media content to your Kotti site',
    long_description=README + '\n\n' + TODO + '\n\n' + AUTHORS + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pylons',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: Repoze Public License',
    ],
    keywords='video audio medialementjs kotti cms pylons pyramid',
    author='Andreas Kaiser',
    author_email='disko@binary-punks.com',
    url='https://github.com/disko/kotti_media',
    license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
    packages=find_packages(exclude=[
        'ez_setup',
        'examples',
        'tests'
    ]),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'testing': tests_require,
        'development': development_requires,
    },
    message_extractors={
        'kotti_media': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
        ],
    },
    entry_points={
        "fanstatic.libraries": ["kotti_media = kotti_media.static:library"],
    }
)
