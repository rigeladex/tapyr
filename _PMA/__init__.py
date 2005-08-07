# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
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
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace

PMA = Package_Namespace ()

PMA.authors         = ["Christian Tanzer", "Martin Glueck"]
PMA.major_version   = _M = 0
PMA.minor_version   = _m = 5
PMA.patchlevel      = _p = 1
PMA.version         = __version__ = "%s.%s.%s" % (_M, _m, _p)
PMA.default_charset = "us-ascii"

def load_user_config (config_fn = "~/PMA/.config.py") :
    import sos
    try :
        execfile (sos.expanded_path (config_fn), dict (PMA = PMA))
    except IOError :
        pass
PMA.load_user_config = load_user_config

del load_user_config
del Package_Namespace

### __END__ PMA.__init__
