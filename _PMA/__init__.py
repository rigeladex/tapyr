# -*- coding: utf-8 -*-
# Copyright (C) 2004-2010 Mag. Christian Tanzer. All rights reserved
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
#    PMA.__init__
#
# Purpose
#    Python Mail Agent package
#
# Revision Dates
#    31-Aug-2004 (CT) Creation
#    22-Mar-2005 (CT) Moved from lib/python/_TFL to svn repository
#    29-Jul-2005 (CT) `default_charset` and `load_user_config` added
#    29-Jul-2005 (CT) `version` and `authors` added
#     7-Aug-2005 (CT) `patchlevel` increased to 1
#     9-Aug-2005 (CT) `locale.getpreferredencoding` used
#     9-Aug-2005 (CT) `file_system_encoding` added
#     9-Aug-2005 (CT) `patchlevel` increased to 2
#     9-Aug-2005 (CT) s/default_charset/default_encoding/g
#    12-Aug-2005 (MG) `patchlevel` increased to 4
#    16-Aug-2005 (CT) `patchlevel` increased to 5
#     3-Jan-2006 (MG) `load_user_config` changed
#     5-Jan-2006 (CT) `load_config_file` factored to `TGL` and
#                     `load_user_config` interface changed (`* config_fn`)
#     9-Jul-2007 (CT) `text_output_width` added
#    27-Dec-2010 (CT) `minor_version` version increased to 7
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
import locale
import sys

PMA = Package_Namespace ()

PMA.authors              = ["Christian Tanzer", "Martin Glueck"]
PMA.major_version        = _M = 0
PMA.minor_version        = _m = 7
PMA.patchlevel           = _p = 0
PMA.version              = __version__ = "%s.%s.%s" % (_M, _m, _p)
PMA.default_encoding     = locale.getpreferredencoding () or "us-ascii"
PMA.file_system_encoding = sys.getfilesystemencoding ()
PMA.text_output_width    = 75

def load_user_config (* config_fn) :
    from _TFL import sos
    from _TGL.load_config_file import load_config_file
    if not config_fn :
        config_fn = ("~", "PMA", ".config.py")
    load_config_file (sos.path.join (* config_fn), dict (PMA = PMA))
PMA.load_user_config = load_user_config

del load_user_config
del locale
del sys
del Package_Namespace

### __END__ PMA.__init__
