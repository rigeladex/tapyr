# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2008 Mag. Christian Tanzer. All rights reserved
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
#    CTK_Dialog
#
# Purpose
#    Dialog classes based on CT_TK
#
# Revision Dates
#    15-Feb-1999 (CT) Creation
#    16-Feb-1999 (CT) `grab_set' protected by `try'
#    22-Oct-1999 (CT) `Combobox_Dialog' added
#     1-Nov-1999 (CT) `Search_Dialog' added
#     2-Nov-1999 (CT) Regexp options added to `Search_Dialog'
#     2-Nov-1999 (CT) Use `History_Spinner' for `Search_Dialog.search_entry'
#     9-Nov-1999 (CT) Parameter `width' removed from calls to `Buttongrid'
#    18-Nov-1999 (CT) `List_Dialog_': bind `<Double-ButtonPress-1>' to
#                     `_ld_ok' instead of `ok' (otherwise the standard TK
#                     binding gets called after the window was laready
#                     destroyed)
#    23-Nov-1999 (CT) `Search_Dialog.search': return after showing
#                     `Regexp error' message box (to avoid second message box
#                     `Unsuccessful search')
#     7-Mar-2000 (CT) `List_Entry_Dialog_' factored
#     7-Mar-2000 (CT) `list_s' added to list dialogs to allow non-string
#                     lists to be handled gracefully
#    13-Mar-2000 (CT) Changed from button `ignorecase' to `case_sensitive'
#                     (to change default to case-insensitive matching)
#    26-Aug-2000 (RM) Added num_opt_val method to Listdropspinner_Dialog to
#                     override size of dialog
#    28-Aug-2000 (RM) num_opt_val removed from Listdropspinner_Dialog
#    13-Dec-2000 (CT) `ask_open_file_name' and `ask_save_file_name' added
#    20-Dec-2000 (CT) `ask_dir_name' added
#    22-Feb-2001 (CT) Use `raise' instead of `raise exc' for re-raise
#    14-May-2001 (CT) `prompt' factored into `Dialog.__init__'
#    14-May-2001 (CT) `name' and `prompt' added to `ask_' functions for
#                     filenames and directories
#    16-May-2001 (CT) Allow `init_val' for file and directory dialogs, too
#    14-Dec-2001 (CT) `_ask_file_name` changed to refuse non-ascii filenames
#    18-Feb-2002 (CT) `Search_Dialog` changed to bind `self.destroy_cmd`
#                     instead of `self.cancel`
#    22-Feb-2002 (MG) `Ancestor*` added and used
#    22-Feb-2002 (MG) `*_Entry` factored
#    22-Feb-2002 (MG) `Many_Dialog`, `*Field`, and `ask_many` added
#    22-Feb-2002 (MG) `Dialog`: `default_*` added
#     4-Nov-2002 (CT) Esthetics
#     4-Nov-2002 (CT) `validate` changed from `return self.result`
#                     to `return self.result not in ("", None)`
#     7-Nov-2002 (CT) Fixed bug introduced on `4-Nov-2002` in
#                     `String_Entry.convert`
#    11-Jun-2003 (CT) s/!= None/is not None/
#    14-Jul-2003 (GWA) `Listdropspinner_Entry`, `Listdropspinner_Field` added
#    15-May-2004 (GWA) `_Field_Entry_` may customize also the `state`
#     7-Jun-2004 (GWA) `Listdropspinner_Field` may customize also `editable`
#    11-Jun-2004 (GKH) deprecation warning removed [10140]
#    28-Jun-2004 (CT)  `ask_open_dir_name` and `ask_save_dir_name` added
#    28-Jun-2004 (CT)  `_ask_file` factored from `_ask_file_name`
#     7-Jul-2004 (CED) `Boolean_Entry`, `ask_yes_no` added
#    13-Oct-2004 (MG)  `Many_Dialog.validate`: set `self.errors` to any empty
#                      list
#    12-Jul-2005 (PGO) `label_ok` and `label_cancel` added
#    10-Apr-2006 (CED) Workaround for Tkinter MacOS bug added
#    02-Aug-2007 (CED) Coding guidelines
#    13-Sep-2007 (MZO) [24618] inheritance fixed
#     7-Nov-2007 (CT)  Moved into package _TFL._TKT._Tk
#     1-Feb-2008 (MG)  `Change_Record.__nonzero__` factored to `Record`
#    ««revision-date»»···
#--

from   _TFL._TKT._Tk.CT_TK  import *
from   _TFL.Filename        import *
from   _TFL.Record          import Record
from   _TFL.d_dict          import d_dict

class Dialog (CT_TK_mixin, C_Toplevel) :
    """Base class for dialogs"""

    Ancestor        = __Ancestor = C_Toplevel

    widget_class    = "Dialog"
    default_width   = 200
    default_height  = 250
    label_ok        = "OK"
    label_cancel    = "Cancel"

    def __init__ ( self, master
                 , name             = None
                 , title            = ""
                 , prompt           = None
                 ) :
        self.__Ancestor.__init__     \
            ( self, master
            , name   = name
            , class_ = self.widget_class
            )
        master       = self.master ### get default if master was None
        self.prompt  = prompt
        self.result  = None
        if title :
            self.title (title)

        body = Frame                 (self)
        body.pack                    ( padx   = 5
                                     , pady   = 5
                                     , expand = YES
                                     , fill   = BOTH
                                     )
        self.initial_focus           = self._setup_body (body) or self
        self._setup_buttonbox        ()
        self._setup_bindings         ()
        try :
            self.grab_set            ()
        except (SystemExit, KeyboardInterrupt), exc :
            raise
        except :
            ### TCL throws an exception if another application has a grab
            ### we ignore this
            pass
        self.protocol                ("WM_DELETE_WINDOW", self.cancel)
        wd = self.num_opt_val        ("width",  self.default_width)
        ht = self.num_opt_val        ("height", self.default_height)
        self.geometry                ( "%dx%d+%d+%d"
                                     % ( wd, ht
                                       , master.winfo_rootx ()
                                       + (master.winfo_width  () - wd) // 2
                                       , master.winfo_rooty ()
                                       + (master.winfo_height () - ht) // 2
                                       )
                                     )
        self.initial_focus.focus_set ()
        self.wait_window             (self)
    # end def __init__

    def _setup_body (self, master) :
        """Create body of dialog. Result should be the widget to get the
           initial focus.

           This must be overridden by descendent classes.
        """
        pass
    # end def _setup_body

    button_cols = 2
    button_side = BOTTOM

    def _setup_buttonbox (self) :
        """Sets up a standard button box. May be overridden by descendent
           classes.
        """
        self.button_box = Buttongrid ( self
                                    , name    = "button_box"
                                    , columns = self.button_cols
                                    , padx    = 2
                                    , pady    = 1
                                    , sticky  = W+E
                                    )
        self.button_box.pack        (side = self.button_side)
        self._add_buttons           ()
    # end def _setup_buttonbox

    def _add_buttons (self) :
        self.button_box.add (self.label_ok, command=self.ok, default=ACTIVE)
        self.button_box.add (self.label_cancel, command=self.cancel)
    # end def _add_buttons

    def _setup_bindings (self) :
        """Setup standard key-bindings. May be overridden by descendent
           classes.
        """
        self.bind ("<Return>", self.ok)
        self.bind ("<Escape>", self.cancel)
    # end def _setup_bindings

    def ok (self, event = None):
        if not self.validate  () :
            self.initial_focus.focus_set () # put focus back
            return
        self.withdraw         ()
        self.update_idletasks ()
        self.apply            ()
        self.cancel           ()
    # end def ok

    def cancel(self, event = None):
        self.master.focus_set () # put focus back to the parent window
        self.destroy          ()
    # end def cancel

    def validate (self):
        return 1 # override
    # end def validate

    def apply (self):
        pass # override
    # end def apply

# end class Dialog

class _Entry_Mixin_ :
    """Provides some commen functions used by all entry."""

    _error = None

    def get (self, error_function = None) :
        try :
            return self.convert ()
        except Exception, exc :
            msg         = self.error_message + "\n\n" + str (exc)
            self._error = msg
            if error_function :
                error_function ("Illegal Value for %s" % self.name, msg)
            else :
                print "Illegal Value\n" + msg
            return None
    # end def get

# end class _Entry_Mixin_

class String_Entry (_Entry_Mixin_, C_Entry):
    """Allows any string as input value."""

    Ancestor      = __Ancestor = C_Entry
    error_message =  ""

    def convert (self) :
        return self.entry.get ()
    # end def convert

# end class String_Entry

class Int_Entry (String_Entry) :
    """Restricts the allowed input values to an INTEGER."""

    error_message = "Not an integer."

    def convert (self) :
        return int (self.entry.get ())
    # end def convert

# end class Int_Entry

class Float_Entry (String_Entry) :
    """Restricts the allowed input values to an FLOAT."""

    Ancestor      = __Ancestor = String_Entry

    error_message = "Not a floating point value."

    def convert (self) :
        r = self.__Ancestor.convert (self)
        if r :
            return float (r)
        else :
            return r
    # end def convert

# end class Float_Entry

class Boolean_Entry (_Entry_Mixin_, C_Checkbutton_Entry) :
    """A Yes/No entry"""

    Ancestor      = __Ancestor = C_Checkbutton_Entry
    error_message = ""

    def convert (self) :
        return eval (self.__Ancestor.get (self) or "0")
    # end def convert

# end class Boolean_Entry

class _Field_Entry_Mixin_ :

    _error   = None

    def get (self, show_error = None) :
        return self.CTK_Widget.get (self)
    # end def get

# end class _Field_Entry_Mixin_

class Listdrop_Entry (_Field_Entry_Mixin_, Listdropentry) :

    Ancestor = __Ancestor = CTK_Widget = Listdropentry

# end class Listdrop_Entry

class Listdrop_Entry_Extended (_Field_Entry_Mixin_, Listdropentry_Extended) :

    Ancestor = __Ancestor = CTK_Widget = Listdropentry_Extended

# end class Listdrop_Entry_Extended

class Listdropspinner_Entry (_Field_Entry_Mixin_, Listdropspinner) :

    Ancestor = __Ancestor = CTK_Widget = Listdropspinner

# end class Listdropspinner_Entry


class Entry_Dialog (Dialog) :
    """Dialog with a single entry field."""

    Ancestor     = __Ancestor = Dialog

    entry_widget = String_Entry
    widget_class = "Entry_Dialog"

    def __init__ ( self, master = None
                 , name             = None
                 , title            = ""
                 , prompt           = None
                 , init_val         = None
                 ) :
        self.init_val  = init_val
        self.__Ancestor.__init__ (self, master, name, title, prompt)
    # end def __init__

    def _setup_body (self, master) :
        self.entry = self.entry_widget \
                        ( master
                        , name          = "dialog_entry"
                        , label         = self.prompt
                        , default       = self.init_val
                        )
        self.entry.pack ()
        return self.entry
    # end def _setup_body

    def validate (self) :
        self.result = self.entry.get (self.show_error)
        return self.result not in ("", None)
    # end def validate

# end class Entry_Dialog

class Boolean_Entry_Dialog (Entry_Dialog) :
    """Query dialog for a single boolewn value."""

    entry_widget = Boolean_Entry

# end class Boolean_Entry_Dialog

class Int_Entry_Dialog (Entry_Dialog) :
    """Query dialog for a single integer value."""

    entry_widget = Int_Entry

# end class Int_Entry_Dialog

class Float_Entry_Dialog (Entry_Dialog) :
    """Query dialog for a single float value."""

    entry_widget = Float_Entry

# end class Float_Entry_Dialog

class List_Dialog_ (Dialog) :
    """Root class for dialog with a listbox."""

    Ancestor     = __Ancestor = Dialog

    def __init__ ( self
                 , master           = None
                 , name             = None
                 , title            = ""
                 , prompt           = None
                 , list             = ()
                 ) :
        self.list      = list
        self.list_s    = map (str, self.list)
        self.__Ancestor.__init__ (self, master, name, title, prompt)
    # end def __init__

    def _setup_body (self, master) :
        self.listbox = self.Listbox (master, self.list_s, name = "listbox")
        if self.prompt :
            self.label = Label  (master, text = self.prompt)
            self.label.pack     (side = TOP, anchor = W)
        self.listbox.pack       (side = TOP, expand = YES, fill = BOTH)
        if self.list :
            self.listbox.select (0)
        return self.listbox
    # end def _setup_body

    def _setup_bindings (self) :
        Dialog._setup_bindings  (self)
        self.bind               ("<Double-ButtonPress-1>", self._ld_ok)
    # end def _setup_bindings

    def _ld_ok (self, event = None) :
        self.listbox.mouse_select (event)
        self.ok                   ()
        return "break"
    # end def _ld_ok

# end class List_Dialog_

class Listbox_Dialog (List_Dialog_) :
    """Dialog with a scrolled listbox."""

    widget_class = "Listbox_Dialog"
    Listbox      = Scrolled_Listbox

    def validate (self) :
        i = self.listbox.index ()
        if i is not None :
            self.result = self.list [i]
            return 1
        return 0
    # end def validate

# end class Listbox_Dialog

class List_Entry_Dialog_ (List_Dialog_) :

    def validate (self) :
        self.result = self.listbox.entry.get ()
        try :
            i           = self.list_s.index (self.result)
            self.result = self.list [i]
        except ValueError :
            pass
        return self.result is not None
    # end def validate

# end class List_Entry_Dialog_

class Combobox_Dialog (List_Entry_Dialog_) :
    """Dialog with a combobox."""

    widget_class = "Combobox_Dialog"
    Listbox      = Combobox

###    def validate (self) :
###        self.result = self.listbox.entry.get ()
###        return self.result is not None
###    # end def validate

# end class Combobox_Dialog

class Listdropspinner_Dialog (List_Entry_Dialog_) :
    """Dialog with a listdropspinner."""

    widget_class    = "Listdropspinner_Dialog"
    Listbox         = Listdropspinner

    _setup_bindings = Dialog._setup_bindings

# end class Listdropspinner_Dialog

class Search_Dialog (BB_Toplevel) :
    """Search dialog"""

    Ancestor        = __Ancestor = BB_Toplevel

    widget_class    = "Search_Dialog"

    _search_history = []

    def __init__ \
        ( self, master, name = None, help = None, close_cmd = None
        , destroy_cmd = None, title = None
        ) :
        """`master' is expceted to provide the functions `find (pattern)' and
           `find_prev ()'.
        """
        self.__Ancestor.__init__ \
            ( self, master
            , name            = name
            , class_          = self.widget_class
            , help            = help
            , close_cmd       = close_cmd   or self.withdraw
            , destroy_cmd     = destroy_cmd or self.cancel
            , title           = title
            , button_box_side = RIGHT
            , button_cols     = 1
            )
        self._setup_dialog   ()
        self._setup_buttons  ()
        self._setup_bindings ()
    # end def __init__

    def _setup_dialog (self) :
        body = self.body = C_Frame            (self)
        self.body.pack                        ( padx   = 5
                                              , pady   = 5
                                              , expand = YES
                                              , fill   = BOTH
                                              , side   = LEFT
                                              )
        self.search_entry = History_Spinner   ( body, self._search_history
                                              , name          = "search_entry"
                                              , label         = "Search for"
                                              , labeljustify  = LEFT
                                              , labelanchor   = W
                                              , labelpos      = TOP
                                              )
        self.search_entry.pack                ( expand = YES
                                              , fill   = X
                                              )
        self._re_button = C_Checkbutton_Entry ( body
                                              , name   = "regexp"
                                              , label  = "regular expression"
                                              )
        self._re_button.pack                  (expand  = YES, fill = X)
        self._re_button.entry.configure       (command = self._do_re)
        self._re_buttons =                    []
        self._make_re_button ("case_sensitive", "match case sensitive")
        self._make_re_button ("multiline",      "'^' matches after newline")
        self._make_re_button ("dotall",         "'.' matches newline")
        self._make_re_button ("verbose",        "ignore whitespace in regexp")
        self._do_re          ()
    # end def _setup_dialog

    def _make_re_button (self, name, label) :
        n = "_" + name
        b = C_Checkbutton_Entry (self.body, name = name, label = label)
        setattr                 (self, n, b)
        b.pack                  (expand = NO, fill = X)
        self._re_buttons.append (b)
    # end def _make_re_button

    def _do_re (self) :
        if self._re_button.get () :
            map (lambda b : b.enable  (), self._re_buttons)
        else :
            map (lambda b : b.disable (), self._re_buttons)
    # end def _do_re

    def _setup_buttons (self) :
        self.button_box.add \
            ("Search",   before = "Close", command = self.search)
        self.button_box.add \
            ("Previous", before = "Close", command = self.search_prev)
    # end def _setup_buttons

    def _setup_bindings (self) :
        """Setup standard key-bindings. May be overridden by descendent
           classes.
        """
        self.bind ("<Return>", self.search)
        self.bind ("<Escape>", self.destroy_cmd)
    # end def _setup_bindings

    def cancel(self, event = None):
        self.master.focus_set () # put focus back to the parent window
        self.destroy          ()
    # end def cancel

    def search (self, event = None) :
        p = pat = self.search_entry.get ()
        if not pat :
            self.deiconify ()
            self.search_entry.focus_set ()
            return
        if self._re_button.get () :
            opt = 0
            if not self._case_sensitive.get () : opt = opt | re.IGNORECASE
            if     self._multiline.get      () : opt = opt | re.MULTILINE
            if     self._dotall.get         () : opt = opt | re.DOTALL
            if     self._verbose.get        () : opt = opt | re.VERBOSE
            try :
                p   = re.compile (pat, opt)
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                exc_typ, exc_val = sys.exc_info () [:2]
                self.body.show_error \
                    ( "Regexp error"
                    , "Invalid regular expression `%s'"":\n\n%s %s"
                    % (p, exc_typ, str (exc_val))
                    )
                return
        result = self.master.find (p)
        if result :
            self.master.popup ()
        else :
            self.body.show_warning ( "Unsuccessful search"
                                   , "Pattern `%s' not found" % pat
                                   )
    # end def search

    def search_prev (self, event = None) :
        self.master.find_prev ()
    # end def search_prev

    def popup (self, event = None) :
        self.deiconify                ()
        self.lift                     ()
        self.search_entry.focus_set   ()
    # end def popup

# end class Search_Dialog

class UndefinedParameter (StandardError) :

    pass

# end class UndefinedParameter

class _Field_Entry_ :
    """Models the specification of any entry for the `ask_main` feature."""

    ### must be redefined by descendents

    entry_widget  = None
    customize     = d_dict (default = None, state = NORMAL)

    with_label    = 1

    def __init__ (self, name, ** parameters) :
        assert self.entry_widget
        self.name      = name
        ### copy the default of the class to the instance
        self.customize = self.customize.copy ()
        for par_name, par_value in parameters.items () :
            if not self.customize.has_key (par_name) :
                raise UndefinedParameter, par_name
            self.customize [par_name] = par_value
    # end def __init__

    def widgets (self, master) :
        if self.with_label :
            label = Label (master, text = self.name)
        else :
            label = None
        return ( label, self.entry_widget
                           (master, name = self.name, ** self.customize)
               )
    # end def widgets

# end class _Field_Entry_

class Separator_Field (_Field_Entry_) :
    """A simple horizontal seperatur."""

    Ancestor     = __Ancestor = _Field_Entry_

    entry_widget = H_Separator
    customize    = d_dict ( text   = ""
                          , relief = entry_widget.default_relief
                          , height = entry_widget.default_size
                          )

    __count = 0

    def __init__ (self, text = None, ** parameters) :
        name = "_Sep_%d" % self.__count
        self._update_count ()
        parameters ["text"] = text
        self.__Ancestor.__init__ (self, name, ** parameters)
    # end def __init__

    def _update_count (self) :
        self.__class__.__count += 1
    # end def _update_count

    def widgets (self, master) :
        label = None
        dict  = self.customize.copy ()
        if self.customize ["text"] :
            entry_widget = Label
            del dict ["height"]
        else :
            entry_widget = H_Separator
            del dict ["text"]
        return ( label, entry_widget (master, name = self.name, ** dict))
    # end def widgets

# end class Separator_Field

class Text_Field (_Field_Entry_) :
    """Allows input of arbitrary text."""

    entry_widget = String_Entry

# end class Text_Field

class Int_Field (_Field_Entry_) :
    """Allow's the input of an INTEGER."""

    entry_widget   = Int_Entry

# end class Int_Field

class Float_Field (_Field_Entry_) :
    """Allow's the input of an FLOAT."""

    entry_widget = Float_Entry

# end class Float_Field

class Boolean_Field (_Field_Entry_) :
    """Allows only Yes/no input"""

    Ancestor      = __Ancestor = _Field_Entry_

    entry_widget  = Boolean_Entry
    customize     = d_dict (Ancestor.customize, default = 1)
# end class Boolean_Field

class Listdrop_Field (_Field_Entry_) :
    """Allows a selection of one entry out of a list."""

    Ancestor     = __Ancestor = _Field_Entry_

    entry_widget = Listdrop_Entry
    customize    = d_dict ( Ancestor.customize
                          , list = []
                          )

# end class Listdrop_Field

class Listdrop_Extended_Field (Listdrop_Field) :
    """Allows a selection of n entries out of a list."""

    Ancestor     = __Ancestor = Listdrop_Field

    entry_widget = Listdrop_Entry_Extended

# end class Listdrop_Extended_Field

class Listdropspinner_Field (_Field_Entry_) :
    """Allows a selection of one entry out of a list."""

    Ancestor     = __Ancestor = _Field_Entry_

    entry_widget = Listdropspinner_Entry
    customize    = d_dict ( Ancestor.customize
                          , list     = []
                          , editable = None
                          )

# end class Listdropspinner_Field

class Change_Record (Record) :
    """Adds a hidden feature to set if values if the `Record` have been
       changed.
    """

    def set_changes (self, changes) :
        self.__dict__ ["_changes"] = changes
    # end def set_changes

    def __len__ (self) : return self._changes

# end class Change_Record

class Many_Dialog (Dialog) :
    """Allows multiple inputs at one time represented in one dialog."""

    Ancestor      = __Ancestor = Dialog

    def __init__ (self
                 , master
                 , fields
                 , name          = None
                 , title         = None
                 , head          = None
                 , width         = 400
                 ) :
        self.default_width = width
        self.fields = tuple (fields)
        if head :
            self.fields = ( Separator_Field (head, relief = GROOVE),
                          ) + self.fields
        self.__Ancestor.__init__ (self, master, name, title)
    # end def __init__

    def _setup_body (self, master) :
        row         = 0
        self.entrys = []
        master.grid_columnconfigure ( 0, weight = 0)
        master.grid_columnconfigure ( 1, weight = 1)
        for field in self.fields :
            label, entry = field.widgets (master)
            if label :
                self.entrys.append ((field, entry))
                label.grid (row = row, column = 0, sticky = "w")
                entry.grid (row = row, column = 1, sticky = "ew")
            else :
                entry.grid ( row = row, column = 0, sticky = "ew"
                           , columnspan = 2
                           )
            row += 1
    # end def _setup_body

    def validate (self) :
        result  = Change_Record ()
        errors  = self.errors = []
        changes = 0
        for field, entry in self.entrys :
            value = entry.get (self.show_error)
            if entry._error :
                errors.append (entry)
            else :
                setattr (result, entry.name, value)
                if value != field.customize ["default"] :
                    changes += 1
        if errors :
            errors [0].focus_set ()
            return None
        else :
            self.result = result
            result.set_changes (changes)
            return result
    # end def validate

# end class Many_Dialog

def ask_yes_no (* args, ** kw) :
    r = Boolean_Entry_Dialog (* args, ** kw)
    return r.result
# end def ask_yes_no

def ask_string (* args, ** kw) :
    r = apply (Entry_Dialog, args, kw)
    return r.result
# end def ask_string

def ask_integer (* args, ** kw) :
    r = apply (Int_Entry_Dialog, args, kw)
    return r.result
# end def ask_integer

def ask_float (* args, ** kw) :
    r = apply (Float_Entry_Dialog, args, kw)
    return r.result
# end def ask_float

def ask_list_element (* args, ** kw) :
    r = apply (Listbox_Dialog, args, kw)
    return r.result
# end def ask_list_element

def ask_list_element_combo (* args, ** kw) :
    r = apply (Combobox_Dialog, args, kw)
    return r.result
# end def ask_list_element_combo

def ask_list_element_spinner (* args, ** kw) :
    r = apply (Listdropspinner_Dialog, args, kw)
    return r.result
# end def ask_list_element_spinner

def _ask_file (tk_fct, kw) :
    try :
        result = apply (root.tk.call, (tk_fct, ) + root._options (kw))
    except TclError, exc :
        ### XXX workaround for damned Tkinter Mac OS bug
        try :
            if not kw.get ("initialdir") :
                kw ["initialdir"]  = "."
            kw ["initialfile"] = ""
            result = apply (root.tk.call, (tk_fct, ) + root._options (kw))
        except TclError, exc :
            print exc
            result = None
    else :
        if result :
            try :
                result = result.encode ("ascii")
            except UnicodeError :
                tkMessageBox.showerror \
                    ( "Encoding error"
                    , "Non-ascii file names are currently not supported"
                    )
                return _ask_file (tk_fct, kw)
    return result
# end def _ask_file

def _ask_file_name (tk_fct, kw) :
    kw = kw.copy ()
    if kw.has_key ("init_val") :
        kw ["initialdir"], kw ["initialfile"] = sos.path.split (kw ["init_val"])
        del kw ["init_val"]
    return _ask_file (tk_fct, kw)
# end def _ask_file_name

def ask_open_file_name (name = None, prompt = None, ** kw) :
    return _ask_file_name ("tk_getOpenFile", kw)
# end def ask_open_file_name

def ask_save_file_name (name = None, prompt = None, ** kw) :
    return _ask_file_name ("tk_getSaveFile", kw)
# end def ask_save_file_name

def _ask_dir_name (mustexist, kw) :
    kw ["mustexist"] = mustexist
    if kw.has_key ("init_val") :
        kw ["initialdir"] = kw ["init_val"]
        del kw ["init_val"]
    for x in "defaultextension", "filetypes", "initialfile" :
        ### we allow these in `kw` and silently remove them to allow callers
        ### to use the same call for `ask_open_file_name/ask_open_dir_name`
        ### (the choice between `ask_open_file_name` and `ask_open_dir_name`
        ### might be done by some other code than the caller!)
        if x in kw :
            del kw [x]
    return _ask_file ("tk_chooseDirectory", kw)
# end def _ask_dir_name

def ask_open_dir_name (** kw) :
    return _ask_dir_name (True, kw)
# end def ask_open_dir_name

def ask_save_dir_name (** kw) :
    return _ask_dir_name (False, kw)
# end def ask_save_dir_name

ask_dir_name = ask_save_dir_name

def ask_many (*args, ** kw) :
    r = Many_Dialog (* args, ** kw)
    return r.result
# end def ask_many

def show_info (message, title = None, ** kw) :
    title = title or "Information"
    return tkMessageBox.showinfo (title, message, ** kw)
# end def show_info

if __name__ == "__main__":
    root.update ()
    #print ask_integer \
    # (root, title = "Spam", prompt = "Egg count", init_val = 12*12)
    #print ask_float \
    # (root, title = "Spam", prompt = "Egg weight\n(in tons)")
    #print ask_string       ( root, title = "Spam", prompt = "Egg label")
    #print ask_list_element ( root, title = "Spam", prompt = "List selection"
    #                       , list = ("foo", "bar", "baz")
    #                       )
    r = ask_many ( root
                 , ( Int_Field       ( "redundany_degree",   default = 2)
                   , Int_Field       ( "replication_degree", default = 5)
                   , Separator_Field ( )
                   , Listdrop_Extended_Field  ( "agreements"
                                     , list    = ["A", "B", "C"]
                                     , default = "('A', 'C')"
                                     )
                   , Boolean_Field   ( "save", default = 0)
                   )
                 , title = "More then one input"
                 , head  = "All inputs are below"
                 )
    print r,len (r)

### __END__ TFL.TKT.Tk.CTK_Dialog
