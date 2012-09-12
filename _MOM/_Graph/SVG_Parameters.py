# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Graph.
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
#    MOM.Graph.SVG_Parameters
#
# Purpose
#    Default parameters for MOM.Graph.SVG renderer
#
# Revision Dates
#    29-Aug-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _MOM                   import MOM
import _MOM._Graph

from _GTW._CSS.import_CSS import *
from _GTW.Parameters      import Definition, P, P_dict

class SVG_Parameters (Definition) :
    """Default parameters for MOM.Graph.SVG renderer."""

    class color (Definition) :

        attr_link       = RGB_X     ("#FFA022", alpha = 0.70)
        is_a_link       = RGB_X     ("#0088DD", alpha = 0.45)
        node_bg         = RGB_X     ("#EDEDED")
        node_border     = RGB_X     ("#999999")
        role_link       = RGB_X     ("#666666")
        text            = RGB_X     ("#000033")

    # end class color

    attr_marker_size    = 4
    font_family         = "sans-serif"
    font_size           = 18
    font_char_width     = font_size  / 2.0
    is_a_marker_size    = 12
    line_height         = font_size  * 1.5
    link_opacity        = 1.0
    node_opacity        = 1.0
    link_stroke_width   = 5
    node_border_width   = 4

# end class SVG_Parameters

if __name__ != "__main__" :
    MOM.Graph._Export ("SVG_Parameters")
### __END__ MOM.Graph.SVG_Parameters