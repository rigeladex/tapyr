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
from  _TFL        import TFL
from   tokenize   import generate_tokens, COMMENT, NAME, OP, STRING
from   tokenize   import NL, NEWLINE, INDENT
from   babel.util import parse_encoding
import babel.support

class Translations (babel.support.Translations) :
    """Add some usefule functions."""

    def exists (self, message, ** kw) :
        domain = kw.pop ("domain", self.DEFAULT_DOMAIN)
        trans  = self._domains.get (domain, self)
        return message in trans._catalog
    # end def exists

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
    other_mo_files = save_unquote \
        (options.get ("message_catalogs"), encoding, False)
    if not isinstance (other_mo_files, (list, tuple)) :
        other_mo_files = (other_mo_files, )
    if other_mo_files :
        transl = Translations.load (* other_mo_files [0])
        for mo in other_mo_files [1:] :
            transl.merge (babel.support.Translation.load (* mo))
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
    TFL._Export ("*")
### __END__ TFL.Babel
