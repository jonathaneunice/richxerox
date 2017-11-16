"""
Manage the Mac pasteboard (aka "clipboard") supporting the
possibility of cutting and pasting rich text (HTML and RTF),
in addition to plain text.
"""

# Mac OS X: put export LC_CTYPE=en_US.utf-8 in .bash_profile to avoid
# anoying console UnicodeError

import Foundation
from AppKit import NSPasteboard
import sys

_PY3 = sys.version_info[0] > 2

if _PY3:
    # pylint: disable=W0622, C0103
    unicode = str

preferred_formats = ['rtf', 'html', 'text']  # in preference order

format2uti = {
    'html': 'public.html',
    'rtf':  'public.rtf',
    'text': 'public.utf8-plain-text'
}
uti2format = dict((v, k) for k, v in format2uti.items())

# UTIs are Uniform Type Identfifiers (http://en.wikipedia.org/wiki/Uniform_Type_Identifier)
# ...even if they sound a lot like urinary tract infections


def UTI(fmt):
    """
    Return the Uniform Type Identfifiers
    for the given simple format name ('rtf', 'html', 'text').
    If the format name is unknown, returns it directly, assuming it's an
    explicit UTI.
    """
    return format2uti.get(fmt, fmt)


def _unicode(pb_string):
    """
    Convert a string returned from pyobjc into a proper Python Unicode
    string.
    """
    return None if pb_string is None else unicode(pb_string)

    # pb.stringForType_ hands back a ``objc.pyobjc_unicode`` value, which is not
    # the same as Python ``unicode``, even though its printed ``repr`` value
    # looks the same. So we typecast into a proper ``unicode`` string. In Python 3,
    # this is the same as ``str``.


def paste(format='text'):
    """
    Return data of the given format ('rtf', 'html', 'text', or an explict UTI) from
    the Mac pasteboard (aka clipboard), if any, otherwise None. Data comes from
    OS X as UTF-8, and is automatically upleveled to Python Unicode.
    """
    pb = NSPasteboard.generalPasteboard()
    contents = pb.stringForType_(UTI(format))
    return _unicode(contents)


def available(neat=True, dyn=False):
    """
    Return list of formats available on the pasteboard. By default, provides a
    simple 'format' name ('rtf', 'html', or 'text') for preferred types, or UTIs
    for other types. By default, excluses items whose type starts with 'dyn.',
    which is a dynamic type lookup scheme for 'unregistered' type codes--beyond
    our current scope of operations.
    """
    items = NSPasteboard.generalPasteboard().pasteboardItems()
    if not items:
        return []
    types = items[0].types()
    if not dyn:
        types = [t for t in types if not t.startswith('dyn.')]
    if neat:
        return [uti2format.get(u, u) for u in types]
    else:
        return types


def pasteall(neat=True, dyn=False):
    """
    Return a dict of all available data types, matched to the associated
    content. Good for curiosity, if not as useful in practice. Arguments
    are as those for available().
    """
    pb = NSPasteboard.generalPasteboard()

    return dict([(_unicode(t), _unicode(pb.stringForType_(UTI(t)))) for t in available(neat, dyn)])


def copy(text=None, clear_first=True, **kwargs):
    """
    Put contents onto the Mac pasteboard (aka clipboard). Default format is
    text. Other formats can be copied with kwargs style. E.g.::
        copy(some_text). This lets a caller add
    multiple formats (representations) in parallel. As a backup, you can also
    provide a direct kwargs dict with actual UTIs. By default, the clipboard
    will be cleared first, so that old data types/snippets hanging around
    from previous operations (or other applications) do not interefere.
    """
    if text is not None:
        kwargs['text'] = text
    pb = NSPasteboard.generalPasteboard()
    if clear_first:
        pb.clearContents()
    pb.declareTypes_owner_([UTI(f) for f in kwargs.keys()], None)

    for fmt, value in kwargs.items():
        new_str = Foundation.NSString.stringWithString_(value).nsstring()
        new_data = new_str.dataUsingEncoding_(Foundation.NSUTF8StringEncoding)
        pb.setData_forType_(new_data, UTI(fmt))


def clear():
    """
    Clears the existing contents of the pasteboard.
    """
    pb = NSPasteboard.generalPasteboard()
    pb.clearContents()


class Pasteboard(object):
    """
    A different way of packaging the copy/paste/clear functionality.
    Came after the functional interface, so really is just a veneer on it.
    """

    # pylint: disable=C0111,R0201,E303

    def available(self, *args, **kwargs):
        return available(*args, **kwargs)

    def get_contents(self, *args, **kwargs):
        return paste(*args, **kwargs)

    def get_all_contents(self, *args, **kwargs):
        return pasteall(*args, **kwargs)

    def set_contents(self, *args, **kwargs):
        return copy(*args, **kwargs)

    def clear(self, *args, **kwargs):
        return clear(*args, **kwargs)


pasteboard = Pasteboard()
