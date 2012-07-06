# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
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
#    GTW.RST.TOP.__test__
#
# Purpose
#    Doctest for package GTW.RST.TOP
#
# Revision Dates
#     5-Jul-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW._RST._TOP.import_TOP import *

from   _TFL.Formatter            import Formatter, formatted_1

formatted = Formatter (width = 240)

__doc__ = """

    >>> root = Root (HTTP = None)
    >>> root
    <Root : />
    >>> root.entries
    []

    >>> root = Root (HTTP = None
    ...     , language          = "en"
    ...     , entries           =
    ...         ( Page
    ...             ( name          = "about"
    ...             )
    ...         , Dir
    ...             ( name          = "news"
    ...             , entries       =
    ...                 ( Page
    ...                     ( name  = "Sensation"
    ...                     )
    ...                 ,
    ...                 )
    ...             )
    ...         )
    ...     )
    >>> root
    <Root : />
    >>> root.entries
    [<Page about: /about>, <Dir news: /news>]
    >>> ets = tuple (root.entries_transitive)
    >>> ets
    (<Page about: /about>, <Dir news: /news>, <Page Sensation: /news/Sensation>)

"""

### __END__ GTW.RST.TOP.__test__