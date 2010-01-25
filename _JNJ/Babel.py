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
#
# Revision Dates
#    24-Jan-2010 (MG) Creation
#    25-Jan-2010 (MG) Looks like we need to strip the first new line in order
#                     to have the right key for the lookup
#    ««revision-date»»···
#--

from  jinja2 import ext
from _TFL._Babel.Extract import Default_Keywords

def Extract (fobj, keywords, comment_tags, config, method) :
    keywords = Default_Keywords
    for lineno, funcname, messages, comments in ext.babel_extract \
        (fobj, keywords, comment_tags, config.options (method)) :
        yield lineno, funcname, messages, comments
# end def Extract

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

ext.extract_from_ast = extract_from_ast

### __END__ JNJ.Babel


