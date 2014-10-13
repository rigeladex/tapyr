# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.MOM.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.TOP.MOM.Field
#
# Purpose
#    Define classes for displaying E_Type attributes as fields
#
# Revision Dates
#    20-Aug-2014 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW                     import GTW
from   _MOM                     import MOM
from   _TFL                     import TFL

from   _MOM.import_MOM          import Q

import _MOM.Entity

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL._Meta.Property      import Alias_Property
from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import filtered_join

import _TFL._Meta.Object
import _TFL.Accessor

class M_Attr (TFL.Meta.Object.__class__) :
    """Metaclass for `Attr`"""

# end class M_Attr

class Attr (TFL.Meta.BaM (TFL.Meta.Object, metaclass = M_Attr)) :
    """Field describing an attribute."""

    def __init__ (self, aq) :
        self.aq = aq
    # end def __init__

    @Once_Property
    @getattr_safe
    def attr (self) :
        return self.aq._attr
    # end def attr

    @Once_Property
    @getattr_safe
    def attr_name (self) :
        return self.attr.name
    # end def attr_name

    @Once_Property
    @getattr_safe
    def css_class (self) :
        cc = self.css_classes
        return filtered_join  (" ", cc) if cc else ""
    # end def css_class

    @Once_Property
    @getattr_safe
    def css_classes (self) :
        result = []
        align  = getattr (self.attr, "css_align", None)
        if align :
            result.append ("-".join (("align", align)))
        return result
    # end def css_classes

    @property ### depends on currently selected language (I18N/L10N)
    @getattr_safe
    def description (self) :
        return _T (self.attr.description)
    # end def description

    @Once_Property
    @getattr_safe
    def name (self) :
        return self.aq._full_name
    # end def name

    @property ### depends on currently selected language (I18N/L10N)
    @getattr_safe
    def ui_name (self) :
        ### put `zero-width-space` before `/`
        return self.aq._ui_name_T.replace ("/", "\u200b/")
    # end def ui_name

    def as_html (self, o, v) :
        return v
    # end def as_thml

    def value (self, o) :
        if isinstance (o, MOM.Id_Entity) :
            o = o.FO
        result = getattr (o, self.name)
        return result
    # end def value

    def __getattr__ (self, name) :
        return getattr (self.attr, name)
    # end def __getattr__

# end class Attr

class Created (Attr) :
    """Field providing the creation date (without time) of an entity."""

    attr_name         = "created"

    @property ### depends on currently selected language (I18N/L10N)
    @getattr_safe
    def description (self) :
        return _T ("Date of creation.")
    # end def description

    @property ### depends on currently selected language (I18N/L10N)
    @getattr_safe
    def ui_name (self) :
        return _T ("Created")
    # end def ui_name

    def value (self, o) :
        return self.__super.value (o).split (" ") [0]
    # end def value

# end class Created

class M_Link (Attr.__class__) :
    """Metaclass for `Link`"""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "Link" and not name.endswith ("_Set") :
            cls.Set = cls.__class__ \
                ( "_".join ((name, "Set"))
                , (cls, Link_Set)
                , dict (__module__ = cls.__module__)
                )
    # end def __init__

# end class M_Link

class Link (TFL.Meta.BaM (Attr, metaclass = M_Link)) :
    """Field that is displayed as HTML link"""

    protocol = None

    @Once_Property
    @getattr_safe
    def css_classes (self) :
        return self.__super.css_classes + ["link"]
    # end def css_classes

    @Once_Property
    @getattr_safe
    def title (self) :
        return None
    # end def title

    def as_html (self, o, v) :
        href      = self._as_html_href  (o, v)
        value     = self._as_html_value (o, v)
        title     = self._as_html_title (o, href, value)
        proto     = self.protocol
        fmt_head  = "<a "
        fmt_href  = "".join \
            ( ( "href=\""
              , "%(proto)s:" if proto and ":" not in href else ""
              , "%(href)s\""
              )
            )
        fmt_tail  = ">%(value)s</a>"
        fmt_title = " title=\"%(title)s\"" if title else ""
        fmt       = "".join ((fmt_head, fmt_href, fmt_title, fmt_tail))
        return fmt % vars ()
    # end def as_html

    def _as_html_href (self, o, v) :
        return v
    # end def _as_html_href

    def _as_html_title (self, o, href, value) :
        return self.title
    # end def _as_html_title

    def _as_html_value (self, o, v) :
        return v
    # end def _as_html_value

# end class Link

class Link_Set (Link) :
    """Field comprising a set of `Link` values."""

    def as_html (self, o, v) :
        def _gen (self, o, v) :
            o_set  = getattr (o.obj, self.name)
            as_html = self.__super.as_html
            for elem in o_set :
                oo  = TFL.Record (obj = TFL.Record (** {self.name : elem}))
                vv  = str (elem.FO)
                yield vv, as_html (oo, vv)
        return "\n".join (html for vv, html in sorted (_gen (self, o, v)))
    # end def as_html

# end class Link_Set

class Account (Link) :
    """Field showing the person an `Account` instance."""

    protocol = "mailto"

    def _as_html_href (self, o, v) :
        account = getattr (o.obj, self.name)
        return account.name
    # end def _as_html_href

    def _as_html_title (self, o, href, value) :
        return "%s %s" % (_T ("Email"), value)
    # end def _as_html_title

    def _as_html_value (self, o, v) :
        account = getattr (o.obj, self.name)
        return account.FO.person if account.person else account.name
    # end def _as_html_value

# end class Account

class Account_Name (Link) :
    """Field showing the name of an `Account` instance."""

    protocol = "mailto"

    def _as_html_href (self, o, v) :
        account = getattr (o.obj, self.name)
        return account.name
    # end def _as_html_href

    def _as_html_title (self, o, href, value) :
        return "%s %s" % (_T ("Email"), value)
    # end def _as_html_title

    def _as_html_value (self, o, v) :
        account = getattr (o.obj, self.name)
        return account.name
    # end def _as_html_value

# end class Account_Name

class Email (Link) :
    """Field showing an `Email` instance."""

    protocol = "mailto"

    def _as_html_title (self, o, href, value) :
        return _T ("Send email to %s") % (value, )
    # end def _as_html_title

# end class Email

class Phone (Link) :
    """Field showing a `Phone` instance."""

    protocol = "tel"

    def _as_html_href (self, o, v) :
        phone = getattr (o.obj, self.name)
        return "+%s %s %s" % tuple (phone.epk_raw [:-1])
    # end def _as_html_href

    def _as_html_title (self, o, href, value) :
        return _T ("Make phone call to %s") % (value, )
    # end def _as_html_title

# end class Phone

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export_Module ()
### __END__ GTW.RST.TOP.MOM.Field
