# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.UI._Test_Command_Mgr
#
# Purpose
#    Test the command manager interface
#
# Revision Dates
#    13-Jan-2005 (MG) Creation
#    19-Jan-2005 (CT) Test fixed
#    ««revision-date»»···
#--

"""
>>> cmd_mgr = TFL.UI.Command_Mgr (
...      1, dict ( menu_1 = CI_Menu ("menu_1")
...              , menu_2 = CI_Menu ("menu_2")
...              )
...     )
>>>
>>> g1 = cmd_mgr.add_group ("Group_1", if_names = ("menu_1", ))
>>> g2 = cmd_mgr.add_group ("Group_2", if_names = ("menu_2", ))
>>>
>>> g1.add_command (TFL.UI.Command ("fct_1", fct_1), if_names = ("menu_1", ))
>>> g1.add_command (TFL.UI.Command ("fct_2", fct_2), if_names = ("menu_1", ))
>>> g2.add_command (TFL.UI.Command ("fct_3", fct_3), if_names = ("menu_2", ))
>>> g2.add_command (TFL.UI.Command ("fct_4", fct_4), if_names = ("menu_2", ))
>>> print cmd_mgr ["Group_1"].interfacers ['menu_1']
menu_1 ['fct_1', 'fct_2']
>>> print cmd_mgr ["Group_1"].interfacers ['menu_2']
Traceback (most recent call last):
  ...
KeyError: 'menu_2'
>>> print cmd_mgr ["Group_2"].interfacers ['menu_1']
Traceback (most recent call last):
  ...
KeyError: 'menu_1'
>>> print cmd_mgr ["Group_2"].interfacers ['menu_2']
menu_2 ['fct_3', 'fct_4']
"""

from   _TFL                   import TFL
import _TFL._UI.Command_Mgr
import _TFL._TKT.Command_Interfacer

def fct_1 () :
    print "fct_1"
# end def fct_1

def fct_2 () :
    print "fct_2"
# end def fct_2

def fct_3 () :
    print "fct_3"
# end def fct_3

def fct_4 () :
    print "fct_4"
# end def fct_4

class CI_Menu (TFL.TKT.Command_Interfacer) :

    def __init__ (self, name, * args, ** kw) :
        self.name  = name
        self.items = []
    # end def __init__

    def add_group (self, name, index = None, delta = 0, ** kw) :
        return self.__class__ (name)
    # end def add_group

    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , info            = None
            , icon            = None
            , as_check_button = False
            , cmd_name        = None
            , ** kw
            ) :
        self.items.append ((name, callback))
    # end def add_command

    def __str__ (self) :
        return "%s %r" % (self.name, [n for (n, f) in self.items])
    # end def __str__

# end class CI_Menu

"""
from _TFL._UI._Test_Command_Mgr import *
cmd_mgr = TFL.UI.Command_Mgr \
    (1, dict ( menu_1 = CI_Menu ("menu_1")
             , menu_2 = CI_Menu ("menu_2")
             )
    )

g1 = cmd_mgr.add_group ("Group_1", if_names = ("menu_1", ))
g2 = cmd_mgr.add_group ("Group_2", if_names = ("menu_2", ))

g1.add_command (TFL.UI.Command ("fct_1", fct_1), if_names = ("menu_1", ))
g1.add_command (TFL.UI.Command ("fct_2", fct_2), if_names = ("menu_1", ))
g2.add_command (TFL.UI.Command ("fct_3", fct_3), if_names = ("menu_2", ))
g2.add_command (TFL.UI.Command ("fct_4", fct_4), if_names = ("menu_2", ))
print cmd_mgr ["Group_1"].interfacers ['menu_1']
print cmd_mgr ["Group_2"].interfacers ['menu_2']
"""

### __END__ TFL.UI._Test_Command_Mgr


