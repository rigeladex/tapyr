# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    TGL.TKT.GTK.Dialog
#
# Purpose
#    Wrapper for the GTK widget Dialog
#
# Revision Dates
#    22-May-2005 (MG) Automated creation
#     3-Jun-2005 (MG) Creation continued
#    28-Jul-2005 (MG) Missing import of `TGL.TKT.GTK.Entry` added,
#                     `Dialog.run` fixed
#    03-Jan-2006 (MG) `Invisible_Entry`, `Invisible_String_Dialog` and
#                     `ask_invisible_string` added
#    03-Jan-2006 (MG) Emit `RESPONSE_OK` if`the `Activate` signal is emitted
#                     by the entry
#    ««revision-date»»···
#--

### todo:
### - ask_list_element
### - ask_list_element_combo
### - ask_list_element_spinner
###
### - ask_open_file_name
### - ask_save_file_name
### - ask_dir_name
### - ask_open_dir_name
### - ask_save_dir_name

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Window
import _TGL._TKT._GTK.Constants
import _TGL._TKT._GTK.H_Box
import _TGL._TKT._GTK.Entry
import _TGL._TKT._GTK.Label

class Dialog (GTK.Window) :
    """Wrapper for the GTK widget Dialog"""

    GTK_Class        = GTK.gtk.Dialog
    __gtk_properties = \
        ( GTK.SG_Property         ("has_separator")
        ,
        )
    _wtk_delegation = GTK.Delegation \
       ( GTK.Delegator ("run")
       )

    vbox = property (lambda s : s.wtk_object.vbox)

# end class Dialog

class _Input_Dialog_ (Dialog) :
    """A Dialog width provides one entry widget."""

    def __init__ ( self
                 , parent  = None
                 , title   = None
                 , prompt  = ""
                 , default = None
                 , name    = None
                 , AC      = None
                 ) :
        self.__super.__init__ \
            ( title   = title, parent = parent, AC = AC
            , buttons = ( "gtk-ok",     GTK.RESPONSE_OK
                        , "gtk-cancel", GTK.RESPONSE_CANCEL
                        )
            )
        TNS = self.TNS
        self.box    = TNS.H_Box                     (AC = AC)
        self.prompt = TNS.Label                     (prompt, AC = AC)
        self.entry  = getattr (TNS, self.entry_cls) (AC = AC)
        self.vbox.pack_start              (self.box.exposed_widget.wtk_object)
        self.box.pack                     (self.prompt, expand = False)
        self.box.pack                     (self.entry,  expand = True)
        self.box.  show                   ()
        self.prompt.show                  ()
        self.entry.show                   ()
        self.entry.bind_add (self.TNS.Signal.Activate, self.respond)
        self.wtk_object.set_default_response (GTK.RESPONSE_OK)
    # end def __init__

    def respond (self, event = None) :
        self.wtk_object.response (GTK.RESPONSE_OK)
    # end def respond

    def run (self) :
        value = None
        while 1 :
            response = self.wtk_object.run ()
            if (  (response == GTK.gtk.RESPONSE_CANCEL)
               or (response == GTK.gtk.RESPONSE_DELETE_EVENT)
               ) :
                break
            value = self.get ()
            if value is not None :
                break
        self.destroy ()
        return value
    # end def run

    def get (self) :
        try :
            return self.convert (self.entry.get ())
        except Exception, exc :
            msg         = self.error_message + "\n\n" + str (exc)
            self._error = msg
            if hasattr (self.TNS, "Error_Dialog") :
                e = self.TNS.Error_Dialog \
                    ("Illegal Value for %s" % self.name, msg, AC = self.AC)
                e.run     ()
                e.destroy ()
            else :
                print "Illegal Value\n" + msg
            return None
    # end def get

# end class _Input_Dialog_

class String_Dialog (_Input_Dialog_) :

    entry_cls     = "Entry"
    convert       = str
    error_message = ""

# end class String_Dialog

class Int_Dialog (String_Dialog) :

    convert       = int
    error_message = "Not an integer."

# end class Int_Dialog

class Float_Dialog (String_Dialog) :

    convert       = float
    error_message = "Not a floating point value."

# end class Float_Dialog

class Invisible_Entry (GTK.Entry) :
    """An entry with an `*` as invisible character"""

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.visibility = False
    # end def __init__

# end class Invisible_Entry

GTK.Invisible_Entry = Invisible_Entry ### in this case `_Export` does not work

class Invisible_String_Dialog (String_Dialog) :

    entry_cls = "Invisible_Entry"

# end class Invisible_String_Dialog

def ask_string (* args, ** kw) :
    d = String_Dialog (* args, ** kw)
    return d.run ()
# end def ask_string

def ask_invisible_string (* args, ** kw) :
    d = Invisible_String_Dialog (* args, ** kw)
    return d.run ()
# end def ask_invisible_string

def ask_integer (* args, ** kw) :
    d = Int_Dialog (* args, ** kw)
    return d.run ()
# end def ask_integer

def ask_float (* args, ** kw) :
    d = Float_Dialog (* args, ** kw)
    return d.run ()
# end def ask_float

if __name__ != "__main__" :
    GTK._Export_Module ()
else :
    import _TGL._TKT._GTK.Combo_Box_Entry
    import _TGL._TKT._GTK.Entry
    import _TGL._TKT._GTK.Message_Dialog
    from _TGL import TGL
    from   _TGL._UI.App_Context   import App_Context
    AC  = App_Context     (TGL)

    w = Int_Dialog (title = "Test input", prompt = "A int", AC = AC)
    print w.run ()
### __END__ TGL.TKT.GTK.Dialog
