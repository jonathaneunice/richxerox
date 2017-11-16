
from richxerox import *
import six

# helper functions


def dict_print(d, heading=None, wrap=True, **kwargs):
    """
    Tidy printing of dictionary elements. Only here
    for demonstation and debugging.
    """
    import textwrap
    initial = kwargs.get('initial_indent', '')
    kwargs['subsequent_indent'] = kwargs.get(
        'subsequent_indent', initial + '    ')

    if heading:
        six.print_(heading)
    TEMPLATE = unicode("   {0}: {1}")
    for key, value in d.items():
        item_text = TEMPLATE.format(key, value)
        if wrap:
            six.print_('\n'.join(textwrap.wrap(item_text, **kwargs)))
        else:
            six.print_(item_text)

# tests


def test_clear():
    clear()
    assert available() == []
    assert list(pasteall().keys()) == []


def test_copypaste():

    t0 = "this is good!"
    h0 = "this is <strong>good</strong>!"
    r0 = "{\\rtf1\\ansi\\ansicpg1252\\cocoartf1187\\cocoasubrtf390\n" \
         "{\\fonttbl\\f0\\froman\\fcharset0 Times-Roman;}\n{\\colortbl;" \
         "\\red255\\green255\\blue255;}\n\\deftab720\n\\pard\\pardeftab720" \
         "\n\n\\f0\\fs24 \\cf0 This is \n\\b good\n\\b0 !}"

    copy(text=t0, html=h0, rtf=r0)

    assert paste('text') == t0
    assert paste('html') == h0
    assert paste('rtf') == r0

    assert len(pasteall().keys()) >= 3


def test_copypaste_unicode():

    t0 = six.u("and\u2012then")
    h0 = six.u("and\u2012<i>then</i>")

    copy(text=t0, html=h0)

    assert paste('text') == t0
    assert paste('html') == h0

    assert len(pasteall().keys()) >= 2


def test_demo_richxerox():
    """
    Let's try it out!
    """

    six.print_(available())
    six.print_(paste())
    dict_print(pasteall(), 'ALL CONTENTS')

    clear()
    dict_print(pasteall(), 'AFTER CLEAR')

    copy(text="this is good!", html="this is <strong>good</strong>!")
    dict_print(pasteall(), 'AFTER COPY')


def test_demo_richxerox_oo():
    # from richxerox import pasteboard

    six.print_(pasteboard.get_contents(format='html'))    # paste
    pasteboard.clear()                              # clear
    pasteboard.set_contents(text="this is good!",   # copy
                            html="this is <strong>good</strong>!")

    dict_print(pasteboard.get_all_contents())       # pasteall

    pb_text = pasteboard.get_contents(format='text')

    assert pb_text == "this is good!"
    assert available() == pasteboard.available()


if __name__ == '__main__':
    test_clear()
    test_copypaste()
    test_demo_richxerox()
    test_demo_richxerox_oo()