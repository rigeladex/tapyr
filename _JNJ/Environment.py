# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
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
#    JNJ.Environment
#
# Purpose
#    Provide wrapper around jinja2.Environment
#
# Revision Dates
#    29-Dec-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _JNJ               import JNJ
from   _TFL               import TFL

import _JNJ.Onion

from   _TFL.predicate     import uniq

from   jinja2             import Environment, FileSystemLoader

def HTML (version = "html/5.jnj", load_path = (), loader = None, globals = {}, translations = None, ** kw) :
    if load_path :
        assert loader is None
        encoding = kw.pop ("encoding", "iso-8859-1")
        loader   = FileSystemLoader (load_path, encoding)
    extensions   = uniq \
        ( kw.pop ("extensions", [])
        + ["jinja2.ext.loopcontrols", "jinja2.ext.i18n", "jinja2.ext.do"]
        + [JNJ.Onion]
        )
    result = JNJ.Environment.active = Environment \
        ( extensions = extensions
        , loader     = loader
        , ** kw
        )
    result.globals.update (globals)
    result.globals ["html_version"] = version
    if translations is not None :
        env.install_gettext_translations (translations)
    return result
# end def HTML

if __name__ != "__main__" :
    JNJ._Export_Module ()
### __END__ JNJ.Environment
