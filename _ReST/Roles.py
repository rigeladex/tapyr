# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package ReST.
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
#    ReST.Roles
#
# Purpose
#    Define some interpreted text roles for reStructuredText
#
# Revision Dates
#    15-Feb-2010 (CT) Creation
#    15-Jan-2011 (CT) `deleted` role added
#    ««revision-date»»···
#--

from   _ReST                      import ReST
from   _TFL.Regexp                import *

from   docutils                   import nodes, utils
from   docutils.parsers.rst.roles import CustomRole, register_local_role

_uri_pat = Regexp \
    ( r"(?P<text> .*)<(?P<uri> [^>]+)>$"
    , re.VERBOSE | re.DOTALL
    )

def _uri_role (role, rawtext, text, lineno, inliner, options={}, content=[]) :
    if _uri_pat.match (text) :
        text = _uri_pat.text.strip ()
        uri  = _uri_pat.uri.strip  ()
    else :
        text = uri = text.strip ()
    scheme   = options.pop ("uri_scheme", None)
    if scheme :
        ref  = "%s:%s" % (scheme, uri)
    else :
        ref  = uri
    node = nodes.reference (rawtext, text, refuri = ref, ** options)
    return [node], []
# end def _uri_role

_email_role = CustomRole ("email", _uri_role, dict (uri_scheme = "mailto"))
_tel_role   = CustomRole ("tel",   _uri_role, dict (uri_scheme = "tel"))

register_local_role (_email_role.name, _email_role)
register_local_role ("tel",            _tel_role)

def _deleted_role (role, rawtext, text, lineno, inliner, options={}, content=[]) :
    node = nodes.inline (rawtext, text, classes = ["deleted"], ** options)
    return [node], []
# end def _deleted_role

register_local_role ("deleted", _deleted_role)

### __END__ ReST.Roles
