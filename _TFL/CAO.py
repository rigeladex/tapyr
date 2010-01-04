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
#     1-Jan-2010 (CT) Creation continued
#     2-Jan-2010 (CT) Creation continued..
#     3-Jan-2010 (CT) Creation continued...
#     4-Jan-2010 (CT) Creation continued....
#    ««revision-date»»···
#--

from   _TFL               import TFL

from   _TFL.Regexp        import Regexp, re

import _TFL.defaultdict
import _TFL.Environment
import _TFL._Meta.Object
import _TFL._Meta.M_Class
import _TFL.predicate
import _TFL.sos

import decimal
import itertools
import sys

class Err (StandardError) :

    def __init__ (self, * args) :
        self.args = args
    # end def __init__

    def __str__ (self) :
        return "Command/argument/option error: %s" % (" ".join (self.args), )
    # end def __str__

    __repr__ = __str__

# end class Err

class Arg (TFL.Meta.M_Class) :
    """Meta class for argument types."""

    Table      = {}

    _spec_pat  = None
    _spec_form = \
        ( """ (?P<name> [^:=# ?]+) """
          """ (?:  : (?P<type>        [%s]    )? (?P<auto_split> [, :]?))? """
          """ (?:  = (?P<default>     [^\#?]* ))? """
          """ (?: \# (?P<max_number>  \d+     ))? """
          """ (?: \? (?P<description> .+      ))? """
          """ $ """
        )

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        r_name = cls.__name__
        if not r_name.startswith ("_") :
            setattr (cls.__class__, r_name, cls)
            if "type_abbr" in dict :
                assert not cls.type_abbr in cls.Table, cls
                cls.Table [cls.type_abbr] = cls
    # end def __init__

    @classmethod
    def from_string (cls, string) :
        pat = cls._spec_pat
        if pat is None :
            pat = cls._spec_pat = Regexp \
                ( cls._spec_form % ("".join (sorted (cls.Table)), )
                , re.VERBOSE | re.DOTALL
                )
        if pat.match (string) :
            Spec = cls.Table [pat.type or "B"]
            kw   = pat.last_match.groupdict ()
            kw.pop ("type", None)
            result = Spec (** kw)
        else :
            raise Err ("Invalid argument or option specification `%s`" % string)
        return result
    # end def from_string

# end class Arg

class Opt (Arg) :
    """Meta class for pure option types (i.e., these are noit usable for
       arguments).
    """

# end class Opt

class _Spec_ (TFL.Meta.Object) :
    """Base class for argument and option types"""

    __metaclass__ = Arg

    alias         = None
    auto_split    = None
    choices       = None
    needs_value   = True

    prefix        = ""

    range_pat     = Regexp \
        ( r"""^\s*"""
          r"""(?P<head> (?: 0[xX])? \d+)"""
          r"""\s*"""
          r"""\.\."""
          r"""\s*"""
          r"""(?P<tail> (?: 0[xX])? \d+)"""
          r"""\s*"""
          r"""(?: : (?P<delta> \d+))?"""
          r"""\s*$"""
        , re.VERBOSE
        )

    def __init__ \
            ( self
            , name          = ""
            , default       = ""
            , description   = ""
            , auto_split    = None
            , max_number    = None
            , hide          = False
            , range_delta   = 1
            , cook          = None
            ) :
        self.name           = name
        self.description    = description
        if auto_split is None :
            auto_split      = self.auto_split
        else :
            self.auto_split = auto_split
        if max_number is None :
            max_number      = self._auto_max_number (self.auto_split)
        self.max_number     = max_number
        self.hide           = hide or name [:2] == "__"
        self.range_delta    = range_delta
        if cook is not None :
            self.cook       = cook
        self._setup_default (default)
    # end def __init__

    def combine (self, values) :
        return values
    # end def combine

    def cook (self, value) :
        return value
    # end def cook

    def cooked (self, value) :
        auto_split = self.auto_split
        cook       = self.cook
        if auto_split and value and auto_split in value :
            values = value.split (auto_split)
        else :
            values = (value, )
        if auto_split :
            values = self._resolve_range (values)
        return [cook (v) for v in values]
    # end def cooked

    def _auto_max_number (self, auto_split) :
        return 0 if auto_split else 1
    # end def _auto_max_number

    def _resolve_range (self, values) :
        pat = self.range_pat
        for value in values :
            if value and pat.match (value) :
                for v in self._resolve_range_1 (value, pat) :
                    yield v
            else :
                yield value
    # end def _resolve_range

    def _resolve_range_1 (self, value, pat) :
        yield value
    # end def _resolve_range_1

    def _safe_eval (self, value) :
        try :
            return eval (value, {}, {})
        except Exception :
            raise Err ("Invalid value `%s` for %s" % (value, self))
    # end def _safe_eval

    def _setup_default (self, default) :
        if isinstance (default, basestring) :
            default  = self.cooked (default)
        elif default is None :
            default  = ()
        elif not isinstance (default, (list, tuple)) :
            default  = (default, )
        self.default = default
    # end def _setup_default

    def __repr__ (self) :
        return "'%s%s:%s%s=%s#%s?%s'" % \
            ( self.prefix
            , self.name
            , getattr (self, "type_abbr", self.__class__.__name__)
            , self.auto_split or ""
            , (self.auto_split or "").join (str (d) for d in self.default)
            , self.max_number
            , self.description or ""
            )
    # end def __repr__

# end class _Spec_

class _Spec_O_ (_Spec_) :
    """Base class for option types"""

    __metaclass__ = Opt

    prefix        = "-"

# end class _Spec_O_

class _Number_ (_Spec_) :
    """Base class for numeric argument and option types"""

    def cook (self, value) :
        if isinstance (value, basestring) :
            value = self._safe_eval (value)
        return self._cook (value)
    # end def cook

    def _resolve_range_1 (self, value, pat) :
        cook  = self.cook
        head  = cook (pat.head)
        tail  = cook (pat.tail) + 1
        delta = cook (pat.delta or self.range_delta)
        for v in range (head, tail, delta) :
            yield v
    # end def _resolve_range_1

# end class _Number_

class Bool (_Spec_O_) :
    """Option with a boolean value"""

    needs_value   = False
    type_abbr     = "B"

    def cook (self, value) :
        if value is None :
            return True
        if not isinstance (value, basestring) :
            return bool (value)
        if value.lower () in ("no", "0", "false") : ### XXX I18N
            return False
        return True
    # end def cook

    def _auto_max_number (self, auto_split) :
        return 1
    # end def _auto_max_number

    def _setup_default (self, default) :
        if default is None :
            default = False
        return self.__super._setup_default (default)
    # end def _setup_default

# end class Bool

class Cmd_Choice (TFL.Meta.Object) :
    """Argument that selects a sub-command"""

    __metaclass__ = Arg

    auto_split    = None
    default       = None
    hide          = False
    max_number    = 1
    needs_value   = False

    def __init__ (self, name, * cmds, ** kw) :
        self.name        = name
        self.sub_cmds    = dict   ((c._name, c) for c in cmds)
        self.description = kw.pop ("description", "")
        assert not kw
    # end def __init__

    @property
    def choices (self) :
        return self.sub_cmds
    # end def choices

    def __getitem__ (self, key) :
        return self.sub_cmds [key]
    # end def __getitem__

# end class Cmd_Choice

class Decimal (_Number_) :
    """Argument or option with a decimal value"""

    type_abbr     = "D"

    def _cook (self, value) :
        if isinstance (value, float) :
            value = str (value)
        return decimal.Decimal (value)
    # end def _cook

# end class Decimal

class Float (_Number_) :
    """Argument or option with a floating point value"""

    type_abbr     = "F"

    _cook         = float

# end class Float

class Help (_Spec_O_) :
    """Option asking for help"""

    alias         = "?"
    auto_split    = ","
    needs_value   = False

    def __init__ (self) :
        self.__super.__init__ \
            ( name          = "help"
            , description   = "Display help about command"
            )
    # end def __init__

    def __call__ (self, cao, indent = 0) :
        return self._handler (cao, indent)
    # end def __call__

    def _handler (self, cao, indent = 0) :
        if cao._cmd._helper :
            cmd._helper (cao)
        else :
            keys  = set (["args", "opts", "summary"])
            vals  = set (v for v in getattr (cao, self.name) if v)
            all_p = (not vals.intersection (keys)) or vals == set (["break"])
            if (all_p or "summary" in vals) :
                self._help_summary (cao, indent)
                if cao._cmd._description :
                    print
            arg_p = any (a for a in cao._arg_list if not a.hide)
            if (all_p or "args" in vals) and arg_p :
                self._help_args (cao, indent, heading = not all_p)
                print
            opt_p = any (o for o in cao._opt_dict.itervalues () if not o.hide)
            if (all_p or "opts" in vals) and opt_p :
                self._help_opts (cao, indent, heading = not all_p)
        return "break" not in vals
    # end def _handler

    def _help_ao (self, ao, cao, head, max_l, prefix = "") :
        if ao.hide :
            return
        name = ao.name
        v    = getattr (cao, name, "")
        print "%s%s%-*s  : %s = %s <default: %s>" % \
            (head, prefix, max_l, name, ao.__class__.__name__, v, ao.default)
        if ao.description :
            print "%s    %s" % (head, ao.description)
        if ao.choices :
            choices = "Possible values: %s" % (", ".join (sorted (ao.choices)))
            print "%s    %s" % (head, choices)
    # end def _help_ao

    def _help_args (self, cao, indent = 0, heading = False) :
        if heading :
            print "%sArguments of %s" % (" " * indent, cao._name)
        indent += 4
        head    = " " * indent
        max_l   = max (len (k) for k in cao._map) + 1
        for arg in cao._arg_list :
            self._help_ao (arg, cao, head, max_l)
        if cao.argv :
            print
            print "%s%-*s  : %s" % (head, max_l, "argv", cao.argv)
    # end def _help_args

    def _help_opts (self, cao, indent = 0, heading = False) :
        if heading :
            print "%sOptions   of %s" % (" " * indent, cao._name)
        indent += 4
        head    = " " * indent
        max_l   = max (len (k) for k in cao._map)
        for name, opt in sorted (cao._opt_dict.iteritems ()) :
            self._help_ao (opt, cao, head, max_l, "-")
    # end def _help_opts

    def _help_summary (self, cao, indent) :
        head = " " * indent
        print "%s%s %s"  % \
            (head, cao._name, " ".join (self._help_summary_args (cao)))
        print "%s    %s" % (head, cao._cmd._description)
    # end def _help_summary

    def _help_summary_args (self, cao) :
        cmd      = cao._cmd
        min_args = cmd._min_args
        max_args = cmd._max_args
        if cmd._arg_list :
            for i, arg in enumerate (cmd._arg_list) :
                if not arg.hide :
                    if i < min_args :
                        yield arg.name
                    else :
                        yield "[%s]" % arg.name
        if max_args < 0 or max_args > len (cmd._arg_list) :
            yield "..."
    # end def _help_summary_args

    def _setup_default (self, default) :
        self.default = ()
    # end def _setup_default

    def __repr__ (self) :
        return "'%s%s %s'" % \
            ( self.prefix
            , self.name
            , self.description
            )
    # end def __repr__

# end class Help

class Int (_Number_) :
    """Argument or option with a integer value"""

    type_abbr     = "I"

    _cook         = int

# end class Int

class Int_X (_Number_) :
    """Argument or option with a integer value, allowing base specification"""

    type_abbr     = "X"

    def _cook (self, value) :
        if isinstance (value, basestring) :
            return int (value, 0)
        return int (value)
    # end def _cook

# end class Int_X

class Key (_Spec_) :
    """Argument or option that specifies a key of a dictionary"""

    def __init__ (self, dict, ** kw) :
        assert all (isinstance (k, basestring) for k in dict)
        self._dict = dict
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    def choices (self) :
        return self._dict
    # end def choices

    def cook (self, value) :
        if value :
            try :
                return self._dict [value]
            except KeyError :
                raise Err \
                    ( "Unkown key `%s` for %s\n    Specify one of: %s"
                    % (value, self, sorted (self._dict))
                    )
        return value
    # end def cook

# end class Key

class Set (_Spec_) :
    """Argument or option that specifies one element of a set of choices"""

    def __init__ (self, choices, ** kw) :
        self.choices = set (choices)
        self.__super.__init__ (** kw)
    # end def __init__

    def cook (self, value) :
        if value and value not in self.choices :
            raise Err \
                ( "Unkown value `%s` for %s\n    Specify one of: %s"
                % (value, self, sorted (self.choices))
                )
        return value
    # end def cook

# end class Set

class Str (_Spec_) :
    """Argument or option with a string value"""

    type_abbr     = "S"

# end class Str

class Str_AS (_Spec_) :
    """Argument or option with a string value, auto-splitting"""

    auto_split    = ","
    type_abbr     = "T"

# end class Str

class Path (_Spec_) :
    """Argument or option with a filename or directory name as value"""

    auto_split    = ":"
    type_abbr     = "P"

    def cook (self, value) :
        if value :
            value = TFL.sos.expanded_path (value)
        return value
    # end def cook

    def _resolve_range (self, values) :
        for value in values :
            for v in TFL.sos.expanded_globs (value) :
                yield v
    # end def _resolve_range

# end class Path

class Cmd (TFL.Meta.Object) :
    """Model a command with options, arguments, and a handler."""

    _handler      = None
    _helper       = None
    _opt_pat      = Regexp \
        ( """ -{1,2} (?P<name> [^:= ]+) """
          """ (?: = (?P<quote> [\"\']?) (?P<value> .*) (?P=quote)? )? """
          """ $ """
        , re.VERBOSE
        )

    def __init__ \
            ( self
            , handler     = None
            , args        = ()
            , min_args    = 0
            , max_args    = -1
            , opts        = ()
            , description = ""
            , name        = ""
            , do_keywords = False
            , helper      = None
            ) :
        assert max_args == -1 or max_args >= min_args
        assert max_args == -1 or max_args >= len (args)
        if handler is not None :
            assert TFL.callable (handler)
            self._handler = handler
        self._opt_spec    = opts
        self._arg_spec    = args
        self._min_args    = min_args
        self._max_args    = max_args
        self._description = description
        self._name        = name or TFL.Environment.script_name ()
        self._do_keywords = do_keywords
        if helper is not None :
            self._helper  = helper
        self._setup_opts (opts)
        self._setup_args (args)
    # end def __init__

    def __call__ (self, _argv = None, ** _kw) :
        if _kw :
            assert not _argv, "Cannot specify both `_argv` and `_kw`"
            cao = self.use (** _kw)
        else :
            help = False
            if _argv is None :
                help  = True
                _argv = sys.argv [1:]
            try :
                cao = self.parse (_argv)
            except Exception, exc :
                if help :
                    print exc, "\n\nUsage :"
                    cao = CAO (self)
                    self.help (cao, indent = 4)
                    return
                else :
                    raise
        return cao ()
    # end def __call__

    def parse (self, argv) :
        result  = CAO  (self)
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
        sc     = self._sub_cmd_choice
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
                raise Err ("Unknown option `%s` [%s]" % (k, v))
        argv_it = iter (rest)
        for arg in argv_it :
            self._handle_arg (arg, argv_it, result)
        result._check ()
        return result
    # end def use

    def _attribute_spec (self, name) :
        if name in self._opt_dict :
            return self._opt_dict [name]
        if name in self._arg_dict :
            return self._arg_dict [name]
        raise AttributeError (name)
    # end def _attribute_spec

    def _handle_arg (self, arg, argv_it, result) :
        al = result._arg_list
        if not al :
            spec = Arg.Str ()
        else :
            spec = al [min (len (result.argv), len (al) - 1)]
        result._set_arg (spec, arg)
    # end def _handle_arg

    def _handle_opt (self, arg, argv_it, result) :
        oa  = result._opt_abbr
        al  = result._opt_alias
        pat = self._opt_pat
        if pat.match (arg) :
            k = pat.group ("name")
            v = pat.group ("value")
            k = al.get    (k, k)
            if k in oa :
                spec = oa [k]
                if spec.needs_value and v is None :
                    try :
                        v = argv_it.next ()
                    except StopIteration :
                        raise Err ("Option `%s` needs a value" % k)
                result._set_opt  (spec, v)
            else :
                matches = \
                    [o for o in sorted (result._opt_dict) if o.startswith (k)]
                if matches :
                    raise Err \
                        ( "Ambiguous option `%s`, matches any of %s"
                        % (arg, matches)
                        )
                else :
                    raise Err ("Unknown option `%s`" % (arg, ))
    # end def _handle_opt

    def _setup_args (self, args) :
        self._arg_list = al  = []
        self._arg_dict = ad  = {}
        self._sub_cmd_choice = None
        od = self._opt_dict
        for i, a in enumerate (args) :
            if isinstance (a, basestring) :
                a = Arg.from_string (a)
            if isinstance (a.__class__, Opt) :
                raise Err \
                    ("Option type `%s` cannot be used for argument" % a)
            assert a.name not in od
            a.index = i
            a.kind  = "argument"
            al.append (a)
            ad [a.name] = a
            if isinstance (a, Cmd_Choice) :
                if self._sub_cmd_choice is None :
                    self._sub_cmd_choice = a
                else :
                    raise Err \
                        ( "Only one sub-command choice is possible, "
                          "two are specified: `%s`, `%s`"
                        % (self._sub_cmd_choice.name, a.name)
                        )
    # end def _setup_args

    def _setup_opt  (self, opt, od, al) :
        od [opt.name] = opt
        opt.kind = "option"
        if opt.alias :
            al [opt.alias] = opt.name
    # end def _setup_opt

    def _setup_opts (self, opts) :
        self._opt_dict  = od = {}
        self._opt_abbr  = oa = {}
        self._opt_alias = al = {}
        for o in opts :
            if isinstance (o, basestring) :
                o = Arg.from_string (o.lstrip ("-"))
            elif not isinstance (o.__class__, Arg) :
                raise Err ("Not a valid option `%s`" % o)
            self._setup_opt (o, od, al)
        if not "help" in od :
            self._setup_opt (Opt.Help (), od, al)
        self._setup_opt_abbr (od, oa)
    # end def _setup_opts

    def _setup_opt_abbr (self, od, result) :
        result.clear ()
        if od :
            def abbrs (i, key) :
                o = od [key]
                for j in range (i, len (key)) :
                    result [key [:j + 1]] = o
            keys = sorted (od)
            ### Just in case `od` has only one entry
            i, k2 = 0, keys [-1]
            last  = 0
            for k1, k2 in TFL.pairwise (keys) :
                i = TFL.first_diff (k1, k2)
                abbrs (max (i, last), k1)
                last = i ### Remembers index of first_diff of last pair
            ### Handle last entry
            abbrs (i, k2)
        return result
    # end def _setup_opt_abbr

    def __getattr__ (self, name) :
        return self._attribute_spec (name)
    # end def __getattr__

    def __getitem__ (self, key) :
        try :
            return self._attribute_spec (key)
        except AttributeError :
            raise KeyError (key)
    # end def __getitem__

# end class Cmd

class CAO (TFL.Meta.Object) :
    """Command with options and arguments supplied."""

    _key_pat = Regexp \
        ( """\s*"""
          """(?P<name> [^= ]+)"""
          """\s* [=] \s* """
          """(?P<value> .*)"""
        , re.VERBOSE
        )

    def __init__ (self, cmd) :
        self._cmd         = cmd
        self._name        = cmd._name
        self._arg_dict    = dict (cmd._arg_dict)
        self._arg_list    = list (cmd._arg_list)
        self._opt_dict    = dict (cmd._opt_dict)
        self._opt_abbr    = dict (cmd._opt_abbr)
        self._opt_alias   = dict (cmd._opt_alias)
        self._do_keywords = cmd._do_keywords
        self.argv         = []
        self._map         = TFL.defaultdict (list)
        self._raw         = TFL.defaultdict (list)
        self._key_values  = dict ()
        self._explicit_n  = 0
    # end def __init__

    def __call__ (self) :
        call_handler = True
        handler      = self._cmd._handler
        if self.help :
            call_handler = self._explicit_n
            if not self._cmd.help (self) :
                call_handler = False
        if call_handler and handler :
            return handler (self)
        return self
    # end def __call__

    def _attribute_value (self, name, map = None) :
        if map is None :
            map = self._map
        if name in self._opt_dict :
            ao   = self._opt_dict   [name]
        elif name in self._arg_dict :
            ao   = self._arg_dict   [name]
        elif name in self._key_values :
            return self._key_values [name]
        else :
            raise AttributeError (name)
        result = map [name]
        if ao.max_number == 1:
            if result :
                result = result [0]
            else :
                result = None
        elif result and map is not self._raw :
            result = ao.combine (result)
        return result
    # end def _attribute_value

    def _check (self) :
        self._finish_setup ()
        min_args = self._cmd._min_args
        max_args = self._cmd._max_args
        argn     = len (self.argv)
        if not self.help :
            if argn < min_args :
                raise Err \
                    ("Need at least %d arguments, got %d" % (min_args, argn))
            if 0 <= max_args < argn :
                raise Err \
                    ( "Maximum number of arguments is %d, got %d"
                    % (max_args, argn)
                    )
    # end def _check

    def _finish_setup (self) :
        map = self._map
        for spec in itertools.chain \
                (self._arg_dict.itervalues (), self._opt_dict.itervalues ()) :
            name = spec.name
            if name not in map :
                d = spec.default
                if d is not None :
                    map [name].extend (d)
    # end def _finish_setup

    def _set_arg (self, spec, value) :
        kp = self._key_pat
        self._explicit_n += 1
        if isinstance (spec, Cmd_Choice) :
            if self.argv :
                raise Err \
                    ("Sub-command `%s` needs to be first argument" % value)
            try :
                self._cmd = sc = spec [value]
            except KeyError :
                raise Err \
                    ( "Unkown sub-command `%s`, specify one of: (%s)"
                    % (value, ", ".join (sorted (spec.sub_cmds)))
                    )
            self._name = " ".join ([self._name, sc._name])
            self._arg_list [:] = sc._arg_list
            self._arg_dict.clear   ()
            self._arg_dict.update  (sc._arg_dict)
            self._opt_dict.update  (sc._opt_dict)
            self._opt_alias.update (sc._opt_alias)
            sc._setup_opt_abbr     (self._opt_dict, self._opt_abbr)
        elif self._do_keywords and kp.match (value) :
            self._key_values [kp.name] = kp.value
        else :
            cv = spec.cooked (value)
            self.argv.extend (cv)
            if spec.name :
                self._map [spec.name].extend (cv)
                self._raw [spec.name].append (value)
    # end def _set_arg

    def _set_opt (self, spec, value) :
        self._explicit_n += spec.name != "help"
        self._map [spec.name].extend (spec.cooked (value))
        if value is not None :
            self._raw [spec.name].append (value)
    # end def _set_opt

    def _set_keys (self, kw) :
        for k, v in kw :
            self._key_values [k] = v
    # end def _set_keys

    def __getattr__ (self, name) :
        try :
            return self._attribute_value (name)
        except AttributeError :
            if name == "argn" :
                return len (self.argv)
            else :
                raise
    # end def __getattr__

    def __getitem__ (self, key) :
        if isinstance (key, basestring) :
            map = self._map
            key, _, raw = TFL.split_hst (key, ":")
            if raw == "raw" :
                map = self._raw
            try :
                return self._attribute_value (key, map)
            except AttributeError :
                raise KeyError (key)
        else :
            return self.argv [key]
    # end def __getitem__

    def __iter__ (self) :
        return iter (self.argv)
    # end def __iter__

# end class CAO

def show (cao) :
    print cao._name
    print "    Options    : %s" % (sorted (cao._opt_abbr), )
    print "    Arguments  : %s" % (sorted (a.name for a in cao._arg_list), )
    for o in sorted (cao._opt_dict) :
        print "    -%-9s : %s" % (o, getattr (cao, o))
    for a in cao._arg_list :
        print "    %-10s : %s" % (a.name, getattr (cao, a.name))
    print "    argv       : %s" % (cao.argv, )
# end def show

__doc__ = """
This module provides classes for defining and processing commands,
arguments, and options. The values for arguments and options can be
parsed from `sys.argv` or supplied by a client via keyword arguments.

A command is defined by creating an instance of the :class:`Command`
with the arguments

- a callback function `handler` that performs the command,

- a tuple of :class:`Arg` instances that defines the possible arguments,

- the minimum number of arguments required `min_args',

- the maximum number of arguments allowed  `max_args'
  (the default -1 means an unlimited number is allowed),

- a tuple of :class:`Arg` or :class:`Opt` that instances defines the
  possible  options,

- a description of the command to be included in the `help',

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

    >>> cmd = Cmd (show, name = "Test", args = ("adam:P=/tmp/test?First arg", "bert:I=42"), opts = ("-verbose:B", "-year:I,=2010"))
    >>> cmd._arg_list
    ['adam:P=/tmp/test#1?First arg', 'bert:I=42#1?']
    >>> sorted (str (o) for o in cmd._opt_dict.itervalues ())
    ["'-help Display help about command'", "'-verbose:B=False#1?'", "'year:I,=2010#0?'"]

    >>> cmd (["-year=2000", "-year", "1999", "-v=no", "/tmp/tmp"])
    Test
        Options    : ['h', 'he', 'hel', 'help', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose', 'y', 'ye', 'yea', 'year']
        Arguments  : ['adam', 'bert']
        -help      : []
        -verbose   : False
        -year      : [2000, 1999]
        adam       : /tmp/tmp
        bert       : 42
        argv       : ['/tmp/tmp']

    >>> cao = cmd.parse (["-year=2000", "-year", "1999", "-v=no", "/tmp/tmp"])
    >>> cao.year
    [2000, 1999]
    >>> cao.verbose
    False
    >>> cao.adam
    '/tmp/tmp'
    >>> cao.bert
    42
    >>> cao.argv
    ['/tmp/tmp']

    >>> cmd (["-year=2000", "-year", "1999", "-verb", "/tmp/tmp", "137"])
    Test
        Options    : ['h', 'he', 'hel', 'help', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose', 'y', 'ye', 'yea', 'year']
        Arguments  : ['adam', 'bert']
        -help      : []
        -verbose   : True
        -year      : [2000, 1999]
        adam       : /tmp/tmp
        bert       : 137
        argv       : ['/tmp/tmp', 137]
    >>> cap = cmd.parse (["-year=2000", "-year", "1999", "-verb", "/tmp/tmp", "137"])
    >>> cap.verbose
    True
    >>> cap.argv
    ['/tmp/tmp', 137]

    >>> coc = Cmd (show,
    ...     name = "Comp", args = (Cmd_Choice ("sub",
    ...       Cmd (show, name = "one", args = ("aaa:S", "bbb:S"), opts = ("y:I", "Z:B")),
    ...       Cmd (show, name = "two", args = ("ccc:I=3", "ddd:T=D"), opts = ("struct:B", ))
    ...       ), ), opts = ("verbose:B", "strict:B")
    ...     )
    >>> coc ([])
    Comp
        Options    : ['h', 'he', 'hel', 'help', 's', 'st', 'str', 'stri', 'stric', 'strict', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose']
        Arguments  : ['sub']
        -help      : []
        -strict    : False
        -verbose   : False
        sub        : None
        argv       : []
    >>> coc (["one"])
    Comp one
        Options    : ['Z', 'h', 'he', 'hel', 'help', 's', 'st', 'str', 'stri', 'stric', 'strict', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose', 'y']
        Arguments  : ['aaa', 'bbb']
        -Z         : False
        -help      : []
        -strict    : False
        -verbose   : False
        -y         : None
        aaa        : None
        bbb        : None
        argv       : []
    >>> coc (["two"])
    Comp two
        Options    : ['h', 'he', 'hel', 'help', 'stri', 'stric', 'strict', 'stru', 'struc', 'struct', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose']
        Arguments  : ['ccc', 'ddd']
        -help      : []
        -strict    : False
        -struct    : False
        -verbose   : False
        ccc        : 3
        ddd        : D
        argv       : []
    >>> coc (["-s"])
    Comp
        Options    : ['h', 'he', 'hel', 'help', 's', 'st', 'str', 'stri', 'stric', 'strict', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose']
        Arguments  : ['sub']
        -help      : []
        -strict    : True
        -verbose   : False
        sub        : None
        argv       : []
    >>> coc (["-s", "one"])
    Comp one
        Options    : ['Z', 'h', 'he', 'hel', 'help', 's', 'st', 'str', 'stri', 'stric', 'strict', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose', 'y']
        Arguments  : ['aaa', 'bbb']
        -Z         : False
        -help      : []
        -strict    : True
        -verbose   : False
        -y         : None
        aaa        : None
        bbb        : None
        argv       : []
    >>> coc (["-s", "two"])
    Comp two
        Options    : ['h', 'he', 'hel', 'help', 'stri', 'stric', 'strict', 'stru', 'struc', 'struct', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose']
        Arguments  : ['ccc', 'ddd']
        -help      : []
        -strict    : True
        -struct    : False
        -verbose   : False
        ccc        : 3
        ddd        : D
        argv       : []
    >>> coc (["two", "-s"])
    Traceback (most recent call last):
      ...
    Err: Command/argument/option error: Ambiguous option `-s`, matches any of ['strict', 'struct']
    >>> coc (["two", "-t"])
    Traceback (most recent call last):
      ...
    Err: Command/argument/option error: Unknown option `-t`
    >>> coc (["two", "one"])
    Traceback (most recent call last):
      ...
    Err: Command/argument/option error: Invalid value `one` for 'ccc:I=3#1?'
    >>> coc (["one", "two"])
    Comp one
        Options    : ['Z', 'h', 'he', 'hel', 'help', 's', 'st', 'str', 'stri', 'stric', 'strict', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose', 'y']
        Arguments  : ['aaa', 'bbb']
        -Z         : False
        -help      : []
        -strict    : False
        -verbose   : False
        -y         : None
        aaa        : two
        bbb        : None
        argv       : ['two']
    >>> coc (["one", "-v", "two", "-Z"])
    Comp one
        Options    : ['Z', 'h', 'he', 'hel', 'help', 's', 'st', 'str', 'stri', 'stric', 'strict', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose', 'y']
        Arguments  : ['aaa', 'bbb']
        -Z         : True
        -help      : []
        -strict    : False
        -verbose   : True
        -y         : None
        aaa        : two
        bbb        : None
        argv       : ['two']
    >>> coc (["one", "-v", "two", "-Z", "three", "four"])
    Comp one
        Options    : ['Z', 'h', 'he', 'hel', 'help', 's', 'st', 'str', 'stri', 'stric', 'strict', 'v', 've', 'ver', 'verb', 'verbo', 'verbos', 'verbose', 'y']
        Arguments  : ['aaa', 'bbb']
        -Z         : True
        -help      : []
        -strict    : False
        -verbose   : True
        -y         : None
        aaa        : two
        bbb        : three
        argv       : ['two', 'three', 'four']

    >>> ko  = Arg.Key (name = "foo", dict = {"1": "frodo", "a": 42})
    >>> cmd = Cmd (show, name = "dict-test", opts = (ko, ))
    >>> cmd (["-foo", "a"])
    dict-test
        Options    : ['f', 'fo', 'foo', 'h', 'he', 'hel', 'help']
        Arguments  : []
        -foo       : 42
        -help      : []
        argv       : []
    >>> cmd (["-foo=1"])
    dict-test
        Options    : ['f', 'fo', 'foo', 'h', 'he', 'hel', 'help']
        Arguments  : []
        -foo       : frodo
        -help      : []
        argv       : []

    >>> _ = coc (["-help=break"])
    Comp [sub] ...
    <BLANKLINE>
        sub       : Cmd_Choice = None <default: None>
            Possible values: one, two
    <BLANKLINE>
        -help     : Help = ['break'] <default: ()>
            Display help about command
        -strict   : Bool = False <default: (False,)>
        -verbose  : Bool = False <default: (False,)>
    >>> _ = coc (["-help=break", "one"])
    Comp one [aaa] [bbb] ...
    <BLANKLINE>
        aaa       : Str = None <default: ()>
        bbb       : Str = None <default: ()>
    <BLANKLINE>
        -Z        : Bool = False <default: (False,)>
        -help     : Help = ['break'] <default: ()>
            Display help about command
        -strict   : Bool = False <default: (False,)>
        -verbose  : Bool = False <default: (False,)>
        -y        : Int = None <default: ()>
    >>> _ = coc (["-help=break", "two"])
    Comp two [ccc] [ddd] ...
    <BLANKLINE>
        ccc       : Int = 3 <default: [3]>
        ddd       : Str_AS = D <default: ['D']>
    <BLANKLINE>
        -help     : Help = ['break'] <default: ()>
            Display help about command
        -strict   : Bool = False <default: (False,)>
        -struct   : Bool = False <default: (False,)>
        -verbose  : Bool = False <default: (False,)>

"""

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.CAO
