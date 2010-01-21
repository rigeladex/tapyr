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
#    21-Jan-2010 (MG) Option to ignore files added
#    21-Jan-2010 (MG) Doc strings are only added specified in the options.
#                     Indent of doc strings is normalized
#    ««revision-date»»···
#--

from   _TFL          import TFL
from   _TFL.Record   import Record
import _TFL.I18N
import _TFL.normalized_indent

from    tokenize     import generate_tokens, COMMENT, NAME, OP, STRING
from    tokenize     import NL, NEWLINE, INDENT
from    babel.util   import parse_encoding, pathmatch
import  babel.support

class Translations (babel.support.Translations) :
    """Add some usefule functions."""

    def exists (self, message, ** kw) :
        domain = kw.pop ("domain", self.DEFAULT_DOMAIN)
        trans  = self._domains.get (domain, self)
        return message in trans._catalog
    # end def exists

    @classmethod
    def load_files (cls, other_mo_files) :
        result         = None
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
    encoding = parse_encoding (fobj) or options.get ("encoding", "iso-8859-1")
    add_doc_strings = options.get ("add_doc_strings", "") == "True"

    ### before we start let's check if we sould ignore this file completly
    ignore_patterns = options.get ("ignore_patterns", "").split (",")
    if not isinstance (ignore_patterns, (list, tuple)) :
        ignore_patterns = (ignore_patterns, )
    file_name           = fobj.name
    for pattern in ignore_patterns :
        if pathmatch (pattern, file_name) :
            print "   Ignore file due to pattern `%s`" % (pattern, )
            return

    ### now that we know that we have to parse this file, lets start
    transl   = Translations.load_files \
        (TFL.I18N.save_eval (options.get ("message_catalogs"), encoding))
    tokens   = generate_tokens (fobj.readline)
    in_def   = in_translator_comments  = False
    wait_for_doc_string                = False
    funcname = lineno = message_lineno = None
    call_stack                         = -1
    buf                                = []
    messages                           = []
    translator_comments                = []
    comment_tag                        = None
    doc_string_ignore_tok              = set ((NL, NEWLINE, INDENT, STRING))

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
            wait_for_doc_string = add_doc_strings
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
            msg = TFL.normalized_indent (TFL.I18N.save_eval (value, encoding))
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
                value = TFL.I18N.save_eval (value, encoding)
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

if __name__ != "__main__" :
    TFL._Export_Module ()
else :
    import _TFL.CAO

    cmd = TFL.CAO.Cmd \
        ( name = "TFL.Babel"
        , args =
            ( TFL.CAO.Cmd_Choice
                ( TFL.CAO.Cmd
                    ( name = "extract"
                    , args = ( TFL.CAO.Path
                                 ("directories:P?"
                                    "Base directory for the extraction"
                                 )
                             ,
                             )
                    )
                , TFL.CAO.Cmd
                    ( name = "language"
                    )
                , TFL.CAO.Cmd
                    ( name = "compile"
                    )
                )
            ,
            )
        )
### __END__ TFL.Babel
