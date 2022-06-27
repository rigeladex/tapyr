# -*- coding: utf-8 -*-
# Copyright (C) 2004-2019 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
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
#    15-Aug-2015 (CT) Use `@eval_function_body` for scoped setup code
#    29-Oct-2015 (CT) Use `utf-8`, not `ascii`, as default `default_encoding`
#     9-Oct-2016 (CT) Remove dependency on `TGL`
#    19-Aug-2019 (CT) Add `msg_base_dirs`
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _TFL.Decorator         import eval_function_body

PMA = Package_Namespace ()

@eval_function_body
def _setup_PMA_properties () :
    import locale
    import sys
    def load_user_config (* config_fn) :
        from _TFL import sos
        from _TFL.load_config_file import load_config_file
        if not config_fn :
            config_fn = ("~", "PMA", ".config.py")
        load_config_file (sos.path.join (* config_fn), dict (PMA = PMA))
    PMA.authors              = ["Christian Tanzer", "Martin Glueck"]
    PMA.major_version        = _M = 0
    PMA.minor_version        = _m = 8
    PMA.patchlevel           = _p = 0
    PMA.version              = __version__ = "%s.%s.%s" % (_M, _m, _p)
    PMA.default_encoding     = locale.getpreferredencoding () or "utf-8"
    PMA.file_system_encoding = sys.getfilesystemencoding ()
    PMA.text_output_width    = 75
    PMA.load_user_config     = load_user_config
    PMA.msg_base_dirs        = []

### __END__ PMA.__init__
