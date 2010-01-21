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
#    ««revision-date»»···
#--

from   _TFL         import TFL
import  gettext

class I18N (object) :
    """Encapsulate all translation functions.

       This class can also be `installed` as a global translation object for
       a jinja environment to allow dynamic language switching.
    """

    all_translations = None
    translations     = gettext.NullTranslations ()

    @classmethod
    def load_languages (cls, * args, ** kw) :
        import _TFL.Babel
        use =kw.pop ("use", None)
        cls.all_translations = all = TFL.Babel.Translations.load_languages \
            (* args, ** kw)
        if use :
            cls.translations = all.language (use)
    # end def load_languages

    @staticmethod
    def mark (text):
        """Mark `text` for translation."""
        return unicode (text)
    # end def mark

    @classmethod
    def ugettext (cls, text, trans = None) :
        """Return the localized translation of `text` (as unicode)."""
        return (trans or cls.translations).ugettext (text)
    # end def ugettext

    @classmethod
    def ungettext (cls, singular, plural = None, n = 99, trans = None) :
        """Return the localized translation of `text` for the plural form
           appropriate for `n` (as unicode).
        """
        if plural is None :
            plural = singular + "s"
        return (trans or cls.translation).ungettext (singular, plural, n)
    # end def ungettext

    @classmethod
    def use_language (cls, lang) :
        if isinstance (lang, basestring) :
            if cls.all_translations :
                lang = cls.all_translations.language (lang)
            else :
                raise TypeError \
                    ("No languages loaded, cannot use %s" % (lang, ))
        cls.translations = lang
    # end def use_language

# end class I18N

_   = I18N.mark
_T  = I18N.ugettext
_Tn = I18N.ungettext

if __name__ != "__main__" :
    TFL._Export ("*", "_T", "_Tn")
### __END__ TFL.I18N
