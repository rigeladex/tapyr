# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.I18N
#
# Purpose
#    Support for internationalization (I18N)
#
# Revision Dates
#    28-Oct-2009 (CT) Creation
#    19-Jan-2010 (CT) `_Tn` changed to make `plural` and `n` optional
#    21-Jan-2010 (MG) Real translation added
#    21-Jan-2010 (CT) Module-level aliases added, `I18N.ungettext` corrected
#    21-Jan-2010 (CT) `load_languages` and `use_language` added
#    21-Jan-2010 (MG) Reworked
#    21-Jan-2010 (MG) `save_eval` added
#    25-Jan-2010 (MG) Support list of languages in `use` and `context`
#    31-Jan-2010 (CT) `import  babel.support` moved inside functions
#    18-Feb-2010 (CT) `Name` added
#    22-Feb-2010 (CT) `choose` factored, `Config.choice` added
#    15-Apr-2010 (MG) `Translations` added and used
#    ««revision-date»»···
#--

from   _TFL            import TFL
from   _TFL.Record     import Record
from   _TFL.predicate  import first, split_hst

import _TFL.Decorator
import  babel.support

import  struct
import  gettext

Config = Record \
   ( Languages  = {"" : gettext.NullTranslations ()}
   , locale_dir = "locale"
   , domains    = ("messages", )
   , choice     = ""
   )
Config.current = Config.Null = Config.Languages [""]

class _Name_ (TFL.Meta.Object) :
    """Translator for names"""

    def __getattr__ (self, name) :
        return _T (name)
    # end def __getattr__

    def __getitem__ (self, key) :
        return _T (key)
    # end def __getitem__

# end class _Name_


class Translations (babel.support.Translations) :
    """Add better support for singula/plural"""

    def _parse(self, fp):
        """Slighly modifiey version of gettext.GNUTranslations._parse."""
        unpack   = struct.unpack
        filename = getattr (fp, "name", "")
        # Parse the .mo file header, which consists of 5 little endian 32
        # bit words.
        self._catalog = catalog = {}
        self.plural   = lambda n: int(n != 1) # germanic plural by default
        buf           = fp.read ()
        buflen        = len     (buf)
        # Are we big endian or little endian?
        magic = unpack ("<I", buf [:4]) [0]
        if magic == self.LE_MAGIC :
            version, msgcount, masteridx, transidx = unpack ("<4I", buf [4:20])
            ii = "<II"
        elif magic == self.BE_MAGIC:
            version, msgcount, masteridx, transidx = unpack (">4I", buf [4:20])
            ii = ">II"
        else:
            raise IOError (0, "Bad magic number", filename)
        # Now put all messages from the .mo file buffer into the catalog
        # dictionary.
        for i in xrange (0, msgcount):
            mlen, moff = unpack (ii, buf [masteridx : masteridx + 8])
            tlen, toff = unpack (ii, buf [transidx  : transidx  + 8])
            mend       = moff + mlen
            tend       = toff + tlen
            if mend < buflen and tend < buflen:
                msg  = buf [moff:mend]
                tmsg = buf [toff:tend]
            else:
                raise IOError (0, "File is corrupt", filename)
            # See if we're looking at GNU .mo conventions for metadata
            if not mlen :
                # Catalog description
                lastk = k = None
                for item in tmsg.splitlines ():
                    item = item.strip ()
                    if not item:
                        continue
                    if ":" in item :
                        k, v           = item.split (":", 1)
                        k              = k.strip ().lower()
                        v              = v.strip ()
                        self._info [k] = v
                        lastk          = k
                    elif lastk :
                        self._info [lastk] += "\n" + item
                    if k == "content-type" :
                        self._charset = v.split ("charset=") [1]
                    elif k == "plural-forms" :
                        v           = v.split     (";")
                        plural      = v [1].split ("plural=") [1]
                        self.plural = c2py        (plural)
            # Note: we unconditionally convert both msgids and msgstrs to
            # Unicode using the character encoding specified in the charset
            # parameter of the Content-Type header.  The gettext documentation
            # strongly encourages msgids to be us-ascii, but some appliations
            # require alternative encodings (e.g. Zope's ZCML and ZPT).  For
            # traditional gettext applications, the msgid conversion will
            # cause no problems since us-ascii should always be a subset of
            # the charset encoding.  We may want to fall back to 8-bit msgids
            # if the Unicode conversion fails.
            if "\x00" in msg :
                # Plural forms
                msgid1, msgid2 = msg.split  ("\x00")
                tmsg           = tmsg.split ("\x00")
                if self._charset:
                    msgid1 = unicode (msgid1, self._charset)
                    msgid2 = unicode (msgid2, self._charset)
                    tmsg   = [unicode (x, self._charset) for x in tmsg]
                for i, msg in enumerate (tmsg) :
                    catalog [(msgid1, i)] = msg
                ### In addtion to the two keys to the catalog as well to be
                ### able to have access to the singular and the last plural
                ### translation as well
                catalog [msgid1] = tmsg [ 0]
                catalog [msgid2] = tmsg [-1]
            else:
                if self._charset :
                    msg       = unicode (msg,  self._charset)
                    tmsg      = unicode (tmsg, self._charset)
                catalog [msg] = tmsg
            # advance to next entry in the seek tables
            masteridx += 8
            transidx  += 8
    # end def _parse

# end class Translations

def add (self, * languages, ** kw) :
    locale_dir = kw.pop ("locale_dir", Config.locale_dir)
    domains    = kw.pop ("domains",    Config.domains)
    use_lang   = kw.pop ("use", "")
    _load_languages (locale_dir, languages, domains)
    if use_lang :
        use (use_lang)
# end def add

def choose (* lang) :
    def _gen (lang) :
        for l in lang :
            yield l, l
        for l in lang :
            if l :
                a, _, b = split_hst (l, "_")
                yield a, b or a
        yield "", ""
    return first (l for l in _gen (lang) if l [0] in Config.Languages)
# end def choose

@TFL.Contextmanager
def context (* lang) :
    """Temporaly change the translation language
    ### Let's fake some Translations
    >>> import  babel.support
    >>> Config.Languages ["l1"] = l1 = babel.support.Translations ()
    >>> Config.Languages ["l2"] = l2 = babel.support.Translations ()
    >>> l1._catalog = dict (text1 = u"L1: Text 1", text2 = u"L1: Text 2")
    >>> l2._catalog = dict (text1 = u"L2: Text 1", text2 = u"L2: Text 2")
    >>> _T ("text1")
    u'text1'
    >>> with context ("l1") :
    ...     _T ("text1")
    ...     _T ("text2")
    u'L1: Text 1'
    u'L1: Text 2'
    >>> with context ("l2") :
    ...     _T ("text1")
    ...     _T ("text2")
    u'L2: Text 1'
    u'L2: Text 2'
    """
    old = Config.current, Config.choice
    try :
       use (* lang)
       yield
    finally :
        Config.current, Config.choice = old
# end def context

def load (* languages, ** kw) :
    locale_dir        = kw.pop ("locale_dir", Config.locale_dir)
    domains           = kw.pop ("domains",    Config.domains)
    use_lang          = kw.pop ("use", "")
    Config.domains    = domains
    Config.locale_dir = locale_dir
    _load_languages (locale_dir, languages, domains)
    if use_lang:
        use (use_lang)
# end def load

def _load_languages (locale_dir, languages, domains) :
    if not isinstance (domains, (list, tuple)) :
        domains = (domains, )
    first_dom   = domains [0]
    domains     = domains [1:]
    for lang in languages :
        Config.Languages [lang] = lang_trans = Translations.load \
            (locale_dir, lang, first_dom)
        if not isinstance (lang_trans, Translations) :
            print "*** Warning, language %s for domain %s not found!" % \
                (lang, first_dom)
        for d in domains :
            new_domain = Translations.load (locale_dir, lang, d)
            if not isinstance (new_domain, Translations) :
                print "*** Warning, language %s for domain %s not found!" % \
                    (lang, d)
            lang_trans.merge (new_domain)
# end def _load_languages

def mark (text):
    """Mark `text` for translation."""
    return unicode (text)
# end def mark

def save_eval (value, encoding = None) :
    # Found in babel....
    # Unwrap quotes in a safe manner, maintaining the string's encoding
    # https://sourceforge.net/tracker/?func=detail&atid=355470&aid=617979&group_id=5470
    if encoding :
        value = "# coding=%s\n%s" % (encoding, value)
    result = eval (value, dict (__builtins__ = {}), {})
    if isinstance (result, basestring) :
        return result.strip ()
    return result
# end def save_eval

def ugettext (text, trans = None) :
    """Return the localized translation of `text` (as unicode)."""
    return (trans or Config.current).ugettext (text)
# end def ugettext

def ungettext (singular, plural = None, n = 99, trans = None) :
    """Return the localized translation of `text` for the plural form
       appropriate for `n` (as unicode).
    """
    if plural is None :
        plural = singular + "s"
    return (trans or Config.current).ungettext (singular, plural, n)
# end def ungettext

def use (* lang) :
    Config.choice  = (l, v) = choose (* lang)
    Config.current = Config.Languages [l]
# end def use

_    = mark
_T   = ugettext
_Tn  = ungettext

Name = _Name_ ()

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.I18N
