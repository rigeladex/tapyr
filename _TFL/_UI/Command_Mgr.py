# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.UI.Command_Mgr
#
# Purpose
#    Manage commands of an interactive application
#
# Revision Dates
#    27-Jun-2000 (CT) Creation
#    29-Jun-2000 (CT) `indent_pat' and `par_pat' added to and used by
#                     `Command'
#    29-Jun-2000 (CT) `desc' added to `add_group'
#    30-Jun-2000 (CT) `Command_Mgr.run' added
#    30-Jun-2000 (CT) `Command_Mgr.batchable' added
#    30-Jun-2000 (CT) Factored from `CTK_Command_Mgr'
#     3-Jul-2000 (CT) `Command.run' added
#     3-Jul-2000 (CT) `args' and `kw' added to `Command_Mgr.run'
#    20-Jul-2000 (CT) Handling of `KeyboardInterrupt' added
#    25-Jul-2000 (CT) `cmd_nam_pat' renamed to `nam_pat'
#    25-Jul-2000 (CT) `formatted_precondition' factored
#    25-Jul-2000 (CT) `TOM_Documented' functionality added
#    26-Jul-2000 (CT) Promote `batchable' to `Command's
#    27-Jul-2000 (CT) `replace_uscore' applied to text to be grokked by TeX
#    31-Jul-2000 (CT) Attribute `batchable' added to `Command.__init__'
#     2-Aug-2000 (CT) `Command_Mgr.run' corrected (apply `run' of
#                     Command object instead of `__call__')
#     9-Aug-2000 (CT) `add_command': optional argument `batchable' added
#    30-Aug-2000 (CT) Return result of `Command.run'
#    31-Aug-2000 (CT) Return result of `Command_Mgr.run'
#     1-Sep-2000 (CT) `batch_mode' added and checked in `check_precondition'
#     7-Sep-2000 (CT) Import of CTK removed (should never have been here)
#    22-Feb-2001 (CT) Use `raise' instead of `raise exc' for re-raise
#     8-May-2001 (CT) `is_applicable' added
#     8-May-2001 (CT) `_check_precondition' factored and constructor added to
#                     `Precondition_Violation'
#    27-Jul-2001 (CT) Migrated into package `TOM`
#     6-Nov-2001 (CT) Import of `traceback` moved from exception handler to
#                     global scope
#     6-Feb-2002 (CT) `TTA_Toolname_Kludge` added to `doc_tex_section`
#    12-Apr-2002 (CT) Use `StandardError` instead of `Exception`
#     3-Sep-2002 (MY) Add missing import for standalone importing
#    11-Jun-2003 (CT) s/== None/is None/
#     8-Jul-2003 (CT) `tex_section` corrected (use `obj.batchable` instead of
#                     `self.batchable`)
#     8-Jul-2003 (CT) `Command_Mgr_Documenter.tex_cmd_list` corrected
#    18-Dec-2003 (CT) `form_dict`, `_cooked_doc`, and `_cook_doc` added and
#                     used
#     9-Mar-2004 (CT) `appl` added to `Command_Mgr`
#     9-Mar-2004 (CT) `Change_Action` added to and used in `Command`
#     9-Mar-2004 (CT)  Dead weight `post_command` removed
#     7-Jun-2004 (CT)  `tex_cmd_list` and `tex_cmd_table` changed to check
#                      for `hasattr (c, "Documenter")`
#    14-Jun-2004 (CT)  Handler for `Exception_Handled` added to `run`
#    13-Jul-2004 (CT)  Handling of `Change_Action` changed (use
#                      `scope.record_change_encapsulated`)
#    28-Sep-2004 (CT) Use `isinstance` instead of type comparison
#    14-Dec-2004 (CT) Small corrections
#    20-Dec-2004 (CT) Factored from TOM
#    21-Dec-2004 (CT) `Command_Group` factored from `Command_Mgr`
#    21-Dec-2004 (CT) `menu` and `toolbar` replaced by `interfacers`
#    21-Dec-2004 (CT) `_real_index` factored
#     7-Jan-2005 (CT) `Command_Mgr.__init__` changed to set instance
#                     attributes before chaining up
#     7-Jan-2005 (CT) `cmd` added to allow attribute access to commands
#                     without name clashes
#     7-Jan-2005 (CT) `add_command` changed to not set `qname` to `.<name>` for
#                     commands added directly to a command manager without a
#                     name
#    10-Jan-2005 (CT) `add_separator` completed (needs to go into `_element`)
#    10-Jan-2005 (CT) `destroy` changed to call `destroy` of all interfacers
#    11-Jan-2005 (CT) `add_separator` changed to be more similar to
#                     `add_command` and `add_group`
#    11-Jan-2005 (CT) `as_check_button` added to `add_command`
#    13-Jan-2005 (MG) Minor fixes
#    19-Jan-2005 (CT) `_element` (NO_List) converted to `_epi` (dictionary of
#                     NO_List indexed by interfacer) and handling of `index`
#                     changed accordingly
#    19-Jan-2005 (CT) Today's changes fixed
#    21-Jan-2005 (MG) `Command.run` fixed to pass the result of the command
#                     to the caller
#    26-Jan-2005 (CT) Call to `Command_Interfacer.add_command` changed from
#                     `as_check_button` to `state_var`
#    ««revision-date»»···
#--

from   _TFL           import TFL

from   Abbr_Key_Dict  import Abbr_Key_Dict
from   NO_List        import NO_List
from   Record         import Record
from   predicate      import *

import _TFL._Meta.Object
import _TFL._UI

import re
import traceback
import weakref

class Exception_Handled (Exception) :
    """Raised after an exception was already handled to bail out from an
       arbitrary position in a call-tree. Should be ignored further up.
    """
# end class Exception_Handled

class Precondition_Violation (StandardError) :
    def __init__ (self, precondition, msg) :
        self.precondition = precondition
        self.msg          = msg
        StandardError.__init__ (self, precondition, msg)
    # end def __init__
# end class Precondition_Violation

class _Command_ (TFL.Meta.Object) :

    batchable   = False ### is the command batchable?
    batch_mode  = False ### are we running in batch_mode?

    interfacers = ()
    button_name = None
    group_name  = None

    indent_pat  = re.compile (r"\n( +)")
    par_pat     = re.compile (r"\n *\n")
    nam_pat     = re.compile (r"[Tt]his command")

    def enable (self) :
        for i in self.interfacers :
            try :
                i.enable_entry (self.name)
            except KeyboardInterrupt :
                raise
            except StandardError :
                if __debug__ :
                    traceback.print_exc ()
                    print str (self), i.__class__, i
    # end def enable

    def disable (self) :
        for i in self.interfacers :
            try :
                i.disable_entry (self.name)
            except KeyboardInterrupt :
                raise
            except StandardError :
                if __debug__ :
                    traceback.print_exc ()
                    print str (self), i.__class__, i
    # end def disable

    def formatted_precondition (self) :
        p = self.precondition
        if p and p.__doc__ :
            result = self.nam_pat.sub ("`%s'" % self.qname, p.__doc__)
            return result
        return ""
    # end def formatted_precondition

    def precondition_name (self) :
        p = self.precondition
        if p :
            return p.__name__
        return "None"
    # end def precondition_name

    def _cooked_doc (self, doc, form_dict) :
        if doc :
            doc     = doc % form_dict
            i_match = self.indent_pat.search (doc)
            if i_match :
                def rep (match, indent = len (i_match.group (1))) :
                    m = match.group (0)
                    return m [0] + " " + m [indent+1:]
                doc = self.indent_pat.sub (rep, doc)
        return doc
    # end def _cooked_doc

# end class _Command_

class Command (_Command_) :
    """Model a command of an interactive application"""

    description = ""

    def __init__ (self, name, command, precondition = None, pv_callback = None, interfacers = None, _doc = None, batchable = 1, Change_Action = None) :
        self.name          = name
        self.command       = command
        self.precondition  = precondition
        self.pv_callback   = pv_callback
        self.interfacers   = interfacers or []
        self.batchable     = batchable
        self.Change_Action = Change_Action
        self._raw_doc      = (_doc or command.__doc__ or "")
    # end def __init__

    def _cook_doc (self, form_dict) :
        doc                = self._cooked_doc (self._raw_doc, form_dict)
        doc, desc          = self.par_pat.split (doc + "\n\n", 1)
        self.__doc__       = doc.strip  ()
        self.description   = desc.strip ()
        if self.precondition :
            p = self.precondition.im_func
            if not hasattr (p, "__cooked") :
                setattr (p, "__cooked", True)
                if p.__doc__ :
                    p.__doc__ = self._cooked_doc (p.__doc__, form_dict)
    # end def _cook_doc

    def destroy (self) :
        for i in self.interfacers.itervalues () :
            i.destroy ()
        self.interfacers = self.command = self.precondition \
                         = self.pv_callback = None
    # end def destroy

    def __call__ (self, event = None) :
        return self.run ()
    # end def __call__

    def run (self, * args, ** kw) :
        result = None
        try :
            if self.check_precondition () :
                result = self._run (* args, ** kw)
        except Exception_Handled :
            pass
        except KeyboardInterrupt :
            print "Command %s canceled" % self.name
        return result
    # end def run

    def _run (self, * args, ** kw) :
        return self.command (* args, ** kw)
    # end def _run

    def is_applicable (self) :
        try :
            self._check_precondition ()
        except Precondition_Violation :
            return 0
        else :
            return 1
    # end def is_applicable

    def _check_precondition (self) :
        if self.batch_mode and not self.batchable :
            msg = "Command %s cannot be used in batch mode" % self.qname
            raise Precondition_Violation, ("batchable", msg)
        p = self.precondition
        if p and not p () :
            msg = self.formatted_precondition ()
            raise Precondition_Violation, (p.__name__, msg)
        return 1
    # end def _check_precondition

    def check_precondition (self) :
        try :
            return self._check_precondition ()
        except Precondition_Violation, exc:
            if self.pv_callback :
                self.pv_callback (exc.precondition, exc.msg)
                return 0
            else :
                raise
    # end def check_precondition

    def update_state (self) :
        p = self.precondition
        if p and not p () :
            self.disable ()
        else :
            self.enable  ()
    # end def update_state

    def __str__ (self) :
        if self.command :
            return getattr (self.command, "__name__", str (self.command))
        else :
            return self.name
    # end def __str__

    def __repr__ (self) :
        return "<function %s at %x>" % \
               (str (self), id (self.command or self))
    # end def __repr__

    def __getattr__ (self, name) :
        if name == "qname" :
            return self.name
        raise AttributeError, name
    # end def __getattr__

# end class Command

class _Command_Getattr_ (TFL.Meta.Object) :

    def __init__ (self, group) :
        self._group = weakref.proxy (group)
    # end def __init__

    def __getattr__ (self, name) :
        return self._group [name]
    # end def __getattr__

# end class _Command_Getattr_

class Command_Group (_Command_) :
    """Manage a group of commands of an interactive application"""

    name_clean = re.compile (r"[^a-zA-Z_0-9]+")
    nam_pat    = re.compile (r"[Tt]his (command )?group")

    def __init__ (self, name, interfacers, parent = None, batchable = False, desc = None, precondition = None) :
        self.__super.__init__ ()
        self.cmd            = _Command_Getattr_ (self)
        self.name           = self.qname = name
        self.interfacers    = interfacers
        self.parent         = parent
        self.batchable      = batchable
        self.precondition   = precondition
        if parent :
            self.root       = parent.root
            if parent.qname :
                self.qname  = "%s.%s" % (parent.qname, name)
        self.n_seps         = 0
        self.description    = self._cooked_doc (desc, self.root.form_dict)
        self.command        = Abbr_Key_Dict ()
        self._group         = NO_List       ()
        self._epi           = dict \
            ([(n, NO_List ()) for n in interfacers.keys ()])
    # end def __init__

    def add_command (self, cmd, group = None, if_names = [], icon = None, index = None, delta = 0, underline = None, accelerator = None, batchable = 0, as_check_button = False) :
        """Add `cmd' to `group'"""
        cmd._cook_doc (self.root.form_dict)
        if group is not None :
            if isinstance (group, (str, unicode, int)) :
                group = self._group [group]
            return group.add_command  \
                ( cmd, None, if_names, icon
                , index, delta, underline, accelerator, batchable
                )
        else :
            self.root._add_precondition (cmd)
            cmd.group_name = self.name
            if self.qname :
                cmd.qname  = "%s.%s" % (self.qname, cmd.name)
            else :
                cmd.qname  = cmd.name
            cmd.batchable  = cmd.batchable and (self.batchable or batchable)
            cmd.appl       = self.root.appl
            cmd.state_var  = None
            if as_check_button :
                cmd.state_var   = self.TNS.Boolean_Variable ()
            if not cmd.pv_callback :
                cmd.pv_callback = self.root.pv_callback
            self.root.command [cmd.qname] = cmd
            if self.parent :
                self.command [cmd.name] = cmd
            cmd.interfacers = []
            for n, i, info in self._interfacers (if_names) :
                _ie   = self._epi        [n]
                index = self._real_index (_ie, index, delta)
                _ie.insert               (index, cmd)
                cmd.interfacers.append   (i)
                i.add_command \
                    ( name            = cmd.name
                    , callback        = cmd
                    , index           = index
                    , underline       = underline
                    , accelerator     = accelerator
                    , icon            = icon
                    , info            = info
                    , state_var       = cmd.state_var
                    , cmd_name        = cmd.qname
                    )
    # end def add_command

    def add_group (self, name, desc = None, precondition = None, if_names = [], index = None, delta = 0, underline = None, batchable = 0) :
        """Add command group `name'."""
        ifacers = {}
        to_do   = []
        for n, i, info in self._interfacers (if_names) :
            _ie         = self._epi        [n]
            index       = self._real_index (_ie, index, delta)
            ifacers [n] = i.add_group      (name, index = index, info = info)
            to_do.append  ((_ie, index))
        group = self.Group_Class \
            ( name          = name
            , interfacers   = ifacers
            , parent        = self
            , batchable     = batchable
            , desc          = desc
            , precondition  = precondition
            )
        self._group.append (group)
        for _ie, index in to_do :
            _ie.insert (index, group)
        if precondition :
            self.root._add_precondition (group)
        return group
    # end def add_group

    def add_separator (self, name = None, group = None, if_names = [], index = None, delta = 0) :
        """Add separator to `group'"""
        if group is not None :
            if isinstance (group, (str, unicode, int)) :
                group = self._group [group]
            return group.add_separator (name, None, if_names, index, delta)
        else :
            if not name :
                name = "sep_%s" % (self.n_seps, )
                self.n_seps += 1
            sep = Record (name = name, destroy = lambda s : 1)
            for n, i, info in self._interfacers (if_names) :
                _ie   = self._epi        [n]
                index = self._real_index (_ie, index, delta)
                _ie.insert               (index, sep)
                i.add_separator          (name, index)
    # end def add_separator

    def destroy (self) :
        self.root = self.parent = self.interfacers = None
        for i in self._epi.itervalues () :
            for e in i :
                e.destroy ()
        self._epi = self._group = self.command = None
    # end def destroy

    def group (self, name) :
        return self._group [name]
    # end def group

    def keys (self) :
        return self.command.keys ()
    # end def keys

    def _interfacers (self, interface_names) :
        interfacers = self.interfacers
        for n in interface_names :
            name, info = (n.split (":", 1) + [None]) [:2]
            yield name, interfacers [name], info
    # end def _interfacers

    def _real_index (self, element, index, delta) :
        if index is None :
            index = len (element)
        if isinstance (index, (str, unicode)) :
            index = element.n_index (index) + delta
        return index
    # end def _real_index

    def __getitem__ (self, index) :
        if self._group.has_key (index) :
            return self._group [index]
        return self.command [index]
    # end def __getitem__

    def __str__ (self) :
        return self.name
    # end def __str__

    def __repr__ (self) :
        return "<%s `%s' at %s>" % \
            (self.__class__.__name__, self.name, id (self))
    # end def __repr__

# end class Command_Group

Command_Group.Group_Class = Command_Group

class Command_Mgr (Command_Group) :
    """Manage toplevel group of commands of an interactive application"""

    def __init__ (self, change_counter, interfacers, pv_callback = None, name = "", batch_mode = False, form_dict = {}, appl = None) :
        self.root           = self
        self.change_counter = change_counter
        self.pv_callback    = pv_callback
        self.batch_mode     = batch_mode
        self.form_dict      = form_dict
        self.appl           = appl
        self.changes        = 0
        self._precondition  = {}
        self.__super.__init__ (name, interfacers, parent = None, batchable = True)
        for i in interfacers.itervalues () :
            i.bind_to_sync (self.update_state)
    # end def __init__

    def run (self, name, * args, ** kw) :
        """Run the command named by `name'"""
        return self.command [name].run (* args, ** kw)
    # end def run

    def is_applicable (self, name) :
        """Returns true if command name by `name' is currently applicable."""
        return self.command [name].is_applicable ()
    # end def is_applicable

    def keys (self) :
        return self.command.keys ()
    # end def keys

    def destroy (self) :
        self.__super.destroy ()
        for p in self._precondition.values () :
            p.command = []
        self.appl = self.pv_callback = s._precondition = None
    # end def destroy

    def _add_precondition (self, cmd) :
        p     = cmd.precondition
        dict  = self.root._precondition
        if not dict.has_key (p) :
            dict [p] = Record (old_value = "None", command = [])
        dict [p].command.append (cmd)
    # end def _add_precondition

    def update_state (self, event = None) :
        """Enable/disable all commands according to their preconditions"""
        if self.changes != int (self.change_counter) :
            try :
                for p, p_desc in self._precondition.items () :
                    new_value = (not p) or p ()
                    if new_value != p_desc.old_value :
                        p_desc.old_value = new_value
                        if new_value :
                            for cmd in p_desc.command :
                                cmd.enable  ()
                        else :
                            for cmd in p_desc.command :
                                cmd.disable ()
            finally :
                self.changes = int (self.change_counter)
    # end def update_state

# end class Command_Mgr

__all__ = ( "Command_Mgr", "Command_Group", "Command", "_Command_"
          , "Precondition_Violation"
          )

if __name__ != "__main__" :
    TFL.UI._Export ("*")
### __END__ TFL.UI.Command_Mgr
