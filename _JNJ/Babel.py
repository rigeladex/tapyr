# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package JNJ.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    JNJ.Babel
#
# Purpose
#    Add additional keywords to the default extraction method and adopt the
#    parameter's
#    Heavily inspired by the jinja2.ext module (unfortunately we had to copy
#    the code to make it work for your purposes)
#
# Revision Dates
#    24-Jan-2010 (MG) Creation
#    25-Jan-2010 (MG) Looks like we need to strip the first new line in order
#                     to have the right key for the lookup
#    23-Feb-2010 (MG) `babel_extract` copied over from `jinja2.ext` because
#                     we want to see the `TemplateSyntaxError`s and we need
#                     to add the `JNJ.Environment.Default_Extensions` to the
#                     environment
#    ««revision-date»»···
#--

from    jinja2             import ext
from   _TFL._Babel.Extract import Default_Keywords
from   _JNJ                import JNJ
import _JNJ.Environment

def Extract (fobj, keywords, comment_tags, config, method) :
    keywords = Default_Keywords
    for lineno, funcname, messages, comments in babel_extract \
        (fobj, keywords, comment_tags, config.options (method)) :
        yield lineno, funcname, messages, comments, None
# end def Extract

def babel_extract (fileobj, keywords, comment_tags, options) :
    """Babel extraction method for Jinja templates.

    :param fileobj: the file-like object the messages should be extracted from
    :param keywords: a list of keywords (i.e. function names) that should be
                     recognized as translation functions
    :param comment_tags: a list of translator tags to search for and include
                         in the results.  (Unused)
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)`` tuples.
             (comments will be empty currently)
    """
    extensions = set ()
    for extension in options.get ("extensions", "").split (",") :
        extension = extension .strip ()
        if not extension:
            continue
        extensions.add (ext.import_string (extension))
    for extension in JNJ.Environment.Default_Extensions :
        if isinstance (extension, basestring) :
            extension = ext.import_string (extension)
        extensions.add (extension)
    if ext.InternationalizationExtension not in extensions :
        extensions.add (ext.InternationalizationExtension)

    environment = ext.get_spontaneous_environment \
        ( options.get ("block_start_string",    ext.BLOCK_START_STRING)
        , options.get ("block_end_string",      ext.BLOCK_END_STRING)
        , options.get ("variable_start_string", ext.VARIABLE_START_STRING)
        , options.get ("variable_end_string",   ext.VARIABLE_END_STRING)
        , options.get ("comment_start_string",  ext.COMMENT_START_STRING)
        , options.get ("comment_end_string",    ext.COMMENT_END_STRING)
        , options.get ("line_statement_prefix") or ext.LINE_STATEMENT_PREFIX
        , options.get ("line_comment_prefix") or ext.LINE_COMMENT_PREFIX
        , str (options.get ("trim_blocks", ext.TRIM_BLOCKS)).lower()
          in ("1", "on", "yes", "true")
        , ext.NEWLINE_SEQUENCE
        , frozenset (extensions)
        # fill with defaults so that environments are shared
        # with other spontaneus environments.  The rest of the
        # arguments are optimizer, undefined, finalize, autoescape,
        # loader, cache size, auto reloading setting and the
        # bytecode cache
        , True, ext.Undefined, None, False, None, 0, False, None
        )

    source = fileobj.read ().decode (options.get ("encoding", "utf-8"))
    node   = environment.parse (source)
    for lineno, func, message in extract_from_ast (node, keywords) :
        yield lineno, func, message, []
# end def babel_extract

def extract_from_ast ( node
                     , gettext_functions = ext.GETTEXT_FUNCTIONS
                     , babel_style       = True
                     ) :
    """Copied from jinja2.ext because we have translation calls hidden in
       Getattr nodes as well.
    """
    for node in node.find_all (ext.nodes.Call) :
        if (  (  not isinstance (node.node, ext.nodes.Name)
              or node.node.name not in gettext_functions
              )
          and ( not isinstance (node.node, ext.nodes.Getattr)
              or node.node.attr not in gettext_functions
              )
          ) :
            continue

        strings = []
        for arg in node.args :
            if (   isinstance (arg,       ext.nodes.Const)
               and isinstance (arg.value, basestring)
               ) :
                strings.append (arg.value.lstrip ("\n"))
            else:
                strings.append (None)

        for arg in node.kwargs :
            strings.append (None)
        if node.dyn_args is not None :
            strings.append (None)
        if node.dyn_kwargs is not None :
            strings.append (None)

        if not babel_style :
            strings = tuple(x for x in strings if x is not None)
            if not strings :
                continue
        else:
            if len (strings) == 1 :
                strings = strings [0]
            else:
                strings = tuple (strings)

        if isinstance (node.node, ext.nodes.Name) :
            yield node.lineno, node.node.name, strings
        else :
            yield node.lineno, node.node.attr, strings
# end def extract_from_ast

### __END__ JNJ.Babel


