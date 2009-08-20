# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Apps.Base.__init__
#
# Purpose
#    Package providing infrastructure for DJO -based dkango applications
#
# Revision Dates
#    14-Jul-2009 (CT) Templates defined (and comment-header added)
#    ««revision-date»»···
#--

from _DJO          import DJO
from _DJO.Media    import Media
from _DJO.Template import Template

_nf_media = Media \
    ( css_links   =
        ( DJO.CSS_Link ("/media/css/jquery-ui-1.7.2.custom.css")
        , DJO.CSS_Link ("/media/css/style.css")
        )
    , scripts     =
        ( DJO.Script (src  = "http://www.google.com/jsapi")
        , DJO.Script (body = 'google.load ("jquery", "1"')
##        , DJO.Script (body = 'google.load ("jquery", "1", {uncompressed:true});')
        , DJO.Script (body = 'google.load ("jqueryui", "1");')
        , DJO.Script (src  = "djo/model_edit_ui.js")
        )
    , js_on_ready =
        ( '$("fieldset.nested-many-2-many-table, fieldset.nested-many-2-many").many2many ();'
        ,
        )
    )

_gs_media = Media \
    ( scripts     =
        ( DJO.Script (src  = "http://www.google.com/jsapi")
        , DJO.Script (body = 'google.load ("search", "1");')
        )
    )

_t_b = Template ("djo-base.html")
_fds = Template ("field_group_div_seq.html")
_fgh = Template ("field_group_horizontal.html")
_ftb = Template ("field_group_tr_body.html")
_fth = Template ("field_group_tr_head.html")
_gmb = Template ("gmap_body.html")
_gmh = Template ("gmap_head.html")
_gsb = Template ("google_custom_search_body.html", _gs_media)
_gsh = Template ("google_custom_search_head.html")
_lof = Template ("login_form.html")
_mof = Template ("model_form.html")
_nan = Template ("nav-neighbor.html")
_nse = Template ("nav-section-entry.html")
_nsl = Template ("nav-section-level.html",         uses = (_nse, ))
_nas = Template ("nav-section.html",               uses = (_nsl, ))
_sme = Template ("nav-sitemap-entry.html")
_sml = Template ("nav-sitemap-level.html",         uses = (_sme, ))
_sim = Template ("nav-sitemap.html",               uses = (_sml, ))
_nmf = Template ("nested_model_form.html",         _nf_media)
_nmt = Template ("nested_model_form_table.html",   _nf_media)

### __END__ DJO.Apps.Base.__init__
