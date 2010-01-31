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
#    ««revision-date»»···
#--

from   _TFL            import TFL
from   _TFL.Record     import Record
from   _TFL.predicate  import first
import  gettext

Config = Record \
   ( Languages  = {None : gettext.NullTranslations ()}
   , locale_dir = "locale"
   , domains    = ("messages", )
   )
Config.current = Config.Null = Config.Languages [None]

def add (self, * languages, ** kw) :
    locale_dir = kw.pop ("locale_dir", Config.locale_dir)
    domains    = kw.pop ("domains",    Config.domains)
    use_lang   = kw.pop ("use", None)
    _load_languages (locale_dir, languages, domains)
    if use_lang :
        ise (use_lang)
# end def add

def load (* languages, ** kw) :
    locale_dir        = kw.pop ("locale_dir", Config.locale_dir)
    domains           = kw.pop ("domains",    Config.domains)
    use_lang          = kw.pop ("use", None)
    Config.domains    = domains
    Config.locale_dir = locale_dir
    _load_languages (locale_dir, languages, domains)
    if use_lang:
        use (use_lang)
# end def load

def _load_languages (locale_dir, languages, domains) :
    import babel.support
    if not isinstance (domains, (list, tuple)) :
        domains = (domains, )
    first_dom   = domains [0]
    domains     = domains [1:]
    Trans_Cls   = babel.support.Translations
    for lang in languages :
        Config.Languages [lang] = lang_trans = Trans_Cls.load \
            (locale_dir, lang, first_dom)
        if not isinstance (lang_trans, Trans_Cls) :
            print "*** Warning, language %s for domain %s not found!" % \
                  (lang, first_dom)
        for d in domains :
            new_domain = Trans_Cls.load (locale_dir, lang, d)
            if not isinstance (new_domain, Trans_Cls) :
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
    Langs  = Config.Languages
    loaded = first ((l for l in lang + (None, ) if l in Langs))
    Config.current = Config.Languages [loaded]
# end def use

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
    ...     TFL._T ("text1")
    ...     TFL._T ("text2")
    u'L1: Text 1'
    u'L1: Text 2'
    >>> with context ("l2") :
    ...     TFL._T ("text1")
    ...     TFL._T ("text2")
    u'L2: Text 1'
    u'L2: Text 2'
    """
    old = Config.current
    try :
       use (* lang)
       yield
    finally :
        Config.current = old
# end def context

_   = mark
_T  = ugettext
_Tn = ungettext

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.I18N
