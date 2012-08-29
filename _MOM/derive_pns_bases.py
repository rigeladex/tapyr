# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.derive_pns_bases
#
# Purpose
#    Derive MOM base classes for a specific package namespace (PNS)
#
# Revision Dates
#    28-Aug-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *

from   _TFL.Regexp            import Regexp, re
import _TFL.Caller

_doc_pat = Regexp (r"\s+ of \s+ ([A-Za-z0-9_.]+)$", re.VERBOSE)

def _derived (PNS, postfix, base, mixin = None, ** kw) :
    name   = base.type_base_name
    result = base.New \
        ( name_postfix  = postfix
        , _real_name    = name
        , head_mixins   = (mixin, ) if mixin else ()
        , is_partial    = True
        , PNS           = PNS
        , __doc__       = _doc_pat.sub
            (" of %s." % (PNS.__name__), base.__doc__)
        , ** kw
        )
    setattr (PNS, name, result)
    return result
# end def _derived

def derive_pns_bases (PNS, parent_PNS = MOM) :
    """Derive and inject MOM-base classes for a specific package namespace"""
    __module__ = TFL.Caller.globals () ["__name__"]
    postfix    = "_" + PNS._._bname
    pPNS       = parent_PNS
    E          = _derived (PNS, postfix, pPNS.Entity, __module__ = __module__)
    for base in \
            ( pPNS.Link1, pPNS.Link2, pPNS.Link2_Ordered, pPNS.Link3
            , pPNS.Object
            ) :
        _derived (PNS, postfix, base, E, __module__ = __module__)
    _derived \
        (PNS, postfix, pPNS.Named_Object, PNS.Object, __module__ = __module__)
# end def derive_pns_bases

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.derive_pns_bases
