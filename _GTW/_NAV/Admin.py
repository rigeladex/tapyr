# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.
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
#    GTW.NAV
#
# Purpose
#    Model navigation for web site
#
# Revision Dates
#    27-Feb-2008 (CT) Creation
#    28-Feb-2008 (CT) `encoding` added and used
#    13-Apr-2008 (CT) `own_links_transitive` corrected (needs to call
#                     `own_links_transitive`, not `own_links`, for sub_dirs)
#    29-Apr-2008 (CT) Default for `input_encoding` defined as class variable
#     3-May-2008 (CT) `Dir.__init__` refactored
#     5-May-2008 (CT) Changed `add_entries` and `from_nav_list_file` to keep
#                     `Type` and `Dir_Type` separate
#     5-May-2008 (CT) Changed `add_entries` to leave `sub_dir` in `d` (and
#                     not pass it positionally to `new_sub_dir`)
#     5-May-2008 (CT) Fixed typo in `new_page` (s/h/href/)
#     6-May-2008 (CT) Changed `new_sub_dir` to keep `src_dir` and `sub_dir`
#                     separate
#     8-May-2008 (CT) `Gallery`, `Photo`, and `Thumbnail` added
#     8-May-2008 (CT) `from_nav_list_file` changed to pass `globals` to
#                     `execfile` (too allow tings like `Type = Gallery` there)
#     9-May-2008 (CT) `_Meta_` and `Table` added
#     9-May-2008 (CT) `top` made into class variable
#    10-May-2008 (MG) `add_page` and `add_sub_dir` fixed
#    10-May-2008 (MG) Use `posixpath` instead of `os.path` (we deal with urls
#                     here not with a files system)
#    12-May-2008 (MG) `url_resolver` and `url_patterns` added
#    12-May-2008 (MG) Context processor `populate_naviagtion_root` added
#    12-May-2008 (MG) `new_sub_dir` and `new_page`: don't normpath `src_dir`
#                     and `href`
#    12-May-2008 (MG) `rhref` added
#    14-May-2008 (CT) `file_stem` fixed
#    14-May-2008 (CT) `Page.__init__` changed to use `self.url_resolver`
#                     instead of `self.parent.url_resolver`
#    14-May-2008 (CT) `dump` added
#    14-May-2008 (CT) `href` converted to property based on new attribute `name`
#    14-May-2008 (CT) `Page.dir` and `Page.level` converted from attributes
#                     to properties
#    14-May-2008 (CT) `Root` and `_Dir_` factored from `Dir`
#    14-May-2008 (CT) `from_dict_list` added
#    14-May-2008 (CT) Bug fixes in `add_entries` and `from_dict_list`
#    14-May-2008 (MG) `Page.parents` added
#    14-May-2008 (MG) `rhref` removed and `_Dir_.url_resolver` removed
#    14-May-2008 (MG) `url_patterns` moved up into `_Site_Entity_`
#    16-May-2008 (MG) `_Site_Entity_.__init__`: Move `url_resolver` in here
#                     (from `_Dir_) and added support for `_Site_Entity_`
#                     which don't have there own url resolver
#    16-May-2008 (MG) `url_resolver_pattern` added
#    16-May-2008 (MG) `_Site_Entity_.href` fixed in case of an empfy `href`
#    17-May-2008 (MG) `_Dir_.delegation_view` added
#    18-May-2008 (MG) Check `src_dir` against None to allow an empty `src_dir`
#    19-May-2008 (CT) Missing import for `Url_Resolver` added
#    20-May-2008 (MG) `_Site_Entity_.relative_to` added, url resolver
#                     handling cleanup
#    20-May-2008 (MG) Bug with `delegation_view` fixed
#    21-May-2008 (MG) `url_resolver_pattern` removed
#    21-May-2008 (CT) `copyright` property added
#    22-May-2008 (MG) `_Site_Entity_.view` added,
#                     `_Dir_.default_view_pattern` added
#                     `Url_Pattern` renamed to `Single_Url_Pattern`
#    22-May-2008 (CT) s/class_method/unbound_method/ (Truth in Advertising)
#    22-May-2008 (CT) `_Site_Entity_.__init__` streamlined
#    22-May-2008 (CT) `_formatted_attr` added to `dump`
#    22-May-2008 (CT) `_Dir_.dump` changed to use `_entries` instead of
#                     `own_links`
#    23-May-2008 (CT) `rendered` added
#    23-May-2008 (CT) Semantics of `_Photo_.name` changed (so that `href`
#                     works properly)
#    23-May-2008 (CT) `Page_ReST` and `Page_ReST_F` added
#    23-May-2008 (CT) `Dyn_Slice_ReST_Dir` added
#    25-May-2008 (MG) `_setup_url_resolver` fixed to work without a parent as
#                     well
#    27-May-2008 (CT) `translator` added
#     8-Jul-2008 (CT) `implicit` added
#     8-Jul-2008 (CT) `Root.universal_view` and `Root.page_from_href` added
#     9-Jul-2008 (CT) `_get_child` added to `_Site_Entity_`, `Gallery`, and
#                     `Dir`
#     9-Jul-2008 (CT) `Gallery` changed to consider `delegation_view`
#     9-Jul-2008 (CT) `_Dir_.rendered` added
#     9-Jul-2008 (CT) Default for `delegation_view` moved from `Dir` to `Root`
#                     (and handling changed to allow `True` for
#                     `delegation_view`, too)
#    10-Jul-2008 (CT) `_view` factored from `universal_view`
#    10-Jul-2008 (CT) `Model_Admin` started
#    11-Jul-2008 (CT) `Model_Admin` continued
#    15-Jul-2008 (CT) Use `DJO.Model_Form` instead of plain old
#                     newsforms.Model_Form
#    15-Jul-2008 (CT) `Site_Admin` added
#    29-Aug-2008 (CT) s/super(...)/__m_super/
#    23-Sep-2008 (CT) `_Site_Entity_.rendered` changed to always put
#                     `page = self` into context (otherwise delegation from
#                     `Dir` to `Page` doesn't work properly)
#    25-Sep-2008 (CT) `Alias` added
#    26-Sep-2008 (CT) Optional argument `nav_page` added to `rendered`
#     3-Oct-2008 (CT) Properties `has_children` and `Type` added
#     3-Oct-2008 (CT) `context ["NAV"]` added to `rendered`
#     3-Oct-2008 (CT) `Alias` changed to inherit from `Page`,
#                     `Alias.__getattr__` added
#     3-Oct-2008 (MG) `populate_naviagtion_root`, `url_pattern`, and
#                     `delegation_view` removed (not needed anymore)
#     5-Oct-2008 (MG) `Bypass_URL_Resolver` added
#     5-Oct-2008 (MG) `none_result` and `no_entries_template` added
#     6-Oct-2008 (MG) `none_result` and` no_entries_template` replaced by
#                     `empty_template`
#                     `_Site_Entity_._view` raise `Http404` in case
#                     `rendered` returns `None`
#                     `Root.url_pattern` and friends added
#     7-Oct-2008 (CT) Esthetics (and spelling)
#     7-Oct-2008 (CT) Gallery changed to use a directory-style `href`
#     7-Oct-2008 (CT) `empty_template` moved from `_Dir_` to `Root`
#     7-Oct-2008 (CT) `auto_delegate` added to support statically generated
#                     files
#     7-Oct-2008 (CT) `page_from_href` changed to try `href` with a trailing
#                     slash, too
#     9-Oct-2008 (CT) Use `.top` to access class variables like
#                     `url_patterns` and `handlers` that might be redefined
#                     for the instance of `Root`
#     9-Oct-2008 (MG) `Root.pre_first_request_hooks` added and used in
#                     `universal_view`
#     9-Oct-2008 (MG) `Site_Admin.__init__` allow models without `admin_args`
#                     set
#    10-Oct-2008 (CT) Esthetics
#                     (and use `.top` to access `pre_first_request_hooks`)
#    10-Oct-2008 (CT) Guard for `DoesNotExist` added to `Changer.rendered`
#                     and `Deleter._view`
#    10-Oct-2008 (MG)  `Site_Admin.__init__` use `unicode
#                      (m._meta.verbose_name_plural)` to resolve the
#                      translation proxy
#    14-Oct-2008 (CT) `_load_view` factored and used in `Url_Pattern.resolve`
#    15-Oct-2008 (CT) `Model_Admin.has_children` and `Model_Admin.prefix` added
#    15-Oct-2008 (CT) `Model_Admin.Field.formatted` changed to not apply
#                     `str` to values of type `unicode`
#    15-Oct-2008 (CT) `Site_Admin.rendered` simplified and then commented out
#    16-Oct-2008 (CT) `Model_Admin._get_child` changed to set proper `name`
#                     for `Changer`
#    17-Oct-2008 (CT) `login_required` added
#    18-Oct-2008 (CT) Factored from monolithic `DJO.Navigation`
#    18-Oct-2008 (CT) `Model_Admin.count` added (because Django templates are
#                     FUBAR -- `link.Model.objects.count` silently fails to
#                     return the count)
#    19-Oct-2008 (CT) s/admin_args/NAV_admin_args/g
#    19-Oct-2008 (CT) Add `top.Models` automatically to `Site_Admin`
#    19-Oct-2008 (CT) `Model_Admin` factored to `DJO.NAV.Model.Admin`
#    23-Jan-2009 (CT) Use `(Model, kind_name)` as index for `top.Models`
#    26-Feb-2009 (CT) `Site_Admin` fixed to handle `top.Models` with
#                     `kind_name` properly
#    27-Feb-2009 (CT)  `_model_entries` changed to add `_Field` to (non-DJO)
#                      models
#    28-May-2009 (CT) s/_Field/_F/g
#     8-Jan-2010 (CT) Moved from DJO to GTW
#    18-Jan-2010 (CT) Surgery
#    25-Jan-2010 (CT) `rendered` changed to take `handler` instead of `context`
#     5-Mar-2010 (CT) `_etype_man_entries` corrected
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV.Base
import _GTW._NAV._E_Type.Admin

from   _TFL._Meta.Once_Property import Once_Property

from   itertools import chain as ichain, repeat as irepeat

class Site_Admin (GTW.NAV.Dir) :
    """Model an admin page for a GTW site."""

    Page            = GTW.NAV.E_Type.Admin
    template        = "site_admin"

    def __init__ (self, src_dir, parent, ** kw) :
        etypes         = kw.pop ("etypes", [])
        self.top.Admin = self
        self.__super.__init__ (src_dir, parent, ** kw)
        self.add_entries (self._etype_man_entries ())
        self.add_entries (etypes)
    # end def __init__

    def _etype_man_entries (self) :
        for man in self.top.E_Types.itervalues () :
            m_kw  = man.admin_args
            title = m_kw.pop ("title", man.title)
            desc  = m_kw.pop ("desc", "%s: %s" % (self.desc, man.name))
            ETM   = m_kw.pop ("ETM", man.ETM)
            Type  = m_kw.pop ("Type", self.Page)
            d     = dict \
                ( name      = man.name
                , title     = title
                , desc      = desc
                , ETM       = ETM
                , kind_name = man.kind_name
                , Type      = Type
                , ** m_kw
                )
            yield d
    # end def _etype_man_entries

    if 1 :
        ### if we want to display a site-admin specific page (and not
        ### just the page of the first child [a E_Type_Admin]), we'll
        ### need to bypass `_Dir_.rendered`
        def rendered (self, handler, template = None) :
            return GTW.NAV._Site_Entity_.rendered (self, handler, template)
        # end def rendered

# end class Site_Admin

if __name__ != "__main__":
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Admin
