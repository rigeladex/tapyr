# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.
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
#    jQuery
#
# Purpose
#    Definition of the javascript and CSS file if jQuery and jQuery UI should
#    be used.
#
# Revision Dates
#     1-May-2010 (MG) Creation
#     3-Aug-2010 (CT) `de_obfuscate_a` added
#     4-Aug-2010 (CT) `fix_a_nospam` factored
#     7-Oct-2010 (CT) `GTW_Gallery` added
#    10-Oct-2010 (CT) `GTW_Externalize` added
#    18-Oct-2010 (CT) `GTW_pixpander` added
#    15-Nov-2010 (CT) `GTW_week_roller` added
#    19-Nov-2010 (CT) `Modernizr` added
#    12-Jan-2011 (CT) `GTW_Input` and `GTW_Label` added
#    20-Jan-2011 (CT) Functions `GTW_Gallery`, `GTW_Externalize`,
#                     `GTW_pixpander`, `GTW_week_roller` renamed to lowercase
#    26-Jan-2011 (CT) `GTW.js` added
#     1-Feb-2011 (CT) Changed `src` of GTW-specific js-files
#     7-Apr-2011 (MG) Use jQuery 1.5.2
#     7-Apr-2011 (MG) Definitions for `jqPlot` added
#     1-Jun-2011 (CT) `GTW_postify_a` added
#    13-Sep-2011 (MG) `s/sort_key/rank/g`
#    19-Oct-2011 (CT) Use jQuery 1.6.4 (but without version number in filename)
#     8-Nov-2011 (CT) Add `GTW_jq_util`
#    22-Nov-2011 (CT) Add `GTW_query_restriction`
#    26-Nov-2011 (CT) Add `GTW_e_type_admin`, `GTW_buttonify`
#     2-Dec-2011 (CT) Use `modernizr.custom.js` instead of specific version
#     6-Dec-2011 (CT) Add `GTW_jsonify`, `GTW_afs_elements`, `GTW_inspect`,
#                     `GTW_jq_afs`, and `GTW_autocomplete`
#    15-Dec-2011 (CT) Add `GTW_UI_Icon_Map`, `GTW_e_type_selector`
#     3-Jan-2012 (CT) Add `requires` to `Script` definitions
#    ««revision-date»»···
#--

from   _GTW import GTW
import _GTW.Media

if __debug__ :
    GTW.Script \
        ( src      = "/media/GTW/js/jquery.js"
        , rank     = -101  ## should be loaded first
        , name     = "jQuery"
        )
    GTW.Script \
        ( src      = "/media/GTW/js/jquery-ui.js"
        , name     = "jQuery_UI"
        , rank     = -100  ## should be loaded first
        , requires = (GTW.Script._.jQuery, )
        )
else :
    GTW.Script \
        ( src      = "/media/GTW/js/jquery.min.js"
        , rank     = -101  ## should be loaded first
        , name     = "jQuery"
        )
    GTW.Script \
        ( src      = "/media/GTW/js/jquery-ui.min.js"
        , name     = "jQuery_UI"
        , rank     = -100  ## should be loaded first
        , requires = (GTW.Script._.jQuery, )
        )

GTW.Script \
    ( src      = "/media/GTW/js/jquery.gritter.js"
    , name     = "jQuery_Gritter"
    , requires = (GTW.Script._.jQuery, )
    )

GTW.Script \
    ( src  = "/media/GTW/js/modernizr.custom.js"
    , name = "Modernizr"
    , rank = -10000   ## should be loaded really first
    )

GTW.CSS_Link ("/media/GTW/css/jquery-ui.css", name = "jQuery_UI")
GTW.CSS_Link \
    ( "/media/GTW/css/jquery.gritter.css"
    , media_type = "screen"
    , name       = "jQuery_Gritter"
    )
GTW.JS_On_Ready \
    ( '$.gritter.Convert_Patagraphs_to_Gitter ("notifications");'
    , name = "jQuery_Gritter"
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW.js"
    , name     = "GTW"
    , rank     = -50
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/UI_Icon_Map.js"
    , name     = "GTW_UI_Icon_Map"
    , rank     = -40
    , requires = (GTW.Script._.GTW, )
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/inspect.js"
    , name     = "GTW_inspect"
    , requires = (GTW.Script._.GTW, )
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jsonify.js"
    , name     = "GTW_jsonify"
    , requires = (GTW.Script._.GTW, )
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/AFS/Elements.js"
    , name     = "GTW_afs_elements"
    , requires = (GTW.Script._.GTW_inspect, )
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/util.js"
    , name     = "GTW_util"
    , requires = (GTW.Script._.Modernizr, GTW.Script._.jQuery, GTW.Script._.GTW)
      ### XXX remove dependency on jQuery
    )

GTW.JS_On_Ready ("$GTW.fix_a_nospam ($);",          name = "de_obfuscate_a")
GTW.JS_On_Ready \
    ( """$("a[href^='http://'], a[href^='https://']").gtw_externalize ();"""
    , name = "GTW_Externalize"
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/util.js"
    , name     = "GTW_jq_util"
    , requires =
        ( GTW.Script._.jQuery
        , GTW.Script._.GTW_jsonify
        )
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/autocomplete.js"
    , name     = "GTW_autocomplete"
    , requires = (GTW.Script._.jQuery_UI, GTW.Script._.GTW_jq_util)
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/buttonify.js"
    , name     = "GTW_buttonify"
    , rank     = -10
    , requires = (GTW.Script._.jQuery_UI, GTW.Script._.GTW_UI_Icon_Map)
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/postify_a.js"
    , name     = "GTW_postify_a"
    , requires = (GTW.Script._.jQuery, GTW.Script._.GTW_jq_util)
    )
GTW.JS_On_Ready \
    ( """$("a.delete").gtw_postify_a ();"""
    , name = "GTW_postify_a"
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/afs.js"
    , name     = "GTW_jq_afs"
    , requires =
        ( GTW.Script._.GTW_afs_elements
        , GTW.Script._.GTW_autocomplete
        )
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/e_type_selector.js"
    , name     = "GTW_e_type_selector"
    , requires =
        ( GTW.Script._.GTW_autocomplete
        , GTW.Script._.GTW_buttonify
        , GTW.Script._.GTW_jq_util
        )
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/query_restriction.js"
    , name     = "GTW_query_restriction"
    , requires =
        ( GTW.Script._.GTW_autocomplete
        , GTW.Script._.GTW_buttonify
        , GTW.Script._.GTW_e_type_selector
        , GTW.Script._.GTW_jq_util
        , GTW.Script._.GTW_util
        )
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/e_type_admin.js"
    , name     = "GTW_e_type_admin"
    , requires =
        ( GTW.Script._.jQuery_UI
        , GTW.Script._.GTW_postify_a
        , GTW.Script._.GTW_query_restriction
        )
    )
GTW.JS_On_Ready \
    ( """$GTW.ETA$.setup_obj_list (); """
    , name = "GTW_e_type_admin"
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/gallery.js"
    , name     = "GTW_Gallery"
    , requires = (GTW.Script._.jQuery_UI, )
    )
GTW.JS_On_Ready \
    ( """$(".thumbnails").gtw_gallery ({ delay : 2000 });"""
    , name = "GTW_Gallery"
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/input.js"
    , name     = "GTW_Input"
    , requires = (GTW.Script._.jQuery, )
    )
GTW.JS_On_Ready \
    ( """$("[placeholder]").gtw_input_placeholders ();"""
    , name = "GTW_Input_Placeholders"
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/label.js"
    , name     = "GTW_Label"
    , requires = (GTW.Script._.jQuery, )
    )
GTW.JS_On_Ready \
    ( """$("label[for]").gtw_label_clicker ();"""
    , name = "GTW_Label_Clicker"
    )
GTW.JS_On_Ready \
    ( """$("label[for]").gtw_label_as_placeholder ();"""
    , name = "GTW_Label_As_Placeholder"
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/pixpander.js"
    , name     = "GTW_pixpander"
    , requires = (GTW.Script._.jQuery, )
    )
GTW.JS_On_Ready \
    ( """$("a[href$='.jpg'] > img, a[href$='.png'] > img").gtw_pixpander ();"""
    , name = "GTW_pixpander"
    )

GTW.Script \
    ( src      = "/media/GTW/js/GTW/jQ/week_roller.js"
    , name = "GTW_week_roller"
    , requires =
        ( GTW.Script._.jQuery_UI
        , GTW.Script._.GTW_util
        )
    )
GTW.JS_On_Ready \
    ( """$(".week-roller").gtw_week_roller (); """
    , name = "GTW_week_roller"
    )

### definitions for jqPlot
GTW.CSS_Link ("/media/GTW/css/jquery.jqplot.min.css", name = "jqPlot")
GTW.Script \
    ( src  = "/media/GTW/js/jqPlot/jquery.jqplot.js"
    , name = "jqPlot"
    )
GTW.Script \
    ( src  = "/media/GTW/js/jqPlot/plugins/jqplot.cursor.min.js"
    , name = "jqPlot_cursor"
    )
GTW.Script \
    ( src  = "/media/GTW/js/jqPlot/plugins/jqplot.dateAxisRenderer.min.js"
    , name = "jqPlot_dateaxis"
    )
GTW.Script \
    ( src  = "/media/GTW/js/jqPlot/plugins/jqplot.canvasAxisTickRenderer.min.js"
    , name = "jqPlot_canvastick"
    )
GTW.Script \
    ( src  = "/media/GTW/js/jqPlot/plugins/jqplot.canvasTextRenderer.min.js"
    , name = "jqPlot_canvastext"
    )
GTW.Script \
    ( src  = "/media/GTW/js/jqPlot/plugins/jqplot.enhancedLegendRenderer.min.js"
    , name = "jqPlot_legend"
    )
GTW.Script \
    ( src = "/media/GTW/js/jqPlot/excanvas.js"
    , condition = "IE"
    , name = "jqPlot_excanvas"
    )

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.jQuery
