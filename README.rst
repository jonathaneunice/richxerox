Rich text cut/copy/paste for Mac OS X.

Usage
=====

::

    from richxerox import *

    print available() # what kind of data is on the clipboard?

    print paste()     # get data in the default format ('text')
    print paste(format='text')  # get text (Unicode)
    print paste(format='rtf')   # get RTF
    print paste(format='html')  # get HTML

    print "ALL CONTENTS:\n", pasteall()

    clear()
    print "ALL CONTENTS AFTER CLEAR:\n", pasteall()

    r = "{\\rtf1\\ansi\\ansicpg1252\\cocoartf1187\\cocoasubrtf390\n" \
        "{\\fonttbl\\f0\\froman\\fcharset0 Times-Roman;}\n{\\colortbl;" \
        "\\red255\\green255\\blue255;}\n\\deftab720\n\\pard\\pardeftab720" \
        "\n\n\\f0\\fs24 \\cf0 This is \n\\b good\n\\b0 !}"
    h = "this is <strong>good</strong>!"
    copy(text="this is good!", html=h, rtf=r)

    print "ALL CONTENTS AFTER COPY:\n", pasteall()

The API is modeled on that of `xerox <http://pypi.python.org/pypi/xerox>`_,
with simple ``copy()`` and ``paste()`` operations.

Think of ``paste()`` as pasting *into* your program and ``copy()`` as copying
*from* your program.

The main difference in the API is that, given the different formats used in rich
text, one must specify the format provided or needed if it is not plain text.
This is done through keyword-style arguments.

Alternative API
===============

If you prefer an object-oriented API::

    from richxerox import *

    print pasteboard.get_contents(format='html')    # paste
    pasteboard.clear()                              # clear
    pasteboard.set_contents(text="this is good!",   # copy
                            html=h, rtf=r)

    print pasteboard.get_all_contents()       # pasteall

Background
==========

I searched long and hard but couldn't find a simple Python module that made
``copy`` and ``paste`` operations on Mac OS X easy and straightforward. `xerox
<http://pypi.python.org/pypi/xerox>`_ works well, but it only supports plain
text. What about browsers and word processors that export rich text with
hyperlinks, styles, and so on? How can you access *that* data?

After banging my head against this a few times, I eventually found code samples
I could adapt and make work without understanding the entirety of Apple's
``Foundation`` and ``AppKit``. This module is the result.

Descent Into RTF
================

Even in this HTML-everywhere age, Apple and Mac OS X apps are unfortunately `RTF
<http://en.wikipedia.org/wiki/Rich_Text_Format>`_-centric. I say unfortunately
because:

  * In my experience, RTF is often not robustly passed between applications.
    Different apps interpret or render the same RTF differently, so font
    sizes and other characteristics change.

  * RTF is *extremely* verbose. Microsoft Word, for instance, emits 29,807
    characters as the copy/cut representation of "This is **good**!"
    Microsoft is known for verbose exports, and RTF itself attempts to
    represent whole documents rather than individual snippets. Still, that's
    roughly 1,000x (a.k.a. three decimal orders of magnitude) as verbose as HTML.
    Try copying existing text in some
    application, then running ``pasteall()`` to get your own taste of this
    madness.

  * If you put multiple forms of text on the clipboard, you don't have much if
    any control which one an application will use when you ask it to "paste"
    data. If you want a single format, better to just put that one format on the
    clipboard.

While Mac apps occasionally put HTML contents on the pasteboard, RTF seems
to be the most common *lingua franca*. I've not found any particularly good,
robust, or up-to-date Python tools for parsing and transforming RTF. The handy
`textutil
<http://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man1/textutil.1.html>`_
tool will, however, convert an RTF file into quite clean HTML, like so::

    textutil -convert html temp.rtf

yielding ``temp.html``. This can be parsed and manipulated with `lxml
<http://pypi.python.org/pypi/lxml>`_ or your favorite HTML/XML library.

Notes
=====

  * Version 1.0.0 updates the testing matrix. Latest versions of 2.7, 3.3,
    3.4, 3.5, the new 3.6 (alpha 2) are confirmed working. Old,
    pre-[SemVer](http://semver.org/) versions have been removed from PyPI;
    they were causing some install problems. Python 3.2 has been withdrawn
    from support as both ancient and no longer being properly supported in
    my local test rig.)

  * As of version 0.6, much more robust handling of Unicode characters.
    Better auto-install, including installing foundation ``pyobjc``
    module if necessary. (`pyobjc` auto-install only works reliably
    on Python 2.7 and above,
    so official support for Python 2.6 has been withdrawn.)

  * If the underlying `pyobjc` library needs to be installed, the process
    will take a *long* time. For example, 4 hours 7 minutes. Don'ty just get
    coffee while it's installing. Take lunch. A long, languorous lunch. And
    then maybe have a nap.

  * Version 0.5 had a mistake in Unicode handling. Even though it passed all
    tests, it over-quoted Unicode coming from real apps. Fixed.

  * Code inspired by and/or based on Genba's `Reading URLs from OS X clipboard with PyObjC <http://genbastechthoughts.wordpress.com/2012/05/20/reading-urls-from-os-x-clipboard-with-pyobjc/>`_
    and Carl M. Johnson's `copy_paste.py <http://blog.carlsensei.com/post/88897796>`_

  * See also `NSPasteboard docs <http://developer.apple.com/library/mac/#documentation/Cocoa/Reference/ApplicationKit/Classes/NSPasteboard_Class/Reference/Reference.html>`_,
    `a discussion on UTIs <http://sigpipe.macromates.com/2009/03/09/uti-problems/>`_, and
    John Siracusa's `discussion of the evolution of Mac OS types <http://www.scribd.com/doc/6915424/Mac-OS-X-104-Tiger#page=52>`_

 *  The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
    `@jeunice on Twitter <http://twitter.com/jeunice>`_
    welcomes your comments and suggestions.

Installation
============

To install the latest version::

    pip install -U richxerox

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade richxerox

(You may need to prefix these with "sudo " to authorize installation.)