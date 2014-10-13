# -*- coding: utf-8 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    DJO.Apps.Base.__init__
#
# Purpose
#    Package providing infrastructure for DJO -based django applications
#
# Revision Dates
#    14-Jul-2009 (CT) Templates defined (and comment-header added)
#    21-Aug-2009 (MG) Use `JS_On_Ready` to set `sort_key` to force setup of
#                     many 2 many to be executed last
#    23-Aug-2009 (MG) Changed location of jquery-ui css
#     7-Sep-2009 (CT) Use `/media/css/djo/m2m.css` instead of
#                     `/media/css/style.css`
#    ««revision-date»»···
#--

from _DJO          import DJO
from _DJO.Media    import Media
from _DJO.Template import Template

_nf_media = Media \
    ( css_links   =
        ( DJO.CSS_Link ("/media/css/djo/jquery-ui-1.7.2.custom.css")
        , DJO.CSS_Link ("/media/css/djo/m2m.css")
        )
    , scripts     =
        ( DJO.Script (src  = "http://www.google.com/jsapi")
        , DJO.Script (body = 'google.load ("jquery", "1");')
##        , DJO.Script (body = 'google.load ("jquery", "1", {uncompressed:true});')
        , DJO.Script (body = 'google.load ("jqueryui", "1");')
        , DJO.Script (src  = "djo/model_edit_ui.js")
        )
    , js_on_ready =
        ( DJO.JS_On_Ready
              ( '$("fieldset.nested-many-2-many-table'
                  ', fieldset.nested-many-2-many").many2many ();'
              , 100
              )
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
