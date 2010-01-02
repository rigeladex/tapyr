# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
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
#    TFL.CAO
#
# Purpose
#    Command argument and option processor
#
# Features provided
#    - Automatic type conversions for arguments and options
#    - Default values for arguments and options
#    - Support for sub-commands
#    - Sub-commands and options can be abbreviated (as long as the
#      abbreviation is unique)
#    - Bounds checks on number of arguments and options
#    - Help
#
# Revision Dates
#    31-Dec-2009 (CT) Creation (based on TFL.Command_Line)
#    ««revision-date»»···
#--

"""
This module provides classes for defining and processing commands,
arguments, and options. The values for arguments and options can be
parsed from `sys.argv` or supplied by a client via keyword arguments.

A command is defined by creating an instance of the :class:`Command`
with arguments

- a tuple of :class:`Arg` instances defines the possible arguments,

- a tuple of :class:`Opt` instances defines the possible options,

- the minimum number of arguments required `min_args',

- the maximum number of arguments allowed  `max_args'
  (the default -1 means an unlimited number is allowed),

- a description of the command to be included in the `help',

- a callback function `handler` that performs the command,

- a `name` for the command (by default, the name of the module defining
  the `Command` is used).

For `Arg` and `Opt`, a shortcut string notation can be used:

    `<name>:<type-spec><auto-split-spec>=<default>#<max-number>?<help>`

Calling a :class:`Command` instance with an argument array, e.g.,
`sys.argv`, parses the arguments and options in the array, stores
their values in the instance, and calls the `handler`.

Calling a :class:`Command` instance with keyword arguments initializes
the argument and option values from those values and calls the
`handler`.

Alternatively, the methods `parse`, `use`, and `handle` can be
called by a client, if explicit flow control is required.

"""

from   _TFL               import TFL

from   _TFL.Regexp        import Regexp, re

import _TFL.Abbr_Key_Dict
import _TFL.Caller
import _TFL._Meta.Object
import _TFL.predicate
import _TFL.sos

import sys

class Error (StandardError) :

    def __init__ (self, * args) :
        self.args = args
    # end def __init__

    def __str__ (self) :
        return "Command/argument/option error: %s" % (" ".join (self.args), )
    # end def __str__

    __repr__ = __str__

# end class Error

class Cmd (TFL.Meta.Object) :
    """Model a command with options, arguments, and a handler."""

    _help_pat     = Regexp ("""^(h(e(lp?)?)?|\?)$""")
    _opt_pat      = Regexp \
        ( """ -{1,2} (?P<name> [^:= ]+) """
          """ (?: = (?P<quote> [\"\']?) (?P<value> .*) (?P=quote)? )? """
          """ $ """
        , re.VERBOSE
        )

    def __init__ \
            ( self, handler
            , opts             = ()
            , args             = ()
            , min_args         = 0
            , max_args         = -1
            , desc             = ""
            , name             = ""
            , process_keywords = False
            ) :
        assert max_args == -1 or max_args >= min_args
        assert max_args == -1 or max_args >= len (args)
        assert TFL.callable (handler)
        self._handler          = handler
        self._opt_spec         = opts
        self._arg_spec         = args
        self._min_args         = min_args
        self._max_args         = max_args
        self._desc             = desc
        self._name             = \
            name or TFL.Caller.globals () ["__name__"] ### XXX ???
        self._process_keywords = process_keywords
        self._parent           = None
        self._setup_opts (opts)
        self._setup_args (args)
    # end def __init__

    def __call__ (self, _argv = None, ** _kw) :
        if _kw :
            assert not _argv, "Cannot specify both `_argv` and `_kw`"
            cao = self.use   (** _kw)
        else :
            if _argv is None :
                _argv = sys.argv [1:]
            cao = self.parse (_argv)
        return cao ()
    # end def __call__

    def parse (self, argv) :
        result  = CAO (self)
        argv_it = iter (argv)
        for arg in argv_it :
            if arg == "--" :
                for arg in argv_it :
                    self._handle_arg (arg, argv_it, result)
            elif arg.startswith ("-") :
                self._handle_opt (arg, argv_it, result)
            else :
                self._handle_arg (arg, argv_it, result)
        result._check ()
        return result
    # end def parse

    def use (self, ** _kw) :
        result = CAO (self)
        ad     = result._arg_dict
        oa     = result._opt_abbr
        rest   = []
        sc     = self._sub_cmd
        if sc and sc.name in _kw :
            result._set_arg (sc, _kw.pop (sc.name))
        for k, v in _kw :
            if k in oa :
                result._set_opt   (oa [k], v)
            elif k in ad :
                result._set_arg   (ad [k], v)
            elif k == "__rest__" :
                rest = v
            elif k == "__kw__" :
                result._set_keys  (v)
            else :
                raise Error ("Unknown option `%s` [%s]" % (k, v))
        argv_it = iter (rest)
        for arg in argv_it :
            self._handle_arg (arg, argv_it, result)
        result._check ()
        return result
    # end def use

    def _handle_arg (self, arg, argv_it, result) :
        al = result._arg_list
        if not al :
            spec = Arg.String ()
        else :
            spec = al [min (len (result.argv), len (al) - 1)]
        result._set_arg (spec, arg)
    # end def _handle_arg

    def _handle_opt (self, arg, argv_it, result) :
        oa  = result._opt_abbr
        pat = self._opt_pat
        if pat.match (arg) :
            k = pat.group ("name")
            v = pat.group ("value")
            if k in oa :
                spec = oa [k]
                if spec.needs_value and v is None :
                    try :
                        v = argv_it.next ()
                    except StopIteration :
                        raise Error ("Option `%s` needs a value" % k)
                result._set_opt  (spec, v)
            elif self._help_pat.match (k) :
                result._set_help (k, v)
            else :
                raise Error ("Unknown or ambiguous option `%s`" % (arg, ))
    # end def _handle_opt

    def _setup_args (self, args) :
        self._arg_list = al = []
        self._arg_dict = ad = {}
        self._sub_cmd  = None
        for i, a in enumerate (args) :
            if isinstance (a, basestring) :
                a = Arg.from_string (a)
            a.index = i
            al.append (a)
            ad [a.name] = a
            if isinstance (a, Cmd) :
                if self._sub_cmd is None :
                    self._sub_cmd = a
                    if a._parent is None :
                        a._parent = self
                    else :
                        raise Error \
                            ( "Sub-command already has a parent `%s`"
                            % a._parent
                            )
                else :
                    raise Error \
                        ( "Only one sub-command is possible, "
                          "two are specified: `%s`, `%s`"
                        % (self._sub_cmd.name, a.name)
                        )
    # end def _setup_args

    def _setup_opts (self, opts) :
        self._opt_dict = od = {}
        self._opt_abbr = oa = {}
        for o in opts :
            if isinstance (o, basestring) :
                o = Arg.from_string (o)
            od [o.name] = o
        self._setup_opt_abbr (od, oa)
    # end def _setup_opts

    def _setup_opt_abbr (self, od, result) :
        result.clear ()
        for l, r in TFL.pairwise (sorted (od)) :
            i = TFL.first_diff (l, r)
            o = od [l]
            for k in range (i, len (l)) :
                result [l [:k + 1]] = o
        return result
    # end def _setup_opt_abbr

# end class Cmd

class CAO (TFL.Meta.Object) :
    """Command with options and arguments supplied."""

    key_pat = Regexp \
        ( """\s*"""
          """(?P<name> [^= ]+)"""
          """\s* [=] \s* """
          """(?P<value> .*)"""
        , re.VERBOSE
        )

    def __init__ (self, cmd) :
        self._cmd         = cmd
        self._arg_dict    = dict (cmd._arg_dict)
        self._opt_dict    = dict (cmd._opt_dict)
        self._opt_abbr    = dict (cmd._opt_abbr)
        self._do_keywords = cmd._process_keywords
        self._do_help     = ()
        self.argv         = []
        self.option       = TFL.defaultdict (list)
        self.keyword      = dict ()
    # end def __init__

    def __call__ (self) :
        call_handler = True
        cmd          = self._cmd
        if self._do_help :
            ### XXX
            call_handler = cmd._parent or self.argv or self._opt_values
        if call_handler :
            return cmd._handler (self)
    # end def __call__

    def _check (self) :
        min_args = self.cmd.min_args
        max_args = self.cmd.max_args
        argn     = len (self.argv)
        if argn < min_args :
            raise Error \
                ("Need at least %d arguments, got %d" % (min_args, argn))
        if 0 <= max_args <= argn :
            raise Error \
                ("Maximum number of arguments is %d, got %d" % (max_args, argn))
    # end def _check

    def _set_arg (self, spec, value) :
        kp = self._key_pat
        if isinstance (spec, Cmd_Choice) :
            if self.argv :
                raise Error \
                    ("Sub-command `%s` needs to be first argument" % value)
            self._sub_cmd = sc = spec [value]
            self._arg_dict.update (sc._arg_dict)
            self._opt_dict.update (sc._opt_dict)
            sc._setup_arg_abbr    (self._opt_dict, self._opt_abbr)
        elif self._do_keywords and kp.match (value) :
            self.keyword [kp.name] = kp.value
        else :
            self.argv.extend (spec.cooked (value))
    # end def _set_arg

    def _set_help (self, k, v) :
        self._do_help = (k, v)
    # end def _set_help

    def _set_opt (self, spec, value) :
        self.option [spec.name].extend (spec.cooked (value))
    # end def _set_opt

    def _set_keys (self, kw) :
        for k, v in kw :
            self.keyword [k] = v
    # end def _set_keys

# end class CAO

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.CAO
