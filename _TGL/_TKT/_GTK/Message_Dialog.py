# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.Message_Dialog
#
# Purpose
#    Wrapper for the GTK widget MessageDialog
#
# Revision Dates
#    03-Jun-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Dialog

class Message_Dialog (GTK.Dialog.Dialog) :
    """Wrapper for the GTK widget MessageDialog"""

    GTK_Class        = GTK.gtk.MessageDialog

    __gtk_properties = \
        ( GTK.Property            ("buttons", get = None)
        , GTK.Property            ("message_type")
        )

    default_type     = GTK.MESSAGE_INFO
    default_buttons  = GTK.gtk.BUTTONS_YES_NO
    default_response = None

    def __init__ ( self
                 , title    = None
                 , message  = None
                 , type     = None
                 , parent   = None
                 , buttons  = None
                 , AC       = None
                 ) :
        if type is None :
            type    = self.default_type
        if buttons is None :
            buttons = self.default_buttons
        self.__super.__init__ \
            ( parent         = parent
            , type           = type
            , buttons        = buttons
            , message_format = message
            , AC             = AC
            )
        if title :
            self.title = title
        if self.default_response is not None :
            self.wtk_object.set_default_response (self.default_response)
    # end def __init__

# end class Message_Dialog

class Info_Dialog (Message_Dialog) :
    """Information message dialog"""

    default_type    = GTK.MESSAGE_INFO
    default_buttons = GTK.gtk.BUTTONS_OK

# end class Info_Dialog

class Warning_Dialog (Info_Dialog) :
    """Warning  message dialog"""

    default_type    = GTK.MESSAGE_WARNING

# end class Warning_Dialog

class Error_Dialog (Info_Dialog) :
    """Error message dialog"""

    default_type    = GTK.MESSAGE_ERROR

# end class Error_Dialog

class Question_Dialog (Message_Dialog) :
    """A dialog with asks a question with the Yes/No nbuttons"""

    default_type    = GTK.MESSAGE_QUESTION
    default_buttons = GTK.gtk.BUTTONS_YES_NO
    buttons         = ()

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        buttons = kw.get ("buttons", self.default_buttons)
        if buttons is GTK.gtk.BUTTONS_NONE and self.buttons :
            self.wtk_object.add_buttons (* self.buttons)
    # end def __init__

# end class Question_Dialog

class OK_Cancel_Question (Question_Dialog) :
    """A question dialog with the ok/cancel buttons"""

    default_buttons = GTK.gtk.BUTTONS_OK_CANCEL

# end class OK_Cancel_Question

class OK_Cancel_Question (Question_Dialog) :
    """A question dialog with the ok/cancel buttons"""

    default_buttons = GTK.gtk.BUTTONS_OK_CANCEL

# end class OK_Cancel_Question

class Yes_No_Question (Question_Dialog) :
    """A question dialog with the yes/no buttons, default is yes"""

    default_response = GTK.RESPONSE_YES

# end class Yes_No_Question


class Yes_No_Cancel_Question (Question_Dialog) :
    """A question dialog with the yes/no/cancel buttons"""

    default_buttons = GTK.gtk.BUTTONS_NONE
    buttons         = \
        ( "gtk-yes",    GTK.RESPONSE_YES
        , "gtk-no",     GTK.RESPONSE_NO
        , "gtk-cancel", GTK.RESPONSE_CANCEL
        )

# end class Yes_No_Cancel_Question

class Cancel_Retry_Question (Yes_No_Cancel_Question) :
    """A question dialog with the yes/no/cancel buttons"""

    buttons         = \
        ("gtk-redo", GTK.RESPONSE_APPLY, "gtk-cancel", GTK.RESPONSE_CANCEL)

# end class Cancel_Retry_Question

if __name__ != "__main__" :
    GTK._Export ("*")
else :
    from _TGL import TGL
    from   _TGL._UI.App_Context   import App_Context
    AC  = App_Context     (TGL)

    for d in ( Info_Dialog, Warning_Dialog, Error_Dialog
             , Question_Dialog
             , OK_Cancel_Question, Yes_No_Question
             , Yes_No_Cancel_Question, Cancel_Retry_Question
             ) :
        w = d            (title = "Test input", message = d.__name__, AC = AC)
        w.wtk_object.run ()

### __END__ TGL.TKT.GTK.Message_Dialog
