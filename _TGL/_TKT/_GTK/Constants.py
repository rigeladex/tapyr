# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
#
#++
# Name
#    TGL.TKT.GTK.Constants
#
# Purpose
#    Provide constants used within the GTK toolkit
#
# Revision Dates
#     8-Apr-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK import GTK
import _TGL._TKT._GTK.Object

gtk = GTK.gtk

GTK._Add \
    ( LEFT                    = gtk.POS_LEFT
    , RIGHT                   = gtk.POS_RIGHT
    , TOP                     = gtk.POS_TOP
    , BOTTOM                  = gtk.POS_BOTTOM
      # Corners (Scrolled_Window placement policies)
    , TOP_LEFT                = gtk.CORNER_TOP_LEFT
    , BOTTOM_LEFT             = gtk.CORNER_BOTTOM_LEFT
    , TOP_RIGHT               = gtk.CORNER_TOP_RIGHT
    , BOTTOM_RIGHT            = gtk.CORNER_BOTTOM_RIGHT
      # Orientation
    , HORIZONTAL              = gtk.ORIENTATION_HORIZONTAL
    , VERTICAL                = gtk.ORIENTATION_VERTICAL
      # Box packing type
    , START                   = gtk.PACK_START
    , END                     = gtk.PACK_END
      # Attachment policies
    , EXPAND                  = gtk.EXPAND
    , FILL                    = gtk.FILL
    , SHRINK                  = gtk.SHRINK
    , RUBBER                  = gtk.EXPAND | gtk.FILL | gtk.SHRINK
      # Scrollbar display policies
    , AUTOMATIC               = gtk.POLICY_AUTOMATIC
    , ALWAYS                  = gtk.POLICY_ALWAYS
    , NEVER                   = gtk.POLICY_NEVER
      # Window types
    , TOPLEVEL                = gtk.WINDOW_TOPLEVEL
    , POPUP                   = gtk.WINDOW_POPUP
      # Window placements
    , POS_NONE                = gtk.WIN_POS_NONE
    , POS_CENTER              = gtk.WIN_POS_CENTER
    , POS_MOUSE               = gtk.WIN_POS_MOUSE
    , POS_CENTER_ALWAYS       = gtk.WIN_POS_CENTER_ALWAYS
    , POS_CENTER_ON_PARENT    = gtk.WIN_POS_CENTER_ON_PARENT
      # Frame styles
    , SHADOW_NONE             = gtk.SHADOW_NONE
    , SHADOW_IN               = gtk.SHADOW_IN
    , SHADOW_OUT              = gtk.SHADOW_OUT
    , SHADOW_ETCHED_IN        = gtk.SHADOW_ETCHED_IN
    , SHADOW_ETCHED_OUT       = gtk.SHADOW_ETCHED_OUT
      # Button_Box packing type
    , BB_DEFAULT              = gtk.BUTTONBOX_DEFAULT_STYLE
    , BB_START                = gtk.BUTTONBOX_START
    , BB_END                  = gtk.BUTTONBOX_END
    , BB_SPREAD               = gtk.BUTTONBOX_SPREAD
    , BB_EDGE                 = gtk.BUTTONBOX_EDGE
      # text directions
    , TEXT_DIR_RTL            = gtk.TEXT_DIR_RTL
    , TEXT_DIR_LTR            = gtk.TEXT_DIR_LTR
    , TEXT_DIR_NONE           = gtk.TEXT_DIR_NONE
      # Toolbar styles and child types
    , TOOLBAR_ICONS           = gtk.TOOLBAR_ICONS
    , TOOLBAR_TEXT            = gtk.TOOLBAR_TEXT
    , TOOLBAR_BOTH            = gtk.TOOLBAR_BOTH
    , TOOLBAR_BOTH_HORIZONTAL = gtk.TOOLBAR_BOTH_HORIZ
    # Wrap modes for Text_View and Label :
    , WRAP_CHAR               = gtk.WRAP_CHAR
    , WRAP_NONE               = gtk.WRAP_NONE
    , WRAP_WORD               = gtk.WRAP_WORD
    # Message types for dialogs :
    , MESSAGE_ERROR           = gtk.MESSAGE_ERROR
    , MESSAGE_INFO            = gtk.MESSAGE_INFO
    , MESSAGE_QUESTION        = gtk.MESSAGE_QUESTION
    , MESSAGE_WARNING         = gtk.MESSAGE_WARNING
    # keysyms for key-press-events
    , Keys                    = gtk.keysyms
    # event masks               :
    , ALL_EVENTS_MASK          = gtk.gdk.ALL_EVENTS_MASK
    , ALT_MASK                 = gtk.gdk.MOD1_MASK
    , BUTTON1_MOTION_MASK      = gtk.gdk.BUTTON1_MOTION_MASK
    , BUTTON2_MOTION_MASK      = gtk.gdk.BUTTON2_MOTION_MASK
    , BUTTON3_MOTION_MASK      = gtk.gdk.BUTTON3_MOTION_MASK
    , BUTTON_MOTION_MASK       = gtk.gdk.BUTTON_MOTION_MASK
    , BUTTON_PRESS_MASK        = gtk.gdk.BUTTON_PRESS_MASK
    , BUTTON_RELEASE_MASK      = gtk.gdk.BUTTON_RELEASE_MASK
    , CONTROL_MASK             = gtk.gdk.CONTROL_MASK
    , ENTER_NOTIFY_MASK        = gtk.gdk.ENTER_NOTIFY_MASK
    , EXPOSURE_MASK            = gtk.gdk.EXPOSURE_MASK
    , FOCUS_CHANGE_MASK        = gtk.gdk.FOCUS_CHANGE_MASK
    , KEY_PRESS_MASK           = gtk.gdk.KEY_PRESS_MASK
    , KEY_RELEASE_MASK         = gtk.gdk.KEY_RELEASE_MASK
    , LEAVE_NOTIFY_MASK        = gtk.gdk.LEAVE_NOTIFY_MASK
    , POINTER_MOTION_HINT_MASK = gtk.gdk.POINTER_MOTION_HINT_MASK
    , POINTER_MOTION_MASK      = gtk.gdk.POINTER_MOTION_MASK
    , PROPERTY_CHANGE_MASK     = gtk.gdk.PROPERTY_CHANGE_MASK
    , PROXIMITY_IN_MASK        = gtk.gdk.PROXIMITY_IN_MASK
    , PROXIMITY_OUT_MASK       = gtk.gdk.PROXIMITY_OUT_MASK
    , SCROLL_MASK              = gtk.gdk.SCROLL_MASK
    , SHIFT_MASK               = gtk.gdk.SHIFT_MASK
    , STRUCTURE_MASK           = gtk.gdk.STRUCTURE_MASK
    , SUBSTRUCTURE_MASK        = gtk.gdk.SUBSTRUCTURE_MASK
    , VISIBILITY_NOTIFY_MASK   = gtk.gdk.VISIBILITY_NOTIFY_MASK

    , SINGLE_CLICK             = gtk.gdk.BUTTON_PRESS
    , DOUBLE_CLICK             = gtk.gdk._2BUTTON_PRESS
    , TRIPLE_CLICK             = gtk.gdk._3BUTTON_PRESS
    # accelerator configuration :
    , ACCEL_VISIBLE            = gtk.ACCEL_VISIBLE
    # selection modes (only for gtk.Treeselection?):
    , SELECTION_SINGLE         = gtk.SELECTION_SINGLE
    , SELECTION_MULTIPLE       = gtk.SELECTION_MULTIPLE
    , SELECTION_BROWSE         = gtk.SELECTION_BROWSE
    , SELECTION_EXTENDED       = gtk.SELECTION_EXTENDED
    # hints for the window manager decoration
    , WINDOW_TYPE_NORMAL       = gtk.gdk.WINDOW_TYPE_HINT_NORMAL
    , WINDOW_TYPE_UTILITY      = gtk.gdk.WINDOW_TYPE_HINT_UTILITY
    , WINDOW_TYPE_SPLASHSCREEN = gtk.gdk.WINDOW_TYPE_HINT_SPLASHSCREEN
    )

### __END__ TGL.TKT.GTK.Constants
