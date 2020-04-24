# -*- coding: utf-8 -*-
# Copyright (C) 2004-2016 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    PMA.Mailcap
#
# Purpose
#    Model mailcap information
#
# Revision Dates
#     4-Sep-2004 (CT) Creation
#     6-Sep-2004 (CT) `needsterminal` considered in `Mailcap_Entry.system`
#    22-Feb-2013 (CT)  Use `TFL.Undef ()` not `object ()`
#    29-Oct-2015 (CT) Improve Python 3 compatibility
#    27-Dec-2016 (CT) Add `encoding` to `as_text`
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib
import _TFL._Meta.Object
import _TFL.Undef

from   _TFL.predicate          import *
from   _TFL.pyk                import pyk
from   _TFL                    import sos

_undefined = TFL.Undef ()

class Mailcap_Entry (TFL.Meta.Object) :
    """Model a single mailcap entry for a specific mime type"""

    def __init__ (self, mime_type, cap_dict) :
        self.mime_type     = mime_type
        self.cap_dict      = cap_dict
        self.copiousoutput = "copiousoutput" in cap_dict
        self.needsterminal = "needsterminal" in cap_dict
        self.test          = cap_dict.get ("test")
    # end def __init__

    def applicable (self, filename = "/dev/null", plist = []) :
        if self.test :
            test_cmd = self.command ("test", filename, plist)
            return sos.system (test_cmd) == 0
        return True
    # end def applicable

    def as_text (self, key, filename = "", plist = [], encoding = None) :
        pipe   = sos.popen  (self.command (key, filename, plist), "r")
        body   = pipe.read  ()
        pipe.close ()
        if encoding is not None :
            body = pyk.decoded (body, encoding)
        result = body.split ("\n")
        return result
    # end def as_text

    def command (self, key, filename = "", plist = []) :
        return Lib.mailcap.subst \
            (self.cap_dict [key], self.mime_type, filename, plist)
    # end def command

    def system (self, key = "view", filename = "/dev/null", plist = []) :
        cmd = self.command (key, filename, plist)
        if self.needsterminal :
            cmd = "xterm -e %s" % cmd
        return sos.system (cmd)
    # end def system

    def __contains__ (self, key) :
        return key in self.cap_dict
    # end def __contains__

    def __getattr__ (self, name) :
        if name in self.cap_dict :
            return self.cap_dict [name]
        raise AttributeError (name)
    # end def __getattr__

    def __getitem__ (self, key) :
        return self.cap_dict [key]
    # end def __getitem__

# end class Mailcap_Entry

class Mailcap_Type (TFL.Meta.Object) :
    """Model all mailcap entries for a specific mime type"""

    def __init__ (self, mime_type, cap_dict_list) :
        self.mime_type     = mime_type
        self.action_dict   = dict \
            ( { "print"    : []}
            , edit         = []
            , int_view     = []
            , view         = []
            )
        self.entry_list    = []
        self._setup (mime_type, cap_dict_list)
    # end def __init__

    def as_text (self, filename, plist = [], encoding = None) :
        for entry in self.action_dict.get ("int_view", []) :
            if entry.applicable (filename, plist) :
                return entry.as_text ("view", filename, plist, encoding)
    # end def as_text

    def system (self, key, filename, plist = []) :
        for entry in self.action_dict.get (key, []) :
            if entry.applicable (filename, plist) :
                return entry.system (key, filename, plist)
    # end def system

    def _setup (self, mime_type, cap_dict_list) :
        action_dict = self.action_dict
        entry_list  = self.entry_list
        action_dict ["ext_view"] = action_dict ["view"]
        add = entry_list.append
        for entry in cap_dict_list :
            add (Mailcap_Entry (mime_type, entry))
        for entry in entry_list :
            for key in "edit", "print", "view":
                if key in entry :
                    action_dict [key].append (entry)
        for entry in dusort \
                ( entry_list
                , lambda e
                : (bool (e.test), e.needsterminal, not e.copiousoutput)
                ) :
            if (   ("view" in entry)
               and (not entry.needsterminal)
               and entry.copiousoutput
               ) :
                action_dict ["int_view"].append (entry)
    # end def _setup

    def __contains__ (self, key) :
        return key in self.action_dict
    # end def __contains__

# end class Mailcap_Type

class _Mailcap_ (TFL.Meta.Object) :
    """Model mailcap database of a Unix system"""

    def __init__ (self, caps = None) :
        if caps is None :
            caps = Lib.mailcap.getcaps ()
        self.caps = caps
        self.mct  = {}
    # end def __init__

    def mime_type (self, name) :
        mct    = self.mct
        result = mct.get (name)
        if name not in mct :
            if name in self.caps :
                result = Mailcap_Type (name, self.caps [name])
            else :
                main_type, sub_type = name.split ("/")
                if sub_type != "*" :
                    result = self.mime_type ("/".join ((main_type, "*")))
            mct [name] = result
        return result
    # end def mime_type

    def __getitem__ (self, key) :
        return self.mime_type (key)
    # end def __getitem__

# end class _Mailcap_

Mailcap = _Mailcap_ ()

if __name__ != "__main__" :
    PMA._Export ("*", "Mailcap")
### __END__ PMA.Mailcap
