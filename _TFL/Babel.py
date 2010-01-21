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
#    21-Jan-2010 (MG) Command interface added
#    21-Jan-2010 (MG) `Translations` replaced by `Existing_Translations`
#    ««revision-date»»···
#--

from   _TFL           import TFL
from   _TFL.Record    import Record
from   _TFL.predicate import any_true
import _TFL.I18N
import _TFL.normalized_indent
import _TFL.CAO
import  os

from    tokenize     import generate_tokens, COMMENT, NAME, OP, STRING
from    tokenize     import NL, NEWLINE, INDENT
from    babel.util   import parse_encoding, pathmatch
import  babel.support
from    babel.messages.frontend import CommandLineInterface
from    babel.messages.pofile   import read_po

class Existing_Translations (object) :
    """Read multiple POT files and checks whether a certain message is
       already part of another template
    """

    def __init__ (self, packages) :
        self.pot_files = []
        if packages :
            for pkg in (p.strip () for p in packages.split (",")) :
                module   = __import__ (pkg)
                base_dir = os.path.dirname (module.__file__)
                pot_file = os.path.join (base_dir, "-I18N", "template.pot")
                self.pot_files.append (read_po (open (pot_file)))
    # end def __init__

    def __contains__ (self, message) :
        return any_true (message in pot for pot in self.pot_files)
    # end def __contains__

# end class Existing_Translations

def extract_python (fobj, keywords, comment_tags, options) :
    """Code taken from babel directly but extended:
       * collect doc strings of functions and classes as well
       * it is possible to specify a list existing message catalog's so that
         only new translation keys will be added to the new catalog.
    """
    encoding = parse_encoding (fobj) or options.get ("encoding", "iso-8859-1")
    add_doc_strings = options.get ("add_doc_strings", "") == "True"

    ### before we start let's check if we sould ignore this file completly
    ignore_patterns = \
        [p.strip () for p in options.get ("ignore_patterns", "").split (",")]
    if not isinstance (ignore_patterns, (list, tuple)) :
        ignore_patterns = (ignore_patterns, )
    file_name           = fobj.name
    for pattern in ignore_patterns :
        if pathmatch (pattern, file_name) :
            print "   Ignore file due to pattern `%s`" % (pattern, )
            return

    ### now that we know that we have to parse this file, lets start
    trans    = Existing_Translations (options.get ("ignore_packages"))
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
            if msg not in trans :
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

                if messages not in trans :
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

def _add_option (cmd_line, * options) :
    cmd_line.extend (options)
# end def _add_option

def _prefix_path (filename, * prefix) :
    if not os.path.isabs (filename) :
        prefix   = prefix + (filename, )
        filename = os.path.abspath (os.path.join (* prefix))
    return filename
# end def _prefix_path

def extract (cmd) :
    """Create the template pot file."""
    babel         = CommandLineInterface ()
    for base_dir in cmd.argv :
        cfg_file      = _prefix_path (cmd.extraction_config, base_dir)
        template_file = _prefix_path (cmd.template_file,     base_dir, "-I18N")
        keywords      = ["_T", "_Tn"]
        keywords.extend (cmd.keywords)
        babel_cmd     = [__file__, "extract"]
        for k in keywords :
            _add_option      (babel_cmd, "-k", k)
        _add_option          (babel_cmd, "-F", cfg_file)
        if cmd.sort :
            babel_cmd.append ("--sort-output")
        _add_option          (babel_cmd, "-o", template_file)
        babel_cmd.extend     (cmd.argv)
        if cmd.dry_run :
            print " ".join (babel_cmd)
        else :
            babel.run        (babel_cmd)
            ### need to clear the handlers to prevent multiple outputs
            babel.log.handlers = []
# end def extract

def language (cmd) :
    """Create or update the messahe catalog for a language."""
    babel         = CommandLineInterface ()
    language      = cmd.argv.pop (0)
    for base_dir in cmd.argv :
        output_dir = _prefix_path (cmd.output_directory,  base_dir)
        pot_file   = _prefix_path (cmd.template_file,     base_dir, "-I18N")
        po_file    = os.path.join (output_dir, "%s.po" % (language, ))
        if os.path.exists (po_file) :
            babel_cmd     = [__file__, "update"]
            for opt, option in ( (cmd.previous,        "--previous")
                               , (cmd.ignore_obsolete, "--ignore-obsolete")
                               , (cmd.no_fuzzy,         "--no-fuzzy-matching")
                               ) :
                if opt :
                    babel_cmd.append (option)
        else :
            babel_cmd     = [__file__, "init"]
        _add_option (babel_cmd, "-l", language)
        _add_option (babel_cmd, "-i", pot_file, "-o", po_file)
        if cmd.dry_run :
            print " ".join (babel_cmd)
        else :
            babel.run        (babel_cmd)
            ### need to clear the handlers to prevent multiple outputs
            babel.log.handlers = []
# end def language

_Cmd = TFL.CAO.Cmd \
    ( name = "TFL.Babel"
    , args =
        ( TFL.CAO.Cmd_Choice
            ( "command"
            , TFL.CAO.Cmd
                ( extract
                , name = "extract"
                , args =
                    ( "directories:P"
                        "?Directories where the extraction should start"
                    ,
                    )
                , opts =
                    ( "extraction_config:S=babel.cfg?"
                        "Name of the extraction config fileconfig"
                    , "keywords:S,?Additional extraction keyowrds"
                    , "sort:B?Generated template should be alphabetical sorted"
                    , "template_file:P=template.pot?Name of the template file"
                    )
                , min_args = 1
                )
            , TFL.CAO.Cmd
                ( language
                , name = "language"
                , args =
                    ( "language:S?Which language should be processed"
                    , "directories:P"
                        "?Directories where the extraction should start"
                    ,
                    )
                , opts =
                    ( "template_file:P=template.pot?Name of the template file"
                    , "ignore_obsolete:B?"
                        "Do not include obsolete messages in the output"
                    , "no_fuzzy:B?Do not use fuzzy matching (default False)"
                    , "output_directory:P=-I18N?Output directory"
                    , "previous:B?Keep previous msgids of translated messages"
                    )
                , min_args = 2
                )
            , TFL.CAO.Cmd
                ( None
                , name = "compile"
                )
            )
        ,
        )
    , opts = ( "dry_run:B?Show the babel command line instead of "
                 "running the command"
             ,
             )
    )
if __name__ != "__main__" :
    TFL._Export_Module ()
else :
    _Cmd ()
### __END__ TFL.Babel
