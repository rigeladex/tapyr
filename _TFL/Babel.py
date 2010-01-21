# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.Babel
#
# Purpose
#    Some extension for the translation system Babel
#
# Revision Dates
#    20-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--
from   _TFL          import TFL
from   _TFL.Record   import Record
import _TFL.Decorator
import _TFL.I18N
from    tokenize     import generate_tokens, COMMENT, NAME, OP, STRING
from    tokenize     import NL, NEWLINE, INDENT
from    babel.util   import parse_encoding
import  babel.support

@TFL.Contextmanager
def change_language (translations, language) :
    """Temporaly change the translation language
    >>> l1 = TFL.Babel.Translations ()
    >>> l2 = TFL.Babel.Translations ()
    >>> class T (object) :
    ...     languages = dict (l1 = l1,  l2 = l2)
    ...     def language (self, l) : return self.languages [l]
    >>> l1._catalog = dict ( text1 = "L1: Text 1"
    ...                    , text2 = "L1: Text 2"
    ...                    )
    >>> l2._catalog = dict ( text1 = "L2: Text 1"
    ...                    , text2 = "L2: Text 2"
    ...                    )
    >>> translations = Record (l1 = l1, l2 = l2)
    >>> l1.ugettext ("text1")
    'L1: Text 1'
    >>> l2.ugettext ("text1")
    'L2: Text 1'
    >>> TFL.I18N._T ("text1")
    u'text1'
    >>> t = T ()
    >>> with change_language (t, "l1") :
    ...     print TFL.I18N._T ("text1")
    ...     print TFL.I18N._T ("text2")
    L1: Text 1
    L1: Text 2
    >>> with change_language (t, "l2") :
    ...     print TFL.I18N._T ("text1")
    ...     print TFL.I18N._T ("text2")
    L2: Text 1
    L2: Text 2
    """
    old_trans = TFL.I18N.translations
    TFL.I18N.translations = translations.language (language)
    try :
        yield
    finally :
        TFL.I18N.translations = old_trans
# end def change_language

class Translations (babel.support.Translations) :
    """Add some usefule functions."""

    def exists (self, message, ** kw) :
        domain = kw.pop ("domain", self.DEFAULT_DOMAIN)
        trans  = self._domains.get (domain, self)
        return message in trans._catalog
    # end def exists

    def language (self, lang) :
        return self.languages.get (lang, self.default)
    # end def language

    @classmethod
    def load_languages (cls, * languages, ** kw) :
        domains              = kw.pop ("domains",    (cls.DEFAULT_DOMAIN, ))
        locale_dir           = kw.pop ("locale_dir", "locale")
        result               = kw.pop ("base", None)
        if not isinstance (domains, (list, tuple)) :
            domains          = (domains, )
        first_dom            = domains [0]
        domains              = domains [1:]
        if not result :
            result           = cls ()
            result.languages = {}
        first                = True
        for lang in languages :
            domain_t = cls.load (locale_dir, lang, first_dom)
            if not isinstance (domain_t, cls) :
                print "*** Warning, language %s for domain %s" % \
                      (lang, first_dom)
            for d in domains :
                domain_t.merge (cls.load (locale_dir, lang, d))
            if not result.languages :
                result.default      = domain_t
            result.languages [lang] = domain_t
        return result
    # end def load_languages

    @classmethod
    def load_files (cls, option, encoding) :
        result         = None
        other_mo_files = save_unquote (option, encoding, False)
        if other_mo_files :
            if not isinstance (other_mo_files, (list, tuple)) :
                other_mo_files = (other_mo_files, )
            if other_mo_files :
                result = cls.load (* other_mo_files [0])
                for mo in other_mo_files [1:] :
                    result.merge (cls.load (* mo))
        return result
    # end def load_files

# end class Translations

def extract_python (fobj, keywords, comment_tags, options) :
    """Code taken from babel directly but extended:
       * collect doc strings of functions and classes as well
       * it is possible to specify a list existing message catalog's so that
         only new translation keys will be added to the new catalog.
    """
    in_def   = in_translator_comments  = False
    wait_for_doc_string                = False
    funcname = lineno = message_lineno = None
    call_stack                         = -1
    buf                                = []
    messages                           = []
    translator_comments                = []
    comment_tag                        = None
    doc_string_ignore_tok              = set ((NL, NEWLINE, INDENT, STRING))
    encoding = parse_encoding (fobj) or options.get ("encoding", "iso-8859-1")
    tokens   = generate_tokens (fobj.readline)
    transl   = Translations.load_files \
        (options.get ("message_catalogs"), encoding)
    for tok, value, (lineno, _), _, _ in tokens :
        if wait_for_doc_string and tok not in doc_string_ignore_tok :
            wait_for_doc_string = False
        if call_stack == -1 and tok == NAME and value in ("def", "class") :
            in_def              = True
        elif tok == OP and value == "(" and funcname :
                message_lineno = lineno
                call_stack    += 1
        elif tok == OP and value == ":" :
            in_def              = False
            wait_for_doc_string = True ### next string is the doc string
            continue
        elif call_stack == -1 and tok == COMMENT :
            # Strip the comment token from the line
            value = value.decode (encoding) [1:].strip ()
            if (   in_translator_comments
               and translator_comments [-1] [0] == lineno - 1
               ) :
                # We're already inside a translator comment, continue appending
                translator_comments.append ((lineno, value))
                continue
            # If execution reaches this point, let's see if comment line
            # starts with one of the comment tags
            for comment_tag in comment_tags :
                if value.startswith (comment_tag) :
                    in_translator_comments = True
                    translator_comments.append ((lineno, value))
                    break
        elif wait_for_doc_string and tok == STRING :
            ### found a doc_string
            msg = save_unquote (value, encoding)
            if not (transl and transl.exists (msg)) :
                    yield (lineno, funcname, msg, [])
            wait_for_doc_string = False
        elif funcname and call_stack == 0 :
            if tok == OP and value == ")" :
                if buf :
                    messages.append ("".join (buf))
                    del buf [:]
                else:
                    messages.append (None)

                if len (messages) > 1 :
                    messages = tuple (messages)
                else:
                    messages = messages [0]
                # Comments don't apply unless they immediately preceed the
                # message
                if (   translator_comments
                   and translator_comments [-1][0] < message_lineno - 1
                   ) :
                    translator_comments = []

                if not (transl and transl.exists (messages)) :
                    yield \
                        ( message_lineno
                        , funcname
                        , messages
                        , [comment [1] for comment in translator_comments]
                        )
                funcname = lineno = message_lineno = None
                call_stack                         = -1
                messages                           = []
                translator_comments                = []
                in_translator_comments             = False
            elif tok == STRING :
                # Unwrap quotes in a safe manner, maintaining the string's
                # encoding
                # https://sourceforge.net/tracker/?func=detail&atid=355470&
                # aid=617979&group_id=5470
                value = save_unquote (value, encoding)
                if isinstance (value, str) :
                    value = value.decode (encoding)
                buf.append (value)
            elif tok == OP and value == "," :
                if buf :
                    messages.append ("".join (buf))
                    del buf [:]
                else:
                    messages.append (None)
                if translator_comments :
                    # We have translator comments, and since we're on a
                    # comma(,) user is allowed to break into a new line
                    # Let's increase the last comment's lineno in order
                    # for the comment to still be a valid one
                    old_lineno, old_comment = translator_comments.pop ()
                    translator_comments.append ((old_lineno + 1, old_comment))
        elif call_stack > 0 and tok == OP and value == ")" :
            call_stack -= 1
        elif funcname and call_stack == -1 :
            funcname = None
        elif tok == NAME and value in keywords :
            funcname = value
# end def extract_python_ext

def save_unquote (value, encoding, strip = True) :
    result = eval ( "# coding=%s\n%s" % (encoding, value)
                , dict (__builtins__ = {})
                , {}
                )
    if strip :
        return result.strip ()
    return result
# end def save_unquote

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Babel
