#! /usr/bin/env python

from setuptools import setup
import sys

def linelist(text):
    """
    Returns each non-blank line in text enclosed in a list.
    """
    return [ l.strip() for l in text.strip().splitlines() if l.split() ]


# If Foundation and AppKit already installed, don't attempt to have setup
# process re-install or update them. However, install them if not currently
# present. 

try:
    # pylint: disable=W0611
    import Foundation
    import AppKit
    needs = []
except ImportError:
    needs = ['pyobjc']

setup(
    name='richxerox',
    version="1.0.1",
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description='copy/paste for Mac OS X for rich text (HTML/RTF) rather than plain text',
    long_description=open('README.rst').read(),
    url='https://bitbucket.org/jeunice/richxerox',
    py_modules=['richxerox'],
    install_requires=needs,
    tests_require = ['tox', 'pytest', 'six'],
    keywords='Mac OS X copy paste clipboard pasteboard rich text RTF HTML',
    classifiers=linelist("""
        Development Status :: 4 - Beta
        Environment :: MacOS X :: Cocoa
        License :: OSI Approved :: BSD License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: Implementation :: CPython
        Topic :: Software Development :: Libraries :: Python Modules
        Topic :: Text Processing :: Markup
        Topic :: Text Processing :: Markup :: HTML
    """)
)
