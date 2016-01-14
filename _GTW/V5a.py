# -*- coding: utf-8 -*-
# Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.V5a
#
# Purpose
#    Definition of javascript modules provided by V5a
#
# Revision Dates
#    14-Jan-2016 (CT) Creation
#    20-Jan-2016 (CT) ...Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _GTW        import GTW
import _GTW.Media

### infrastructure
GTW.Script \
    ( src       = "/media/GTW/js/V5a/V5a.js"
    , name      = "V5a"
    , rank      = -70  ## should be loaded first
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/bind.js"
    , name      = "V5a_bind"
    , requires  = (GTW.Script._.V5a, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/extend.js"
    , name      = "V5a_extend"
    , requires  = (GTW.Script._.V5a, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/has_class_all.js"
    , name      = "V5a_has_class_all"
    , requires  = (GTW.Script._.V5a, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/has_class_any.js"
    , name      = "V5a_has_class_any"
    , requires  = (GTW.Script._.V5a, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/history_test.js"
    , name      = "V5a_history_test"
    , requires  = (GTW.Script._.V5a, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/history_push.js"
    , name      = "V5a_history_push"
    , requires  = (GTW.Script._.V5a_history_test, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/merge.js"
    , name      = "V5a_merge"
    , requires  = (GTW.Script._.V5a, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/query.js"
    , name      = "V5a_query"
    , requires  = (GTW.Script._.V5a, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/string_to_int_array.js"
    , name      = "V5a_string_to_int_array"
    , requires  = (GTW.Script._.V5a, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/trigger.js"
    , name      = "V5a_trigger"
    , requires  = (GTW.Script._.V5a_extend, )
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/type_name.js"
    , name      = "V5a_type_name"
    , requires  = (GTW.Script._.V5a, )
    )

### scripts

GTW.Script \
    ( src       = "/media/GTW/js/V5a/de_obfuscate_a_nospam.js"
    , name      = "V5a_de_obfuscate_a_nospam"
    , requires  =
        ( GTW.Script._.V5a_merge
        , GTW.Script._.V5a_query
        , GTW.Script._.V5a_string_to_int_array
        )
    )

GTW.JS_On_Ready \
    ( """$V5a.de_obfuscate_a_nospam ();"""
    , name      = "V5a_de_obfuscate_a_nospam"
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/externalize.js"
    , name      = "V5a_externalize"
    , requires  =
        ( GTW.Script._.V5a_bind
        , GTW.Script._.V5a_has_class_any
        , GTW.Script._.V5a_merge
        , GTW.Script._.V5a_query
        )
    )

GTW.JS_On_Ready \
    ( """$V5a.externalize ();"""
    , name      = "V5a_externalize"
    )

GTW.JS_On_Ready \
    ( """$V5a.externalize """
      """({selectors : {external : "form a"}"""
      """, skip_classes : ["button", "internal", "pure-button", "ui-icon"]"""
      """});"""
    , name      = "V5a_Form_externalize"
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/nav_off_canvas.js"
    , name      = "V5a_nav_off_canvas"
    , requires  =
        ( GTW.Script._.V5a_bind
        , GTW.Script._.V5a_merge
        , GTW.Script._.V5a_query
        )
    )
GTW.JS_On_Ready \
    ( """$V5a.nav_off_canvas ();"""
    , name      = "V5a_nav_off_canvas"
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/page_notifications.js"
    , name      = "V5a_page_notifications"
    , requires  =
        ( GTW.Script._.V5a_bind
        , GTW.Script._.V5a_merge
        , GTW.Script._.V5a_query
        )
    )
GTW.JS_On_Ready \
    ( """$V5a.page_notifications ();"""
    , name      = "V5a_page_notifications"
    )

GTW.Script \
    ( src       = "/media/GTW/js/V5a/pixpander.js"
    , name      = "V5a_pixpander"
    , requires  =
        ( GTW.Script._.V5a_bind
        , GTW.Script._.V5a_merge
        , GTW.Script._.V5a_query
        )
    )
GTW.JS_On_Ready \
    ( """$V5a.pixpander ();"""
    , name      = "V5a_pixpander"
    )

### __END__ GTW.V5a
