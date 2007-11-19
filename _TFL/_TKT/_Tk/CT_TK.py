# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2007 Mag. Christian Tanzer. All rights reserved
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
#    CT_TK
#
# Purpose
#    - Add widget types to those supported by Tkinter (TK)
#    - Provide module around Tkinter and friends to simplify import and use
#      and avoid name clashes resulting from `from Tkinter import *'
#
# Revision Dates
#    16-Mar-1998 (CT) Creation (Separator's)
#    21-Mar-1998 (CT) Virtual events, CT_TK_mixin, and read_option_file added
#    22-Mar-1998 (CT) Scrollable's added
#    23-Mar-1998 (CT) Helplabel, Balloon, Notebook, Tabbed_Notebook added
#    24-Mar-1998 (CT) Panedwindow's, Listdropentry and Spinner's added
#    28-Mar-1998 (CT) Scrollbar of `Scrolled_Listbox' conditional on size
#                     Size of `Listdropentry' minimized
#                     Adjust `wraplength' of `Helplabel'
#    29-Mar-1998 (CT) H_Strut added and used by Entrycontainer
#     2-Apr-1998 (CT) `Helplabel' renamed to `Statusframe'
#     4-Apr-1998 (CT) `Entrycontainer' renamed to `C_Entry'
#                     `CFrame'         remaned to `C_Frame'
#     4-Apr-1998 (CT) Mixins factored from Listdropentry, Combobox, and
#                     Spinner
#     4-Apr-1998 (CT) Listdropspinner added
#     4-Apr-1998 (CT) Entrybox added
#     4-Apr-1998 (CT) Multicombobox added
#     6-Apr-1998 (CT) `<FocusOut>' binding for Listdropentry added
#     7-Apr-1998 (CT) Buttonbox added
#     8-Apr-1998 (CT) Key-Up and Key-Down bindings added to `Spinner_'
#     8-Apr-1998 (CT) Combo-Bindings with special bindtag added
#     9-Apr-1998 (CT) `reload' defined for `Scrolled_Listbox', `Listdrop_',
#                     `Listspinner_' and `Listdropspinner'
#     9-Apr-1998 (CT) Parameter `state'   added to all C_Entry-descendents
#     9-Apr-1998 (CT) Parameter `bindtag' added to all C_Entry-descendents
#    10-Apr-1998 (CT) `script_path' factored, Bitmaps loaded from
#                     `script_path'
#    11-Apr-1998 (CT) Multicombobox_X added
#    12-Apr-1998 (CT) Functions interfacing to tkMessageBox added to
#                     CT_TK_mixin
#    14-Apr-1998 (CT) `push' and `pop' added to `Statusframe'
#    18-Apr-1998 (CT) C_Menu added
#    19-Apr-1998 (CT) Parameter `fixed_width' added to `V_Scrollable'
#    21-Apr-1998 (CT) `Statusframe' split into `Statusframe_' and `Statuslabel'
#                     `Statustext' added
#    21-Apr-1998 (CT) `fixed_width' and `fixed_height' added to C_Entry and
#                     descendents
#    23-Apr-1998 (CT) `read_option_files' added
#    23-Apr-1998 (CT) Use `os.path.samefile' to compare directories in
#                     `read_option_file'
#     1-Jun-1998 (CT) `C_Entry.set' changed to set entry-state to normal
#                     temporarily
#     2-Jun-1998 (CT) Message_Window added
#     4-Jun-1998 (CT) `write' added to `Message_Window'
#     5-Jun-1998 (CT) `CT_TK_mixin' added to ancestor-list of `C_Menu'
#     5-Jun-1998 (CT) `busy_cursor' and `normal_cursor' added to `CT_TK_mixin'
#     5-Jun-1998 (CT) `replace_matches' added to `Message_Window'
#     9-Jun-1998 (CT) `enable'/`disable' added
#    10-Jun-1998 (CT) _Coupled_V_Scrolled added
#    11-Jun-1998 (CT) C_Listbox factored from Scrolled_Listbox
#    11-Jun-1998 (CT) Listbox_Couple added
#    12-Jun-1998 (CT) `disabledForeground' and `disabledBackground' added
#    13-Jun-1998 (CT) _Coupled_V_Scrolled renamed to V_Scrolled_Tuple_
#    13-Jun-1998 (CT) Listbox_Couple renamed to Listbox_Tuple
#    13-Jun-1998 (CT) Entry_Tuple factored from Entrybox
#    13-Jun-1998 (CT) Combo_Tuple added
#    14-Jun-1998 (CT) Position of spinner-buttons of Listdropspinner changed
#                     from LEFT to RIGHT
#    14-Jun-1998 (CT) `bindtag' added to Buttonbox
#    14-Jun-1998 (CT) Combo_Tuple corrected
#    15-Jun-1998 (CT) Initialize `root' from `Tkinter._default_root' if
#                     already existing
#    17-Jun-1998 (CT) `C_Entry.disable' disables `label', too
#    14-Jul-1998 (CT) `define_edit_menu' added to `CT_TK_mixin'
#    20-Jul-1998 (CT) `H_Scrolled_Tuple_' and `Scrolled_Tuple_' added
#     5-Aug-1998 (CT) `labeljustify' added
#    16-Aug-1998 (CT) Renamed `script_path' to `path'
#    16-Aug-1998 (CT) Don't use `sys.argv' to determine `path' when import-ed
#    16-Aug-1998 (CT) Parameters `event' and `delay' added to `Balloon.activate'
#    19-Aug-1998 (CT) `pane_off_ht' and `pane_off_wd' added to `Panedwindow's
#    19-Aug-1998 (CT) Sash of `Panedwindow' made drag-able
#    20-Aug-1998 (CT) `upper_limit_*' added to `Panedwindow'
#    20-Aug-1998 (CT) `Message_Window.ignore' bound to allow C-c for copying
#                     a selection
#    21-Aug-1998 (CT) `Progress_Gauge' added
#    23-Aug-1998 (CT) Use `anchor = CENTER' for placing `Progress_Gauge' and
#                     its children
#    24-Aug-1998 (CT) `Progress_Gauge_T' added
#    26-Aug-1998 (CT) `cursor' of `Progress_Gauge' set to "watch"
#    26-Aug-1998 (CT) `title' added to `Progress_Gauge_T'
#    27-Aug-1998 (CT) `ask_*_file_name' added
#    30-Aug-1998 (CT) Removed `scan_mark/scan_dragto' bindings for
#                     `_*Scrolled_Tuple_'
#     6-Sep-1998 (CT) `Scrolled_Text' added
#     6-Sep-1998 (CT) `C_Text' factored from `Scrolled_Text' and
#                     `Message_Window'
#     6-Sep-1998 (CT) `Slide_Show' added
#    30-Oct-1998 (CT) `path' converted from attribute into function to avoid
#                     it being fixed during byte compilation before delivery
#    30-Oct-1998 (CT) Use `imp.find_module' to get path
#     1-Nov-1998 (CT) Use Command_Line for parsing command line
#    13-Nov-1998 (CT) `ask_yes_no_cancel' added
#    10-Dec-1998 (CT) `put_help', `push_help', and `pop_help' added to
#                     `Message_Window'
#    10-Dec-1998 (CT) `delete_tagged' added to `C_Text'
#    10-Dec-1998 (CT) `Buttonbox.buttonconfigure' updates `cmd_map'
#    10-Dec-1998 (CT) `help' added to `Slide_Show'
#    10-Dec-1998 (CT) `C_Entry' passes `labelanchor' to `Label'
#    16-Dec-1998 (CT) `labelanchor' added to all(?) descendents of `C_Entry'
#    16-Feb-1999 (CT) `self.update' added to `Progress_Gauge_T.activate'
#    16-Feb-1999 (CT) `read_option_file' changed to use `Environment.path_of'
#                     instead of `CT_TK.path' to search for option file
#    17-Feb-1999 (CT) Use `Environment.script_path ()' instead of
#                     `Command_Line.script_path' in `__main__' script
#    22-Feb-1999 (CT) `_complete' added to `C_Entry'
#    22-Feb-1999 (CT) `complete' added to `Listdropentry', `Combo_Entry' and
#                     `Listspinner'
#    22-Mar-1999 (CT) `Entrybox': place `label' in `self' instead of
#                     `self.frame'
#    31-Mar-1999 (CT) `Filename_Entry' added
#     1-Apr-1999 (CT) `_popup_complete_menu' added to `C_Entry'
#     2-Apr-1999 (CT) Cascades added to `_popup_complete_menu'
#    20-Apr-1999 (CT) Assignments to `self.master' removed (is done by
#                     `BaseWidget' anyway)
#    18-May-1999 (CT) `CT_TK_mixin.__show' renamed to `CT_TK_mixin._show__'
#                     `CT_TK_mixin._ask__' added
#    18-May-1999 (CT) Exception handler added to `V_Scrollable.see_y_fraction'
#    26-May-1999 (CT) `Listspinner_.change' corrected (always use `index' to
#                     find index of current element)
#     2-Jun-1999 (CT) `Fileview' added
#     4-Jun-1999 (CT) `C_Text': bind `Any-Key' to `ignore' if `DISABLED' is
#                     passed in for `state' (instead of passing
#                     `state' on to `Text')
#     4-Jun-1999 (CT) `Fileview': always pass `DISABLED' to `Scrolled_Text'
#    11-Jun-1999 (CT) `_sanitize_dir' called for file dialogs to avoid Tcl
#                     errors for non-existing directories
#    16-Jun-1999 (CT) `ignore' doesn't ignore <Control-O>, <Control-S>, and
#                     <Control-W>
#     1-Jul-1999 (CT) Use `sos' instead of `os'
#    16-Jul-1999 (CT) `ask_dir_name' and `Dirname_Entry' added
#    21-Jul-1999 (CT) `Entry_History' and `C_Entry._history' added
#    21-Jul-1999 (CT) `Combobox_Listdropspinner' added
#    27-Jul-1999 (CT) `Entry_History.add' allows more than one value
#     4-Aug-1999 (CT) `Multicombobox' and `Multicombobox_X' removed
#     4-Aug-1999 (CT) `on_change' added (proposed by Harald Angelow)
#    10-Aug-1999 (HA) `on_change' only added in 'set' from C_Entry
#    10-Aug-1999 (CT) Formatting restored after `HA's changes
#    10-Aug-1999 (CT) `self.Ancestor' replaced by `Fileview.Ancestor'
#     1-Sep-1999 (HA) `on_change' also added in  C_Listbox and
#                     'mouse_select' hacked - Sorry !!!
#    27-Sep-1999 (CT) `read_option_file': protect `samefile' by exception
#                     handler (non-existent directories trigger an exception)
#    28-Sep-1999 (MY) Select events in Combobox_Listdropspinner bound for
#                     Listdropspinner
#    29-Sep-1999 (CT) `C_Checkbutton_Entry' added
#    29-Sep-1999 (CT) Combobox_Listdropspinner inherits only from
#                     Listdropspinner (and uses the combobox instead of
#                     inheriting from it)
#    30-Sep-1999 (MY) `fixed_height' added to Combobox_Listdropspinner
#     5-Oct-1999 (CT) `Combobox_Listdropspinner.set_and_sync' added
#    21-Oct-1999 (CT) `{H,V}Panedwindow_.drag' corrected for case `not event'
#                     (computation of `y': don't add `self.winfo_root{x,y}')
#    21-Oct-1999 (CT) `Panedwindow_.divide' factored from `{H,V}Panedwindow_'
#    21-Oct-1999 (CT) `C_Menu.__init__': convert `name' to lowercase
#    22-Oct-1999 (CT) `Boolean_Variable' added
#    22-Oct-1999 (CT) Virtual event `<<printAll>>' added
#    28-Oct-1999 (CT) `BB_Toplevel' added
#     1-Nov-1999 (CT) `BB_Toplevel': distinguish between `close_cmd' and
#                     `destroy_cmd'
#     2-Nov-1999 (CT) `inner_entrypos' and `anchor'  of `C_Checkbutton_Entry'
#                     changed to `RIGHT' and `E' (from `LEFT' and `W'),
#                     respectively
#     2-Nov-1999 (CT) `History_Spinner' added
#     2-Nov-1999 (CT) `buttonbind' added to `Buttonbox'
#     2-Nov-1999 (CT) `_enable_entry' and `_disable_entry' factored
#     3-Nov-1999 (CT) Handling of `g_delta' added to `Progress_Gauge'
#                     Arguments for `reset' added to
#                     `Progress_Gauge_T.activate'
#     3-Nov-1999 (CT) `Notebook.name' renamed to `Notebook.p_name'
#     3-Nov-1999 (CT) `Buttongroup' factored from `Buttonbox'
#     3-Nov-1999 (CT) `C_Button' added
#     3-Nov-1999 (CT) `Buttonbox' renamed to `Buttongrid'
#     3-Nov-1999 (CT) `Buttonboxes' added
#     4-Nov-1999 (CT) `Buttongroup.buttonactivate': set `default = DISABLED'
#                     instead of `default = NORMAL' for the old active button
#     4-Nov-1999 (CT) `undrop_focus_out' implemented to handle Windows idioty
#     5-Nov-1999 (CT) `ask_*': pass `default' option to tkMessageBox
#     5-Nov-1999 (CT) `Buttongroup.add': set option `highlightbackground' to
#                     background color
#     5-Nov-1999 (CT) `height' and `_is_framed' added to `Buttongroup'
#     5-Nov-1999 (CT) `Combo_Tuple_Xtern' added
#     9-Nov-1999 (CT) Parameter `width' removed from calls to `Buttongrid'
#     9-Nov-1999 (CT) `C_Listbox.list_box_height' factored
#     9-Nov-1999 (CT) `C_Entry.frame_expand' factored
#     9-Nov-1999 (CT) `Combo_' factored from `Combobox_' and
#                     `Combobox_Listdropspinner'
#     9-Nov-1999 (CT) `combo_fill' and `combo_expand' factored
#     9-Nov-1999 (CT) `Scrollable_':
#                     * use `self.vport.create_window (...)' instead of
#                           `Window (self.vport, ...)'
#                     * `hull_repack' added to descendents
#     9-Nov-1999 (CT) `V_Scrollable': `change_width' added
#    10-Nov-1999 (CT) `V_Scrollable.hull_repack': use `winfo_reqheight'
#                     instead of `winfo_height'
#    10-Nov-1999 (CT) `Panedwindow_': `change_size' calls
#                     `after_idle (_change_size)' instead of doing
#                     `_change_size's job immediately
#    15-Nov-1999 (MY) CT_TK_mixin.option_value now supports string tuples
#     2-Dec-1999 (CT) `Combo_Tuple.col_label' anchored `W' and made sticky `EW'
#     2-Dec-1999 (CT) `Dirname_Entry.popup_file_selector' changed to append
#                     `sos.sep' to directory specification and convert
#                     `sos.altsep' to `sos.sep'
#     9-Dec-1999 (CT) `auto_pop_help' added to `Buttongroup' and descendents
#     9-Dec-1999 (CT) `C_Menu.help': pop before push
#     9-Dec-1999 (CT) `Message_Window._stack_level' renamed to
#                     `Message_Window.hlp_lvl' (to avoid a mysterious bug --
#                     `self._stack_level = self._stack_level + 1' had no
#                     consistent effect: it would influence tag but nothing
#                     else)
#     9-Dec-1999 (CT) `C_Menu.help':
#                     - support for functors (i.e., object instances with
#                       __call__ method) added
#                     - `menu_help' added (returns a string to be displayed
#                       by `C_Menu' -- the `menu_helper' has to display the
#                       string himself)
#    10-Dec-1999 (CT) `C_Menu':
#                     - `add_command' and `insert_command': removed parameter
#                       `cnf'
#                     - `clear' added
#                     - `set_auto_short_cuts' added
#                     - `__add' refactored
#                     - `add_cascade' and `add_checkbutton' added
#    13-Dec-1999 (CT) `C_Menu._toggle_button' added and bound to shortcuts of
#                     checkbuttons
#    14-Dec-1999 (CT) `C_Menu.hlp_map' added and used
#    19-Jan-2000 (CT) `change_callback' added to `Panedwindow_'
#    31-Jan-2000 (CT) `path' checks `PY_FROZEN'
#     4-Feb-2000 (CT) `C_Listbox.indices' factored
#     4-Feb-2000 (CT) `C_Listbox_Extended' and `Scrolled_Listbox_Extended'
#                     added
#     7-Feb-2000 (CT) `Listdropentry_Extended' added
#     7-Feb-2000 (CT) Key bindings for `Listdropentry_Extended' added
#     9-Feb-2000 (CT) `Editor_Entry' added
#    10-Feb-2000 (CT) `Editor_Entry' finished
#    11-Feb-2000 (CT) Use `getcwd' if `_path' equals `sos.curdir'
#    11-Feb-2000 (CT) `read_option_file' got parameter `dur_dir'
#    14-Feb-2000 (CT) `dur_dir' renamed to `cur_dir'
#    25-Feb-2000 (CT) Exception handler around initialization of `root' added
#                     and code using `root' protected by `if root'
#     1-Mar-2000 (CT) Exception handler introduced at 25-Feb-2000: write
#                     traceback to standard output
#     7-Mar-2000 (CT) `Combo_Entry.after_idle_select_binding' added to handle
#                     `<ButtonRelease-1>' properly
#    29-Mar-2000 (CT) `std_pathes' added and used
#    29-Mar-2000 (CT) `Image_Mgr'  added and used
#    31-Mar-2000 (CT) `Combo_Tuple.add_entry': `pack_propagate (0)' and
#                     `configure (height = ...)' added
#    13-Apr-2000 (CT) Use `Environment.frozen' to determine if application is
#                     frozen
#    13-Apr-2000 (CT) `Bitmap_Mgr' added and used for bitmaps instead of
#                     `Image_Mgr'
#    13-Apr-2000 (CT) `Ancestor' replaced by `__Ancestor'
#                     (can use `self.__Ancestor' instead of `<class>.Ancestor')
#    13-Apr-2000 (CT) Use callback `button_help' instead of `button_helper'
#    13-Apr-2000 (CT) Use callback `menu_help'   instead of `menu_helper'
#    14-Apr-2000 (CT) `_set_options' added
#    14-Apr-2000 (CT) `path' factored into `Environment.module_path'
#    26-Apr-2000 (CT) Use `Environment.default_dir' and
#                     `Environment.home_dir' in `std_pathes'
#    20-Jun-2000 (CT) `Editor_Entry': `Cancel' function and button added
#    21-Jun-2000 (CT) `Editor_Entry':
#                     - make `transient' instead of using `<FocusOut>'
#                       binding to remove the window
#                     - use `Scrolled_Text' instead of `C_Text' for editor
#                     - `minsize' set to (200, 100)
#    21-Jun-2000 (CT) `Scrolled_Text': parameter `x_scroll' added
#    26-Jun-2000 (CT) `put_button_help': don't display balloon for for
#                     disabled buttons
#    27-Jun-2000 (CT) `enable_entry' and `disable_entry' added to
#                     `C_Menu' and `Buttongroup'
#    29-Jun-2000 (CT) `C_Text.disable' factored
#    30-Jun-2000 (CT) Binding for `<Unmap>' added to `C_Menu' (was commented
#                     out)
#    20-Jul-2000 (CT) `set_maxsize' added
#    20-Jul-2000 (CT) `cancel_button' added to `Progress_Gauge'
#    24-Jul-2000 (CT) `Progress_Gauge': set/release grab to make `update' save
#    25-Jul-2000 (CT) `C_Text': use class attribute `body_name' instead of
#                     literal "text"
#    31-Jul-2000 (CT) `Balloon.__init__': call `withdraw' after `transient'
#    31-Jul-2000 (CT) `Progress_Gauge_T': call `withdraw' after `transient'
#    31-Jul-2000 (CT) `BB_Toplevel': redefined `destroy' and `withdraw' to
#                     allow binding to key events (optional `event' argument)
#     1-Aug-2000 (CT) Tabs removed (introduced by HA)
#     2-Aug-2000 (CT) `C_Entry': use `FLAT' relief for disabled entries
#     2-Aug-2000 (CT) `C_Entry': default for `disabledBackground' changed
#                     from `gray90' to `lightyellow2'
#     7-Aug-2000 (CT) Name of close-button of `BB_Toplevel' configurable
#     7-Aug-2000 (CT) Name of close-button of `Editor_Entry.drop_box' changed
#                     from `Close' to `Commit' (and `Cancel' button put to
#                     the left of the `Commit' button)
#     7-Aug-2000 (CT) `grab_set' protected by exception handler
#     8-Aug-2000 (CT) `C_Toplevel' factored from `BB_Toplevel' (and
#                     `state_mgr' added)
#     9-Aug-2000 (CT) `_bind_completer' factored and binding to `<Alt-Space>'
#                     added to it
#     9-Aug-2000 (CT) `Buttongroup.put_button_help': for buttcons, display
#                     command name in balloon and description in help window
#                     (for text buttons, display description in balloon or
#                     help window depending on the button state)
#    11-Aug-2000 (CT) `save_geometry' factored
#    11-Aug-2000 (CT) `save_geometry': don't save full screen geometry
#    11-Aug-2000 (CT) `Panedwindow_': `_change_frame_size' added
#    11-Aug-2000 (CT) `_change_frame_size' disabled as it doesn't seem to do
#                     anything (XXX come back to this, cf. Gra00, p93)
#    14-Aug-2000 (CT) `C_Menu': `enable_entry' and `disable_entry' pass
#                     `index (label)' to `entryconfigure' (instead of `label')
#    14-Aug-2000 (CT) `set_maxsize': `- 20' replaced by optional parameters
#                     `x_margin' and `y_margin'
#    14-Aug-2000 (CT) `save_geometry': safety marging for determination
#                     window maximization increased to 100 vertical and 70
#                     horizontal
#    21-Aug-2000 (CT) `_ask_file_name' factored and `kw ["parent"]' set to
#                     `self'
#     8-Sep-2000 (CT) `Image_Mgr_.add': apply `make_absolute' to `filename'
#    11-Sep-2000 (CT) `abs_directory' corrected (`sos.path.abspath' returns
#                     an empty directory for an empty argument)
#    27-Sep-2000 (CT) Missing `return' added to `ask_dir_name' (error
#                     introduced with change of 21-Aug-2000)
#    28-Sep-2000 (CT) s/database/data base/g
#    13-Dec-2000 (CT) s/data base/database/g
#    22-Feb-2001 (CT) Use `raise' instead of `raise exc' for re-raise
#    25-Jun-2001 (CT) `Progress_Gauge.__init__' calls `reset'
#     6-Nov-2001 (CT) Import of `traceback` moved from exception handler to
#                     global scope
#     7-Nov-2001 (CT) `Progress_Gauge` binds `withdraw` to `WM_DELETE_WINDOW`
#    14-Dec-2001 (CT) `_ask_file_name` changed to refuse non-ascii filenames
#    18-Dec-2001 (CT) Argument `offy` added to `Balloon.activate`
#    19-Feb-2002 (CT) HV_Scrollable added, H_Scrollable_ and V_Scrollable_
#                     factored and other heavy surgery in Scrollable_ family
#    11-Apr-2002 (CT) `_update_and_check_kbi` factored and called from
#                     `Progress_Gauge.inc` for tiny increments, too
#    20-Jun-2002 (CT) C_Frame_: s/./_/ for widget names
#    18-Jul-2002 (CT) `Buttongrid.regrid` changed to not use
#                     `Button.grid_forget` (sometimes barfs under Py22/Win32)
#     8-Oct-2002 (CT) `Progress_Gauge_T.activate` changed to use `title` for
#                     `label` if not `label` was passed
#    18-Dec-2002 (CT) `set_maxsize` changed to return `x, y`
#    18-Mar-2003 (CT) s/Image_Mgr_/_Image_Mgr_/g
#    18-Mar-2003 (CT) `_Image_Mgr_.normalized` factored and
#                     `sos.path.normcase` added to it
#     5-May-2003 (CT) Exception handler added to
#                     `Scrolled_Listbox_._change_size_pending`
#    11-Jun-2003 (CT) s/== None/is None/
#    11-Jun-2003 (CT) s/!= None/is not None/
#     1-Jul-2003 (GWA) correct path added to filename in `read_option_file`
#     9-Feb-2004 (CT)  s/eval/int/
#    17-Feb-2004 (CT)  `Tkinter.wantobjects=False` added to avoid annoyances
#                      like `AttributeError: '_tkinter.Tcl_Obj' object has no
#                      attribute 'encode'` from TK8.4
#    11-Mar-2004 (CT)  `num_opt_val` changed back to use `eval` instead of
#                      `int`
#    24-May-2004 (CT)  `_ask_file_name` changed to use `root` instead of
#                      `self` as default `parent` (otherwise Win32 makes the
#                      dialog model with regard to `self` but not to other
#                      `Toplevel` windows of the application)
#    27-May-2004 (GWA) Integer division fixed "/" -> "//"
#    11-Jun-2004 (GKH) deprecation warning removed [10140]
#     7-Jul-2004 (MG)  `Balloon.instance` added
#     3-Aug-2004 (MG)  Merge changes from `nco_devel_branch`
#    10-Sep-2004 (CED) `Progress_Gauge.inc` made more robust
#    20-Sep-2004 (CED) Check for empty range moved from `inc` to `reset`
#    20-Sep-2004 (CED) Empty range check moved to begin of function
#    20-Sep-2004 (CED) Negative ranges are forbidden also
#    21-Sep-2004 (CED) Zero is allowed again (`inc` should not be called in
#                      that case)
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#     1-Oct-2004 (GKH) deprecation warning removed [11618]
#    22-Oct-2004 (CED) `Zipped_Image`, `Zipped_Image_Mgr` added
#    22-Oct-2004 (CED) `Zipped_Image` catches KeyError
#    22-Oct-2004 (CED) `Zipped_Image_Mgr` improved to deal with directories
#                      inside the zipfile
#    22-Oct-2004 (CED) `_Zipped_Image_Mgr_` factored out and
#                      `Zipped_Bitmap_Mgr` added, all classes converted to
#                      new-style classes
#    23-Oct-2004 (CED) 'BadZipfile` also caught
#    23-Oct-2004 (CED) `Option_Mgr`, `Zipped_Option_Mgr` added.
#     5-Nov-2004 (CED) `ask_dir_name` changed to use `tk_chooseDirectory`
#    11-Jan-2005 (CT)  `C_Menu.insert_checkbutton` added
#    12-Jan-2005 (CT)  `std_pathes` changed to include `-Images` subdirectory
#                      of the directory where this module was loaded from
#    12-Jan-2005 (CT)  Broken window donated by GWA on 1-Jul-2003 fixed
#    18-Jan-2005 (CT)  `_Image_Mgr_.get` added
#     1-Feb-2005 (CT)  `canonical_key_name` factored
#    15-Feb-2005 (CT)  `C_Text.index` added
#    16-Feb-2005 (CT)  `C_Text.search` added
#    17-Feb-2005 (CT)  `C_Text.mark_set` added
#    20-Feb-2005 (CT)  Individual delegator-definitions of `C_Text` replaced
#                      by `_auto_delegate` and `__getattr__`
#    22-Feb-2005 (CT)  `C_Text.place_cursor` added
#    24-Feb-2005 (CT)  `tag_bind` added to `C_Text._auto_delegate`
#    15-Mar-2005 (CT)  `Progress_Gauge` and `Progress_Gauge_T` changed to
#                      handle multiple `activate` calls gracefully
#     6-Apr-2005 (CT)  `make_active` added to `CT_TK_mixin`
#     8-Apr-2005 (CT)  `Buttongroup._index` changed to limit numeric `b`
#                      arguments to `len (self.button)`
#    13-Apr-2005 (PGO) `new_page` takes index parameter
#    19-Apr-2005 (CT)  `CT_TK_mixin.make_active` changed to delegate to
#                      `master.make_active` if possible (to support things
#                      like pages in a notebook in a generic way)
#    19-Apr-2005 (CT)  Small style improvements
#    25-Apr-2005 (CT)  `Progress_Gauge.show_percent` added
#                      (and style improvements)
#    25-Apr-2005 (CT)  `Progress_Gauge.cycle` added
#    26-Apr-2005 (CT)  `C_Menu.popup` added
#    16-May-2005 (CT)  `std_pathes` changed to look for `-Images` in all
#                      entries of `sys.path`
#    20-May-2005 (CT)  `Scrolled_Text` changed to allow `x_scroll_default` as
#                      class variable
#    20-May-2005 (CT)  `wtk_widget` added to `C_Frame` instances
#    20-May-2005 (CT)  Argument `frac` added to `Panedwindow_.change_size`
#    13-Jul-2005 (CED) `std_pathes` changed to use sets
#    11-Aug-2005 (CT)  `_ctrl_replace` changed for `NT` (`Shift` for
#                      uppercase bindings)
#    30-Aug-2005 (CT)  Use `endswith` instead of `find`
#    31-Aug-2005 (CT)  `Buttongroup.add` changed to deal gracefully with `None`
#                      passed for `bitmap` or `image`
#    16-Sep-2005 (MZO) fixed canonical_key_name - remove always <>
#    13-Jul-2006 (MZO) [20988] icon added to mgr
#    25-Jul-2006 (CED) `Zipped_Image` fixed
#    12-Oct-2006 (CED) `Num_Spinner`s behaviour changed
#    22-Nov-2006 (CED) `Num_Slider` added
#     7-Mar-2007 (MZO) [23116] bitmap `edit_oe_read_only` loaded
#     3-May-2007 (MZO) [24232] `change` of `Listspinner_` fixed
#    14-May-2007 (MZO) consistent mouse wheel scroll in `Listbox_Tuple_` added
#    02-Aug-2007 (CED) Coding guidelines
#    13-Sep-2007 (MZO) [24618] set toplevel icon
#    19-Nov-2007 (CT)  `Balloon.body`: added `anchor = W, justify = LEFT`
#    19-Nov-2007 (CT)  Imports corrected
#    19-Nov-2007 (CT)  `string` functions replaced by `str` methods
#    ««revision-date»»···
#--

import Tkinter
Tkinter.wantobjects = False

from   Tkconstants import *
from   Tkinter     import *
from   Tkinter     import _flatten, _default_root
from   Canvas      import *

from   _TFL.Filename    import Filename
from   _TFL.Functor     import *
from   _TFL.NO_List     import NO_List
from   _TFL.predicate   import *
from   _TFL             import Environment
from   _TFL             import sos
from   _TFL             import TFL
import _TFL._Meta.Object

import tkMessageBox

import imp
import re
import sys
import traceback
import types
import zipfile

_undefined = object ()

# augment Tkconstants's list of special tags, marks and insert positions
START  = "1.0"

def path () :
    """Returns path where module resides"""
    return Environment.module_path ("CT_TK")
# end def path

_std_pathes = None

def std_pathes () :
    """Returns standards pathes where to look for auxiliary files like option
       files and bitmaps.
    """
    global _std_pathes
    if _std_pathes is None :
        p           = path ()
        _std_pathes = []
        _img_pathes = []
        seen        = set ()
        for s in sys.path :
            si = sos.path.join (s, "-Images")
            if sos.path.isdir (si) :
                _img_pathes.append (si)
        for q in ( p
                 , sos.path.join (p, "-Images")
                 , Environment.default_dir
                 , Environment.home_dir
                 ) + tuple (_img_pathes) :
            if q not in seen :
                _std_pathes.append (q)
                seen.add (q)
    return _std_pathes
# end def std_pathes

class Option_Mgr (TFL.Meta.Object) :
    """Provide methods to read option files"""

    def __init__ (self) :
        self._already_read_option_file = {}
    # end def __init__

    def _read_option_file (self, tk, filename) :
        filename = sos.path.abspath (filename)
        if filename in self._already_read_option_file :
            return
        try :
            if sos.path.isfile (filename) :
                tk.option_readfile (filename)
                self._already_read_option_file [filename] = 1
        except (SystemExit, KeyboardInterrupt), exc :
            raise
        except :
            pass
    # end def _read_option_file

    def read_option_file (self, tk, filename, cur_dir = sos.curdir) :
        """This reads the option file(s) `filename' if it exists.
           `read_option_file' looks for `filename' in the program's
           directory and python search path, the current directory,
           and in the users home directory (if environment variable
           HOME is set).
           `read_option_file' reads `filename' from all directories where it
           finds it.
           `filename' is read by calling `tk.option_readfile'.
        """
        try :
            path = Environment.path_of (filename) or cur_dir
            self._read_option_file (tk, sos.path.join (path, filename))
            for p in std_pathes () :
                self._read_option_file (tk, sos.path.join (p, filename))
        except (SystemExit, KeyboardInterrupt), exc :
            raise
        except :
            ### ignore exceptions triggered by non-existent directories and
            ### similar nuisances
            pass
    # end def read_option_file

    def read_option_files (self, tk, filename, cur_dir = sos.curdir) :
        """Read generic and platform-specific option files."""
        ps_file = Filename    ("." + sos.name, filename)
        self.read_option_file (tk, filename,     cur_dir)
        self.read_option_file (tk, ps_file.name, cur_dir)
    # end def read_option_files
# end class Option_Mgr

option_mgr = Option_Mgr ()
### XXX Backward compatibility
read_option_files = option_mgr.read_option_files
read_option_file  = option_mgr.read_option_file

class Zipped_Option_Mgr (Option_Mgr) :
    """Provides methods to read options files inside a zipfile"""

    def __init__ (self, archive) :
        self.__super.__init__ ()
        if not isinstance (archive, Filename) :
            archive = Filename (archive)
        self.archive = archive
    # end def __init__

    def read_option_file (self, tk, filename, cur_dir = None) :
        try :
            filename = sos.sep.join \
                ( [ c for c in filename.split (sos.sep)
                    if c != "."
                  ]
                )
            if filename in self._already_read_option_file :
                return
            zf = zipfile.ZipFile (self.archive.abs_name (), "r")
            if filename in zf.namelist () :
                ### Tkinter seems to have no way specifiy the contents
                ### of an option file directly. So we have to temporarily
                ### unpack the file (we do not want to use homegrown
                ### code to parse the file contents and call `add_option`
                ### for each entry).
                self._unzip_and_read_file (tk, filename, zf)
            zf.close ()
        except (IOError, zipfile.BadZipfile) :
            pass
    # end def read_option_file

    def _unzip_and_read_file (self, tk, filename, zf) :
        try :
            data = zf.read     (filename)
            name = sos.tmpnam  ()
            outf = open        (name, "w")
            outf.write         (data)
            outf.close         ()
            tk.option_readfile (name)
            self._already_read_option_file [filename] = 1
            sos.unlink         (name)
        except (SystemExit, KeyboardInterrupt) :
            raise
        except :
            pass
    # end def _unzip_and_read_file

# end class Zipped_Option_Mgr

_key_pattern            = re.compile ("-Key-")
_ctrl_pattern           = re.compile ("Control-(.)")
_angle_brackets_pattern = re.compile ("^<(?P<kn>.*)>$")
if sos.name == "nt" :
    def _ctrl_replace (match) :
        h = "Ctrl"
        c = match.group (1)
        if c.islower () :
            c = c.upper ()
        else :
            h = "+".join (("Shift", h))
        return "+".join ((h, c))
    # end def _ctrl_replace
else :
    def _ctrl_replace (match) :
        return "C-"    + match.group (1)
    # end def _ctrl_replace

def virtual_key_name (vev, widget = None) :
    """Returns name of key bound to virtual event `vev'."""
    widget = widget or root
    result = widget.event_info (vev)
    if result :
        result = canonical_key_name (result [0])
    return result
# end def virtual_key_name

def canonical_key_name (name) :
    """Returns canonical form of key `name`."""
    if name is None :
        return
    result = _key_pattern.sub ("-", name)
    if _ctrl_pattern.search (result) :
        result = _ctrl_pattern.sub (_ctrl_replace, result)
    match_brackets = _angle_brackets_pattern.match (result)
    if match_brackets :
        result = match_brackets.groupdict () ["kn"]
    return result
# end def canonical_key_name

def add_bindtag (widget, bindtag, before = 0) :
    btags = widget.bindtags ()
    widget.bindtags (btags [:before] + (bindtag, ) + btags [before:])
# end def add_bindtag

def ignore_event (event = None) : pass
def break_event  (event = None) : return "break"

class _Image_Mgr_ (TFL.Meta.Object) :
    """Root class for management of a collection of bitmaps (.xbm) and/or
       images (.gif)
    """

    Image_class = { ".xbm" : BitmapImage}

    def __init__ (self, * d) :
        """Construct a Image_Mgr, looking in directories specified by `d' for
           bitmaps and images (in addition to looking in the `std_pathes')
        """
        self.x_map  = {}
        self.files  = {}
        self.pathes = list (d) + std_pathes ()
    # end def __init__

    def add (self, filename, name = None) :
        """Add bitmap or image in `filename' to collection.

           If `name' is not specified, it defaults to `filename.base'.

           `kw' is passed to `BitmapImage' or `PhotoImage', respectively.
        """
        if not isinstance (filename, Filename) :
            filename = Filename (filename, ".xbm")
        assert (self.Image_class.has_key (filename.ext))
        if not sos.path.isfile (filename.name) :
            fn = filename.base_ext
            for p in self.pathes :
                if Environment.path_contains (p, fn) :
                    filename = Filename (fn, default_dir = p)
                    break
        filename.make_absolute ()
        if not name :
            name = filename.base
        name = self.normalized (name)
        if self.files.has_key (name) :
            if self.files [name].name != filename.name :
                print "Name clash for %s %s: %s vs. %s" \
                      % ( self.Image_class [filename.ext]
                        , name, filename.name, self.files [name].name
                        )
                return None
        else :
            self.files [name] = filename
        return name
    # end def add

    def get (self, name, default = None) :
        try :
            return self [name]
        except KeyError :
            return default
    # end def get

    def normalized (self, name) :
        return sos.path.normcase (name.replace (".", "_"))
    # end def normalized

    def __getitem__ (self, name) :
        return self.x_map [self.normalized (name)]
    # end def __getitem__

    def keys (self) :
        return self.files.keys ()
    # end def keys

# end class _Image_Mgr_

class Image_Mgr (_Image_Mgr_):
    """Provide management of a collection of bitmaps (.xbm) and images (.gif)
    """

    __Ancestor  = Ancestor = _Image_Mgr_

    Image_class = { ".xbm" : BitmapImage
                  , ".gif" : PhotoImage
                  }

    def __init__ (self, * d) :
        """Construct a Image_Mgr, looking in directories specified by `d' for
           bitmaps and images (in addition to looking in the `std_pathes')
        """
        self.__super.__init__ (* d)
        self.cnf = {}
    # end def __init__

    def add (self, filename, name = None, ** kw) :
        """Add bitmap or image in `filename' to collection.

           If `name' is not specified, it defaults to `filename.base'.

           `kw' is passed to `BitmapImage' or `PhotoImage', respectively.
        """
        name = self.__super.add (filename, name)
        if name :
            self.cnf [name] = kw
        return name
    # end def add

    def __getitem__ (self, name) :
        name = self.normalized (name)
        if not self.x_map.has_key (name) :
            filename          = self.files [name]
            self.x_map [name] = self.Image_class \
                [filename.ext] (file = filename.name, cnf = self.cnf [name])
        return self.x_map [name]
    # end def __getitem__

# end class Image_Mgr

image_mgr = Image_Mgr ()

class Bitmap_Mgr (_Image_Mgr_) :
    """Provide management of a collection of bitmaps (.xbm)"""

    __Ancestor  = Ancestor = _Image_Mgr_

    def add (self, filename, name = None) :
        """Add bitmap in `filename' to collection.

           If `name' is not specified, it defaults to `filename.base'.
        """
        name = self.__super.add (filename, name)
        if name :
            self.x_map [name] = "@" + self.files [name].name
    # end def add

# end class Bitmap_Mgr

bitmap_mgr = Bitmap_Mgr ()

class Zipped_Image (TFL.Meta.Object) :
    """Image class modelling an image file inside a zipfile."""

    def __init__ (self, name, archive, ** kw) :
        self.kw       = kw.copy ()
        self.name     = name
        try :
            zf        = zipfile.ZipFile (archive, "r")
            ### XXX *#gfrfx!*+#
            for p in ["", "-Images"] :
                try :
                    fn = sos.path.join (p, name)
                    self.data = zf.read (fn)
                    break
                except KeyError :
                    pass
            else :
                raise KeyError
            zf.close ()
        except (IOError, KeyError, zipfile.BadZipfile) :
            self.data = ""
    # end def __init__

    def image (self, image_cls) :
        return image_cls (data = self.data, ** self.kw)
    # end def image

# end class Zipped_Image

class _Zipped_Image_Mgr_ (_Image_Mgr_) :
    """Provide management of a collection of images inside a zip file"""

    __Ancestor  = Ancestor = Image_Mgr

    def __init__ (self, archive) :
        self.__super.__init__ ()
        if not isinstance (archive, Filename) :
            archive = Filename (archive)
        self.archive = archive
    # end def __init__

    def add (self, filename, name = None, ** kw) :
        name = self.__super.add (filename, name,  ** kw)
        self.files [name] = Filename (filename)
    # end def add

# end class _Zipped_Image_Mgr_

class Zipped_Image_Mgr (_Zipped_Image_Mgr_, Image_Mgr) :

    def __getitem__ (self, name) :
        name = self.normalized (name)
        if not self.x_map.has_key (name) :
            imgfile = self.files [name]
            zimg    = Zipped_Image \
                ( imgfile.name, self.archive.abs_name ()
                , cnf = self.cnf [name]
                )
            img_cls = self.Image_class [imgfile.ext]
            self.x_map [name] = zimg.image (img_cls)
        return self.x_map [name]
    # end def __getitem__

# end class Zipped_Image_Mgr

### Yes, we do NOT want to inherit from `Bitmap_Mgr` here
class Zipped_Bitmap_Mgr (_Zipped_Image_Mgr_) :

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._unpacked = []
    # end def __init__

    def __getitem__ (self, name) :
        name = self.normalized (name)
        if not self.x_map.has_key (name) :
            imgfile = self.files [name]
            ### Due a bug in TKinter, it is not possible
            ### to specify bitmap data directly. It works only
            ### with the '@filename' method. So we have to unpack
            ### the needed file on demand. (I don't like this way,
            ### but it seems to be the only possible solution).
            unziped_name = self._unzip_file (imgfile)
            self.x_map [name] = "@" + unziped_name
        return self.x_map [name]
    # end def __getitem__

    def _unzip_file (self, imgfile) :
        name = sos.tmpnam ()
        if not sos.path.exists (name) :
            zimg = Zipped_Image (imgfile.name, self.archive.abs_name ())
            try :
                outf = open (name, "w")
                outf.write  (zimg.data)
                outf.close  ()
                self._unpacked.append (name)
            except IOError :
                name = ""
        return name
    # end def _unzip_file

    def cleanup (self) :
        ### If a 'Zipped_Bitmap_Mgr' is used, you should call 'cleanup'
        ### in the end.
        for f in self._unpacked :
            try :
                sos.unlink (f)
            except (IOError, OSError) :
                pass
    # end def cleanup

# end class Zipped_Bitmap_Mgr

class CT_TK_mixin :
    """Provide some convenience functions for widget classes of CT_TK"""

    inverse_pos  = { TOP    : BOTTOM
                   , BOTTOM : TOP
                   , LEFT   : RIGHT
                   , RIGHT  : LEFT
                   }

    master       = None

    def make_active (self) :
        """Make widget `self` active"""
        try :
            master_make_active = getattr (self.master, "make_active", None)
            if callable (master_make_active) :
                master_make_active ()
            else :
                toplevel = self.winfo_toplevel ()
                toplevel.deiconify ()
                toplevel.lift      ()
            self.focus_set ()
        except TclError :
            pass
    # end def make_active

    def option_value (self, name, default, className = None, widget = None,
                      separator = None) :
        """Return value for option `name' from TK option database or
           `default'. If a separator string is specified, then a tuple of
           strings is returned. In the optionfile they are separated by
           'separator' strings.
        """
        if not widget    : widget    = self
        if not className : className = self.widget_class
        value = widget.option_get (name, className)
        if value == "" :
            value = default
        elif separator is not None :
            value = tuple (filter ( None
                                  , map ( lambda a : a.strip ()
                                        , value.split (separator)
                                        )
                                  )
                          )
        return value
    # end def option_value

    def num_opt_val (self, name, default, className = None, widget = None) :
        result = self.option_value (name, default, className, widget)
        if isinstance (result, (str, unicode)) :
            result = eval (result, {}, {})
        return result
    # end def num_opt_val

    def _set_option (self, name, default, dict) :
        if not dict.has_key (name) : dict [name] = default
    # end def _set_option

    def _set_options (self, dict, ** kw) :
        map ( lambda (name, default), set = self._set_option, dict = dict
                  : set (name, default, dict)
            , kw.items ()
            )
    # end def _set_options

    def _sanitized_dir (self, dir_name) :
        if not (dir_name and sos.path.isdir (dir_name)) :
            dir_name = sos.getcwd ()
        return dir_name
    # end def _sanitized_dir

    def _sanitize_dir (self, kw, dir_attr = "initialdir") :
        if kw.has_key (dir_attr) :
            kw [dir_attr] = self._sanitized_dir (kw [dir_attr])
    # end def _sanitize_dir

    def _ask_file_name (self, tk_fct, args, kw) :
        self._sanitize_dir (kw)
        self._set_option   ("parent", root, kw)
        try :
            result = apply ( self.tk.call
                           , (tk_fct, ) + args + self._options (kw)
                           )
        except TclError, exc :
            print exc
            result = None
        else :
            if result :
                try :
                    result = result.encode ("ascii")
                except UnicodeError :
                    self.show_error \
                        ( "Encoding error"
                        , "Non-ascii file names are currently not supported"
                        )
                    return self._ask_file_name (tk_fct, args, kw)
        ### for Win32 this is necessary to remove the dialog window
        ### (it stays in front of `self' sometimes)
        if sos.name == "nt" : self.update ()
        return result
    # end def _ask_file_name

    def ask_open_file_name (self, * args, ** kw) :
        return self._ask_file_name ("tk_getOpenFile", args, kw)
    # end def ask_open_file_name

    def ask_save_file_name (self, * args, ** kw) :
        return self._ask_file_name ("tk_getSaveFile", args, kw)
    # end def ask_save_file_name

    def ask_dir_name (self, * args, ** kw) :
        result = self._ask_file_name ("tk_chooseDirectory", args, kw)
        return result
    # end def ask_dir_name

    def _show__ (self, show_fct, * args, ** kw) :
        self._set_option ("parent", self, kw)
        result = apply (show_fct, args, kw)
        return result
    # end def _show__

    _ask__ = _show__

    def show_error (self, * args, ** kw) :
        """Display an error window using `tk_messageBox'."""
        return apply (self._show__, (tkMessageBox.showerror, ) + args, kw)
    # end def show_error

    def show_warning (self, * args, ** kw) :
        """Display a warning window using `tk_messageBox'."""
        return apply (self._show__, (tkMessageBox.showwarning, ) + args, kw)
    # end def show_warning

    def show_info (self, * args, ** kw) :
        """Display an info window using `tk_messageBox'."""
        return apply (self._show__, (tkMessageBox.showinfo, ) + args, kw)
    # end def show_info

    def ask_question (self, * args, ** kw) :
        """Display a confirmation window (yes/no) using `tk_messageBox'."""
        return apply (self._ask__, (tkMessageBox.askquestion, ) + args, kw)
    # end def ask_question

    def ask_ok_cancel (self, * args, ** kw) :
        """Display a confirmation window (ok/cancel) using `tk_messageBox'."""
        self._set_option ("default", tkMessageBox.OK, kw)
        return apply (self._ask__, (tkMessageBox.askokcancel, ) + args, kw)
    # end def ask_ok_cancel

    def ask_yes_no (self, * args, ** kw) :
        """Display a confirmation window (yes/no) using `tk_messageBox'."""
        self._set_option ("default", tkMessageBox.YES, kw)
        return apply (self._ask__, (tkMessageBox.askyesno, ) + args, kw)
    # end def ask_yes_no

    def ask_yes_no_cancel (self, * args, ** kw) :
        """Display a confirmation window (yes/no/cancel) using
           `tk_messageBox'.
        """
        self._set_option ("default", tkMessageBox.YES, kw)
        kw ["type"] = tkMessageBox.YESNOCANCEL
        return apply ( self._ask__
                     , (tkMessageBox._show, ) + args
                     , kw
                     )
    # end def ask_yes_no_cancel

    def ask_retry_cancel (self, * args, ** kw) :
        """Display a confirmation window (retry/cancel) using
           `tk_messageBox'.
        """
        self._set_option ("default", tkMessageBox.RETRY, kw)
        return apply (self._ask__, (tkMessageBox.askretrycancel, ) + args, kw)
    # end def ask_retry_cancel

    def busy_cursor (self, cursor = "watch", widget = None) :
        """Display a busy cursor until application becomes idle."""
        self._busy_cursor (cursor, widget)
    # end def busy_cursor

    def _busy_cursor (self, cursor = "watch", widget = None) :
        if not widget : widget = self
        if (  (not hasattr (widget, "saved_cursor"))
           or widget.saved_cursor is None
           ) :
            widget.saved_cursor = widget.cget ("cursor")
        widget.configure        (cursor = cursor)
        widget.update_idletasks ()
    # end def _busy_cursor

    def normal_cursor (self, widget = None) :
        """Display normal cursor."""
        self._normal_cursor (widget)
    # end def normal_cursor

    def _normal_cursor (self, widget = None) :
        if not widget : widget = self
        if (   hasattr (widget, "saved_cursor")
           and widget.saved_cursor is not None
           ) :
            widget.configure        (cursor = widget.saved_cursor)
            widget.update_idletasks ()
            widget.saved_cursor = None
    # end def _normal_cursor

    def _menu_selection_cmd (self, event, cmd) :
        w = self.focus_lastfor ()
        if w :
            ### stolen from /usr/lib/tk8.0/console.tcl
            self.tk.call ('event', 'generate', str (w), cmd)
    # end def _menu_selection_cmd

    def menu_copy_cmd (self, event = None) :
        """Copy selection."""
        return self._menu_selection_cmd (event, "<<Copy>>")
    # end def menu_copy_cmd

    def menu_cut_cmd (self, event = None) :
        """Cut selection."""
        return self._menu_selection_cmd (event, "<<Cut>>")
    # end def menu_cut_cmd

    def menu_paste_cmd (self, event = None) :
        """Paste selection."""
        return self._menu_selection_cmd (event, "<<Paste>>")
    # end def menu_paste_cmd

    def define_edit_menu (self, master, menu_class = Menu, ** kw) :
        """Define a menu for cut/copy/paste functions."""
        self.edit_menu = apply (menu_class, (master, ), kw)
        self.edit_menu.add_command \
            ( label       = "Cut"
            , command     = self.menu_cut_cmd
            , underline   = 2
            , accelerator = virtual_key_name ("<<Cut>>")
            )
        self.edit_menu.add_command \
            ( label       = "Copy"
            , command     = self.menu_copy_cmd
            , accelerator = virtual_key_name ("<<Copy>>")
            , underline   = 0
            )
        self.edit_menu.add_command \
            ( label       = "Paste"
            , command     = self.menu_paste_cmd
            , accelerator = virtual_key_name ("<<Paste>>")
            , underline   = 4
            )
        return self.edit_menu
    # end def define_edit_menu

    def set_maxsize (self, x = None, y = None, x_margin = 0, y_margin = 0) :
        """Set maximum size of `self's toplevel window to `x', `y'

           (or screen `width - x_margin' and `height - y_margin', if any of
           them is not passed in)
        """
        x_max = self.winfo_screenwidth  () - x_margin # - 20
        y_max = self.winfo_screenheight () - y_margin # - 20
        x     = max                     (x or x_max, x_max)
        y     = max                     (y or y_max, y_max)
        self.winfo_toplevel             ().maxsize (x, y)
        return x, y
    # end def set_maxsize

    def _bind_completer (self, widget, action) :
        for ev in ("<<complete>>", "<Alt-space>") :
            widget.bind (ev, action)
    # end def _bind_completer

    def save_geometry (self, state_mgr, name, widget = None) :
        """Save `widget's (default: self) geometry in `state_mgr's dictionary
           `window_geometry' under key `name'
        """
        w = (widget or self).winfo_toplevel ()
        if state_mgr and name :
            g      = w.geometry           ()
            mw, mh = w.minsize            ()
            ww, wh = w.winfo_width        (), w.winfo_height       ()
            sw, sh = w.winfo_screenwidth  (), w.winfo_screenheight ()
            x,  y  = w.winfo_rootx        (), w.winfo_rooty        ()
            ### print name, x, y, g, mh, wh, sh, mw, ww, sw
            ### print sh -wh, sw - ww
            if (   g
               and (wh >= max (mh, 50) and ww >= max (mw, 50))
               and (sh - wh > 100 and sw - ww > 70)
               ) :
                ### don't register an uninitialized geometry
                ### don't register full screen geometry
                ### (100 and 70 are just out of thin air -- they depend on
                ### the style of window and screen decoration added by the
                ### window manager, e.g., a horizontal or vertical task bar
                ### in WNT, ...)
                state_mgr.window_geometry [name] = g
    # end def save_geometry

# end class CT_TK_mixin

class C_Frame_ (CT_TK_mixin, Frame) :
    def __init__ (self, master = None, name = None, class_ = Frame, ** kw) :
        if name :
            name = name.lower   ()
            name = name.replace (".", "_")
        self.name = name
        Frame.__init__ (self, master, name = name, class_ = class_)
        self.wtk_widget = self
        if kw :
            self.configure (** kw)
    # end def __init__
# end class C_Frame_

class C_Frame  (C_Frame_) :
    def __init__ (self, master = None, name = None, class_ = Frame, ** kw) :
        apply (C_Frame_.__init__, (self, master, name, class_), kw)
    # end def __init__
# end class C_Frame

class C_Text (C_Frame) :
    """Provide a text widget inside a C_Frame"""

    widget_class = "C_Text"
    body_name    = "text"
    ipadx        = ipady = 0
    padx         = pady  = 1

    _auto_delegate       = dict_from_list \
        ( ( "bind"
          , "index"
          , "mark_set"
          , "mark_unset"
          , "search"
          , "tag_add"
          , "tag_bind"
          , "tag_configure"
          , "tag_remove"
          )
        )

    def __init__ (self, master, name = None, state = NORMAL, ** kw) :
        apply (self._init_head, (master, name, state), kw)
        self._init_tail ()
    # end def __init__

    def _init_head (self, master, name, state, ** kw) :
        C_Frame.__init__           ( self, master
                                   , class_         = self.widget_class
                                   , name           = name
                                   )
        self.state     = state
        self.body      = Text      ( self
                                   , name           = self.body_name
                                   )
        if kw : apply              ( self.body.configure, (), kw)
        if state == DISABLED :
            self.disable ()
            self.state = NORMAL
    # end def _init_head

    def _init_tail (self) :
        self._set_grid             ()
        self.body.mark_set         ( "at_end", self.body.index (INSERT))
        self.last_key = None
    # end def _init_tail

    __class_bindtag = class_btag = None

    def disable (self) :
        bt = self.body.bindtags ()
        if "Text" not in bt : return
        i  = list (bt).index ("Text")
        if not self.__class_bindtag :
            self._copy_class_bindings ()
        self.body.bindtags (bt [:i] + (self.__class_bindtag,) + bt [i+1:])
    # end def disable

    def _copy_class_bindings (self) :
        self.class_btag = C_Text.__class_bindtag = bt = "C_Text"
        for seq in ( '<<Copy>>', '<B1-Enter>', '<B1-Leave>'
                   , '<B1-Motion>', '<B2-Motion>', '<Button-1>'
                   , '<ButtonRelease-1>', "<Control-Button-1>"
                   , "<Control-Key-Down>", "<Control-Key-End>"
                   , "<Control-Key-Home>", "<Control-Key-Left>"
                   , "<Control-Key-Next>", "<Control-Key-Prior>"
                   , "<Control-Key-Right>", "<Control-Key-Up>"
                   , "<Control-Key-a>", "<Control-Key-b>"
                   , "<Control-Key-e>", "<Control-Key-f>"
                   , "<Control-Key-n>", "<Control-Key-p>"
                   , "<Control-Key-space>", "<Control-Key-v>"
                   , "<Control-Shift-Key-Down>", "<Control-Shift-Key-End>"
                   , "<Control-Shift-Key-Home>", "<Control-Shift-Key-Left>"
                   , "<Control-Shift-Key-Right>", "<Control-Shift-Key-Up>"
                   , "<Control-Shift-Key-space>", "<Double-Button-1>"
                   , "<Double-Shift-Button-1>", "<Key-Down>"
                   , "<Key-End>", "<Key-Home>", "<Key-Left>", "<Key-Next>"
                   , "<Key-Prior>", "<Key-Right>", "<Key-Select>", "<Key-Up>"
                   , "<Shift-Button-1>", "<Shift-Key-Down>"
                   , "<Shift-Key-End>", "<Shift-Key-Home>"
                   , "<Shift-Key-Left>", "<Shift-Key-Next>"
                   , "<Shift-Key-Prior>", "<Shift-Key-Right>"
                   , "<Shift-Key-Select>"
                   , "<Triple-Button-1>", "<Triple-Shift-Button-1>"
                   ) :
            self.body.bind_class (bt, seq, self.body.bind_class ("Text", seq))
    # end def _copy_class_bindings

    def _set_grid (self) :
        self.body.grid             ( sticky         = "ewns"
                                   , column         = 0
                                   , row            = 0
                                   , padx           = self.padx
                                   , pady           = self.pady
                                   , ipadx          = self.ipadx
                                   , ipady          = self.ipady
                                   )
        self.grid_columnconfigure  ( 0, weight = 1)
        self.grid_rowconfigure     ( 0, weight = 1)
    # end def _set_grid

    def ignore (self, event = None) :
        key    = event.keysym
        result = "break"
        if key in ("Control_L", "Control_R") : key = "Control"
        if (  (   self.last_key == "Control"
              and key.lower () in ("c", "o", "w", "s")
              )
           or (key in ( "Control", "Next", "Prior"
                      , "Up", "Down", "Home", "End", "Left", "Right"
                      )
              )
           ) :
            result = ""
        self.last_key = key
        return result
    # end def ignore

    def get (self, head = START, tail = END) :
        return self.body.get (head, tail)
    # end def get

    def put (self, text, * tags) :
        apply (self.insert,   (END, text, ) + tags)
        self.update_idletasks ()
    # end def put

    write = put

    def insert (self, * args, ** kw) :
        """Insert text into `self.body'."""
        try     :
            self.body.configure (state = NORMAL)
            apply               (self.body.insert, args, kw)
        finally :
            self.body.configure (state = self.state)
    # end def insert

    def delete (self, * args, ** kw) :
        """Delete text from `self.body'."""
        try     :
            self.body.configure (state = NORMAL)
            apply               (self.body.delete, args, kw)
        finally :
            self.body.configure (state = self.state)
    # end def delete

    def delete_tagged (self, tag) :
        """Delete all text tagged by `tag'."""
        ranges = self.body.tag_ranges (tag)
        n      = len (ranges)
        i      = 0
        while i < n :
            head, tail = ranges [i:i+2]
            i          = i + 2
            self.delete (head, tail)
    # end def delete_tagged

    def clear (self) :
        """Clear `self.body' (i.e., remove all text from the widget)."""
        self.delete (START, END)
    # end def clear

    def busy_cursor (self, cursor = "watch") :
        self._busy_cursor   (cursor, self.body)
        self._busy_cursor   (cursor)
    # end def busy_cursor

    def normal_cursor (self) :
        self._normal_cursor (self.body)
        self._normal_cursor ()
    # end def normal_cursor

    def _place_cursor (self, index) :
        ### Default binding of text widget as shown by wish :
        ### % bind Text <Key-Up>
        ###     tkTextSetCursor %W [tkTextUpDownLine %W -1]
        ### The newest version of TK shows:
        ###     tk::TextSetCursor %W [tk::TextUpDownLine %W -1]
        try :
            self.body.tk.call ("tk::TextSetCursor",  self.body._w, index)
        except TclError :
            self.body.tk.call ("tkTextSetCursor",  self.body._w, index)
    # end def _place_cursor

    def place_cursor (self, index) :
        self._place_cursor    (index)
        self.body.focus_force ()
    # end def place_cursor

    def __getattr__ (self, name) :
        if name in self._auto_delegate :
            return getattr (self.body, name)
        raise AttributeError, name
    # end def __getattr__

# end class C_Text

class Scrolled_Text (C_Text) :
    """Provide a text widget with horizontal and vertical scrollbars."""

    widget_class     = "Scrolled_Text"
    x_scroll_default = True

    def __init__ \
        ( self, master, name = None, state = NORMAL
        , x_scroll = _undefined, ** kw
        ) :
        self._init_head (master, name, state, ** kw)
        self.y_scroll      = Scrollbar ( self, name     = "scroll"
                                       , orient         = VERTICAL
                                       , takefocus      = 0
                                       , command        = self.body.yview
                                       )
        if x_scroll is _undefined :
            x_scroll = self.x_scroll_default
        if x_scroll :
            self.x_scroll  = Scrollbar ( self, name     = "scroll_x"
                                       , orient         = HORIZONTAL
                                       , takefocus      = 0
                                       , command        = self.body.xview
                                       )
            self.body.configure        ( xscrollcommand = self.x_scroll.set
                                       , yscrollcommand = self.y_scroll.set
                                       )
        else :
            self.x_scroll  = None
            self.body.configure        ( yscrollcommand = self.y_scroll.set)
        self._init_tail ()
    # end def __init__

    def _set_grid (self) :
        self.y_scroll.grid         ( sticky         = "ns"
                                   , column         = 1
                                   , row            = 0
                                   , pady           = 1
                                   )
        if self.x_scroll :
            self.x_scroll.grid     ( sticky         = "ew"
                                   , column         = 0
                                   , row            = 1
                                   , padx           = 1
                                   )
        C_Text._set_grid           (self)
    # end def _set_grid

# end class Scrolled_Text

class H_Strut (C_Frame_) :
    """Provide a frame with a controlled minimum horizontal size."""

    strut_class = "H_Strut"

    def __init__ ( self, master
                 , strut_name  = None
                 , strut_class = None
                 , strut_width = 0
                 , ** kw
                 ) :
        apply (C_Frame_.__init__, (self, master), kw)
        self.h_strut = Frame ( self
                             , name        = strut_name
                             , class_      = strut_class or self.strut_class
                             , height      = 0
                             , borderwidth = 0
                             , relief      = FLAT
                             )
        if strut_width :     self.h_strut.configure (width = strut_width)
        self.h_strut.pack    (side = TOP)
    # end def __init__

# end class H_Strut

class V_Strut (C_Frame_) :
    """Provide a frame with a controlled minimum vertical size."""

    strut_class = "V_Strut"

    def __init__ ( self, master
                 , strut_name   = None
                 , strut_class  = None
                 , strut_height = 0
                 , ** kw
                 ) :
        apply (C_Frame_.__init__, (self, master), kw)
        self.v_strut = Frame ( self
                             , name        = strut_name
                             , class_      = strut_class or self.strut_class
                             , width       = 0
                             , height      = strut_height
                             , borderwidth = 0
                             , relief      = FLAT
                             )
        self.v_strut.pack    (side = LEFT)
    # end def __init__

# end class V_Strut

class Statusframe_ (C_Frame) :
    """Root class for help frames."""

    widget_class = "Statusframe"

    def __init__ (self, master, name = None) :
        C_Frame.__init__ \
            (self, master, class_ = self.widget_class, name = name)
        self.txt_widget = self.Inner_Widget ( self
                                            , name   = "text"
                                            , relief = FLAT
                                            , borderwidth = 0
                                            , cursor      = "top_left_arrow"
                                            )
        self.txt_widget.pack                ( fill   = BOTH
                                            , expand = YES
                                            , side   = LEFT
                                            , padx   = 4
                                            , pady   = 1
                                            )
        self.backg      = self.txt_widget.cget ("background")
        self.foreg      = self.txt_widget.cget ("foreground")
        self.help_bg    = self.option_value    ("helpBackground",  "yellow")
        self.help_fg    = self.option_value    ("helpForeground",  "red")
        self.error_bg   = self.option_value    ("errorBackground", "cyan")
        self.error_fg   = self.option_value    ("errorForeground", "black")
        self.stack      = []
    # end def __init__

    def put_help (self, text) :
        self._activate (text, self.help_bg, self.help_fg)
    # end def put_help

    def push_help  (self, text) :
        self._push (text, self.put_help, self.help_bg, self.help_fg)
    # end def push_help

    def push_err_msg (self, text) :
        self._push   (text, self.put_err_msg, self.error_bg, self.error_fg)
    # end def push_err_msg

    def _push (self, text, fct, bg = None, fg = None) :
        save = self.text ()
        if save : self.stack.insert (1, (fct, save))
        self._activate (text, bg or self.help_bg, fg or self.help_fg)
    # end def _push

    def pop (self) :
        if self.stack :
            saved = self.stack [0]
            del self.stack [0]
            saved [0] (saved [1])
        else :
            self.deactivate ()
    # end def pop

    pop_help = pop_err_msg = pop

    def put_err_msg (self, text) :
        self._activate (text, self.error_bg, self.error_fg)
    # end def put_err_msg

    def busy_cursor (self, cursor = "watch") :
        self._busy_cursor   (cursor, self.txt_widget)
        self._busy_cursor   (cursor)
    # end def busy_cursor

    def normal_cursor (self) :
        self._normal_cursor (self.txt_widget)
        self._normal_cursor ()
    # end def normal_cursor

# end class Statusframe_

class Statustext (Statusframe_) :
    """Provide help frame using a text widget."""

    widget_class = "Statustext"

    Inner_Widget = Text

    def __init__ (self, master, name = None) :
        Statusframe_.__init__     ( self, master, name = name)
        self.txt_widget.configure ( background = self.backg
                                  , foreground = self.foreg
                                  , state      = DISABLED
                                  , wrap       = "word"
                                  , width      = 0
                                  )
        self.y_scroll = Scrollbar ( self, name = "scroll"
                                  , orient     = VERTICAL
                                  , takefocus  = 0
                                  , command    = self.txt_widget.yview
                                  )
        self.y_scroll.pack        ( fill       = Y
                                  , side       = RIGHT
                                  , pady       = 1
                                  )
        self.txt_widget.configure (yscrollcommand = self.y_scroll.set)
    # end def __init__

    def text (self) :
        return self.txt_widget.get (START, END)
    # end def text

    def _activate (self, text, bg, fg) :
        if text :
            self.update_idletasks ()
            self.txt_widget.configure ( state      = NORMAL)
            self.txt_widget.delete    ( START, END)
            self.txt_widget.insert    ( END,   text)
            self.txt_widget.configure ( background = bg
                                      , foreground = fg
                                      , state      = DISABLED
                                      )
            self.configure            ( background = bg)
    # end def _activate

    def deactivate (self) :
        self.txt_widget.configure ( state      = NORMAL)
        self.txt_widget.delete    ( START, END)
        self.txt_widget.configure ( background = self.backg
                                  , foreground = self.foreg
                                  , state      = DISABLED
                                  )
        self.configure            ( background = self.backg)
    # end def deactivate

# end class Statustext

class Statuslabel (Statusframe_) :
    """Provide help frame using a label widget."""

    widget_class = "Statuslabel"

    Inner_Widget = Label

    def __init__ (self, master, name = None) :
        Statusframe_.__init__  (self, master, name = name)
    # end def __init__

    def text (self) :
        return self.txt_widget.cget ("text")
    # end def text

    def _activate (self, text, bg, fg) :
        if text :
            self.update_idletasks ()
            self.txt_widget.configure ( text       = text
                                      , wraplength = self.winfo_width () * 0.85
                                      , background = bg
                                      , foreground = fg
                                      )
            self.configure            ( background = bg)
    # end def _activate

    def deactivate (self) :
        self.txt_widget.configure ( text        = ""
                                  , background = self.backg
                                  , foreground = self.foreg
                                  )
        self.configure            ( background = self.backg)
    # end def deactivate

# end class Statuslabel

class Message_Window (C_Text) :
    """Provide a scrollable window for status messages."""

    widget_class = "Message_Window"

    def __init__ ( self, master
                 , name = None, state = NORMAL, width = 0, fill = X
                 ) :
        self._init_head               ( master, name, state
                                      , relief        = FLAT
                                      , wrap          = "word"
                                      , width         = width
                                      , borderwidth   = 0
                                      , cursor        = "top_left_arrow"
                                      , insertofftime = 0
                                      )
        self.txt_widget = self.body
        self.fill       = fill
        self.y_scroll   = Scrollbar   ( self, name    = "scroll"
                                      , orient        = VERTICAL
                                      , takefocus     = 0
                                      , command       = self.txt_widget.yview
                                      )
        self.txt_widget.configure     (yscrollcommand = self.y_scroll.set)
        self.txt_widget.tag_configure ("all",       lmargin2 = "1c")
        self.disable                  ()
        self.hlp_lvl = 0
        self._init_tail               ()
    # end def __init__

    def _set_grid (self) :
        self.txt_widget.pack      ( fill        = self.fill
                                  , expand      = YES
                                  , side        = LEFT
                                  , padx        = 4
                                  , pady        = 1
                                  )
        self.y_scroll.pack        ( fill        = Y
                                  , side        = RIGHT
                                  , pady        = 1
                                  )
    # end def _set_grid

    def insert (self, pos, text, * tags) :
        try     :
            if "help" not in tags :
                self.clear_help ()
            self.txt_widget.configure (state  = NORMAL)
            self.txt_widget.insert    (pos, text, tags + ("all", ))
            self.txt_widget.see       (pos)
            if text and text [-1] == "\n" :
                ### avoid an empty line at the end of the widget
                self.txt_widget.yview ("scroll", -1, "units")
        finally :
            self.txt_widget.configure (state  = self.state)
    # end def insert

    def see (self, pos) :
        """Scroll text widget so that `pos' is visible."""
        self.txt_widget.see (pos)
        if pos == END :
            last = self.txt_widget.get (pos)
        else :
            last = self.txt_widget.get (pos + " -1 char")
        if last and last == "\n" :
            ### avoid an empty line at the end of the widget
            self.txt_widget.yview ("scroll", -1, "units")
    # end def see

    def replace_matches (self, pattern, repl = "", head = START, tail = END) :
        """Replaces all occurrences of regular expression `pattern' between
           indices `head' and `tail' with `repl'.
        """
        old_text = self.txt_widget.get (head, tail)
        new_text = re.sub (pattern, repl, old_text)
        if old_text != new_text :
            self.delete (head, tail)
            self.insert (tail, new_text)
    # end def replace_matches

    def clear_help (self) :
        self.delete_tagged ("help")
        self.hlp_lvl = 0
    # end def clear_help

    def put_help (self, text) :
        self.clear_help ()
        if text and text [-1] != "\n" :
            text = text + "\n"
        self.put (text, "help")
    # end def put_help

    def push_help  (self, text) :
        self.hlp_lvl = self.hlp_lvl + 1
        tag          = "help_%s" % self.hlp_lvl
        if text and text [-1] != "\n" :
            text = text + "\n"
        self.put (text, "help", tag)
    # end def push_help

    push_err_msg = push_help

    def pop (self) :
        tag          = "help_%s" % self.hlp_lvl
        self.hlp_lvl = max (self.hlp_lvl - 1, 0)
        self.delete_tagged (tag)
    # end def pop

    pop_help = pop_err_msg = pop

# end class Message_Window

class Progress_Gauge (C_Frame) :
    """Provide a widget for displaying a progress gauge."""

    widget_class = "Progress_Gauge"

    cycle        = False
    show_percent = True

    dx = 20

    def __init__ ( self, master
                 , name             = None
                 , label            = ""
                 , active           = False # after creation window is inactive
                 , cursor           = "watch"
                 , cancel_button    = False
                 ) :
        C_Frame.__init__    \
            ( self, master
            , name        = name
            , class_      = self.widget_class
            , relief      = RAISED
            , borderwidth = 3
            , cursor      = cursor
            )
        self.ht       = self.num_opt_val  ("height",       40)
        self.wd       = self.num_opt_val  ("width",       200)
        self.bar_ht   = self.num_opt_val  ("gaugeHeight",  20)
        self.bar_wd   = self.num_opt_val  ("gaugeWidth",  180)
        self.color    = self.option_value ("gaugeColor",  "blue")
        self.ht       = max               (self.ht, self.bar_ht + 40)
        self.wd       = max               (self.wd, self.bar_wd + self.dx)
        self.upper    = C_Frame (self, name = "upper")
        self.gauge    = Canvas  \
            ( self.upper
            , name               = "gauge"
            , highlightthickness = 0
            , width              = self.bar_wd
            , height             = self.bar_ht
            )
        self.label    = Label \
            ( self.upper
            , text               = label
            , name               = "label"
            , width              = 40
            , anchor             = CENTER
            )
        Rectangle \
            ( self.gauge
            , (0, 0), (0, self.bar_ht)
            , fill         = self.color
            , outline      = ""
            , width        = 0
            , tags         = "bar"
            )
        CanvasText \
            ( self.gauge
            , (self.bar_wd // 2, self.bar_ht // 2)
            , anchor       = CENTER
            , text         = ""
            , tags         = "value"
            )
        if cancel_button :
            self.lower    = C_Frame ( self, name = "lower")
            self.button   = Button \
                ( self.lower
                , text    = "Cancel"
                , command = self.kb_interrupt
                )
            self.ht       = self.ht + 20
        else :
            self.button   = None
        self._kbi_pending = None
        self._activations = 0
        self.reset (label)
        if active :
            self.activate ()
        self.configure    (width  = self.wd, height = self.ht)
    # end def __init__

    def activate (self, cycle = False) :
        self.cycle         = bool (cycle)
        self.show_percent  = not cycle
        self._activations += 1
        self.pack       (expand = YES, fill = BOTH)
        self.upper.pack (expand = YES, fill = BOTH)
        if self.button :
            self.lower.pack   (fill = X)
            self.button.pack  (side = BOTTOM)
            try :
                self.grab_set ()
            except TclError :
                ### ignore errors resulting from another window already
                ### having the grab (which happens if user repositions the
                ### main window, for instance)
                pass
        self.gauge.place \
            ( relx   = 0.5
            , rely   = 0.66
            , anchor = CENTER
            )
        self.label.place \
            ( relx   = 0.5
            , rely   = 0.20
            , anchor = CENTER
            )
        self._kbi_pending = None
    # end def activate

    def deactivate (self, force = False) :
        self._activations -= 1
        if force or self._activations <= 0 :
            self._activations = 0
            if self.button :
                try :
                    self.grab_release ()
                except TclError :
                    ### ignore errors resulting from another window already
                    ### having the grab (which happens if user repositions the
                    ### main window, for instance)
                    pass
            self.pack_forget ()
    # end def deactivate

    def reset (self, label = None, g_range = 100, g_delta = 1, cycle = False) :
        self.cycle        = bool (cycle)
        self.show_percent = not cycle
        if g_range < 0 :
            ### This is an error of the caller
            raise ValueError, "Range must be positive (got %d)" % g_range
        if label :
            self.set_label (label)
        self.set_value (0)
        self._g_range = g_range
        self._g_delta = g_delta
        self._g_index = 0
        self._g_value = 0
    # end def reset

    def inc (self, delta = 1) :
        cycle = self.cycle
        delta = (delta * (cycle or 1))
        gi    = self._g_index = self._g_index + delta
        gv    = self._g_value = self._g_value + delta
        gr    = self._g_range
        if abs (gv) >= self._g_delta :
            if cycle :
                if gi > gr:
                    self._g_index = gi = gr - delta
                    self.cycle    = -1
                elif gi < 0 :
                    self._g_index = gi = abs (delta)
                    self.cycle    = +1
            val = (100.0 * gi) // gr
            self.set_value (val)
            self._g_value = 0
        elif self.button :
            self._update_and_check_kbi ()
    # end def inc

    def set_label (self, text) :
        self.label.configure (text = text)
        self.label.place \
            ( relx   = 0.5
            , rely   = 0.20
            , anchor = CENTER
            )
    # end def set_label

    def set_value (self, value) :
        value = max (value, 0)
        value = min (value, 100)
        head  = 0
        tail  = 0.01 * value * self.bar_wd
        if self.cycle :
            head = tail - 0.05 * self.bar_wd
        self.gauge.coords ("bar", head, 0, tail, self.bar_ht)
        text = ""
        if self.show_percent :
            text = "%3d%%" % (value, )
        self.gauge.itemconfigure ("value", text = text)
        self._update_and_check_kbi ()
    # end def set_value

    def _update_and_check_kbi (self) :
        if self.button :
            self.update           ()
        else :
            self.update_idletasks ()
        if self._kbi_pending :
            self._kbi_pending = None
            raise KeyboardInterrupt
    # end def _update_and_check_kbi

    def kb_interrupt (self, event = None) :
        self._kbi_pending = 1
    # end def kb_interrupt

# end class Progress_Gauge

class Progress_Gauge_T (CT_TK_mixin, Toplevel) :
    """Provide a toplevel widget containing a Progress_Gauge"""

    widget_class = "Progress_Gauge"

    def __init__ ( self, master
                 , name             = None
                 , label            = ""
                 , active           = 0 # after creation window is inactive
                 , cursor           = "watch"
                 , title            = ""
                 , cancel_button    = 0
                 ) :
        Toplevel.__init__ \
            ( self, master
            , name          = name
            , class_        = self.widget_class
            , cursor        = cursor
            )
        self.withdraw       ()
        self.gauge = Progress_Gauge \
            ( self, "frame", label, active, cursor
            , cancel_button = cancel_button
            )
        self.bg    = self.gauge.cget ("background")
        self.configure \
            ( width         = self.gauge.wd
            , height        = self.gauge.ht
            , background    = self.bg
            )
        self.protocol       ("WM_DELETE_WINDOW", self.withdraw)
        if active :
            self.activate   (title)
        else :
            self.deactivate ()
        if cancel_button :
            self.transient  (master)
            self.withdraw   ()
    # end def __init__

    def activate \
        (self, title = "", label = " ", g_range = 100, g_delta = 1
        , cycle = False
        ) :
        x = ( self.master.winfo_rootx ()
            + (self.master.winfo_width () - self.gauge.wd) // 2
            )
        y = ( self.master.winfo_rooty ()
            + (self.master.winfo_height () - self.gauge.ht) // 2
            )
        self.reset     (label, g_range, g_delta, cycle = cycle)
        self.deiconify ()
        self.tkraise   ()
        self.geometry \
            ("%dx%d+%d+%d" % (self.gauge.wd, self.gauge.ht, x, y))
        if sos.name == "nt" : self.update ()
        ### without the following statement the window is transparent under
        ### WindowsNT
        self.configure         (background = self.bg)
        self.gauge.activate    (cycle = cycle)
        self.focus_set         ()
        if title :
            self.title         (title)
            if label == " " :
                self.set_label (title)
            self.update        ()
    # end def activate

    def deactivate (self, force = False) :
        try :
            if force or self.gauge._activations <= 1 :
                self.withdraw ()
            self.gauge.deactivate (force = force)
        except TclError :
            pass
    # end def deactivate

    def reset (self, * args, ** kw) :
        self.gauge.reset (* args, ** kw)
    # end def reset

    def inc (self, * args, ** kw) :
        self.gauge.inc (* args, ** kw)
    # end def inc

    def set_label (self, * args, ** kw) :
        self.gauge.set_label (* args, ** kw)
    # end def set_label

    def set_value (self, * args,  ** kw) :
        self.gauge.set_value (* args, ** kw)
    # end def set_value

# end class Progress_Gauge_T

class C_Button (CT_TK_mixin, Button) :

    def __init__ (self, master = None, name = None, ** kw) :
        self._set_options ( kw
                          , name      = name.lower ()
                          , takefocus = 0
                          , text      = name
                          )
        apply             (Button.__init__, (self, master), kw)
        self.name = name
    # end def __init__

# end class C_Button

class Buttongroup (CT_TK_mixin) :
    """Provide group of buttons.

       The buttons are accessible by index or name. The can be activated and
       deactivated as a group. One button of the group can be
       button-activated as the default button.
    """

    widget_class  = "Buttongroup"

    balloon_owner = None

    def __init__ ( self
                 , help          = None
                 , height        = None
                 , width         = None
                 , buttonstate   = NORMAL
                 , bindtag       = None
                 , auto_pop_help = 1
                 , balloon       = None
                 ) :
        self.help          = help
        self.balloon       = balloon
        self.height        = height
        self.width         = width
        self.buttonstate   = buttonstate
        self.bindtag       = bindtag
        self.auto_pop_help = auto_pop_help
        self.button        = NO_List ()
        self.cmd_map       = {}
        self.active        = None
        self.pending       = None
        self.helped        = None
    # end def __init__

    def add ( self, master, button_name
            , before      = None
            , bindtag     = None
            , default     = NORMAL
            , height      = None
            , width       = None
            , cmd_name    = None
            , ** kw
            ) :
        """Add a button with name `button_name' and parent widget `master'."""
        i       = self._index (before)
        width   = width  or self.width
        height  = height or self.height
        is_text = not (kw.get ("bitmap") or kw.get ("image"))
        if height and width :
            if is_text :
                master = Frame        (master, height = height, width  = width)
                master.pack_propagate (0)
                is_framed = 1
            else :
                is_framed = 0
        else :
            is_framed = 0
            if is_text :
                self._set_option  ("width", width, kw)
        self._set_option          ("state", self.buttonstate, kw)
        self._set_option          ( "highlightbackground"
                                  , master.cget ("background")
                                  , kw
                                  )
        button = C_Button         (master, button_name, ** kw)
        self.button.insert        (i, button)
        button._is_framed = is_framed
        button._is_text   = is_text
        button._cmd_name  = cmd_name or button_name
        if button._is_framed :
            button.pack (fill = BOTH, expand = YES)
        if default == ACTIVE :
            self.buttonactivate (button_name)
        if self.help :
            if kw.has_key ("command") :
                self.cmd_map [button.cget ("text")] = kw ["command"]
                self.cmd_map [i]                    = kw ["command"]
            button.bind ("<Enter>", self.put_button_help)
            if self.auto_pop_help :
                button.bind ("<Leave>", self.pop_button_help)
        if bindtag or self.bindtag :
            add_bindtag (button, bindtag or self.bindtag)
        return button
    # end def add

    def put_button_help (self, event = None) :
        if event : button = event.widget
        else     : return
        state = button.cget ("state")
        try :
            label = button.cget  ("text")
            cmd   = self.cmd_map [label]
            try :
                msg = cmd.im_self.button_help (label, cmd, cmd.__doc__)
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                msg = cmd.__doc__
            msg = msg.strip ()
            if   self.balloon and (state == NORMAL or not button._is_text) :
                if button._is_text :
                    b_msg = msg
                else :
                    b_msg = button._cmd_name
                    if self.help :
                        self.help.push_help (msg)
                        self.helped = button
                self.__class__.balloon_owner = self
                self.balloon.activate ( button, b_msg
                                      , x     = event.x_root - event.x
                                      , y     = event.y_root - event.y
                                      , delay = 500
                                      )
            elif self.help :
                self.help.push_help (msg)
                self.helped = button
        except (SystemExit, KeyboardInterrupt), exc :
            raise
        except :
            pass
    # end def put_button_help

    def pop_button_help (self, event = None) :
        if self.balloon_owner :
            self.balloon_owner.balloon.deactivate ()
            self.balloon_owner.active_help = None
            self.__class__.balloon_owner   = None
        if self.helped :
            self.help.pop_help ()
            self.helped = None
    # end def pop_button_help

    def _index (self, b) :
        button = self.button
        length = len (button)
        if b is None :
            return length
        elif isinstance (b, (str, unicode)) :
            try :
                return button.n_index (b)
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                return length
        else :
            return min (b, length)
    # end def _index

    def activate (self) :
        """Activates all buttons of button box."""
        self._change_state (NORMAL)
        if self.active :
            self.buttonconfigure (self.active, default = ACTIVE)
    # end def activate

    enable = activate

    def deactivate (self) :
        """Deactivates all buttons of button box."""
        self._change_state (DISABLED)
    # end def deactivate

    disable = deactivate

    def _change_state (self, state) :
        self.buttonstate = state
        map (lambda b, s = state : b.configure (state = s), self.button)
    # end def _change_state

    def enable_entry (self, button) :
        self.button [button].configure (state = NORMAL)
    # end def enable_entry

    def disable_entry (self, button) :
        self.button [button].configure (state = DISABLED)
    # end def disable_entry

    def buttonactivate  (self, button) :
        if self.active :
            self.buttonconfigure (self.active, default = NORMAL) # DISABLED
        if button :
            self.buttonconfigure (button,      default = ACTIVE)
        self.active = button
    # end def buttonactivate

    def buttonconfigure (self, button, ** kw) :
        apply (self.button [button].configure, (), kw)
        if self.help :
            if kw.has_key ("text") :
                if kw.has_key ("command") :
                    self.cmd_map [kw ["text"]] = kw ["command"]
                else :
                    self.cmd_map [kw ["text"]] = self.cmd_map [button]
    # end def buttonconfigure

    def buttonbind (self, button, * args, ** kw) :
        """Call `bind' for `button'"""
        apply (self.button [button].bind, args, kw)
    # end def buttonbind

    def flash     (self, button) : self.button [button].flash     ()
    def invoke    (self, button) : self.button [button].invoke    ()
    def focus_set (self, button) : self.button [button].focus_set ()

    def _info (self) :
        for b in self.button :
            f = b
            if b._is_framed : f = b.master
            print "%-10s: (%s) [%s, %s] [%s, %s] [%s, %s]" % \
                  ( b ["text"]
                  , b ["font"]
                  , b ["width"]
                  , b ["height"]
                  , f.winfo_width  ()
                  , f.winfo_height ()
                  , f.winfo_reqwidth  ()
                  , f.winfo_reqheight ()
                  )
    # end def _info

# end class Buttongroup

class Buttongrid (Buttongroup, C_Frame) :
    """Provide geometry management for `Buttongroup'.

       Geometry management for the buttons is done via grid.
    """

    widget_class = "Buttongrid"

    def __init__ ( self, master
                 , name          = None
                 , help          = None
                 , columns       = 32
                 , height        = None
                 , width         = None
                 , padx          = 0
                 , pady          = 0
                 , sticky        = ""
                 , buttonstate   = NORMAL
                 , bindtag       = None
                 , auto_pop_help = 1
                 , balloon       = None
                 , ** kw
                 ) :
        apply (C_Frame.__init__, (self, master, name, self.widget_class), kw)
        height = height or self.num_opt_val  ("pixelHeight", None)
        width  = width  or self.num_opt_val  ("pixelWidth",  None)
        Buttongroup.__init__ ( self, help, height, width
                             , buttonstate, bindtag, auto_pop_help, balloon
                             )
        self.columns     = max (columns, 1)
        self.padx        = padx
        self.pady        = pady
        self.sticky      = sticky
        self.columnspan  = []
        if bindtag : add_bindtag (self, bindtag)
    # end def __init__

    def add ( self, button_name
            , columnspan = 1
            , ** kw
            ) :
        """Add a button with name `button_name'. The button is automatically
           put into the grid.
        """
        button = apply (Buttongroup.add, (self, self, button_name), kw)
        self.columnspan.insert (self._index (button_name), max (columnspan, 1))
        if not self.pending  :
            self.pending = self.after_idle (self.regrid)
        return button
    # end def add

    def regrid (self) :
        gridded = self.grid_slaves ()
        for g in gridded :
            g.grid_forget ()
        c = 0
        for i in range (len (self.button)) :
            c = c + (c % self.columnspan [i])
            b = self.button [i]
            if b._is_framed :
                b = b.master
            b.grid ( row        = c // self.columns
                   , column     = c % self.columns
                   , padx       = self.padx
                   , pady       = self.pady
                   , sticky     = self.sticky
                   , columnspan = self.columnspan [i]
                   )
            c = c + self.columnspan [i]
        self.pending = None
    # end def regrid

    def ungrid (self, button) :
        b = self.button [button]
        if b._is_framed :
            b = b.master
        b.grid_forget ()
    # end def ungrid

# end class Buttongrid

class Buttonboxes (Buttongroup) :
    """Provide geometry management for buttons of `Buttongroup' located in
       any number of frames .

       Geometry management for the buttons is done via pack.
    """

    widget_class = "Buttonboxes"

    def __init__ ( self
                 , name          = None
                 , help          = None
                 , height        = None
                 , width         = None
                 , padx          = 0
                 , pady          = 0
                 , expand        = NO
                 , fill          = None
                 , buttonstate   = NORMAL
                 , bindtag       = None
                 , auto_pop_help = 1
                 , balloon       = None
                 , ** kw
                 ) :
        Buttongroup.__init__ ( self, help, height, width, buttonstate
                             , bindtag, auto_pop_help, balloon
                             )
        self.padx        = padx
        self.pady        = pady
        self.expand      = expand
        self.fill        = fill
    # end def __init__

    def add ( self, master, button_name
            , side = LEFT
            , ** kw
            ) :
        """Add a button with name `button_name'"""
        button = Buttongroup.add (self, master, button_name, ** kw)
        button._pack_side = side
        self._button_pack (button)
        return button
    # end def add

    def _button_pack (self, button) :
        side = button._pack_side
        if button._is_framed :
            button = button.master
        button.pack ( side   = side
                    , padx   = self.padx
                    , pady   = self.pady
                    , expand = self.expand
                    , fill   = self.fill
                    )
    # end def _button_pack

    def repack (self)         :
        map (self._button_pack, self.button)
    # end def repack

    def unpack (self, button_name) :
        button = self.button [button_name]
        if button._is_framed :
            button = button.master
        button.pack_forget ()
    # end def unpack

# end class Buttonboxes

class Balloon (CT_TK_mixin, Toplevel) :
    """Provide balloon help widget."""

    widget_class = "Balloon"
    instance     = None

    def __init__ ( self, master
                 , offx     = 20
                 , offy     = -5
                 , delay    = 500 # delay before activation of balloon in ms
                 , name     = None
                 , arrow    = 1
                 ) :
        if name : name = name.lower ()
        Toplevel.__init__     ( self, master
                              , class_      = self.widget_class
                              , name        = name
                              , borderwidth = 1
                              )
        self.overrideredirect (1)
        self.transient        (master.winfo_toplevel ())
        self.withdraw         ()
        self.offx       = offx
        self.offy       = offy
        self.delay      = delay
        self.txt        = None
        self.x = self.y = 0
        self.pending    = None
        frame           = Frame (self,  name = "top", borderwidth = 2)
        self.body       = Label \
            ( frame
            , anchor  = W
            , justify = LEFT
            , name    = "text"
            )
        frame.pack        (fill = X)
        self.body.pack    (side = LEFT, fill = X, padx = 1, pady = 1)
        if arrow :
            arrow       = Label \
                ( frame
                , anchor  = NW
                , bitmap  = bitmap_mgr ["arrow"]
                )
            arrow.pack    (side = LEFT, fill = Y, before = self.body)
        if self.instance is None :
            self.__class__.instance = self
    # end def __init__

    def activate \
        ( self, attachmnt, txt, x = None, y = None, delay = None
        , offx = 0, offy = None
        ) :
        self.deactivate ()
        if txt :
            self.txt     = txt
            x            = x or attachmnt.winfo_rootx  ()
            y            = y or attachmnt.winfo_rooty  ()
            self.x       = x + self.offx + (offx or 0)
            self.y       = y + self.offy + (offy or attachmnt.winfo_height ())
            self.pending = self.after (delay or self.delay, self._show)
    # end def activate

    def deactivate (self) :
        if self.pending :
            self.after_cancel (self.pending)
            self.pending = None
        self.withdraw ()
    # end def deactivate

    def _show (self) :
        # for WinNT the order of the following statements matters !!!
        # the call to `geometry' must be made _after_ `deiconify' !!!
        # otherwise the balloon appears in the upper left corner of the screen
        try     :
            if self.x and self.y :
                self.body.configure (text = self.txt)
                self.deiconify      ()
                self.tkraise        ()
                self.geometry       ("+%d+%d" % (self.x, self.y))
        finally :
            self.pending = None
    # end def _show

# end class Balloon

class C_Listbox (C_Frame) :
    """Customization of listbox class."""

    widget_class = "C_Listbox"

    list_box_height = None

    def __init__ ( self, master, list = (), name = None
                 , selectmode = BROWSE
                 ) :
        C_Frame.__init__ ( self, master, class_ = self.widget_class
                         , name = name
                         )
        self.list_box    = Listbox   ( self
                                     , name             = "listbox"
                                     , selectmode       = selectmode
                                     , exportselection  = 0
                                     , height           = self.list_box_height
                                     )
        lb               = self.list_box
        lb.pack            (side = LEFT, fill = BOTH, expand = YES)
        self._define_keys  ()
        apply              (self.insert, (END,) + tuple (list))
        self.disabled_bg = self.option_value \
            ("disabledBackground", "grey90", lb)
        self.disabled_fg = self.option_value \
            ("disabledForeground", "#a3a3a3", lb)
        self.normal_bg   = lb.cget ("background")
        self.normal_fg   = lb.cget ("foreground")
        self.enabled     = 1
    # end def __init__

    def _define_keys (self) :
        lb   = self.list_box
#        btag = "%s_%d_after_class" % (self.widget_class, id (self))
#        add_bindtag   (lb,   btag, -1)
#        lb.bind_class (btag, "<ButtonRelease-1>",  self.mouse_focus)
        lb.bind       ("<ButtonPress-1>",          self.mouse_select, add=1)
        lb.bind       ("<ButtonRelease-1>",        self.mouse_focus,  add=1)
        lb.bind       ("<Prior>",                  self.key_prior)
        lb.bind       ("<Next>",                   self.key_next)
    # end def _define_keys

    def _change_size (self, event=None) : pass

    def insert (self, * args) :
        apply (self.list_box.insert, args)
        self._change_size ()
    # end def insert

    def delete (self, first, last = None) :
        self.list_box.delete (first, last)
        self._change_size ()
    # end def delete

    def reload (self, list) :
        self.list_box.delete (0, END)
        apply                (self.insert, (0, ) + tuple (list))
    # end def reload

    def indices (self) :
        item = self.list_box.curselection ()
        if item :
            ### `item' should be list of `int',
            ### but Tkinter 1.63 returns strings
            try              : item = map (int, item)
            except TypeError : pass
        return item or ()
    # end def indices

    def index (self) :
        item  = self.indices ()
        i     = None
        if item :
            i = item [0]
        return i
    # end def index

    def mouse_focus (self, event = None) :
        event.widget.focus       ()
        return self.mouse_select (event)
    # end def mouse_focus

    def on_change (self) : pass

    def mouse_select (self, event = None) :
        if self.enabled :
            index = "@%d,%d" % (event.x, event.y)
            self.select (index)
        else :
            return "break"
    # end def mouse_select

    def _mouse_select (self, index) :
        w = self.list_box
        w.select_clear  (0, END)
        w.select_anchor (index)
        w.select_set    (ANCHOR, index)
    # end def _mouse_select

    def select (self, index) :
        w = self.list_box
        w.select_clear  (0, END)
        w.select_set    (index)
        w.activate      (index)
        w.see           (index)
        self.on_change  ()
    # end def select

    def enable (self) :
        """Enable input into widget."""
        if not self.enabled :
            lb = self.list_box
            self.enabled = 1
            lb.configure ( takefocus  = 1
                         , background = self.normal_bg
                         , foreground = self.normal_fg
                         )
            lb.bindtags  (self.__saved_bintags)
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        if self.enabled :
            self.enabled         = 0
            lb                   = self.list_box
            self.__saved_bintags = lb.bindtags ()
            lb.configure ( takefocus  = 0
                         , background = self.disabled_bg
                         , foreground = self.disabled_fg
                         )
            lb.bindtags  ("{}")
    # end def disable

    def prior_index (self, event) :
        index = self.index ()
        delta = max (int (event.widget.cget ("height")) // 2, 1)
        return  max (index - delta, 0)
    # end def prior_index

    def key_prior (self, event) :
        self.select (self.prior_index (event))
    # end def key_prior

    def next_index (self, event) :
        index = self.index ()
        delta = max (int (event.widget.cget ("height")) // 2, 1)
        if index is None :
            index = event.widget.size ()
        return min (index + delta, event.widget.size () - 1)
    # end def next_index

    def key_next (self, event) :
        self.select (self.next_index (event))
    # end def key_next

    def focus_force (self) :
        self.list_box.focus_force ()
    # end def focus_force

    def focus_set (self) :
        self.list_box.focus_set ()
    # end def focus_set

    focus = focus_set
# end class C_Listbox

class C_Listbox_Extended (C_Listbox) :
    """C_Listbox with extended selectmode."""

    def __init__ ( self, master, list = (), name = None
                 , selectmode = EXTENDED
                 ) :
        C_Listbox.__init__ (self, master, list, name, selectmode)
    # end def __init__

    def _define_keys (self) : pass

    def selected_items (self) :
        return map (lambda i,  s = s : s.list_box.get (i), self.indices ())
    # end def selected_items

    def set (self, values) :
        """Add each of the `values' to the current selection"""
        w = self.list_box
        l = list (w.get (0, END))
        w.select_clear  (0, END)
        index = None
        for v in values :
            try :
                index = l.index (v)
                w.select_set    (index)
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                pass
        if index is not None :
            w.activate (index)
            w.see      (index)
    # end def set

# end class C_Listbox_Extended

class Scrolled_Listbox_ :
    """Mixin for scrolled listboxes."""

    def __init__ (self) :
        self.y_scroll_pending = None
        self.y_scroll         = None
    # end def __init__

    def _init_tail (self) :
        self.y_scroll = Scrollbar  ( self, name = "scroll"
                                   , orient     = VERTICAL
                                   , takefocus  = 0
                                   , command    = self.list_box.yview
                                   )
        self.list_box.configure    (yscrollcommand   = self.y_scroll.set)
        self.list_box.bind         ("<Configure>",     self._change_size)
    # end def _init_tail

    def _change_size (self, event=None) :
        if not self.y_scroll_pending :
            self.y_scroll_pending = self.after_idle (self._change_size_pending)
    # end def _change_size

    def _change_size_pending (self, event=None) :
        try :
            self.update_idletasks    ()
            yr = self.list_box.yview ()
            if yr == (0.0, 1.0) :
                self._y_scroll_pack_forget ()
            else :
                self._y_scroll_pack ()
        except TclError :
            pass
        self.y_scroll_pending = None
    # end def _change_size_pending

    def _y_scroll_pack (self) :
        self.y_scroll.pack (side = RIGHT, fill = Y, before = self.list_box)
    # end def _y_scroll_pack

    def _y_scroll_pack_forget (self) :
        self.y_scroll.pack_forget ()
    # end def _y_scroll_pack_forget

# end class Scrolled_Listbox_

class Scrolled_Listbox (Scrolled_Listbox_, C_Listbox) :
    """Listbox with scrollbar."""

    widget_class = "Scrolled_Listbox"

    def __init__ ( self, master, list = (), name = None
                 , selectmode = BROWSE
                 ) :
        Scrolled_Listbox_.__init__ (self)
        C_Listbox.__init__         ( self, master, list
                                   , name       = name
                                   , selectmode = selectmode
                                   )
        self._init_tail            ()
    # end def __init__

# end class Scrolled_Listbox

class Scrolled_Listbox_Extended (Scrolled_Listbox_, C_Listbox_Extended) :
    """Listbox with scrollbar."""

    widget_class = "Scrolled_Listbox"

    def __init__ ( self, master, list = (), name = None
                 , selectmode = EXTENDED
                 ) :
        Scrolled_Listbox_.__init__  (self)
        C_Listbox_Extended.__init__ ( self, master, list
                                    , name       = name
                                    , selectmode = selectmode
                                    )
        self._init_tail             ()
    # end def __init__

# end class Scrolled_Listbox_Extended

class H_Scrolled_Tuple_ :
    """Mixin providing the ability to scroll a set of widgets as a unit."""

    def __init__ (self) :
        self.x_scroll = Scrollbar ( self
                                  , name       = "x_scroll"
                                  , orient     = HORIZONTAL
                                  , takefocus  = 0
                                  , command    = self.xview
                                  )
        self._x_scrolled = []
    # end def __init__

    def xview (self, * args) :
        if not args :
            return self._x_scrolled [0].xview ()
        else :
            for w in self._x_scrolled :
                apply (w.xview, args)
    # end def xview

    def add_h_scrolled (self, * widgets) :
        """Adds all `widgets' to set of widgets scrolled as a unit."""
        for w in widgets :
            clss = w.winfo_class    ()
            self._x_scrolled.append (w)
            w.configure             (xscrollcommand = self.x_scroll.set)
#           w.bind_class            (clss, "<Button-2>",  self.scan_mark)
#           w.bind_class            (clss, "<B2-Motion>", self.scan_dragto)
    # end def add_h_scrolled

    def scan_mark (self, event) :
        map ( lambda w, x = event.x, y = event.y : w.scan_mark (x, y)
            , self._x_scrolled
            )

    def scan_dragto (self, event) :
        map ( lambda w, x = event.x, y = event.y : w.scan_dragto (x, y)
            , self._x_scrolled
            )

# end class H_Scrolled_Tuple_

class V_Scrolled_Tuple_ :
    """Mixin providing the ability to scroll a set of widgets as a unit."""

    def __init__ (self) :
        self.y_scroll = Scrollbar ( self
                                  , name       = "y_scroll"
                                  , orient     = VERTICAL
                                  , takefocus  = 0
                                  , command    = self.yview
                                  )
        self._y_scrolled = []
    # end def __init__

    def yview (self, * args) :
        if not args :
            return self._y_scrolled [0].yview ()
        else :
            for w in self._y_scrolled :
                apply (w.yview, args)
    # end def yview

    def add_v_scrolled (self, * widgets) :
        """Adds all `widgets' to set of widgets scrolled as a unit."""
        for w in widgets :
            clss = w.winfo_class    ()
            self._y_scrolled.append (w)
            w.configure             (yscrollcommand = self.y_scroll.set)
#           w.bind_class            (clss, "<Button-2>",  self.scan_mark)
#           w.bind_class            (clss, "<B2-Motion>", self.scan_dragto)
    # end def add_v_scrolled

    def scan_mark (self, event) :
        map ( lambda w, x = event.x, y = event.y : w.scan_mark (x, y)
            , self._y_scrolled
            )

    def scan_dragto (self, event) :
        map ( lambda w, x = event.x, y = event.y : w.scan_dragto (x, y)
            , self._y_scrolled
            )

# end class V_Scrolled_Tuple_

class Scrolled_Tuple_ (H_Scrolled_Tuple_, V_Scrolled_Tuple_) :
    """Mixin providing the ability to scroll a set of widgets as a unit."""

    def __init__ (self) :
        H_Scrolled_Tuple_.__init__ (self)
        V_Scrolled_Tuple_.__init__ (self)
    # end def __init__

    def scan_mark (self, event) :
        H_Scrolled_Tuple_.scan_mark (self, event)
        V_Scrolled_Tuple_.scan_mark (self, event)
    # end def scan_mark

    def scan_dragto (self, event) :
        H_Scrolled_Tuple_.scan_dragto (self, event)
        V_Scrolled_Tuple_.scan_dragto (self, event)
    # end def scan_dragto

# end class Scrolled_Tuple_

class Listbox_Tuple_ (V_Scrolled_Tuple_, Scrolled_Listbox_) :
    """Root for coupled listboxes scrolled by 1 scrollbar."""

    def __init__ (self, selectmode = BROWSE) :
        Scrolled_Listbox_.__init__   (self)
        V_Scrolled_Tuple_.__init__ (self)

        self.selectmode = selectmode

        btag = "%s_%d_Listbox_Tuple" % (self.widget_class, id (self))
        self.binding_tag = btag
        for k in ( "<Up>",   "<Down>", "<Control-Home>", "<Control-End>"
                 , "<Next>", "<Prior>"
                 ) :
            self.bind_class (btag, k, self.key_select)
    # end def __init__

    def add_listbox (self, w) :
        """Add a new listbox to `self'."""
        if self._y_scrolled :
            assert (self.list_box.size () == w.list_box.size ())
        self.add_v_scrolled   (w.list_box)
        add_bindtag           (w.list_box, self.binding_tag, 2)
        w.list_box.bind       ("<Button-1>",        self.mouse_select, add = 1)
        w.list_box.bind       ("<Button-4>",        self._mouse_wheel_up      )
        w.list_box.bind       ("<Button-5>",        self._mouse_wheel_down    )
        w.list_box.bind       ("<B1-Motion>",       self.mouse_select, add = 1)
        w.list_box.bind       ("<ButtonRelease-1>", self.mouse_finish, add = 1)
        if len (self._y_scrolled) == 1 :
            self.list_box = w.list_box
            w.list_box.bind ("<Configure>", self._change_size)
        return w
    # end def add_listbox

    def _mouse_wheel_up (self, event = None) :
        delta = event and event.delta or -1
        self.yview (SCROLL, delta, UNITS)
        return "break"
    # end def _mouse_wheel_up

    def _mouse_wheel_down (self, event = None) :
        delta = event and event.delta or +1
        self.yview (SCROLL, delta, UNITS)
        return "break"
    # end def _mouse_wheel_down

    def _y_scroll_pack (self) :
        self.y_scroll.pack ( side = RIGHT, fill = Y
                           , before = self.list_box.master
                           )
    # end def _y_scroll_pack

    def insert (self, index, * lists) :
        assert (len (lists) == len (self._y_scrolled))
        for lb, args in paired (self._y_scrolled, lists) :
            apply (lb.insert, (index, ) + _flatten ((args, )))
        self._change_size ()
    # end def insert

    def delete (self, first, last = None) :
        for lb in self._y_scrolled :
            lb.delete (first, last)
        self._change_size ()
    # end def delete

    def reload (self, * lists) :
        self.delete (0, END)
        apply       (self.insert, (0, ) + lists)
    # end def reload

    def mouse_finish (self, event = None) :
        widget = event.widget
        if widget.master.enabled :
            index  = widget.index (widget.nearest (event.y))
            for lb in self._y_scrolled :
                lb.master.select (index)
    # end def mouse_finish

    def mouse_select (self, event = None) :
        for lb in self._y_scrolled :
            lb.master.mouse_select (event)
    # end def mouse_select

    def select (self, index) :
        for lb in self._y_scrolled :
            lb.master.select (index)
    # end def select

    def key_select (self, event = None) :
        if event :
            self.select (event.widget.master.index ())
        else :
            self.select (0)
    # end def key_select

    def enable (self) :
        """Enable input into widget."""
        for lb in self._y_scrolled :
            lb.master.enable ()
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        for lb in self._y_scrolled :
            lb.master.disable ()
    # end def disable

# end class Listbox_Tuple_

class Listbox_Tuple (Listbox_Tuple_, C_Frame) :
    """Set of coupled listboxes scrolled by 1 scrollbar."""

    widget_class   = "Listbox_Tuple"

    def __init__ ( self, master, lists = 2, name = None
                 , selectmode = BROWSE
                 ) :
        C_Frame.__init__             ( self, master
                                     , class_ = self.widget_class
                                     , name   = name
                                     )
        assert (lists >= 0)
        Listbox_Tuple_.__init__      (self, selectmode)
        self._make_listboxes         (lists)
    # end def __init__

    def _make_listboxes (self, n) :
        for i in range (n) :
            w = self._new_listbox ( self
                                  , name = "listbox" + `i`
                                  , selectmode = self.selectmode
                                  )
            self.add_listbox      ( w)
            w.pack                ( side = LEFT, fill = BOTH, expand = YES)
    # end def _make_listboxes

    def _new_listbox (self, master, name, list = None, selectmode = BROWSE) :
        if list is None :
            list = []
        return C_Listbox ( master
                         , list       = list
                         , name       = name
                         , selectmode = selectmode
                         )
    # end def _new_listbox

# end class Listbox_Tuple

class Separator_ (C_Frame) :
    """Root class for horizontal and vertical separator widgets."""

    widget_class   = "Separator"

    default_size   = 2
    default_relief = SUNKEN

    def __init__ (self, master, name = None, ** kw) :
        C_Frame.__init__ ( self, master
                         , class_ = self.widget_class
                         , name   = name
                         , relief = self.default_relief
                         )

        ### unfortunately, we cannot read the option database before creating
        ### the frame
        size = self.option_value ("size", self.default_size)
        self._set_option         ("width",  size, kw)
        self._set_option         ("height", size, kw)
        self.configure           (kw)
    # end def __init__

    def pack (self, ** kw) :
        self._set_option ("side",   self.default_side, kw)
        self._set_option ("padx",   self.default_padx, kw)
        self._set_option ("pady",   self.default_pady, kw)
        kw ["fill"] = self.default_fill
        apply (C_Frame.pack, (self, ), kw)
    # end def pack

    def grid (self, span = None, ** kw) :
        self._set_option ("sticky", self.default_sticky, kw)
        self._set_option ("padx",   self.default_padx,   kw)
        self._set_option ("pady",   self.default_pady,   kw)
        self.grid_kw = kw
        if span : self._set_option (self.span_name, span, kw)
        else    : self.after_idle  (self.config_span)
        apply (C_Frame.grid, (self, ), kw)
    # end def grid

# end class Separator_

class H_Separator (Separator_) :
    """Horizontal separator widget."""

    default_side   = TOP
    default_fill   = X
    default_sticky = W+E
    default_padx   = 2
    default_pady   = 4
    span_name      = "columnspan"

    def config_span (self, event=None) :
        C_Frame.grid_configure ( self
                               , columnspan = self.master.grid_size () [0]
                               )
    # end def config_span

# end class H_Separator

class V_Separator (Separator_) :
    """Vertical separator widget."""

    default_side   = LEFT
    default_fill   = Y
    default_sticky = N+S
    default_padx   = 4
    default_pady   = 2
    span_name      = "rowspan"

    def config_span (self, event=None) :
        self._set_option       ("column", 0, self.grid_kw)
        self.columnconfigure   (self.grid_kw ["column"], weight = 1)
        C_Frame.grid_configure (self, rowspan = self.master.grid_size () [1])
    # end def config_span

# end class V_Separator

class Scrollable_ (C_Frame) :
    """Root class for scrollable widgets."""

    widget_class = "Scrollable"

    def __init__ ( self, master = None, name = None
                 , width = 0, height = 0
                 , ** kw
                 ) :
        C_Frame.__init__ (self, master, class_ = self.widget_class, name = name)
        self.vport        = Canvas  (self, name = "vport")
        if width  :       self.vport.configure (width  = width)
        if height :       self.vport.configure (height = height)
        self.hull         = C_Frame (self.vport, name = "hull")
        self.vport.config (kw)
        self.hull.bind    ("<Configure>", self.change_size)
        self.hull.pack    = self._hull_pack
        self.hull.grid    = self._hull_pack
        self.vport.create_window (0, 0, window = self.hull, anchor = NW)
    # end def __init__

    def change_scrollregion (self, bbox = None) :
        if not bbox :
            bbox = self.vport.bbox ("all")
        self.vport.configure (scrollregion = bbox)
    # end def change_scrollregion

    def change_size (self, event=None) :
        self.change_scrollregion ()
    # end def change_size

    def _hull_pack  (self, * args, ** kw) :
        raise NameError, ( "Hull of scrollable widget "
                         + self.__class__.__name__
                         + " cannot be packed/gridded"
                         )
    # end def _hull_pack

    def vport_pack (self, * args) :
        self.vport.grid ( sticky     = "ewns"
                        , column     = 0
                        , row        = 0
                        , padx       = 1
                        , pady       = 1
                        )
        self.grid_columnconfigure (0, weight = 1)
        self.grid_rowconfigure    (0, weight = 1)
    # end def vport_pack

    def _see_fraction (self, fraction, epsilon, scrollb, vport_view) :
        try :
            (head, tail) = scrollb.get ()
            spread = (tail - head)
            if   head > fraction :
                new_head = max (fraction - 0.5 * spread, 0)
                new_tail = new_head + spread
            elif tail < fraction + epsilon :
                new_tail = min (fraction + 0.5 * spread, 1)
                new_head = new_tail - spread
            else :
                new_head = new_tail  = 0

            if 0 <= new_head < new_tail <= 1:
                scrollb.set (new_head, new_tail)
                vport_view  ("moveto", new_head)
        except (SystemExit, KeyboardInterrupt), exc :
            raise
        except :
            pass
    # end def _see_fraction

# end class Scrollable_

class H_Scrollable_ :
    """Mixin for horizontally scrollable widgets"""

    def __init__ (self) :
        self.x_scroll   = Scrollbar ( self
                                    , orient    = HORIZONTAL
                                    , command   = self.vport.xview
                                    , takefocus = 0
                                    )
        self.vport.config           (xscrollcommand = self.x_scroll.set)
        self.x_scroll_pack          ()
    # end def __init__

    def x_scroll_pack (self) :
        self.x_scroll.grid ( sticky     = "ew"
                           , column     = 0
                           , row        = 1
                           , pady       = 1
                           )
    # end def x_scroll_pack

    def x_scroll_unpack (self) :
        self.x_scroll.grid_forget ()
    # end def x_scroll_unpack

    def see_x_fraction (self, fraction, epsilon) :
        """Scrolls so that horizontally position `fraction' is in view."""
        self._see_fraction (fraction, epsilon, self.x_scroll, self.vport.xview)
    # end def see_x_fraction

    def see (self, widget) :
        """Scrolls so that `widget' is in view."""
        width = self.hull.winfo_width ()
        if self.scrolling :
            frac = float (widget.winfo_rootx  () - self.hull.winfo_rootx ()
                         ) / width
            eps  = float (widget.winfo_width ()) / width
            self.see_x_fraction (frac, eps)
    # end def see

# end class H_Scrollable_

class H_Scrollable (H_Scrollable_, Scrollable_) :
    """Foundation for horizontally scrollable widgets."""

    Ancestor = __Ancestor = Scrollable_
    Mixin    = __Mixin    = H_Scrollable_

    def __init__ (self, master = None, ** kw) :
        self.__Ancestor.__init__ (self, master, ** kw)
        self.__Mixin.__init__    (self)
        self.vport_pack          ()
    # end def __init__

    scroll_pack   = Mixin.x_scroll_pack
    scroll_unpack = Mixin.x_scroll_unpack

    def change_size (self, event=None) :
        self.change_scrollregion ()
        self.vport.configure     (height = self.hull.winfo_height ())
    # end def change_size

    def hull_repack (self) :
        width  = self.hull.winfo_reqwidth   ()
        height = self.vport.winfo_height    ()
        self.vport.delete                   ( "all")
        self.vport.create_window            ( 0, 0
                                            , window = self.hull
                                            , anchor = NW
                                            , width  = width
                                            , height = height
                                            )
    # end def hull_repack

# end class H_Scrollable

class V_Scrollable_ :
    """Mixin for vertically scrollable widgets."""

    def __init__ (self, fixed_width, static_scroll_bar) :
        self._y_pending        = None
        self.fixed_width       = fixed_width
        self.static_scroll_bar = static_scroll_bar
        self.pending           = None
        self.scrolling         = 1
        self.y_scroll          = Scrollbar \
            ( self
            , orient    = VERTICAL
            , command   = self.vport.yview
            , takefocus = 0
            )
        self.vport.config  (yscrollcommand = self.y_scroll.set)
        self.y_scroll_pack ()
    # end def __init__

    def y_scroll_pack (self) :
        self.y_scroll.grid ( sticky     = "ns"
                           , column     = 1
                           , row        = 0
                           , padx       = 1
                           )
        self.scrolling = 1
    # end def y_scroll_pack

    def y_scroll_unpack (self) :
        if not self.static_scroll_bar :
            self.y_scroll.grid_forget ()
            self.scrolling = None
    # end def y_scroll_unpack

    def see_y_fraction (self, fraction, epsilon) :
        """Scrolls so that vertical position `fraction' is in view."""
        if self.scrolling :
            self._see_fraction \
                (fraction, epsilon, self.y_scroll, self.vport.yview)
    # end def see_y_fraction

    def see (self, widget) :
        """Scrolls so that `widget' is in view."""
        height = self.hull.winfo_height ()
        if self.scrolling :
            frac = float (widget.winfo_rooty  () - self.hull.winfo_rooty ()
                         ) / height
            eps  = float (widget.winfo_height ()) / height
            self.see_y_fraction (frac, eps)
    # end def see

# end class V_Scrollable_

class V_Scrollable (V_Scrollable_, Scrollable_) :
    """Foundation for vertically scrollable widgets."""

    Ancestor = __Ancestor = Scrollable_
    Mixin    = __Mixin    = V_Scrollable_

    def __init__ ( self
                 , master            = None
                 , fixed_width       = None
                 , static_scroll_bar = None
                 , ** kw
                 ) :
        self.__Ancestor.__init__ (self, master, ** kw)
        self.__Mixin.__init__    (self, fixed_width, static_scroll_bar)
        self.vport_pack          ()
    # end def __init__

    scroll_pack   = Mixin.y_scroll_pack
    scroll_unpack = Mixin.y_scroll_unpack

    def change_size (self, event=None) :
        ###print event.widget.winfo_class (), event.widget
        if not self._y_pending :
            self._y_pending = self.after_idle (self.shrink_maybe)
    # end def change_size

    def change_width (self, event = None) :
        """Callback function to be bound to `<Configure>'."""
        self.update_idletasks  ()
        nw  = self.winfo_width () - self.y_scroll.winfo_width ()
        ### h = self.hull
        ### print self, self.vport.winfo_width (), self.vport.bbox ("all")
        self.vport.configure   (width = nw)
        self.hull_repack       ()
    # end def change_width

    def hull_repack (self) :
        width  = self.vport.winfo_width    ()
        height = self.hull.winfo_reqheight ()
        self.vport.delete                  ( "all")
        self.vport.create_window           ( 0, 0
                                           , window = self.hull
                                           , anchor = NW
                                           , width  = width
                                           , height = height
                                           )
    # end def hull_repack

    def shrink_maybe (self, event=None) :
        try     :
            self.update_idletasks ()
            try :
                self.change_scrollregion ()
                if not self.fixed_width :
                    hh = self.hull.winfo_width () + 2
                    if self.vport.winfo_width () < hh :
                        self.vport.configure (width = hh)
                if self.y_scroll.get () == (0.0, 1.0) :
                    self.scroll_unpack ()
                else :
                    self.scroll_pack ()
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                ## `shrink_maybe' is sometimes called after the
                ## deletion of `vport'
                pass
            self.update_idletasks () # avoid recursion by changes made by
                                     # shrink_maybe
        finally :
            self._y_pending = None
    # end def shrink_maybe

# end class V_Scrollable

class HV_Scrollable (H_Scrollable_, V_Scrollable_, Scrollable_) :
    """Foundation for horizontally and vertically scrollable widgets"""

    Ancestor = __Ancestor = Scrollable_
    Mixin_H  = __Mixin_H  = H_Scrollable_
    Mixin_V  = __Mixin_V  = V_Scrollable_

    def __init__ ( self
                 , master            = None
                 , static_scroll_bar = None
                 , ** kw
                 ) :
        self.__Ancestor.__init__ (self, master, ** kw)
        self.__Mixin_H.__init__  (self)
        self.__Mixin_V.__init__  (self, 0, static_scroll_bar)
        self.vport_pack          ()
    # end def __init__

    def scroll_pack (self) :
        self.__Mixin_H.x_scroll_pack (self)
        self.__Mixin_V.y_scroll_pack (self)
    # end def scroll_pack

    def scroll_unpack (self) :
        self.__Mixin_H.x_scroll_unpack (self)
        self.__Mixin_V.y_scroll_unpack (self)
    # end def scroll_unpack

    def change_size (self, event=None) :
        self.change_scrollregion ()
    # end def change_size

    def hull_repack (self) :
        width  = self.hull.winfo_reqwidth   ()
        height = self.hull.winfo_reqheight  ()
        self.vport.delete                   ( "all")
        self.vport.create_window            ( 0, 0
                                            , window = self.hull
                                            , anchor = NW
                                            , width  = width
                                            , height = height
                                            )
    # end def hull_repack

    def see (self, widget) :
        """Scrolls so that `widget' is in view."""
        self.__Mixin_H.see (self, widget)
        self.__Mixin_V.see (self, widget)
    # end def see

# end class HV_Scrollable

class Notebook (C_Frame) :
    """Notebook widget supporting the display of any of a number of pages in
       a given frame.
    """

    widget_class = "Notebook"

    def __init__ (self, master = None, name = None) :
        self.__INIT__       (master, name)
        self.pack_propagate (0)
    # end def __init__

    def __INIT__ (self, master = None, name = None) :
        C_Frame.__init__ \
            (self, master, class_ = self.widget_class, name = name)
        self.page    = {}
        self.p_name  = {}
        self.active  = None
        self.pending = None
    # end def __INIT__

    def book (self) : return self

    def new_page (self, name) :
        """Add a page named `name' to the notebook."""
        self.page   [name] = page = Frame \
            (self.book (), name = name.lower ())
        self.p_name [page] = name
        if not self.pending :
            self.select (page)
        page.deiconify = page.make_active = lambda : self.display (name)
        return page
    # end def new_page

    def page_bind (self, page_name, event, command, * args, ** kw) :
        """Bind the callback `command` to `event` of `page_name`."""
        try :
            page = self.page [page_name]
            page.bind (event, command, * args, ** kw)
        except KeyError :
            print "Unknown page", page_name, self.page.keys ()
    # end def page_bind

    def display (self, name) :
        """Display page `name'."""
        self.select (self.page [name])
    # end def display

    def select (self, page) :
        """Display `page'."""
        if not self.pending :
            self.after_idle (self._display)
        if page :
            self.pending = page
    # end def select

    def _display (self) :
        self._fix_size ()
        if self.active  :
            self.active.pack_forget ()
        if self.pending :
            self.pending.pack (expand = YES, fill = BOTH)
        (self.active, self.pending) = (self.pending, None)
    # end def _display

    def _req_width  (self) :
        return 0
    # end def _req_width

    def _fix_size   (self) :
        self.update_idletasks ()
        max_wd = max_ht = 0
        for p in self.page.values () :
            max_wd = max (max_wd, p.winfo_reqwidth  ())
            max_ht = max (max_ht, p.winfo_reqheight ())
        max_wd = max (max_wd, self._req_width ())
        border = 2 * int (self.cget ("borderwidth"))
        self.book ().configure \
            ( width  = max_wd + border
            , height = max_ht + border
            )
    # end def _fix_size

# end class Notebook

class Tab_ :

    def __init__ (self, master, name, x, margin, font, command) :
        self.name       = name
        self.command    = command
        self.txt        = CanvasText  ( master
                                      , x + margin, -0.15 * margin
                                      , anchor = SW
                                      , text   = " " + name + " "
                                      , font   = font
                                      , tags   = name
                                      )
        bbox            = master.bbox (self.txt)
        (width, height) =             (bbox [2] - bbox [0],bbox [3] - bbox [1])
        self.box        = Polygon     \
            ( master
            , x,                      0
            , x + margin,             -height - 0.5 * margin
            , x + margin + width,     -height - 0.5 * margin
            , x + 2 * margin + width, 0
            , outline = "black"
            , tags    = (name, "tab", "tab-" + name)
            )
        master.tkraise                (self.txt)
        master.tag_bind               (name, "<ButtonPress-1>", self.do)
        self.width  = width
        self.height = height
    # end def __init__

    def do (self, event=None) : self.command (self.name)

# end class Tab_

class Tabbed_Notebook (Notebook) :
    """Tabbed notebook widget."""

    widget_class = "Tabnotebook"

    def __init__ (self, master = None, name = None) :
        Notebook.__INIT__   (self, master, name = name)

        self.tabs  = Canvas  ( self, name = "tabs", highlightthickness = 0)
        self.nbook = C_Frame ( self, name = "book"
                             , class_ = Notebook.widget_class
                             )
        self.tabs.pack       (fill = X)
        self.nbook.pack_propagate (0)
        self.nbook.pack      (fill = BOTH, expand = YES)

        self.p_names        = []
        self.tab_pending    = None
        self.margin         = self._num_tab_opt ("margin", 6)
        self.tabcolor       = self._tab_option  ("tabColor",       "grey65")
        self.activetabcolor = self._tab_option  ("activeTabColor", "grey85")
        self.tab_font       = self._tab_option  ("font", "Helvetica")
    # end def __init__

    def book (self) : return self.nbook

    def new_page (self, name, state = NORMAL, index = None) :
        """Add a page named `name' to the notebook at position `index'"""
        if index is None :
            index = len (self.p_names)
        self.p_names.insert (index, name)
        page       = Notebook.new_page (self, name)
        page.state = state
        if not self.tab_pending :
            self.tab_pending = self.after_idle (self._fix_tabs)
        return page
    # end def new_page

    def change_page (self, name, state) :
        self.page [name].state = state
        if not self.tab_pending :
            self.tab_pending = self.after_idle (self._fix_tabs)
    # end def change_page

    def _display (self) :
        Notebook._display (self)
        name = self.p_name [self.active]
        self.tabs.itemconfigure   ("tab",         fill = self.tabcolor)
        self.tabs.itemconfigure   ("tab-" + name, fill = self.activetabcolor)
        self.tabs.tkraise         (name)
    # end def _display

    def _tab_option  (self, name, default) :
        result = self.option_value (name, default, widget = self.tabs)
        return result
    # end def _tab_option

    def _num_tab_opt (self, name, default) :
        return self.num_opt_val (name, default, widget = self.tabs)
    # end def _num_tab_opt

    def _req_width (self) :
        return int (self.tabs.cget ("width")) + self.margin + 2
    # end def _req_width

    def _fix_tabs (self) :
        if not self.tab_pending : return
        try     :
            self.tabs.delete ("all")
            x = max_ht = 0
            for p in self.p_names :
                if self.page [p].state == NORMAL :
                    t      = Tab_ ( self.tabs, p, x
                                  , margin  = self.margin
                                  , font    = self.tab_font
                                  , command = self.display
                                  )
                    x      = x + t.width + self.margin
                    max_ht = max (max_ht, t.height)
            height = max_ht + 0.5 * self.margin
            self.tabs.move      ("all",  0, height + 1)
            self.tabs.configure (width = x, height = height)
        finally :
            self.tab_pending = None
    # end def _fix_tabs

# end class Tabbed_Notebook

class Slide :
    """One slide of a Slide_Show"""

    def __init__ (self, widget, action = None, action_name = None) :
        self.widget      = widget
        self.action      = action
        self.action_name = action_name
    # end def __init__

# end class Slide

class Slide_Show (C_Frame) :
    """Provide a widget containing a sequence of widgets (slides) with `next'
       and `prev' navigation buttons and an optional action button performing
       a slide-specific action.
    """

    widget_class = "Slide_Show"

    def __init__ (self, master, name = None, help = None) :
        C_Frame.__init__               ( self, master
                                       , class_ = self.widget_class
                                       , name   = name
                                       )
        self.hull       = C_Frame      ( self, name = "hull")
        self.button_box = Buttongrid   ( self
                                       , name        = "button_box"
                                       , padx        = 5
                                       , pady        = 5
                                       , buttonstate = DISABLED
                                       , help        = help
                                       )
        self.button_box.pack           ( side        = BOTTOM
                                       , fill        = X
                                       )
        self.hull.pack                 ( side        = TOP
                                       , fill        = BOTH
                                       , expand      = YES
                                       )
        self._add_buttons              ()
        self.slide   = []
        self.active  = None
    # end def __init__

    def _add_buttons (self) :
        self.button_box.add ("Prev",   command = self.prev)
        self.button_box.add ("Action", command = self.act)
        self.button_box.add ("Next",   command = self.next)
        self.button_box.grid_columnconfigure (1, weight = 1)
    # end def _add_buttons

    def add_slide ( self, Widget_Class
                  , action = None, action_name = None
                  , before = None
                  , * args, ** kw
                  ) :
        """Adds a slide to slide_show in front of slide with index `before'
           (the new slide is appended if `before' is not specified).
           The slide is a widget of type Widget_Class which is created by
           `add_slide' with the call:
               apply (Widget_Class, (self.hull, ) + args, kw)
        """
        slide = Slide ( apply (Widget_Class, (self.hull, ) + args, kw)
                      , action, action_name
                      )
        if before is None :
            before = len (self.slide)
        self.slide.insert (before, slide)
        if self.active is None :
            self.select (before)
        return slide.widget
    # end def add_slide

    def select (self, i) :
        """Select slide with index `i'."""
        if self.active is not None :
            self.slide [self.active].widget.pack_forget ()
        self.active = i
        slide = self.slide [self.active]
        slide.widget.pack (expand = YES, fill = BOTH)
        self.button_box.buttonconfigure ("Next", state = NORMAL)
        self.button_box.buttonconfigure ("Prev", state = NORMAL)
        if   i == 0 :
            self.button_box.buttonconfigure  ("Prev",   state = DISABLED)
        if   i == len (self.slide) - 1 :
            self.button_box.buttonconfigure  ("Next",   state = DISABLED)
        if slide.action_name :
            self.button_box.buttonconfigure  \
                ( "Action", state = NORMAL
                , text = slide.action_name
                , command = slide.action or self.act
                )
            self.after_idle                  (self.button_box.regrid)
            self.action = slide.action
        else :
            self.button_box.buttonconfigure  ( "Action", state = DISABLED
                                             , text = ""
                                             , command = self.act
                                             )
            self.after_idle (Functor (self.button_box.ungrid, "Action"))
            self.action = None
    # end def select

    def act (self, event = None) :
        """Execute action related to this page."""
        if self.action : self.action ()
    # end def act

    def next (self, event = None) :
        """Goto next page."""
        if self.active is not None :
            self.select (min (self.active + 1, len (self.slide) - 1))
    # end def next

    def prev (self, event = None) :
        """Goto previous page."""
        if self.active is not None :
            self.select (max (self.active - 1, 0))
    # end def prev

# end class Slide_Show

class Grip_ (C_Frame) :

    def __init__ (self, master, i, sash, class_, name = None) :
        C_Frame.__init__ \
            (self, master, class_ = class_, name = name, relief = RAISED)
        self.i      = i
        self.sash   = sash
        for w in self, sash :
            w.bind ("<ButtonPress-1>",       self.grab)
            w.bind ("<B1-Motion>",           self.drag)
            w.bind ("<ButtonRelease-1>",     self.drop)
        sash.configure (cursor = self.cget ("cursor"))
    # end def __init__

    def grab (self, event = None) :
        self.configure   (relief = SUNKEN)
    # end def grab

    def drag (self, event = None) :
        self.master.drag (self.i, event)
    # end def drag

    def drop (self, event = None) :
        self.master.drop (self.i, event)
        self.configure   (relief = RAISED)
    # end def drop

# end class Grip_

class Panedwindow_ (C_Frame) :
    """Root class for paned windows."""

    widget_class     = "Panedwindow"

    upper_limit_frac = 0.95
    lower_limit_frac = 0.05
    upper_limit_pixl = 0
    lower_limit_pixl = 0

    def __init__ \
        (self, master = None, name = None, change_callback = None, ** kw) :
        C_Frame.__init__ (self, master, class_ = self.widget_class, name = name)
        self.change_callback = change_callback
        if kw :
            self.configure (kw)
        self.pane = []
        for i in range (len (self.pane_name)) :
            pane = C_Frame (self, name = self.pane_name [i])
            pane.place ( relx      = self.pane_relx   [i]
                       , rely      = self.pane_rely   [i]
                       , anchor    = self.pane_anchor [i]
                       , relheight = self.pane_rel_ht [i]
                       , relwidth  = self.pane_rel_wd [i]
                       , height    = self.pane_off_ht [i]
                       , width     = self.pane_off_wd [i]
                       )
            self.pane.append (pane)
        self.sash = []
        self.grip = []
        for i in range (len (self.pane_name [1:])) :
            sash = self.pane_separator (self, name = "separator%d" % i)
            relx = 0.5 * (self.pane_relx [i] + self.pane_relx [i+1])
            rely = 0.5 * (self.pane_rely [i] + self.pane_rely [i+1])
            sash.place \
                ( relx                    = relx
                , rely                    = rely
                , anchor                  = CENTER
                , ** { self.pane_sep_size : 1.0 }
                )
            self.sash.append (sash)
            grip = Grip_ ( self, i
                         , sash   = sash
                         , class_ = "Panedwindow_Grip"
                         , name   = self.grip_name
                         )
            self._grip_place (grip, i)
            self.grip.append (grip)
        self.frac         = 0.5
        self._pw_pending  = None
        self._pwf_pending = 1 ### disable `_change_frame_size'
        self.bind ("<Configure>", self.change_size)
    # end def __init__

    def change_size (self, event = None, frac = None) :
        if frac is not None :
            self.frac = frac
        if not self._pw_pending :
            self._pw_pending = self.after_idle (self._change_size)
    # end def change_size

    def _change_size (self) :
        self._pw_pending = None
        self.drop (0)
    # end def _change_size

    def drop (self, i, event = None) :
        self.divide (self.drag (i, event), i)
    # end def drop

    def divide (self, frac, i = 0) :
        self.frac = frac
        self.sash [i    ].place (** {self.pane_rel_name  : frac})
        self.grip [i    ].place (** {self.pane_rel_name  : frac})
        self.pane [i    ].place (** {self.pane_rel_size  : frac})
        self.pane [i + 1].place (** {self.pane_rel_size  : 1 - frac})
        if not self._pwf_pending :
            self._pwf_pending = self.after_idle \
                ( lambda s = self, i = i : s._change_frame_size (i))
        if self.change_callback :
            self.change_callback ()
    # end def divide

    def _change_frame_size (self, i = 0) :
        try     :
            frac = self.frac
            size = self._widget_size ()
            one  = (frac       * size) - 5
            two  = ((1 - frac) * size) - 5
            print self.name, self.pane_size, size, one, two
            if min (one, two) > 20 :
                self.pane [i    ].configure (** {self.pane_size : one})
                self.pane [i + 1].configure (** {self.pane_size : two})
        finally :
            self._pwf_pending = None
    # end def _change_frame_size

    def _drag (self, i, offset, size) :
        frac = self._fraction (i, offset, size)
        self.sash [i].place (** {self.pane_rel_name : frac})
        self.grip [i].place (** {self.pane_rel_name : frac})
        return frac
    # end def _drag

    def _upper_limit (self, i, key) :
        if i + 1 >= len (self.grip) :
            result = 1.0
        else :
            result = int ((self.grip [i + 1]).place_info () [key])
        return min (result, self.upper_limit_frac)
    # end def _upper_limit

    def _lower_limit (self, i, key) :
        if i == 0 :
            result = 0.0
        else :
            result = int ((self.grip [i - 1]).place_info () [key])
        return max (result, self.lower_limit_frac)
    # end def _lower_limit

    def _fraction (self, i, offset, size) :
        offset = max (offset, self.lower_limit_pixl)
        offset = min (offset, size - self.upper_limit_pixl)
        frac   = float (offset) / size
        frac   = max (frac, self._lower_limit (i, self.pane_rel_name))
        frac   = min (frac, self._upper_limit (i, self.pane_rel_name))
        return frac
    # end def _fraction

# end class Panedwindow_

class H_Panedwindow (Panedwindow_) :
    """Provide a window with two panes side by side."""

    grip_name     = "h_grip"

    pane_name      = ("left", "right")
    pane_relx      = (0.0,    1.0)
    pane_rely      = (0.5,    0.5)
    pane_anchor    = (W,      E)
    pane_rel_ht    = (1.0,    1.0)
    pane_rel_wd    = (0.5,    0.5)
    pane_off_ht    = (0,      0)
    pane_off_wd    = (-3,    -3)
    pane_separator = V_Separator
    pane_sep_size  = "relheight"
    pane_rel_size  = "relwidth"
    pane_rel_name  = "relx"
    pane_size      = "width"

    ### This class doesn't really work for more than two panes because the
    ### algorithm implemented for `divide' is too primitive
    ### To make it work for more than two panes, the calls of
    ### `pane [...].place' must be changed

    def __init__ (self, master = None, ** kw) :
        apply (Panedwindow_.__init__, (self, master), kw)
        self.left  = self.pane [0]
        self.right = self.pane [1]
    # end def __init__

    def _grip_place (self, grip, i) :
        relx = 0.5 * (self.pane_relx [i] + self.pane_relx [i+1])
        grip.place (relx = relx, rely = 0.90, anchor = CENTER)
    # end def _grip_place

    def drag (self, i, event = None) :
        if event :
            x = event.x_root - self.winfo_rootx ()
        else :
            x = self.frac    * self.winfo_width ()
        return self._drag (i, x, self.winfo_width ())
    # end def drag

    def _widget_size (self) :
        return self.winfo_width ()
    # end def _widget_size

# end class H_Panedwindow

class V_Panedwindow (Panedwindow_) :
    """Provide a window with two panes on top of each other."""

    grip_name      = "v_grip"

    pane_name      = ("upper", "lower")
    pane_relx      = (0.5,    0.5)
    pane_rely      = (0.0,    1.0)
    pane_anchor    = (N,      S)
    pane_rel_ht    = (0.5,    0.5)
    pane_rel_wd    = (1.0,    1.0)
    pane_off_ht    = (-3,    -3)
    pane_off_wd    = (0,      0)
    pane_separator = H_Separator
    pane_sep_size  = "relwidth"
    pane_rel_size  = "relheight"
    pane_rel_name  = "rely"
    pane_size      = "height"

    ### This class doesn't really work for more than two panes because the
    ### algorithm implemented for `divide' is too primitive
    ### To make it work for more than two panes, the calls of
    ### `pane [...].place' must be changed

    def __init__ (self, master = None, ** kw) :
        apply (Panedwindow_.__init__, (self, master), kw)
        self.upper = self.pane [0]
        self.lower = self.pane [1]
    # end def __init__

    def _grip_place (self, grip, i) :
        rely = 0.5 * (self.pane_rely [i] + self.pane_rely [i+1])
        grip.place (relx = 0.90, rely = rely, anchor = CENTER)
    # end def _grip_place

    def drag (self, i, event = None) :
        if event :
            y = event.y_root - self.winfo_rooty  ()
        else :
            y = self.frac    * self.winfo_height ()
        return self._drag (i, y, self.winfo_height ())
    # end def drag

    def _widget_size (self) :
        return self.winfo_height ()
    # end def _widget_size

# end class V_Panedwindow

class Entry_History :
    """History for an entry widget."""

    def __init__ (self, values = None) :
        if values :
            self.values = list (values)
        else :
            self.values = []
    # end def __init__

    def add (self, * v) :
        for value in v :
            if not value : return
            if value in self.values :
                self.values.remove (value)
            self.values.append (value)
    # end def add

    def prev (self, value) :
        if not self.values :
            result = value
        else :
            try :
                i = self.values.index (value) - 1
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                i = len (self.values) - 1
            result = self.values [i]
            self.add (value)
        return result
    # end def prev

    def next (self, value) :
        if not self.values :
            result = value
        else :
            l = len (self.values)
            try :
                i = self.values.index (value) + 1
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                i = l
            if i >= l :
                i = i - l
            result = self.values [i]
            self.add (value)
        return result
    # end def next

    def attach (self, entry) :
        """Attach `self' to `entry' widget."""
        if not isinstance (entry, C_Entry) : return
        first = (entry._history is None)
        entry._history = self
        if first :
            entry.entry.bind ("<<HistNext>>",     entry._hist_next)
            entry.entry.bind ("<<HistPrev>>",     entry._hist_prev)
            entry.entry.bind ("<<HistComplete>>", entry._hist_complete)
    # end def attach
# end class Entry_History

class C_Entry (C_Frame) :
    """Container for an Entry plus related widgets.

       The widget hierarchy of an C_Entry looks like:

           Name                   TK-class
           ====================================================================
           self                   C_Entry
             self.frame           Frame              # packs label and entry
               self.entrybox      H_Strut            # controls entry size
                 self.entry       Entry              # what its all about
               self.label         Label              # optional
    """

    widget_class    = "C_Entry"

    inner_entrypos  = LEFT # position of entry inside H_Strut
    entry_expand    = YES
    frame_expand    = YES

    fixed_height    = "24"

    def __init__ ( self, master
                 , name         = None
                 , entryname    = "entry"
                 , entryfill    = X
                 , entrypos     = LEFT
                 , label        = None
                 , labelpos     = LEFT
                 , labelanchor  = None
                 , labeljustify = None
                 , default      = None
                 , state        = NORMAL
                 , takefocus    = 1
                 , bindtag      = None
                 ) :
        C_Frame.__init__ ( self, master
                         , class_             = self.widget_class
                         , name               = name
                         , borderwidth        = 0
                         , highlightthickness = 0
                         )
        self.fixed_width  = self.num_opt_val  ("fixed_width", "0")
        if self.fixed_width :
            self.fixed_height =  self.num_opt_val ( "fixed_height"
                                                  , self.__class__.fixed_height
                                                  )
            self.configure       ( width  = self.fixed_width
                                 , height = self.fixed_height
                                 )
            self.pack_propagate  (0)

        self.frame     = Frame   ( self
                                 , name               = "frame"
                                 , borderwidth        = 0
                                 , relief             = FLAT
                                 , highlightthickness = 0
                                 )
        self.entrybox  = H_Strut ( self.frame, "entry_strut", "C_Entry"
                                 , name      = "entry"
                                 )
        self.entry     = self._make_entry (entryname, state, takefocus, bindtag)

        self.entry.pack          ( side   = self.inner_entrypos
                                 , fill   = entryfill
                                 , expand = self.entry_expand
                                 )
        self.entrybox.pack       ( side   = self.inverse_pos [labelpos]
                                 , fill   = entryfill, expand = YES
                                 )
        if label is not None :
            self.label    = Label           ( self.frame
                                            , text    = label
                                            , name    = "label"
                                            , justify = labeljustify
                                            , anchor  = labelanchor
                                            )
            self.label_bg = self.label.cget ("background")
            self.label_fg = self.label.cget ("foreground")
            self.label.pack                 ( side   = labelpos
                                            , anchor = labelanchor
                                            )
        else :
            self.label = None
        self.frame.pack          ( side   = entrypos
                                 , fill   = X
                                 , expand = self.frame_expand
                                 )

        self.has_focus   = None
        self.state       = state
        self.enabled     = 1
        self.backg       = self.entry.cget   ("background")
        self.foreg       = self.entry.cget   ("foreground")
        self.relief      = self.entry.cget   ("relief")
        self.focus_bg    = self.option_value ("focusBackground", "yellow")
        self.focus_fg    = self.option_value ("focusForeground", "red")
        self.disabled_bg = self.option_value \
            ("disabledBackground", "lightyellow2")
        self.disabled_fg = self.option_value ("disabledForeground", "#a3a3a3")
        self._c_menu     = None
        self._in_c_menu  = None
        self._history    = None
        self.entry.bind  ("<FocusIn>",  self.highlight_focus)
        self.entry.bind  ("<FocusOut>", self.unhighlight_focus)
        self.set         (default)
    # end def __init__

    def _make_entry (self, entryname, state, takefocus, bindtag) :
        entry = Entry  ( self.entrybox
                       , name      = entryname
                       , width     = 0
                       , state     = state
                       , takefocus = takefocus
                       )
        if bindtag :
            add_bindtag (entry, bindtag)
        return entry
    # end def _make_entry

    def on_change (self) : pass

    def set (self, value) :
        """Set entry to `value'."""
        try     :
            self.entry.configure (state = NORMAL)
            self.entry.delete (0, END)
            if value is not None :
                self.entry.insert (0, value)
                self.on_change    ()
        finally :
            self.entry.configure (state = self.state)
    # end def set

    def get (self) :
        return self.entry.get ()
    # end def get

    def highlight_focus (self, event = None) :
        self.entry.configure ( background = self.focus_bg
                             , foreground = self.focus_fg
                             )
        self.has_focus = 1
    # end def highlight_focus

    def unhighlight_focus (self, event = None) :
        self.entry.configure (background=self.backg, foreground=self.foreg)
        if self._c_menu and not self._in_c_menu :
            self._unpost_complete_menu ()
        if self._history :
            self._history.add (self.get ())
        self._in_c_menu = None
        self.has_focus  = None
    # end def unhighlight_focus

    def focus_set (self) :
        if self.entry : self.entry.focus_set ()
    # end def focus_set

    def enable (self) :
        """Enable input into widget."""
        if not self.enabled :
            self.enabled = 1
            self._enable_entry ()
            if self.label :
                self.label.configure ( foreground = self.label_fg
                                     #, background = self.label_bg
                                     )
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        if self.enabled :
            self.enabled         = 0
            e                    = self.entry
            self.__saved_bintags = e.bindtags ()
            self._disable_entry  ()
            if self.label :
                self.label.configure ( foreground = self.disabled_fg
                                     #, background = self.disabled_bg
                                     )
    # end def disable

    def _enable_entry (self) :
        self.entry.configure ( takefocus  = 1
                             , state      = self.state
                             , background = self.backg
                             , foreground = self.foreg
                             , relief     = self.relief
                             )
    # end def _enable_entry

    def _disable_entry (self) :
        self.entry.configure ( takefocus  = 0
                             , state      = DISABLED
                             , background = self.disabled_bg
                             , foreground = self.disabled_fg
                             , relief     = FLAT
                             )
    # end def _disable_entry

    def _complete (self, from_list, show_completions = 1) :
        "Completes current value by looking at values in `from_list'."
        if self._c_menu : self._unpost_complete_menu ()
        v = self.entry.get ()
        if v :
            l = list    (from_list)
            m = matches (l, v)
            if m :
                completion = common_head (m)
                if completion :
                    if completion != v :
                        self.set (completion)
                        return (completion, m)
                if show_completions and len (m) > 1 :
                    self._popup_complete_menu (m)
        elif show_completions :
            self._popup_complete_menu (from_list)
        return v, None
    # end def _complete

    completion_menu_rows = 20

    def _popup_complete_menu (self, list) :
        l    = len (list)
        r    = self.completion_menu_rows
        menu = self._c_menu = Menu (self.master, tearoff = 0)
        if l <= r :
            self._fill_menu (menu, list)
        else :
            for i in range (0, l, r) :
                sub_menu = Menu  (menu, tearoff = 0)
                self._fill_menu  (sub_menu, list [i : i + r])
                menu.add_cascade (label = list [i], menu = sub_menu)
        menu.bind ( "<ButtonPress-1>", self._enter_c_menu, add = 1)
        menu.post ( self.entry.winfo_rootx () + self.entry.winfo_width  () - 5
                  , self.entry.winfo_rooty () + self.entry.winfo_height () - 5
                  )
    # end def _popup_complete_menu

    def _enter_c_menu (self, event = None) :
        self._in_c_menu = 1
    # end def _enter_c_menu

    def _unpost_complete_menu (self, event = None) :
        self._c_menu.unpost  ()
        self._c_menu.destroy ()
        self._c_menu = None
    # end def _unpost_complete_menu

    def _complete_set (self, v) :
        self.set (v)
        if self._c_menu : self._unpost_complete_menu ()
    # end def _complete_set

    def _fill_menu (self, menu, list) :
        r = self.completion_menu_rows + 1
        i = 0
        for m in list :
            menu.add_command ( label       = m
                             , command     = Functor (self._complete_set, m)
                             , columnbreak = (i % r) == 0
                             )
            i = i + 1
    # end def _fill_menu

    def _hist_next (self, event = None) :
        if self._history :
            self.set (self._history.next (self.get ()))
    # end def _hist_next

    def _hist_prev (self, event = None) :
        if self._history :
            self.set (self._history.prev (self.get ()))
    # end def _hist_prev

    def _hist_complete (self, event = None) :
        if self._history :
            self._popup_complete_menu (self._history.values)
    # end def _hist_complete

# end class C_Entry

class C_Checkbutton_Entry (C_Entry) :
    """C_Entry with a Checkbutton instead of an entry"""

    widget_class   = "C_Checkbutton_Entry"

    inner_entrypos = RIGHT
    entry_expand   = NO

    def __init__ (self, master, onvalue = "1", offvalue = "", * args, ** kw) :
        self.onvalue  = onvalue
        self.offvalue = offvalue
        apply (C_Entry.__init__, (self, master) + args, kw)
        if self.label :
            self.label.bind ("<ButtonRelease-1>", self._invoke_by_label)
    # end def __init__

    def _make_entry (self, entryname, state, takefocus, bindtag) :
        self._variable = StringVar   (self.entrybox)
        entry          = Checkbutton ( self.entrybox
                                     , name      = entryname
                                     , width     = 0
                                     , state     = state
                                     , takefocus = takefocus
                                     , variable  = self._variable
                                     , anchor    = E
                                     , onvalue   = self.onvalue
                                     , offvalue  = self.offvalue
                                     )
        if bindtag :
            add_bindtag (entry, bindtag)
        entry.get = self.get
        entry.set = self.set
        return entry
    # end def _make_entry

    def set (self, value) :
        """Set entry to `value'."""
        if value :
            self.entry.select   ()
        else :
            self.entry.deselect ()
    # end def set

    def get (self) :
        return self._variable.get ()
    # end def get

    def _complete (self, * args, ** kw) :
        return None, None
    # end def _complete

    def _invoke_by_label (self, event = None) :
        if self.enabled :
            self.entry.invoke ()
    # end def _invoke_by_label

    if sos.name == "nt" :
        def _enable_entry (self) :
            self.entry.configure ( takefocus  = 1
                                 , state      = self.state
                                 )
        # end def _enable_entry

        def _disable_entry (self) :
            self.entry.configure ( takefocus  = 0
                                 , state      = DISABLED
                                 )
        # end def _disable_entry
    else :
        def _enable_entry (self) :
            self.entry.configure ( takefocus  = 1
                                 , state      = self.state
                                 , background = self.backg
                                 , foreground = self.foreg
                                 )
        # end def _enable_entry

        def _disable_entry (self) :
            self.entry.configure ( takefocus  = 0
                                 , state      = DISABLED
                                 , background = self.disabled_bg
                                 , foreground = self.disabled_fg
                                 )
        # end def _disable_entry
    # end if sos.name == "nt"

# end class C_Checkbutton_Entry

class Entry_Tuple :
    """Set of coupled entries."""

    def __init__ (self) :
        self.entry = []
    # end def __init__

    def add (self, entry) :
        self.entry.append (entry)
    # end def add

    def get (self) :
        return map (lambda x : x.get (), self.entry)
    # end def get

    def set (self, value) :
        map (lambda p : p [0].set (p [1]), paired (self.entry, value))
    # end def set

    def enable (self) :
        """Enable input into widget."""
        for entry in self.entry : entry.enable  ()
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        for entry in self.entry : entry.disable ()
    # end def disable

# end class Entry_Tuple

class Entrybox (Entry_Tuple, C_Frame) :
    """Container for a number of entries."""

    widget_class = "Entrybox"

    def __init__ ( self, master
                 , name         = None
                 , entryfill    = X
                 , entryexpand  = YES
                 , entrypos     = LEFT
                 , framepos     = None
                 , label        = None
                 , labelpos     = LEFT
                 , labelanchor  = S
                 , labeljustify = None
                 , labelpadx    = None
                 , labelpady    = None
                 , ** kw
                 ) :
        if not framepos          : framepos = entrypos
        apply                    ( C_Frame.__init__
                                 , (self, master, name, self.widget_class)
                                 , kw
                                 )
        self.frame     = Frame   ( self
                                 , name               = "frame"
                                 , borderwidth        = 0
                                 , relief             = FLAT
                                 , highlightthickness = 0
                                 )
        self.frame.pack          (side = framepos, fill = BOTH, expand = YES)
        self.entrypos    = entrypos
        self.entryfill   = entryfill
        self.entryexpand = entryexpand
        if label is not None :
            self.label = Label   ( self # 22-Mar-1999 # self.frame
                                 , text    = label
                                 , name    = "label"
                                 , justify = labeljustify
                                 )
            self.label.pack      ( side    = labelpos
                                 , fill    = X
                                 , anchor  = labelanchor
                                 , padx    = labelpadx
                                 , pady    = labelpady
                                 )
        Entry_Tuple.__init__     (self)
    # end def __init__

    def add (self, entry, ** pack_kw) :
        Entry_Tuple.add   (self, entry)
        self._set_option  ("side",   self.entrypos,    pack_kw)
        self._set_option  ("fill",   self.entryfill,   pack_kw)
        self._set_option  ("expand", self.entryexpand, pack_kw)
        apply             (entry.pack, (), pack_kw)
    # end def add

# end class Entrybox

class Listdrop_ (CT_TK_mixin) :
    """Provide mixin functionality for a drop-down listbox.

       This mixin works only in descendants of C_Entry.
    """

    Listbox = Scrolled_Listbox

    def __init__ (self, master, list, side, state = NORMAL) :
        self.dropped     = None
        self.list        = map              (None, list)
        self.drop_button = Button           ( self.entrybox
                                            , name       = "dropbutton"
                                            , bitmap     = bitmap_mgr
                                                               ["small_combo"]
                                            , command    = self.toggle
                                            , takefocus  = 0
                                            , state      = state
                                            )
        self.drop_button.pack               ( side = side, before = self.entry)
        self.drop_box    = Toplevel         ( self
                                            , class_ = self.widget_class
                                            , name   = "dropbox"
                                            )
        self.drop_box.withdraw              ( )
        self.drop_box.overrideredirect      ( 1)
        self.scroll_box  = self.Listbox     ( self.drop_box, list
                                            , name  = "dropdown"
                                            )
        self.scroll_box.pack                (fill = BOTH, expand = YES)
        self._define_keys                   ()
    # end def __init__

    def _define_keys (self) :
        self.scroll_box.list_box.bind       ( "<ButtonRelease-1>"
                                            , self.mouse_select, add = 1
                                            )
        self.scroll_box.list_box.bind       ( "<Return>"
                                            , self.key_select, add = 1
                                            )
        self.scroll_box.list_box.bind       ( "<FocusOut>"
                                            , self.undrop_focus_out
                                            )
    # end def _define_keys

    def reload (self, list) :
        self.list = map (None, list)
        self.scroll_box.reload (list)
        if not self.get () in list : self.set (None)
    # end def reload

    def toggle (self, event = None) :
        if not self.dropped :
            self.drop   (event)
        else                :
            self.undrop (event)
    # end def toggle

    def drop   (self, event = None) :
        if self.dropped : return
        else            : self.dropped = 1
        ht    = self.entrybox.winfo_height    ()
        wd    = self.entrybox.winfo_width     ()
        x     = self.entrybox.winfo_rootx     ()
        y     = self.entrybox.winfo_rooty     () + ht - 1
        rht   = min (self.drop_box.winfo_reqheight (), 4 * ht)
        self.drop_box.deiconify               ()
        self.drop_box.tkraise                 ()
        self.drop_box.geometry                ("%dx%d+%d+%d"% (wd, rht, x, y))
        self._sync_dropdown                   ()
        self.scroll_box.list_box.focus        ()
    # end def drop

    def _sync_dropdown (self) :
        curr = self.get                       ()
        i = 0
        if curr :
            if curr not in self.list :
                try :
                    curr = int (curr)
                    i    = self.list.index (curr)
                except (SystemExit, KeyboardInterrupt), exc :
                    raise
                except :
                    i = 0
            else :
                i = self.list.index (curr)
        self.scroll_box.select         (i)
    # end def _sync_dropdown

    def undrop (self, event = None) :
        if self.dropped :
            self.drop_box.withdraw ()
            self.dropped = None
    # end def undrop

    def undrop_focus_out (self, event = None) :
        ### under Windows, the <FocusOut> binding unfortunately means that a
        ### click on the drop-button doesn't remove the listbox

        ### (the FocusOut event arrives before the event for the clicking of
        ### the button -- therefore toggle believes it has to drop)
        ### use of `after' and `after_idle' do not help

        ### therefore the `winfo_containing' trickery must be used to decide
        ### whether the event was generated by a click on the drop-button or
        ### not (if yes, we don't do anything and let the `toggle' command of
        ### the drop-button do it's work)
        if event :
            w = self.winfo_containing ( self.drop_button.winfo_pointerx ()
                                      , self.drop_button.winfo_pointery ()
                                      )
            if w != self.drop_button :
                self.undrop (event)
        else :
            self.undrop (event)
    # end def undrop_focus_out

    def mouse_select (self, event) :
        self.select (self.scroll_box.list_box.nearest (event.y), event)
    # end def mouse_select

    def key_select (self, event = None) :
        self.select (self.scroll_box.index  (), event)
    # end def key_select

    def select (self, i, event = None) :
        if i is not None and self.list :
            self.set       (self.list [i])
            self.undrop    (event)
            self.focus_set ()
        return i
    # end def select

    def enable (self) :
        """Enable input into widget."""
        self.drop_button.configure (state = NORMAL)
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        self.drop_button.configure (state = DISABLED)
    # end def disable

# end class Listdrop_

class Listdropentry_ (Listdrop_, C_Entry) :
    """Entry with dropdown listbox."""

    widget_class = "Listdropentry"

    def __init__ ( self, master, list
                 , name         = None
                 , entryname    = None
                 , entryfill    = X
                 , entrypos     = LEFT
                 , label        = None
                 , labelpos     = LEFT
                 , labelanchor  = None
                 , labeljustify = None
                 , default      = None
                 , state        = NORMAL
                 , takefocus    = 1
                 , bindtag      = None
                 , editable     = None
                 ) :
        if editable is None :
            editable = (state == NORMAL)
        self.editable = editable
        C_Entry.__init__   ( self, master
                           , name         = name
                           , entryname    = entryname
                           , entryfill    = entryfill
                           , entrypos     = entrypos
                           , label        = label
                           , labelpos     = labelpos
                           , labelanchor  = labelanchor
                           , labeljustify = labeljustify
                           , default      = default
                           , state        = state
                           , takefocus    = takefocus
                           , bindtag      = bindtag
                           )
        Listdrop_.__init__ ( self, master, list, RIGHT, state = state)
        if not editable : C_Entry.disable (self)
    # end def __init__

    def enable (self) :
        """Enable input into widget."""
        if self.editable :
            C_Entry.enable (self)
        Listdrop_.enable (self)
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        C_Entry.disable   (self)
        Listdrop_.disable (self)
    # end def disable

# end class Listdropentry_

class Listdropentry (Listdropentry_) :
    """Entry with dropdown listbox."""

    def __init__ (self, * args, ** kw) :
        apply (Listdropentry_.__init__, (self, ) + args, kw)
        self._bind_completer (self.entry, self.complete)
    # end def __init__

    def complete (self, event = None) :
        C_Entry._complete (self, self.list)
    # end def complete

# end class Listdropentry

class Listdropentry_Extended (Listdropentry_) :
    """Entry with dropdown listbox with extended selectmode"""

    Listbox = Scrolled_Listbox_Extended

    def _define_keys (self) :
        Listdropentry_._define_keys   (self)
        self.scroll_box.list_box.bind ( "<Shift-ButtonRelease-1>"
                                      , lambda * args : "break"
                                      )
        self.scroll_box.list_box.bind ( "<Shift-Double-ButtonRelease-1>"
                                      , self.key_select
                                      )
        self.scroll_box.list_box.bind ( "<Control-ButtonRelease-1>"
                                      , lambda * args : "break"
                                      )
        self.scroll_box.list_box.bind ( "<Control-Double-ButtonRelease-1>"
                                      , self._double_control_select
                                      )
    # end def _define_keys

    def reload (self, list) :
        Listdropentry_.reload (self, list)
        self._sync_dropdown   ()
    # end def reload

    def _sync_dropdown (self) :
        try :
            vs = int (self.get ())
            self.scroll_box.set (vs)
        except (SystemExit, KeyboardInterrupt), exc :
            raise
        except :
            pass
    # end def _sync_dropdown

    def select (self, i, event = None) :
        if i is not None and self.list :
            selection = self.scroll_box.indices ()
            l         = self.list
            value     = ", ".join (repr (l [i]) for i in selection)
            if value :
                self.set   ( "(%s%s)"
                           % (value, ("", ", ") [len (selection) == 1])
                           )
            else :
                self.set   ("")
            self.undrop    (event)
            self.focus_set ()
        return i
    # end def select

    def _double_control_select (self, event) :
        if event :
            w = self.scroll_box.list_box
            i = w.nearest      (event.y)
            if i in self.scroll_box.indices () :
                w.select_set   (i)
            else :
                w.select_clear (i)
            self.key_select    (event)
            return "break"
    # end def _double_control_select

# end class Listdropentry_Extended

class Combo_Entry :
    """Listbox combined with entry.

       This class provides everything necessary for the synchronization of
       the listbox- and the entry-widgets.

       It does not supply any geometry management (no container-widget for
       listbox and entry).
    """

    widget_class = "Combo_Entry"

    def __init__ ( self, c_listbox
                 , entry          = None
                 , select_event   = "<Double-ButtonPress-1>"
                 , bindtag        = None
                 , select_binding = None
                 ) :
        self.combo_box = c_listbox
        self.list_box  = lbox = c_listbox.list_box
        if entry :
            ### for descendants of `Combo_Entry' which are also descendants
            ### of `C_Entry' the value of `entry' must be none
            ###
            ### `entry' is only used for classes using a `C_Entry' instead
            ### of inheriting from `C_Entry'
            self.entry     = entry
            self._complete = entry._complete
        lbox.bind (select_event, self.mouse_select, add = 1)
        if select_binding :
            self.select_binding = select_binding
        else :
            self.select_binding = self.key_select
        btag = "%s_%d_Combo_Entry" % (self.widget_class, id (self))
        self._define_keys (btag)
        add_bindtag       (lbox, btag, -1)
        if bindtag :
            add_bindtag (lbox, bindtag)
    # end def __init__

    def _define_keys (self, btag) :
        for k in ( "<Up>",   "<Down>", "<Control-Home>", "<Control-End>"
                 , "<ButtonPress-1>"
                 , "<Next>", "<Prior>"
                 ) :
            self.list_box.bind_class (btag, k, self.select_binding)
        for k in ("<ButtonRelease-1>", ) :
            ### if `<ButtonRelease-1>' is handled immediately,
            ### `self.select_binding' doesn't work as expected -- the entry
            ### shows the value selected by `<ButtonPress-1>' instead of the
            ### value shown by the combobox itself
            ###
            ### therefore, it is done `after_idle'
            self.list_box.bind_class (btag, k, self.after_idle_select_binding)
        if self.entry :
            self.entry._bind_completer (self.entry, self.complete)
        self._select_binding_pending = None
    # end def _define_keys

    def after_idle_select_binding (self, event = None) :
        if not self._select_binding_pending :
            self._select_binding_pending = self.list_box.after_idle \
                (lambda s=self, e=event : s._after_idle_select_binding (e))
    # end def after_idle_select_binding

    def _after_idle_select_binding (self, event) :
        self._select_binding_pending = None
        self.select_binding (event)
    # end def _after_idle_select_binding

    def complete (self, event = None) :
        v = self.entry.get ()
        if v :
            l = list (self.list_box.get (0, END))
            c, m = self._complete (l)
            if m :
                self.combo_box.select (l.index (m [-1]))
                self.combo_box.select (l.index (m [0]))
    # end def complete

    def mouse_select (self, event) :
        self.select (self.list_box.nearest (event.y))
    # end def mouse_select

    def key_select (self, event = None) :
        self.select (self.combo_box.index ())
    # end def key_select

    def select (self, i) :
        if i is not None :
            try    :
                self._entry_set (self.list_box.get (i))
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                pass
    # end def select

    def _entry_set (self, val)     : self.entry.set         (val)
    def insert     (self, i, elem) : self.combo_box.insert  (i, elem)
    def delete     (self, i)       : self.combo_box.delete  (i)
    def reload     (self, list)    : self.combo_box.reload  (list)
    def enable     (self)          : self.combo_box.enable  ()
    def disable    (self)          : self.combo_box.disable ()

# end class Combo_Entry

class Combo_ :
    """Provide mixin functionality for diverse combo-listboxes.

       This mixin works only in descendants of C_Entry.
    """

    fixed_height    = "180"
    frame_expand    = YES
    combo_fill      = X
    combo_expand    = None

# end class Combo_

class Combobox_ (CT_TK_mixin, Combo_, Combo_Entry) :
    """Provide mixin functionality for a combo-listbox.

       This mixin works only in descendants of C_Entry.
    """

    Listbox_class   = Scrolled_Listbox

    def __init__ ( self, master, list, side, select_event
                 , before      = None
                 , bindtag     = None
                 ) :
        combo_box = self.Listbox_class ( self, list, name = "combo")
        combo_box.pack                 ( side   = side
                                       , fill   = self.combo_fill
                                       , expand = self.combo_expand
                                       , before = before
                                       )
        Combo_Entry.__init__           ( self, combo_box
                                       , select_event   = select_event
                                       , bindtag        = bindtag
                                       )
    # end def __init__

    def _entry_set (self, val) : self.set (val)

# end class Combobox_

class Combobox (Combobox_, C_Entry) :
    """Entry with static listbox."""

    widget_class = "Combobox"

    def __init__ ( self, master, list
                 , select_event   = "<Double-ButtonPress-1>"
                 , name           = None
                 , entryname      = None
                 , entryfill      = X
                 , entrypos       = TOP
                 , label          = None
                 , labelpos       = LEFT
                 , labelanchor    = S
                 , labeljustify   = None
                 , default        = None
                 , state          = NORMAL
                 , takefocus      = 1
                 , bindtag        = None
                 ) :
        C_Entry.__init__   ( self, master
                           , name         = name
                           , entryname    = entryname
                           , entryfill    = entryfill
                           , entrypos     = entrypos
                           , label        = label
                           , labelpos     = labelpos
                           , labelanchor  = labelanchor
                           , labeljustify = labeljustify
                           , default      = default
                           , state        = state
                           , takefocus    = takefocus
                           , bindtag      = bindtag
                           )
        Combobox_.__init__ ( self, master, list
                           , self.inverse_pos [entrypos]
                           , select_event
                           , bindtag = bindtag
                           )
    # end def __init__

    def enable (self) :
        """Enable input into widget."""
        Combobox_.enable (self)
        C_Entry.enable   (self)
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        Combobox_.disable (self)
        C_Entry.disable   (self)
    # end def disable

# end class Combobox

class Combo_Tuple (Listbox_Tuple_, Entry_Tuple, C_Frame) :
    """Set of coupled combo entries scrolled by 1 scrollbar."""

    widget_class = "Combo_Tuple"

    def __init__ ( self, master
                 , entry_number   = 2      ### number of entries in Combo_Tuple
                 , name           = None
                 , selectmode     = BROWSE
                 , select_event   = "<Double-ButtonPress-1>"
                 , col_labels     = ()
                 , row_labels     = ()
                 , state          = NORMAL
                 , takefocus      = 1
                 , bindtag        = None
                 , col_label_row  = 0
                 , listbox_row    = 1
                 , entry_row      = 2
                 , padx           = 1
                 , pady           = 1
                 ) :
        C_Frame.__init__         ( self, master, class_ = self.widget_class
                                 , name = name
                                 )
        Entry_Tuple.__init__     (self)
        Listbox_Tuple_.__init__  (self, selectmode  = selectmode)
        self.entry_number        = entry_number
        self.select_event        = select_event
        self.state               = state
        self.takefocus           = takefocus
        self.bindtag             = bindtag
        self.col_label_row       = col_label_row
        self.listbox_row         = listbox_row
        self.entry_row           = entry_row
        self.padx                = padx
        self.pady                = pady
        self.col_label           = []
        self.row_label           = []
        self.combo               = []
        self.list_boxes          = []
        if col_labels :
            assert (len (col_labels) == entry_number)
            for l in col_labels :
                self.col_label.append (Label ( self
                                             , text   = l
                                             , padx   = 2
                                             , anchor = W
                                             )
                                      )
        else :
            self.col_label = [None] * entry_number
        self.col_label.append (Frame (self))
        if row_labels :
            for l in row_labels :
                self.row_label.append (Label (self, text = l, padx = 2))
    # end def __init__

    def add_listbox (self, LB_class, * args,  ** kw) :
        """Add a listbox of type `LB_class' to `Combo_Tuple'."""
        assert (len (self.list_boxes) < self.entry_number)
        lb = apply                 (LB_class, (self, ) + args, kw)
        Listbox_Tuple_.add_listbox (self, lb)
        self.list_boxes.append     (lb)
    # end def add_listbox

    def add_entry (self, Entry_class, * args, ** kw) :
        """Add an entry of type `Entry_class' to `Combo_Tuple'."""
        assert (len (self.entry) < self.entry_number)
        entry = apply        (Entry_class, (self, ) + args, kw)
        Entry_Tuple.add      (self, entry)
        ### 31-Mar-2000
        ### set height of `entry' and disable it's `pack_propagate' to avoid
        ### spurious changes of the widths of the grid-row
        entry.configure      (height = entry.fixed_height)
        entry.pack_propagate (0)
    # end def add_entry

    def init_finish (self) :
        """Completes initialization of `Combo_Tuple'. This must be called
           after all listboxes and entries were added and before the
           `Combo_Tuple' is used.
        """
        assert (len (self.entry)      == self.entry_number)
        assert (len (self.list_boxes) == self.entry_number)
        for lb, e in paired (self.list_boxes, self.entry) :
            self.combo.append ( Combo_Entry ( lb, e
                                            , self.select_event
                                            , self.bindtag
                                            , self.key_select_after
                                            )
                              )
        self._grid_col (self.row_label,  0,                  1, "e")
        self._grid_row (self.col_label,  self.col_label_row, 1, "ew")
        self._grid_row (self.list_boxes, self.listbox_row,   1, "ewsn")
        self._grid_row (self.entry,      self.entry_row,     1, "ew")
        self.grid_rowconfigure (self.listbox_row, weight = 1)
        for i in range (1, self.entry_number + 1) :
            self.grid_columnconfigure (i, weight = 1)
        self.grid_columnconfigure (self.entry_number + 1, minsize = 20)
    # end def init_finish

    def _grid_col (self, widgets, col, start_row, sticky) :
        row = start_row
        for w in widgets :
            if w : self._grid_one (w, row, col, sticky)
            row = row + 1
    # end def _grid_col

    def _grid_row (self, widgets, row, start_col, sticky) :
        col = start_col
        for w in widgets :
            if w : self._grid_one (w, row, col, sticky)
            col = col + 1
    # end def _grid_row

    def _grid_one (self, widget, row, col, sticky, padx = None, pady = None) :
        if padx is None :
            padx = self.padx
        if pady is None :
            pady = self.pady
        widget.grid ( row    = row
                    , column = col
                    , padx   = padx
                    , pady   = pady
                    , sticky = sticky
                    )
    # end def _grid_one

    def _y_scroll_pack (self) :
        self._grid_one ( self.y_scroll
                       , self.listbox_row
                       , self.entry_number + 1
                       , "ns"
                       , padx = 0
                       )
    # end def _y_scroll_pack

    def _y_scroll_pack_forget (self) :
        self.y_scroll.grid_forget ()
    # end def _y_scroll_pack_forget

    def key_select_after (self, event = None) :
        for c in self.combo:
            c.key_select (event)
        self.on_change ()
    # end def key_select_after

    def select (self, i) :
        if i is not None :
            Listbox_Tuple_.select (self, i)
            for c in self.combo :
                c.select (i)
            self.on_change ()
    # end def select

    def on_change (self) : pass

    def enable (self) :
        """Enable input into widget."""
        Entry_Tuple.enable    (self)
        Listbox_Tuple_.enable (self)
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        Entry_Tuple.disable    (self)
        Listbox_Tuple_.disable (self)
    # end def disable

    def focus_force (self) :
        if self.list_boxes :
            self.list_boxes [0].focus_force ()
    # end def focus_force

    def focus_set (self) :
        if self.list_boxes :
            self.list_boxes [0].focus_set ()
    # end def focus_set

    focus = focus_set
# end class Combo_Tuple

class Combo_Tuple_X (Combo_Tuple) :
    """Combo_Tuple with additional target entries."""

    def __init__ (self, ** kw) :
        apply (Combo_Tuple.__init__, (self, ), kw)
        self.target = Entry_Tuple ()
    # end def __init__

    def add_target_entry (self, Entry_class, * args, ** kw) :
        """Add an entry of type `Entry_class' to `self.target'."""
        assert (len (self.target.entry) < self.entry_number)
        entry = apply (Entry_class, (self, ) + args, kw)
        self.target.add (entry)
    # end def add_target_entry

    def init_finish (self) :
        """Completes initialization of `Combo_Tuple'. This must be called
           after all listboxes and entries were added and before the
           `Combo_Tuple' is used.
        """
        assert (len (self.target.entry) == self.entry_number)
        Combo_Tuple.init_finish (self)
        row = self.entry_row + 1
        self._grid_row (self.target.entry, row, 1, "ew")
    # end def init_finish

    def enable (self) :
        """Enable input into widget."""
        Combo_Tuple.enable  (self)
        self.target.enable  ()
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        Combo_Tuple.disable (self)
        self.target.disable ()
    # end def disable

# end class Combo_Tuple_X

class Combo_Tuple_Xtern (Combo_Tuple) :
    """Combo_Tuple with additional target entries in a separate widget."""

    class _Entrybox (Entrybox) :
         pass
    # end class _Entrybox

    def __init__ (self, t_master, ** kw) :
        apply (Combo_Tuple.__init__, (self, ), kw)
        self.target = self._Entrybox ( t_master
                                     , name = "target"
                                     , entryfill    = None
                                     , entryexpand  = NO
                                     )
        self.bind                    ("<Configure>", self.repack_target)
        self.__pending = None
    # end def __init__

    def add_target_entry (self, Entry_class, * args, ** kw) :
        """Add an entry of type `Entry_class' to `self.target'."""
        assert (len (self.target.entry) < self.entry_number)
        entry = apply (Entry_class, (self.target.frame, ) + args, kw)
        self.target.add (entry)
    # end def add_target_entry

    def init_finish (self) :
        """Completes initialization of `Combo_Tuple'. This must be called
           after all listboxes and entries were added and before the
           `Combo_Tuple' is used.
        """
        assert (len (self.target.entry) == self.entry_number)
        Combo_Tuple.init_finish (self)
        self.repack_target      ()
    # end def init_finish

    def repack_target (self, event = None) :
        if not self.__pending :
            self.__pending = self.after_idle (self._repack_target)
    # end def repack_target

    def _repack_target (self, event = None) :
        self.__pending = None
        self._grid_row (self.target.entry, 1, 1, "ew")
        g = self.target.frame
        for i in range (1, self.entry_number + 1) :
            e = self.entry [i - 1]
            ### for some reason, setting `minsize' to `e.winfo_width' doesn't
            ### line up corresponding columns of `entry' and `target',
            ### because, apparently, `winfo_width' doesn't include the `padx'
            w = e.winfo_width () + 2 * int (e.grid_info () ["padx"])
            g.grid_columnconfigure (i, weight = 1, minsize = w)
        g.grid_columnconfigure (self.entry_number + 1, minsize = 20)
    # end def _repack_target

    def enable (self) :
        """Enable input into widget."""
        Combo_Tuple.enable  (self)
        self.target.enable  ()
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        Combo_Tuple.disable (self)
        self.target.disable ()
    # end def disable

# end class Combo_Tuple_Xtern

#### Multicombobox and Multicombobox_X are obsolete
#### (replaced by Combo_Tuple and Combo_Tuple_X)

####class Multicombobox (Combobox_, Entrybox) :
####    """Combobox with structured elements.
####
####       The contents of the listbox is split/joined into/from a number of
####       entries.
####    """
####
####    widget_class = "Multicombobox"
####
####    separator    = " "
####
####    def __init__ ( self, master, list
####                 , select_event   = "<Double-ButtonPress-1>"
####                 , name           = None
####                 , entryname      = None
####                 , entryfill      = X
####                 , entrypos       = TOP
####                 , listboxpos     = TOP
####                 , label          = None
####                 , labelpos       = LEFT
####                 , labelanchor    = S
####                 , labeljustify   = None
####                 , labelpadx      = None
####                 , labelpady      = None
####                 , bindtag        = None
####                 , entry_sep      = None
####                 ) :
####        if entry_sep : self.separator = entry_sep
####        self.list = list
####        Entrybox.__init__  ( self, master
####                           , name         = entryname
####                           , entryfill    = entryfill
####                           , entrypos     = entrypos
####                           , framepos     = listboxpos
####                           , label        = label
####                           , labelpos     = labelpos
####                           , labelanchor  = labelanchor
####                           , labeljustify = labeljustify
####                           , labelpadx    = labelpadx
####                           , labelpady    = labelpady
####                           )
####        Combobox_.__init__ ( self, master, list
####                           , listboxpos
####                           , select_event
####                           , before  = self.frame
####                           , bindtag = bindtag
####                           )
####    # end def __init__
####
####    def reload (self, list) :
####        self.list = list
####        Combobox_.reload (self, list)
####
####    def select (self, i) :
####        if i is not None and self.list :
####            self.set (string.split (self.list [i], self.separator))
####
####    def enable (self) :
####        """Enable input into widget."""
####        Entrybox.enable  (self)
####        Combobox_.enable (self)
####
####    def disable (self) :
####        """Disable input into widget."""
####        Entrybox.disable  (self)
####        Combobox_.disable (self)
##### end class Multicombobox
####
####class Multicombobox_X (Multicombobox) :
####    """Multicombobox with additional target entries."""
####
####    fixed_height    = "210"
####
####    def __init__ ( self, master, list
####                 , select_event   = "<Double-ButtonPress-1>"
####                 , name           = None
####                 , entryname      = None
####                 , entryfill      = X
####                 , entrypos       = TOP
####                 , listboxpos     = TOP
####                 , label          = None
####                 , labelpos       = LEFT
####                 , labelanchor    = S
####                 , labeljustify   = None
####                 , labelpadx      = None
####                 , labelpady      = None
####                 , bindtag        = None
####                 , entry_sep      = None
####                 , targetlabel    = None
####                 ) :
####        Multicombobox.__init__ ( self, master, list
####                               , select_event   = select_event
####                               , name           = name
####                               , entryname      = entryname
####                               , entryfill      = entryfill
####                               , entrypos       = entrypos
####                               , listboxpos     = listboxpos
####                               , label          = label
####                               , labelpos       = labelpos
####                               , labelanchor    = labelanchor
####                               , labeljustify   = labeljustify
####                               , labelpadx      = labelpadx
####                               , labelpady      = labelpady
####                               , bindtag        = bindtag
####                               , entry_sep      = entry_sep
####                               )
####
####        ### self.target masquerades as an entrybox
####        self.target    = Frame   ( self
####                                 , name               = "target"
####                                 , borderwidth        = 0
####                                 , relief             = FLAT
####                                 , highlightthickness = 0
####                                 )
####        self.target.pack         ( side               = listboxpos
####                                 , fill               = BOTH
####                                 , expand             = YES
####                                 )
####        if targetlabel is not None :
####            self.target_label = Label ( self.target
####                                      , text = targetlabel
####                                      , name = "label"
####                                      )
####            self.target_label.pack    ( side   = labelpos
####                                      , fill   = X
####                                      , padx   = labelpadx
####                                      , pady   = labelpady
####                                      )
####        self.target.entry = []
####        self.target.add   = self.target_add
####        self.target.get   = self.target_get
####        self.target.set   = self.target_set
####    # end def __init__
####
####    def target_add (self, entry, ** pack_kw) :
####        self.target.entry.append (entry)
####        self._set_option  ("side",   self.entrypos,    pack_kw)
####        self._set_option  ("fill",   self.entryfill,   pack_kw)
####        self._set_option  ("expand", self.entryexpand, pack_kw)
####        apply             (entry.pack, (), pack_kw)
####
####    def target_get (self) :
####        return map (lambda x : x.get (), self.target.entry)
####
####    def target_set (self, value) :
####        map ( lambda p : p [0].set (p [1])
####            , paired (self.target.entry, value)
####            )
####
####    def enable (self) :
####        """Enable input into widget."""
####        Multicombobox.enable (self)
####        for entry in self.target.entry : entry.enable ()
####
####    def disable (self) :
####        """Disable input into widget."""
####        Multicombobox.disable (self)
####        for entry in self.target.entry : entry.disable ()
##### end class Multicombobox_X

class Up_Down_Button (C_Frame) :
    """Button pair for increment/decrement operation on an entry."""

    widget_class = "Up_Down_Button"

    def __init__ ( self, master, entry
                 , name         = None
                 , up_command   = None
                 , down_command = None
                 , state        = NORMAL
                 ) :
        """If `up_command' (`down_command') is not given, `entry.next'
           (`entry.prev') is used as command for the buttons.
        """
        C_Frame.__init__ ( self, master, class_ = self.widget_class
                         , name = name
                         )
        self.entry   = entry
        self.state   = state
        if up_command   : self.next_cmd = up_command
        else            : self.next_cmd = entry.next
        if down_command : self.prev_cmd = down_command
        else            : self.prev_cmd = entry.prev

        self.next = Button ( self, name  = "next"
                           , bitmap      = bitmap_mgr ["small_decr"]
                           , takefocus   = 0
                           , state       = state
                           , borderwidth = 1
                           )
        self.prev = Button ( self, name  = "prev"
                           , bitmap      = bitmap_mgr ["small_incr"]
                           , takefocus   = 0
                           , state       = state
                           , borderwidth = 1
                           )
        self._bind_buttons ()
        self.next.pack (side = BOTTOM)
        self.prev.pack (side = TOP)
    # end def __init__

    def _bind_buttons (self) :
        if self.state == NORMAL :
            self.next.bind ("<ButtonPress-1>", self.next_cmd)
            self.prev.bind ("<ButtonPress-1>", self.prev_cmd)
    # end def _bind_buttons

    def _unbind_buttons (self) :
        self.next.bind ("<ButtonPress-1>", break_event)
        self.prev.bind ("<ButtonPress-1>", break_event)
    # end def _unbind_buttons

    def enable (self) :
        """Enable input into widget."""
        for button in self.next, self.prev :
            button.configure (state = NORMAL)
        self._bind_buttons ()
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        for button in self.next, self.prev :
            button.configure (state = DISABLED)
        self._unbind_buttons ()
    # end def disable

# end class Up_Down_Button

class Num_Slider (C_Entry) :

    def __init__ (self, master, from_v, to_v, ** kw) :
        self.from_v = from_v
        self.to_v   = to_v
        C_Entry.__init__ (self, master, ** kw)
    # end def __init__

    def _make_entry (self, entryname, state, takefocus, bindtag) :
        entry = Scale \
            ( self.entrybox, from_ = self.from_v, to = self.to_v
            , orient = HORIZONTAL, showvalue = False
            )
        self._old_get = entry.get
        self._old_set = entry.set
        entry.get     = self.get
        entry.set     = self.set
        return entry
    # end def _make_entry

    def get (self) :
        return str (self._old_get ())
    # end def get

    def set (self, value) :
        if value not in ("", None) :
            self._old_set (int (value))
    # end def set

# end class Num_Slider

class Spinner_ (CT_TK_mixin) :
    """Provide mixin functionality for a spinner entry.

       This mixin works only in descendants of C_Entry.
    """

    speed_default = 200
    speed_min     =  50
    speed_delta   =  30

    def __init__ ( self, master
                 , side        = RIGHT
                 , before      = None
                 , state       = NORMAL
                 ) :
        self.pending     = None
        self.speed       = self.speed_default
        self.spin_button = Up_Down_Button \
            ( self.entrybox, self
            , name    = "spinbutton"
            , state   = state
            )
        self.spin_button.pack      (side = side, before = before)
        self.spin_button.next.bind ("<ButtonRelease-1>", self.cancel_pending)
        self.spin_button.prev.bind ("<ButtonRelease-1>", self.cancel_pending)
        self.entry.bind            ("<KeyPress-Up>",     self._prev)
        self.entry.bind            ("<KeyPress-Down>",   self._next)
    # end def __init__

    def _schedule (self, fct) :
        self.pending = self.after (self.speed, fct)
        if self.speed > self.speed_min :
            self.speed = self.speed - self.speed_delta
    # end def _schedule

    def next (self, event = None) :
        self._next     (event)
        self._schedule (self.next)
    # end def next

    def prev (self, event = None) :
        self._prev     (event)
        self._schedule (self.prev)
    # end def prev

    def _next (self, event = None) :
        self.change    (self.inc)
    # end def _next

    def _prev (self, event = None) :
        self.change    (- self.inc)
    # end def _prev

    def cancel_pending (self, event = None) :
        if self.pending : self.after_cancel (self.pending)
        self.speed = self.speed_default
    # end def cancel_pending

    def enable (self) :
        """Enable input into widget."""
        self.spin_button.enable ()
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        self.spin_button.disable ()
    # end def disable

# end class Spinner_

class Spinnerentry_ (Spinner_, C_Entry) :
    """Root class for spinner widgets.
       A spinner is an entry field with associated increment/decrement buttons.
    """

    def __init__ ( self, master
                 , name           = None
                 , entryname      = None
                 , entryfill      = X
                 , entrypos       = LEFT
                 , label          = None
                 , labelpos       = LEFT
                 , labelanchor    = E
                 , labeljustify   = None
                 , default        = None
                 , state          = NORMAL
                 , takefocus      = 1
                 , bindtag        = None
                 ) :
        C_Entry.__init__  ( self, master
                          , name         = name
                          , entryname    = entryname
                          , entryfill    = entryfill
                          , entrypos     = entrypos
                          , label        = label
                          , labelpos     = labelpos
                          , labelanchor  = labelanchor
                          , labeljustify = labeljustify
                          , default      = default
                          , state        = state
                          , takefocus    = takefocus
                          , bindtag      = bindtag
                          )
        Spinner_.__init__ ( self, master, RIGHT
                          , state     = state
                          )
    # end def __init__

    def enable (self) :
        """Enable input into widget."""
        C_Entry.enable  (self)
        Spinner_.enable (self)
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        C_Entry.disable  (self)
        Spinner_.disable (self)
    # end def disable

# end class Spinnerentry_

class Num_Spinner (Spinnerentry_) :
    """Spinner widget for numeric input."""

    widget_class = "Num_Spinner"

    def __init__ ( self, master
                 , lo_bound       = None, hi_bound = None
                 , inc            = None, wrap     = 1
                 , name           = None
                 , entryname      = None
                 , entryfill      = X
                 , entrypos       = LEFT
                 , label          = None
                 , labelpos       = LEFT
                 , labelanchor    = E
                 , labeljustify   = None
                 , default        = None
                 , state          = NORMAL
                 , takefocus      = 1
                 , bindtag        = None
                 ) :
        Spinnerentry_.__init__ ( self, master
                               , name         = name
                               , entryname    = entryname
                               , entryfill    = entryfill
                               , entrypos     = entrypos
                               , label        = label
                               , labelpos     = labelpos
                               , labelanchor  = labelanchor
                               , labeljustify = labeljustify
                               , default      = default
                               , state        = state
                               , takefocus    = takefocus
                               , bindtag      = bindtag
                               )
        self.lo_bound = lo_bound
        self.hi_bound = hi_bound
        self.wrap     = wrap
        ### The "up" button subtracts `inc`, so we change the sign here,
        ### cause for a Num_Spinner, "up" should count up
        if inc : self.inc = -inc
        else   : self.inc = -1
    # end def __init__

    def change (self, inc) :
        value = self.get ()
        if value is not None :
            try :
                value = int (value) + inc
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                self.show_error ( "Illegal Integer"
                                , "Integer value expected; \n"
                                + "got `" + value +  "' instead."
                                )

            if   (self.lo_bound is not None) and self.lo_bound > value :
                if self.wrap : value = self.hi_bound
                else         : value = self.lo_bound
            elif (self.hi_bound is not None) and self.hi_bound < value :
                if self.wrap : value = self.lo_bound
                else         : value = self.hi_bound

            self.set (value)
        elif (inc < 0) and (self.lo_bound is not None) :
            self.set (self.lo_bound)
        elif (inc > 0) and (self.hi_bound is not None) :
            self.set (self.hi_bound)
        self.focus_set ()
    # end def change
# end class Num_Spinner

class Listspinner_ (CT_TK_mixin) :
    """Provide mixin functionality for a spinner-listbox.

       This mixin works only in descendants of C_Entry.
    """

    inc = 1

    def __init__ (self, list, default) :
        self.list  = map (None, list)
        self.last  = default
        self.i     = self.index (default)
    # end def __init__

    def reload (self, list) :
        self.list = map (None, list)
        if not self.get () in list :
            self.last = None
            self.set (None)
    # end def reload

    def index (self, value) :
        if value is None :
            return 0
        else :
            try    :
                return self.list.index (value)
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                return 0
    # end def index

    def change (self, delta) :
        if not self.list : return
        value = self.get ()
        if value is not None:
            self.i = self.index (value) + delta
            if self.i <  0               : self.i = len (self.list) - 1
            if self.i >= len (self.list) : self.i = 0
        elif (delta < 0)  :
            self.i = 0
        elif (delta > 0) :
            self.i = len (self.list) - 1
        self.set       (self.list [self.i])
        self.focus_set ()
    # end def change
# end class Listspinner_

class Listspinner (Listspinner_, Spinnerentry_) :
    """Spinner widget for list of values."""

    widget_class = "Listspinner"

    def __init__ ( self, master, list
                 , name           = None
                 , entryname      = None
                 , entryfill      = X
                 , entrypos       = LEFT
                 , label          = None
                 , labelpos       = LEFT
                 , labelanchor    = E
                 , labeljustify   = None
                 , default        = None
                 , state          = NORMAL
                 , takefocus      = 1
                 , bindtag        = None
                 ) :
        Spinnerentry_.__init__ ( self, master
                               , name         = name
                               , entryname    = entryname
                               , entryfill    = entryfill
                               , entrypos     = entrypos
                               , label        = label
                               , labelpos     = labelpos
                               , labelanchor  = labelanchor
                               , labeljustify = labeljustify
                               , default      = default
                               , state        = state
                               , takefocus    = takefocus
                               , bindtag      = bindtag
                               )
        Listspinner_.__init__  ( self, list, default)
        self._bind_completer   ( self.entry, self.complete)
    # end def __init__

    def complete (self, event = None) :
        C_Entry._complete (self, self.list)
    # end def complete

# end class Listspinner

class Listdropspinner (Listspinner_, Spinner_, Listdropentry) :
    """Entry with spinner and dropdown listbox."""

    def __init__ ( self, master, list
                 , name         = None
                 , entryname    = None
                 , entryfill    = X
                 , entrypos     = RIGHT
                 , label        = None
                 , labelpos     = LEFT
                 , labelanchor  = None
                 , labeljustify = None
                 , default      = None
                 , state        = NORMAL
                 , takefocus    = 1
                 , bindtag      = None
                 , editable     = None
                 ) :
        Listdropentry.__init__   ( self, master, list
                                 , name         = name
                                 , entryname    = entryname
                                 , entryfill    = entryfill
                                 , entrypos     = entrypos
                                 , label        = label
                                 , labelpos     = labelpos
                                 , labelanchor  = labelanchor
                                 , labeljustify = labeljustify
                                 , default      = default
                                 , state        = state
                                 , takefocus    = takefocus
                                 , bindtag      = bindtag
                                 , editable     = editable
                                 )
        Spinner_.__init__        ( self, master
                                #, side        = LEFT
                                 , before      = self.entry
                                 , state       = state
                                 )
        Listspinner_.__init__    ( self, list, default)
    # end def __init__

    def reload (self, list) :
        Listspinner_.reload  (self, list)
        Listdropentry.reload (self, list)
    # end def reload

    def enable (self) :
        """Enable input into widget."""
        Listdropentry.enable (self)
        Spinner_.enable      (self)
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        Listdropentry.disable (self)
        Spinner_.disable      (self)
    # end def disable

# end class Listdropspinner

class History_Spinner (Listdropspinner) :
    """Entry widget with listdropspinner for history of values entered into
       the entry.
    """

    def __init__ (self, master, history = None, ** kw) :
        self._entry_history = Entry_History (history)
        apply ( Listdropspinner.__init__
              , (self, master, ())
              , kw
              )
        self._entry_history.attach (self)
        self.list = self._entry_history.values
        self.scroll_box.reload (self.list)
    # end def __init__

    def unhighlight_focus (self, event = None) :
        Listdropspinner.unhighlight_focus (self, event)
        self.scroll_box.reload (self.list)
    # end def unhighlight_focus

# end class History_Spinner

class Combobox_Listdropspinner (Combo_, Listdropspinner) :
    """Provides a Listdropspinner entry with a static listbox.
    """

    widget_class    = "Combobox"

    def __init__ ( self, master, list
                 , select_event   = "<Double-ButtonPress-1>"
                 , name           = None
                 , entryname      = None
                 , entryfill      = X
                 , entrypos       = TOP
                 , label          = None
                 , labelpos       = LEFT
                 , labelanchor    = S
                 , labeljustify   = None
                 , default        = None
                 , state          = NORMAL
                 , takefocus      = 1
                 , bindtag        = None
                 ) :
        """Constructs the listdropspinner with an additional listbox attached
           and synchronized

           self          The object itself
           master        The master widget in wchich the widget resides
           list          The list of textual entries
           select_event  selcetion event, default = doubleclick button 1
           name          Name of the widget, default = None
           entryname     Name of the entry, default = None
           entryfill     Fill method of the entry, default = X
           entrypos      position of the listdropspinner, default = TOP
           label         widget label name, default = None
           labelpos      position of the label, default = LEFT
           labelanchor   Anchor direction of the label text (NSWE), default = S
           labeljustify  Justification of the label text, default = None
           state         Displaying state of the widget, default = NORMAL
           takefocus     the widget may take the focus, default = 1
           bindtag       a binding tag, default = None
        """

        Listdropspinner.__init__     ( self, master, list
                                     , name         = name
                                     , entryname    = entryname
                                     , entryfill    = entryfill
                                     , entrypos     = entrypos
                                     , label        = label
                                     , labelpos     = labelpos
                                     , labelanchor  = labelanchor
                                     , labeljustify = labeljustify
                                     , default      = default
                                     , state        = state
                                     , takefocus    = takefocus
                                     , bindtag      = bindtag
                                     )
        combo_box = Scrolled_Listbox ( self, list, name = "combo")
        combo_box.pack               ( side   = self.inverse_pos [entrypos]
                                     , fill   = self.combo_fill
                                     , expand = self.combo_expand
                                     , before = None
                                     )
        self.combo_box   = combo_box
        self.combo_entry = Combo_Entry ( combo_box
                                       , entry        = self
                                       , select_event = select_event
                                       , bindtag      = bindtag
                                       )
        self.lbox        = self.combo_entry
        ### cannot do this before creation of `self.combo_box'
        self.set         = self.set_and_sync
    # end def __init__

    def mouse_select (self, event) :
        if event.widget == self.scroll_box.list_box:
            Listdropspinner.mouse_select  (self, event)
        if event.widget == self.combo_entry.list_box:
            self.combo_entry.mouse_select (event)
    # end def mouse_select

    def select (self, i, event = None) :
        if i is not None and self.list :
            self.set              (self.list [i])
            self.undrop           (event)
            self.focus_set        ()
        return i
    # end def select

    def set_and_sync (self, value) :
        Listdropspinner.set (self, value)
        try :
            self.combo_box.select (self.list.index (value))
        except (SystemExit, KeyboardInterrupt), exc :
            raise
        except :
            ### hide exceptions due to values not in `self.list'
            pass
    # end def set_and_sync

    def enable (self) :
        """Enable input into widget."""
        self.combo_box.enable     ()
        Listdropspinner.enable    (self)
    # end def enable

    def disable (self) :
        """Disable input into widget."""
        self.combo_box.disable    ()
        Listdropspinner.disable   (self)
    # end def disable

    def reload (self, list) :
        """Reload the widget."""
        self.combo_box.reload     (list)
        Listdropspinner.reload    (self, list)
    # end def reload
# end class Combobox_Listdropspinner

class C_Menu (CT_TK_mixin, Menu) :
    """Augment `Menu' with help for menu commands."""

    balloon_owner = None
    widget_class  = "Menu"

    _n            = 0

    def __init__ (self, master = None, help = None, balloon = None, ** kw) :
        if kw.has_key ("name") :
            kw ["name"] = kw ["name"].lower ()
        apply (Menu.__init__, (self, master), kw)
        self.help_widget         = help
        self.balloon             = balloon
        self.cmd_map             = {}
        self.hlp_map             = {}
        self._short_map          = {}
        self._pending_short_cuts = {}
        self.active_help         = None
        if help or balloon :
            if 0 :
                ### this code doesn't work for whatever reasons
                ### (e.g., in TTPplan, only one of the entries of the menu bar
                ### really has the `btag' and thus reacts to the bindings;
                ### even these bindings do not work, though -- `index
                ### (ACTIVE)' returns None instead of the active entry)
                self.__class__._n = self._n + 1
                btag = "%s_%s_btag" % (self.widget_class, self._n)
                add_bindtag     (self, btag, -1)
                self.bind_class \
                    (btag, "<<help>>",       self._help_active_entry)
                self.bind_class \
                    (btag, "<<MenuSelect>>", self._help_active_entry)
                self.bind_class (btag, "<Unmap>",        self.deactivate_help)
            ### the following <Motion> binding works under Unix but not under
            ### Windows
            self.bind ("<Motion>",       self.help)
            self.bind ("<Unmap>",        self.deactivate_help)
        ### the following hacks around a bug in Tkinter 1.63 which doesn't
        ### correctly handle menus configured as menubar
        hacked_name = str (self).replace (".", "#")
        self.master.children [hacked_name] = self
    # end def __init__

    def clear (self) :
        """Delete all entries from menu"""
        self.delete (0, END)
        self._short_map          = {}
        self._pending_short_cuts = {}
    # end def clear

    def enable_entry (self, label) :
        self.entryconfigure (self.index (label), state = NORMAL)
    # end def enable_entry

    def disable_entry (self, label) :
        self.entryconfigure (self.index (label), state = DISABLED)
    # end def disable_entry

    def add_command (self, ** kw) :
        self.__add (Menu.add_command, kw)
    # end def add_command

    def insert_command (self, index, ** kw) :
        self.__add (Menu.insert_command, kw, index)
    # end def insert_command

    def add_cascade (self, ** kw) :
        self.__add (Menu.add_cascade, kw)
    # end def add_cascade

    def insert_cascade (self, index, ** kw) :
        self.__add (Menu.insert_cascade, kw, index)
    # end def insert_cascade

    def add_checkbutton (self, ** kw) :
        self.__add (Menu.add_checkbutton, kw)
    # end def add_checkbutton

    def insert_checkbutton (self, ** kw) :
        self.__add (Menu.insert_checkbutton, kw)
    # end def insert_checkbutton

    def popup (self, event, xdelta = 15, ydelta = 5) :
        self.post (event.x_root - xdelta, event.y_root - ydelta)
    # end def popup

    def __add (self, fct, kw, * args) :
        if kw.has_key ("_doc") and kw.has_key ("label") :
            self.hlp_map [kw ["label"]] = kw ["_doc"]
            del kw ["_doc"]
        self._handle_shortcut (kw)
        apply (fct, (self, ) + args, kw)
        if kw.has_key ("command") and kw.has_key ("label") :
            self.cmd_map [kw ["label"]] = kw ["command"]
    # end def __add

    def _handle_shortcut (self, kw) :
        if kw.has_key ("label") :
            label = kw ["label"]
            if kw.has_key ("underline") and kw ["underline"] is not None :
                short_cut = label [kw ["underline"]]
                if (   self._short_map.has_key (short_cut)
                   and short_cut not in "0123456789"
                   ) :
                    msg = ( "Duplicate short cut `%s' for "
                            "menu entries `%s' and `%s'"
                          )
                    print msg % (short_cut, self._short_map [short_cut], label)
                    self._add_pending_short_cut (short_cut, label)
                else :
                    self._short_map [short_cut] = label
            else :
                sc, i = self._letter_shortcut (label, label [0], 0)
                if sc :
                    self._add_pending_short_cut (sc, label)
    # end def _handle_shortcut

    def _add_pending_short_cut (self, short_cut, label) :
        short_cut = short_cut.lower ()
        if not self._pending_short_cuts.has_key (short_cut) :
            self._pending_short_cuts [short_cut] = []
        self._pending_short_cuts [short_cut].append (label)
    # end def _add_pending_short_cut

    def set_auto_short_cuts (self) :
        """Set short cuts automatically for all menu entries for which no
           unique short cut was explicitly set.
        """
        items = sorted ( self._pending_short_cuts.items ()
                       , lambda (scl, ll), (scr, lr) :
                             cmp (scl, scr) or cmp (len (ll), len (lr))
                       )
        for sc, labels in items :
            del self._pending_short_cuts [sc]
            for label in labels :
                self._set_auto_short_cut (sc, label, label.lower ().index (sc))
        for sc, label in self._short_map.items () :
            if self.type (label) in ("checkbutton", "radiobutton") :
                self.bind ("<Key %s>" % sc, self._toggle_button)
                if ("a" <= sc <= "z") :
                    self.bind ("<Key %s>" % sc.upper (), self._toggle_button)
    # end def set_auto_short_cuts

    def _toggle_button (self, event) :
        ### toggle checkbutton or radiobutton without unposting the menu
        sc = event.keysym.lower ()
        if self._short_map.has_key (sc) :
            self.invoke (self._short_map [sc])
            return "break"
    # end def _toggle_button

    def _set_auto_short_cut (self, sc, label, i = 0) :
        sc, i = self._unique_short_cut (label, sc, i)
        if sc is not None :
            self._short_map [sc] = label
            self.entryconfigure (label, underline = i)
    # end def _set_auto_short_cut

    def _letter_shortcut (self, label, sc, i) :
        sc = sc.lower ()
        while not ("a" <= sc <= "z") :
            i = i + 1
            if i > len (label) : return None, None
            sc = label [i].lower ()
        return sc, i
    # end def _letter_shortcut

    def _unique_short_cut (self, label, sc, i) :
        sc, i = self._letter_shortcut (label, sc, i)
        if sc and self._short_map.has_key (sc) :
            for i in range (i, len (label)) :
                sc = label [i].lower ()
                if not ("a" <= sc <= "z")           : continue
                if not self._short_map.has_key (sc) : return sc, i
            return None, None
        else :
            return sc, i
    # end def _unique_short_cut

    def help (self, event = None) :
        if   event : widget = event.widget
        else       : widget = self
        if self.winfo_containing (event.x_root, event.y_root) == self :
            try :
                index = self.index     ("@%d" % (event.y, ))
                label = self.entrycget (index, "label")
                self._help_label       (label, widget, event)
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                pass
        else :
            self.deactivate_help ()
    # end def help

    def _help_active_entry (self, event = None) :
        ### print ".",
        ### unfortunately, `index (ACTIVE)' doesn't work as advertised
        ###                (it always returns `None')
        try :
            index = self.index (ACTIVE)
            print "kieselack %s" % index
            if index is not None :
                label = self.entrycget (index, "label")
                self._help_label       (label, self, event)
            else :
                pass
                ### print "no active index?"
        except (SystemExit, KeyboardInterrupt), exc :
            raise
        except :
            traceback.print_exc ()
            pass
    # end def _help_active_entry

    def _help_label (self, label, widget = None, event = None) :
        widget = widget or self
        if label and (  self.cmd_map.has_key (label)
                     or self.hlp_map.has_key (label)
                     ) :
            if label != self.active_help :
                self.deactivate_help ()
                old_help         = self.active_help
                self.active_help = label
                cmd = self.cmd_map.get (label)
                msg = self.hlp_map.get (label, "")
                if (not msg) and cmd :
                    msg = cmd.__doc__
                if cmd :
                    try :
                        if hasattr (cmd, "im_self") :
                            msg = cmd.im_self.menu_help (label, cmd, msg)
                        else :
                            msg = cmd.menu_help         (label, cmd, msg)
                    except (SystemExit, KeyboardInterrupt), exc :
                        raise
                    except :
                        pass
                if   self.balloon :
                    self.__class__.balloon_owner = self
                    if event :
                        x, y  = event.x_root, event.y_root
                    else :
                        x = y = None
                    self.balloon.activate  ( widget, msg
                                           , x = x, y = y
                                           , delay = 50
                                           )
                elif self.help_widget :
                    self.help_widget.push_help (msg)
                else                  :
                    pass # print msg
        else :
            self.deactivate_help ()
    # end def _help_label

    def deactivate_help (self, event = None) :
        if self.balloon_owner :
            self.balloon_owner.balloon.deactivate ()
            self.balloon_owner.active_help = None
            self.__class__.balloon_owner   = None
        elif self.help_widget and self.active_help :
            self.help_widget.pop_help ()
            self.active_help = None
    # end def deactivate_help

# end class C_Menu

class Filename_Entry (C_Entry) :
    """Provide an entry widget for the input of filenames."""

    widget_class = "Filename_Entry"

    def __init__ ( self, master
                 , name             = None
                 , entryname        = "entry"
                 , entryfill        = X
                 , entrypos         = LEFT
                 , label            = None
                 , labelpos         = LEFT
                 , labelanchor      = None
                 , labeljustify     = None
                 , default          = None
                 , state            = NORMAL
                 , takefocus        = 1
                 , bindtag          = None
                 , must_exist       = 0
                 , defaultextension = None
                 , filetypes        = None
                 , selector_title   = None
                 ) :
        C_Entry.__init__          ( self, master
                                  , name         = name
                                  , entryname    = entryname
                                  , entryfill    = entryfill
                                  , entrypos     = entrypos
                                  , label        = label
                                  , labelpos     = labelpos
                                  , labelanchor  = labelanchor
                                  , labeljustify = labeljustify
                                  , default      = default
                                  , state        = state
                                  , takefocus    = takefocus
                                  , bindtag      = bindtag
                                  )
        self.must_exist         = must_exist
        self.defaultextension   = defaultextension
        self.filetypes          = filetypes
        self.selector_title     = selector_title
        self.menu_button = Button ( self.entrybox
                                  , name       = "menubutton"
                                  , bitmap     = bitmap_mgr ["more"]
                                  , command    = self.popup_file_selector
                                  , takefocus  = 0
                                  , state      = state
                                  )
        self.menu_button.pack     ( side = RIGHT, before = self.entry)
        self._bind_completer      ( self.entry, self.popup_file_selector)
    # end def __init__

    def popup_file_selector (self, event = None) :
        self.entry.focus_set ()
        old = self.get ()
        if old :
            file = sos.path.basename (old)
            path = sos.path.dirname  (old)
        else :
            file = path = ""
        new = apply ( (self.ask_save_file_name, self.ask_open_file_name)
                          [self.must_exist]
                    , ()
                    , { "defaultextension" : self.defaultextension
                      , "filetypes"        : self.filetypes
                      , "initialdir"       : path
                      , "initialfile"      : file
                      , "title"            : self.selector_title or self.name
                      }
                    )
        if new :
            self.set (new)
        self.after_idle (self.entry.focus_set)
    # end def popup_file_selector

# end class Filename_Entry

class Dirname_Entry (Filename_Entry) :

    widget_class = "Dirname_Entry"

    __Ancestor   = Ancestor = Filename_Entry

    def popup_file_selector (self, event = None) :
        self.entry.focus_set ()
        old = self.get ()
        if old :
            if sos.altsep :
                old = old.replace (sos.altsep, sos.sep)
            if not old.endswith (sos.sep) :
                old += sos.sep
            path = old
        else :
            path = ""
        new = apply ( self.ask_dir_name
                    , ()
                    , { "defaultextension" : self.defaultextension
                      , "filetypes"        : self.filetypes
                      , "initialdir"       : path
                      , "title"            : self.selector_title or self.name
                      }
                    )
        if new :
            self.set (new)
        self.after_idle (self.entry.focus_set)
    # end def popup_file_selector
# end class Dirname_Entry

class Editor_Entry (C_Entry) :
    """Provide an entry widget for text with popup editor widget."""

    widget_class = "Editor_Entry"

    def __init__ ( self, master
                 , name             = None
                 , entryname        = "entry"
                 , entryfill        = X
                 , entrypos         = LEFT
                 , label            = None
                 , labelpos         = LEFT
                 , labelanchor      = None
                 , labeljustify     = None
                 , default          = None
                 , state            = NORMAL
                 , takefocus        = 1
                 , bindtag          = None
                 , editor_title     = None
                 ) :
        C_Entry.__init__          ( self, master
                                  , name         = name
                                  , entryname    = entryname
                                  , entryfill    = entryfill
                                  , entrypos     = entrypos
                                  , label        = label
                                  , labelpos     = labelpos
                                  , labelanchor  = labelanchor
                                  , labeljustify = labeljustify
                                  , default      = default
                                  , state        = state
                                  , takefocus    = takefocus
                                  , bindtag      = bindtag
                                  )
        self.editor_title = editor_title
        self.menu_button  = Button ( self.entrybox
                                   , name       = "menubutton"
                                   , bitmap     = bitmap_mgr ["more"]
                                   , command    = self.popup_editor
                                   , takefocus  = 0
                                   )
        self.drop_box     = None
        self.dropped      = 0
        self.menu_button.pack      ( side = RIGHT, before = self.entry)
        self.entry.bind            ("<<edit>>", self.popup_editor)
    # end def __init__

    def _drop_box (self) :
        if not self.drop_box :
            drop_box = BB_Toplevel     ( self
                                       , class_      = self.widget_class
                                       , name        = "dropbox"
                                       , close_cmd   = self.close_editor
                                       , destroy_cmd = self.cancel_editor
                                       , title       = self.editor_title
                                       , close_name  = "Commit"
                                       )
            self.drop_box              = drop_box
            drop_box.transient         ( self)
            drop_box.button_box.add    ( "Cancel"
                                       , command     = self.cancel_editor
                                       , before      = "Commit"
                                       )
            drop_box.withdraw          ()
            edit_box = Scrolled_Text   ( drop_box
                                       , name        = "editor"
                                       , state       = self.state
                                       , x_scroll    = 0
                                       , wrap        = "word"
                                       )
            self.edit_box              = edit_box
            edit_box.pack              (fill = BOTH,  expand = YES)
            # edit_box.bind            ("<FocusOut>", self.cancel_editor)
            edit_box.bind              ("<Escape>",   self.cancel_editor)
            edit_box.bind              ("<Tab>",      self.close_editor)
            edit_box.bind              ("<<edit>>",   self.close_editor)
            entrybox = self.entrybox
            d  = 2 ### to compensate for size of window border
            f  = 1 ###    (use f = 2, d = 5 if not transient/overrideredirect)
            ht = entrybox.winfo_height ()
            x  = entrybox.winfo_rootx  () + d
            y  = entrybox.winfo_rooty  () + d + ht * f - 1
            drop_box.geometry          ("+%d+%d" % (x, y))
            drop_box.minsize           (200, 100)
        return self.drop_box
    # end def _drop_box

    def popup_editor (self, event = None) :
        if self.dropped :
            return self.cancel_editor (event)
        self.dropped = 1
        drop_box = self._drop_box     ()
        edit_box = self.edit_box
        old      = self.get           ()
        edit_box.clear                ()
        edit_box.put                  (old)
        drop_box.deiconify            ()
        drop_box.tkraise              ()
        edit_box.body.focus_set       ()
    # end def popup_editor

    def cancel_editor (self, event = None) :
        if self.dropped :
            self.drop_box.withdraw  ()
            self.after_idle         (self.entry.focus_set)
            self.dropped = None
        return "break"
    # end def cancel_editor

    def close_editor (self, event = None) :
        if self.dropped :
            new = self.edit_box.get (START, END).strip ()
            self.set (new)
            return self.cancel_editor ()
        return "break"
    # end def close_editor

# end class Editor_Entry

class Fileview (Scrolled_Text) :
    """Display a file in a text window"""

    widget_class = "Fileview"
    __Ancestor   = Ancestor = Scrolled_Text

    def __init__ (self, master, file, name = None, ** kw) :
        if isinstance (file, (str, unicode)) :
            file = open ( file, "r")
        apply           ( self.__Ancestor.__init__
                        , (self, master, name, DISABLED), kw
                        )
        self.insert     ( "at_end", file.read ())
    # end def __init__
# end class Fileview

class Boolean_Variable (IntVar) :
    """Wrap an IntVar so that it can be used directly as boolean value
       (without going through `get').
    """

    def __nonzero__ (self) :
        return self.get () != 0
    # end def __nonzero__

# end class Boolean_Variable

class C_Toplevel (CT_TK_mixin, Toplevel) :

    __Ancestor   = Ancestor = Toplevel
    widget_class = "Toplevel"
    state_mgr    = None
    window_title_bar_icon_name = None

    def __init__ \
        ( self, master = None, name = None, class_ = None, close_cmd = None
        , destroy_cmd = None, title = None, state_mgr = None, ** kw
        ) :
        if name :
            name = name.lower ()
        self.name          = name
        self._sname        = title or name
        self.close_cmd     = close_cmd   or self.withdraw
        self.destroy_cmd   = destroy_cmd or self.destroy
        kw.update          ({"name" : name, "class" : self.widget_class})
        apply              (self.__Ancestor.__init__, (self, master), kw)
        self.set_maxsize   ()
        self.protocol      ("WM_DELETE_WINDOW", self.destroy_cmd)
        self.bind          ("<Escape>",         self.close_cmd)
        if title :
            self.title     (title)
        if state_mgr :
            ### don't override class attribute with None
            self.state_mgr   = state_mgr
        if self.state_mgr :
            self._pending_gu = None
            self._restore_geometry ()
            self.bind ("<Configure>", self._defer_update_state_mgr)
            self.bind ("<Motion>",    self._defer_update_state_mgr)
        self._set_window_title_bar_icon ()
    # end def __init__

    def withdraw (self, event = None) :
#        self.save_geometry       (self.state_mgr, self._sname)
        self.__Ancestor.withdraw (self)
    # end def withdraw

    def destroy (self, event = None) :
#        self.save_geometry      (self.state_mgr, self._sname)
        self.__Ancestor.destroy (self)
    # end def destroy

    def _defer_update_state_mgr (self, event = None) :
        if not self._pending_gu :
            self._pending_gu = self.after_idle (self._update_state_mgr)
    # end def _defer_update_state_mgr

    def _update_state_mgr (self) :
        try     :
            self.save_geometry (self.state_mgr, self._sname)
        finally :
            self._pending_gu = None
    # end def _update_state_mgr

    def _restore_geometry (self) :
        g = self.geometry_state ()
        if g :
            self.geometry (g)
    # end def _restore_geometry

    def geometry_state (self) :
        if self.state_mgr and self._sname :
            return self.state_mgr.window_geometry.get (self._sname)
        return None
    # end def geometry_state

    def _set_window_title_bar_icon (self) :
        if  (   self.window_title_bar_icon_name
            and sos.path.exists (self.window_title_bar_icon_name)
            ) :
            try :
                ico = self.window_title_bar_icon_name
                if sys.platform != "win32" :
                    ico = "@%s" % ico
                self.iconbitmap (ico)
            except :
                if __debug__ and (not Environment.frozen ()) :
                    raise
    # end def _set_window_title_bar_icon

# end class C_Toplevel

class BB_Toplevel (CT_TK_mixin, C_Toplevel) :
    """Toplevel with buttonbox with a close button."""

    __Ancestor   = Ancestor = C_Toplevel
    widget_class = "Toplevel"

    def __init__ \
        ( self, master = None, name = None, class_ = None, help = None
        , close_cmd = None, destroy_cmd = None, title = None
        , button_box_side = BOTTOM, button_cols = 32, close_name = "Close"
        , state_mgr = None
        ) :
        self.__Ancestor.__init__ \
            ( self, master, name, class_
            , close_cmd, destroy_cmd, title, state_mgr
            )
        self.button_box = Buttongrid   ( self
                                       , name        = "button_box"
                                       , padx        = 5
                                       , pady        = 5
                                       , help        = help
                                       , columns     = button_cols
                                       )
        self.button_box.pack           ( side        = button_box_side
                                       , fill        = X
                                       )
        self.button_box.add            ( close_name
                                       , command = close_cmd or self.withdraw
                                       )
    # end def __init__

# end class BB_Toplevel

if _default_root :
    root = _default_root
else :
    try :
        root = _default_root = Tk ()
    except (SystemExit, KeyboardInterrupt), exc :
        raise
    except :
        traceback.print_exc ()
        root = _default_root = None

if root :
    ### The <Next> and <Prior> keys are handled somewhat strangely by the
    ### standard bindings of the TK listbox. Therefore they are disabled here.
    root.bind_class ("Listbox", "<Next>",  ignore_event)
    root.bind_class ("Listbox", "<Prior>", ignore_event)

    if   sos.name == "posix" :
        root.event_add ("<<StartScan>>",    "<ButtonPress-2>")
        root.event_add ("<<ContinueScan>>", "<B2-Motion>")
        root.event_add ("<<print>>",        "<F16>")
        ### Labeled F12 at TTTech
        ### linux machines
        root.event_add ("<<printAll>>",     "<Control F16>")
        ### Labeled F12 at TTTech
        ### linux machines
    elif sos.name == "nt"    :
        root.event_add ("<<StartScan>>",    "<Shift-ButtonPress-1>")
        root.event_add ("<<ContinueScan>>", "<Shift-B1-Motion>")
        root.event_add ("<<print>>",        "<L2>")
        ### ??? ### <F12> key
        root.event_add ("<<printAll>>",     "<Control L2>")
        ### ??? ### <F12> key
    elif sos.name == "mac"   :
        root.event_add ("<<StartScan>>",    "<Shift-ButtonPress-1>")
        root.event_add ("<<ContinueScan>>", "<Shift-B1-Motion>")
        root.event_add ("<<print>>",        "<F12>")
        root.event_add ("<<printAll>>",     "<Control F12>")

    root.event_add ("<<copy>>",         "<Alt-c>")
    root.event_add ("<<complete>>",     "<Alt-i>")
    root.event_add ("<<edit>>",         "<Alt-e>")
    root.event_add ("<<new>>",          "<Alt-n>")
    root.event_add ("<<move>>",         "<Alt-r>")
    root.event_add ("<<undo>>",         "<Alt-z>")
    root.event_add ("<<view>>",         "<Alt-v>")
    root.event_add ("<<HistNext>>",     "<Alt-Down>")
    root.event_add ("<<HistPrev>>",     "<Alt-Up>")
    root.event_add ("<<HistComplete>>", "<Alt-q>")

    root.event_add ("<<help>>",         "<F1>")

    bitmap_mgr.add ("arrow.xbm")
    bitmap_mgr.add ("small_combo.xbm")
    bitmap_mgr.add ("small_decr.xbm")
    bitmap_mgr.add ("small_incr.xbm")
    bitmap_mgr.add ("more.xbm")
    bitmap_mgr.add ("calc.xbm")
    bitmap_mgr.add ("edit_oe.xbm")
    bitmap_mgr.add ("edit_oe_read_only.xbm")

    if __name__ != "__main__":
        read_option_files (root, "CT_TK.opt")
    else :
        _path = Environment.script_path ()
        read_option_files (root, "CT_TK.opt")

        tn = Tabbed_Notebook (root)
        tn.pack (expand = YES, fill = BOTH, padx = 5, pady = 5)
        p = tn.new_page ("List-Widgets")
        slc = Listbox_Tuple (p, 2)
        slc.pack   ()
        slc.insert ( END
                   , range (1, 25)
                   , ( "a", "b", "c", "d", "e", "f", "g", "h", "i"
                     , "j", "k", "l"
                     , "a", "b", "c", "d", "e", "f", "g", "h", "i"
                     , "j", "k", "l"
                     )
                   )
        slc = Combo_Tuple ( p
                          , col_labels = ("numbers", "letters")
                          , row_labels = ("From: ", "To: ")
                          )
        slc.pack   (side = BOTTOM)
        slc.add_listbox  (C_Listbox, list = range (1, 25))
        slc.add_entry    (Listdropspinner, range (1, 13))
        slc.add_listbox  \
            (C_Listbox, list =
                ( "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"
                , "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"
                )
            )
        slc.add_entry    (Listdropspinner, ("a", "c", "e", "g", "i", "k"))
        slc.init_finish  ()
        p = tn.new_page ("Entry-Widgets")
        lds = Listdropspinner \
            ( p
            , ("Completer", "Jänner", "Februar", "März", "April", "Mai", "Juni")
            , default = "März"
            )
        Entry_History ().attach (lds)
        lds.pack ()
        H_Separator (p).pack ()
        Listspinner        ( p
                           , ("abc", "abcd", "abcx", "April", "Mai", "Juni")
                           , default = "März"
                           ).pack ()
        H_Separator (p).pack ()
        Num_Spinner        ( p, default = 5, lo_bound = 1, hi_bound = 12
                           #, inc = -1 #, wrap = 0
                           ).pack ()
        H_Separator (p).pack ()
        Listdropentry      (p, range (4)).pack ()
        H_Separator (p).pack ()
        Listdropentry      (p, range (8), default = 2, state = DISABLED).pack ()
        H_Separator (p).pack ()
        eb = Entrybox (p, label = "Horizontal entrybox", labelpos = LEFT)
        eb.pack       ()
        eb.add        ( Listdropspinner ( eb
                                        , ( "Jänner", "Februar", "März"
                                          , "April", "Mai", "Juni"
                                          , "Juli", "August", "September"
                                          , "Oktober", "November", "Dezember"
                                          )
                                        , default = "Juni"
                                        )
                      , padx = 2, pady = 2
                      )
        eb.add        \
            ( Num_Spinner (eb, default = 7, lo_bound = 1, hi_bound = 24)
            , padx = 2, pady = 2
            )
        H_Separator (p).pack ()
        eb = Entrybox ( p, entrypos = TOP, entryfill = Y
                      , label = "Vertical entrybox", labelpos = TOP
                      )
        eb.pack       ()
        eb.add        ( Listdropspinner ( eb
                                        , ( "Jänner", "Februar", "März"
                                          , "April", "Mai", "Juni"
                                          , "Juli", "August", "September"
                                          , "Oktober", "November", "Dezember"
                                          )
                                        , default = "Juni"
                                        )
                      , padx = 2, pady = 2
                      )
        eb.add \
            ( Num_Spinner (eb, default = 7, lo_bound = 1, hi_bound = 24)
            , padx = 2, pady = 2
            )
    ####    H_Separator (p).pack ()
    ####    mc = Multicombobox ( p
    ####                       , ( "h1 c1"
    ####                         , "h1 c2"
    ####                         , "h2 c1"
    ####                         , "h3 c3"
    ####                         , "error"
    ####                         )
    ####                       , listboxpos = TOP, entrypos = LEFT
    ####                       )
    ####    mc.pack            ()
    ####    mc.add \
    ####        (C_Entry
    ####            (mc, label="Host",    labelpos = TOP), padx = 2, pady = 2
    ####        )
    ####    mc.add \
    ####       (C_Entry
    ####            (mc, label="Cluster", labelpos = TOP), padx = 2, pady = 2
    ####       )
        H_Separator (p).pack ()
        Combobox    (p, range (24)).pack ()
        p = tn.new_page ("Panes")
        pn = H_Panedwindow (p, width = 200, height = 150)
        pn.pack (expand = YES, fill = BOTH, padx = 5, pady = 5)
        Label ( pn.pane [0], width = 150
              , text =
                "   left pane ............................................."
              ).pack (fill = BOTH, expand = YES)
        pnr = V_Panedwindow (pn.pane [1])
        pnr.pack (expand = YES, fill = BOTH)
        Label ( pnr.pane [0], width = 80
              , text =
                "   middle pane ............................................"
              ).pack (fill = BOTH, expand = YES)
        Label ( pnr.pane [1], width = 120
              , text =
                "   right pane ............................................"
              ).pack (fill = BOTH, expand = YES)
        p = tn.new_page ("First")
        Label ( p, text = "First Kieselack"
              , justify = CENTER
              ).pack (fill = BOTH, expand = YES)
        elb = Scrolled_Listbox_Extended \
                  ( p
                  , ( "a", "b", "c", "d", "e", "f", "g", "h", "i"
                    , "j", "k", "l"
                    )
                  )
        elb.pack  (side = BOTTOM)
        p = tn.new_page ("Second")
        Label ( p, text = "Another Kieselack"
              , justify = CENTER
              ).pack (fill = BOTH, expand = YES)
    #    Label \
    #        ( p, image = PhotoImage
    #            (file = "/swing/python/distrib/ptui-1.1pr1/icons/logo.gif")
    #        , justify = CENTER
    #        ).pack (fill = BOTH, expand = YES)
        p = tn.new_page ("···")
        Label ( p, text = "Under construction...", height = 12
              , justify = CENTER
              ).pack (fill = BOTH, expand = YES)
        p = tn.new_page ("Last")
        Label ( p, text = "No more Kieselacks", width = 40
              , justify = CENTER
              ).pack (fill = BOTH, expand = YES)
        tn.select   (p)
        tn.update   ()
        tn.display  ("List-Widgets")
        tn.mainloop ()
