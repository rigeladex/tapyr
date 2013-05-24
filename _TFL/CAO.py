# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer All rights reserved
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
#     7-Jan-2010 (CT) Creation continued.....
#    11-Jan-2010 (CT) Some more documentation added
#    16-Feb-2010 (CT) `Cmd._handle_arg` and `Cmd._setup_args` changed to
#                     empty `args` spec properly
#     4-Mar-2010 (CT) `Abs_Path` added
#    19-May-2010 (CT) `_set_keys` corrected (s/kw/kw.iteritems ()/)
#    16-Jun-2010 (CT) `File_System_Encoding`, `Input_Encoding`, and
#                     `Output_Encoding` added
#    16-Jun-2010 (CT) s/print/pyk.fprint/
#    22-Jun-2010 (CT) `put_keywords` added
#    25-Jun-2010 (CT) Support for callable `default`
#    28-Jun-2010 (CT) `default` changed to a property to delay evaluation of
#                     the `default` value (which might be a callable)
#    30-Jul-2010 (CT) `Config` and `_conf_opt` added
#    31-Jul-2010 (CT) `Bundle` added,
#                     Support for sub-commands added to `CAO._finish_setup`
#     1-Aug-2010 (CT) `_Spec_.cooked_default` factored and used in `CAO._cooked`
#     1-Aug-2010 (CT) `Cmd_Choice.__getattr__` added
#     1-Aug-2010 (CT) `Config.cook` changed to pass `context` with
#                     `C = cao._cmd` to `load_config_file`
#     2-Aug-2010 (CT) `Bundle` handling changed (major surgery)
#                     * `Cmd_Choice.__call__` factored from `CAO._set_arg`
#                     * `CAO._parse_args` and `._use_args` factored from
#                       `Cmd.parse` and `.use`
#                     * `Cmd._handle_arg` and `._handle_opt` moved to `CAO`
#     2-Aug-2010 (CT) `Help` for `Bundle` added
#    10-Aug-2010 (CT) `Cmd.__init__` changed to optionally take `description`
#                     from `handler.__doc__`
#    16-Aug-2010 (CT) Use `_min_args` and `_max_args` from sub-command
#     9-Nov-2010 (CT) `Binary` added (a kind of `Bool` that requires a value)
#     9-Nov-2010 (CT) `max_name_length` added and used for formatting of `help`
#     9-Nov-2010 (CT) `Help` changed to recognize `all` (and `*`)
#    17-Jan-2011 (CT) Use a `Word_Trie` instead of a `dict` to handle
#                     abbreviations, removed `_opt_abbr` from `Cmd`
#    20-Jul-2011 (CT) `_Encoding_.cook` changed to change `TFL.user_config`
#                     instead of `TFL.I18N.Config`
#    30-Jan-2012 (CT) Add `CAO.GET`
#    14-Mar-2012 (CT) Add empty `__builtins__` to `_safe_eval`
#    15-May-2012 (CT) Allow abbreviations for `Cmd_Choice`
#    17-May-2012 (CT) Add optional argument `defaults` to `Cmd`
#    25-May-2012 (CT) Change `Path._resolve_range` to apply `expanded_path`
#    31-May-2012 (CT) Add `** kw` to `_Spec_.__init__`
#    31-May-2012 (CT) Change `Path._resolve_range` to call `_resolve_range_1`;
#                     redefine `Abs_Path._resolve_range_1` instead of
#                     `Abs_Path._resolve_range`;
#    31-May-2012 (CT) Add `Rel_Path`;
#                     derive `Config` from `Rel_Path`, not `Abs_Path`
#    31-May-2012 (CT) Add `check_bun` to `CAO._handle_arg`,
#                     don't `check_bun` after `--`
#     2-Jun-2012 (CT) Streamline `Arg.from_string`
#     4-Jun-2012 (CT) Add `vals` to `Help.topics`
#     4-Jun-2012 (CT) Improve output of `Help`
#     7-Jun-2012 (CT) Use `TFL.r_eval`
#    21-Jun-2012 (CT) Add `Time_Zone`; factor `_User_Config_Entry_`, `cook_o`
#    21-Jun-2012 (CT) Add and use `implied_value` to fix help output for `Bool`
#    21-Jun-2012 (CT) Change `CAO.__getattr__` to cache results
#    15-Jan-2013 (MG) Add global option `Pdb_on_Exception`
#    27-Jan-2013 (CT) Don't unnecessarily redefine `sys.excepthook`
#    29-Jan-2013 (CT) Adapt doctest to new option `Pdb_on_Exception`
#    18-Feb-2013 (CT) Change `_Number_.cook` to try `_cook` in case of eval Err
#    22-Feb-2013 (CT) Change `_Number_.cook` to `raise err`, if any
#    22-Feb-2013 (CT)  Use `TFL.Undef ()` not `object ()`
#    24-Feb-2013 (CT) Split `__test__` from `__doc__`, add to `__doc__`
#    18-Mar-2013 (CT) Change `_safe_eval` to not convert `self` to string
#    18-Mar-2013 (CT) Change `_Number_._resolve_range_1` to save match variables
#    23-May-2013 (CT) Use `TFL.Meta.BaM` for Python-3 compatibility
#    23-May-2013 (CT) Improve Python-3 compatibility
#    ««revision-date»»···
#--

from   __future__       import print_function

from   _TFL               import TFL

from   _TFL               import pyk, sos
from   _TFL.I18N          import _, _T, _Tn
from   _TFL.Regexp        import Regexp, re
from   _TFL.Trie          import Word_Trie as Trie

import _TFL.Accessor
import _TFL.Context
import _TFL.defaultdict
import _TFL.Environment
import _TFL._Meta.M_Class
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL._Meta.Property
import _TFL.predicate
import _TFL.r_eval
import _TFL.Undef

from   itertools          import chain as ichain

import decimal
import sys

class Err (Exception) :

    def __init__ (self, * args) :
        self.args = args
    # end def __init__

    def __str__ (self) :
        return "Command/argument/option error: %s" % \
            (" ".join (str (a) for a in self.args), )
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
                assert len (cls.type_abbr) == 1, cls
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
            kw     = pat.last_match.groupdict ()
            type   = kw.pop ("type", "B")
            Spec   = cls.Table [type]
            result = Spec (** kw)
        else :
            raise Err ("Invalid argument or option specification `%s`" % string)
        return result
    # end def from_string

# end class Arg

class Opt (Arg) :
    """Meta class for pure option types (i.e., these are not usable for
       arguments).
    """

# end class Opt

class _Spec_ (TFL.Meta.BaM (TFL.Meta.Object, metaclass = Arg)) :
    """Base class for argument and option types"""

    alias         = None
    auto_split    = None
    choices       = None
    implied_value = None
    kind          = "argument"
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
            , default       = None
            , description   = ""
            , auto_split    = None
            , max_number    = None
            , hide          = False
            , range_delta   = 1
            , cook          = None
            , rank          = 0
            , ** kw
            ) :
        self.name           = name
        self.default        = default
        self.description    = description
        if auto_split is not None :
            self.auto_split = auto_split
        if max_number is None :
            max_number      = self._auto_max_number (self.auto_split)
        self.max_number     = max_number
        self.hide           = hide or name [:2] == "__"
        self.range_delta    = range_delta
        self.rank           = rank
        if cook is not None :
            self.cook       = cook
        self.__dict__.update (kw)
    # end def __init__

    def combine (self, values) :
        return values
    # end def combine

    def cook (self, value, cao = None) :
        return value
    # end def cook

    ### `cook_o` can be redefined to act on the result of `cook`
    cook_o = TFL.Meta.Alias_Property ("cook")

    def cooked (self, value, cao = None) :
        auto_split = self.auto_split
        cook       = self.cook_o
        if auto_split and value and auto_split in value :
            values = value.split (auto_split)
        else :
            values = (value, )
        if auto_split :
            values = self._resolve_range (values, cao)
        return [cook (v, cao) for v in values]
    # end def cooked

    def cooked_default (self, cao = None) :
        result = self.__default
        if TFL.callable (result) :
            result = result ()
        if isinstance (result, pyk.string_types) :
            result = self.cooked (result, cao)
        elif result is None :
            result = ()
        elif not isinstance (result, (list, tuple)) :
            result = [result]
        return result
    # end def cooked_default

    @property
    def default (self) :
        result = self.__cooked_default
        if result is None :
            self.__cooked_default = result = self.cooked_default ()
        return result
    # end def default

    @default.setter
    def default (self, value) :
        self._set_default (value)
    # end def default

    @property
    def raw_default (self) :
        result = self.__default
        if TFL.callable (result) :
            result = result ()
        return result
    # end def raw_default

    def _auto_max_number (self, auto_split) :
        return 0 if auto_split else 1
    # end def _auto_max_number

    def _resolve_range (self, values, cao) :
        pat = self.range_pat
        for value in values :
            if value and pat.match (value) :
                for v in self._resolve_range_1 (value, cao, pat) :
                    yield v
            else :
                yield value
    # end def _resolve_range

    def _resolve_range_1 (self, value, cao, pat = None) :
        yield value
    # end def _resolve_range_1

    def _safe_eval (self, value) :
        if value :
            try :
                return TFL.r_eval (value)
            except Exception :
                ### Don't convert `self` to a string here because that
                ### triggers a call to `cook` which might reset pattern
                ### variables
                raise Err ("Invalid value `%s` for " % (value), self)
    # end def _safe_eval

    def _set_default (self, default) :
        self.__cooked_default = None
        self.__default        = default
    # end def _set_default

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

class _Spec_O_ (TFL.Meta.BaM (_Spec_, metaclass = Opt)) :
    """Base class for option types"""

    kind          = "option"
    prefix        = "-"

# end class _Spec_O_

class _Config_ (_Spec_O_) :
    """Base class for config options"""

# end class _Config_

class _User_Config_Entry_ (_Spec_O_) :
    """Mixin for options that go into TFL.user_config."""

    def __init__ (self, ** kw) :
        if "name" not in kw :
            kw ["name"] = self.__class__.__name__.lower ()
        if "default" not in kw :
            kw ["default"] = self._get_default ()
        if "description" not in kw :
            kw ["description"] = self.__class__.__doc__
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    def name_in_user_config (self) :
        return self.name
    # end def name_in_user_config

    def cook_o (self, value, cao = None) :
        result = self.__super.cook_o (value, cao)
        if result :
            from _TFL.User_Config import user_config
            result = user_config.set_default (self.name_in_user_config, result)
        return result
    # end def cook_o

    def _get_default (self) :
        return None
    # end def _get_default

# end class _User_Config_Entry_

class _Encoding_ (_User_Config_Entry_) :
    """Base class for encoding option types"""

    def __init__ (self, ** kw) :
        assert "name" not in kw
        kw ["name"] = name = self.__class__.__name__.lower ()
        self.abbr   = name.rsplit ("_", 1) [0]
        self.__super.__init__ (** kw)
    # end def __init__

    def _get_default (self) :
        import locale
        return locale.getpreferredencoding ()
    # end def _get_default

# end class _Encoding_

class _Number_ (_Spec_) :
    """Base class for numeric argument and option types"""

    def cook (self, value, cao = None) :
        err = None
        if isinstance (value, pyk.string_types) :
            try :
                value = self._safe_eval (value)
            except Err as exc :
                err = exc ### try `_cook` ("08" doesn't work for `Int`, otherwise)
        try :
            return self._cook (value)
        except (ValueError, TypeError) as exc :
            raise err or Err ("%s for %s `%s`" % (exc, self.kind, self.name))
    # end def cook

    def _resolve_range_1 (self, value, cao, pat) :
        cook     = self.cook
        ### Extract match variables because errors in `cook` might trigger
        ### another pattern match overwriting them
        r_head   = pat.head
        r_tail   = pat.tail
        r_delta  = pat.delta
        head     = cook (r_head, cao)
        tail     = cook (r_tail, cao) + 1
        delta    = cook (r_delta or self.range_delta, cao)
        for v in range (head, tail, delta) :
            yield v
    # end def _resolve_range_1

# end class _Number_

class Bool (_Spec_O_) :
    """Option with a boolean value"""

    implied_value = "True"
    needs_value   = False
    type_abbr     = "B"

    def cook (self, value, cao = None) :
        if value is None :
            return True
        if not isinstance (value, pyk.string_types) :
            return bool (value)
        if value.lower () in ("no", "0", "false") : ### XXX I18N
            return False
        return True
    # end def cook

    def _auto_max_number (self, auto_split) :
        return 1
    # end def _auto_max_number

    def _set_default (self, default) :
        if default is None :
            default = False
        return self.__super._set_default (default)
    # end def _set_default

# end class Bool

class Binary (Bool) :
    """Option with a required boolean value"""

    needs_value = True
    type_abbr   = "Y"

# end class Binary

class Cmd_Choice (TFL.Meta.BaM (TFL.Meta.Object, metaclass = Arg)) :
    """Argument that selects a sub-command"""

    auto_split    = None
    default       = None
    hide          = False
    kind          = "sub-command"
    max_number    = 1
    needs_value   = False
    raw_default   = None

    def __init__ (self, name, * cmds, ** kw) :
        self.name        = name
        self.sub_cmds    = dict   ((c._name, c) for c in cmds)
        self.sub_abbr    = Trie   (self.sub_cmds)
        self.description = kw.pop ("description", "")
        assert not kw
    # end def __init__

    def __call__ (self, value, cao) :
        cao._cmd     = sc = self._get_sub_cmd (value)
        cao._name         = " ".join ([cao._name, sc._name])
        cao._min_args     = sc._min_args
        cao._max_args     = sc._max_args
        cao._arg_list [:] = sc._arg_list
        cao._arg_dict.clear   ()
        cao._arg_dict.update  (sc._arg_dict)
        cao._bun_dict.update  (sc._bun_dict)
        cao._opt_dict.update  (sc._opt_dict)
        cao._opt_abbr.update  (sc._opt_dict, sc._opt_alias)
        cao._opt_alias.update (sc._opt_alias)
        cao._opt_conf.extend  (sc._opt_conf)
    # end def __call__

    @property
    def choices (self) :
        return self.sub_cmds
    # end def choices

    @TFL.Meta.Once_Property
    def _max_name_length (self) :
        return max \
            (sc._max_name_length for sc in pyk.itervalues (self.sub_cmds))
    # end def _max_name_length

    def cooked_default (self, cao = None) :
        return self.default
    # end def cooked_default

    def _get_sub_cmd (self, name) :
        sub_abbr = self.sub_abbr
        sub_cmds = self.sub_cmds
        matches, unique = sub_abbr.completions (name)
        if unique :
            return sub_cmds [unique]
        else :
            if matches :
                raise Err \
                    ( "Ambiguous sub-command `%s`, matches any of %s"
                    % (name, matches)
                    )
            else :
                raise Err \
                    ( "Unkown sub-command `%s`, specify one of: (%s)"
                    % (name, ", ".join (sorted (sub_cmds)))
                    )
    # end def _get_sub_cmd

    def __getattr__ (self, name) :
        return self.sub_cmds [name]
    # end def __getattr__

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
        if value is not None :
            return decimal.Decimal (value)
    # end def _cook

# end class Decimal

class File_System_Encoding (_Encoding_) :
    """Encoding used to convert Unicode filenames into operating system filenames."""

    def _get_default (self) :
        return sys.getfilesystemencoding ()
    # end def _get_default

# end class File_System_Encoding

class Float (_Number_) :
    """Argument or option with a floating point value"""

    type_abbr     = "F"

    _cook         = float

# end class Float

class Help (_Spec_O_) :
    """Option asking for help"""

    alias          = "?"
    auto_split     = ","
    needs_value    = False
    topics         = set (["args", "buns", "cmds", "opts", "summary", "vals"])
    default_topics = set (["args", "buns", "opts", "summary"])

    def __init__ (self) :
        self.__super.__init__ \
            ( name          = "help"
            , description   = _ ("Display help about command")
            )
    # end def __init__

    def __call__ (self, cao, indent = 0) :
        return self._handler (cao, indent)
    # end def __call__

    def cook (self, value, cao = None) :
        if value is None :
            return True
        return self.__super.cook (value, cao)
    # end def cook

    def _handler (self, cao, indent = 0) :
        cmd = cao._cmd
        if cmd._helper :
            cmd._helper (cao)
        else :
            nl     = self.nl = self._nl_gen ()
            topics = self.topics
            wanted = set (v for v in getattr (cao, self.name) if v)
            most_p = False
            if wanted.issubset (set (["all", "*"])) :
                wanted = topics
                most_p = True
            elif wanted == set ([True]) :
                wanted = self.default_topics
                most_p = True
            elif not wanted.issubset (topics) :
                pyk.fprint \
                    ( "Possible help topics:\n    "
                    , ", ".join (sorted (ichain (topics, ("all", "help"))))
                    )
            if "summary" in wanted :
                next (nl)
                self._help_summary (cao, indent)
            arg_p     = any (a for a in cao._arg_list if not a.hide)
            want_args = "args" in wanted
            if want_args and arg_p :
                next (nl)
                self._help_args (cao, indent, heading = not most_p)
            if "cmds" in wanted :
                next (nl)
                self._help_cmds \
                    (cao, indent+ (4 * want_args), heading = not want_args)
            opt_p = any \
                (o for o in pyk.itervalues (cao._opt_dict) if not o.hide)
            if "opts" in wanted and opt_p :
                next (nl)
                self._help_opts (cao, indent, heading = not most_p)
            if "buns" in wanted and cao._bun_dict :
                next (nl)
                self._help_buns (cao, indent + (4 * most_p))
            if "vals" in wanted :
                next (nl)
                self._help_values (cao, indent + (4 * most_p))
    # end def _handler

    def _help_ao (self, ao, cao, head, max_l, prefix = "") :
        if ao.hide :
            return
        name = ao.name
        try :
            v = cao ["%s:raw" % name]
        except KeyError :
            v = ""
        pyk.fprint \
            ( "%s%s%-*s  : %s"
            % (head, prefix, max_l, name, ao.__class__.__name__)
            )
        if ao.description :
            pyk.fprint (head, ao.description, sep = "    ")
        if ao.choices :
            choices = "Possible values: %s" % (", ".join (sorted (ao.choices)))
            pyk.fprint (head, choices, sep = "    ")
    # end def _help_ao

    def _help_args (self, cao, indent = 0, heading = False) :
        if heading :
            pyk.fprint ("%sArguments of %s" % (" " * indent, cao._name))
        indent += 4
        head    = " " * indent
        max_l   = cao._max_name_length
        for arg in cao._arg_list :
            self._help_ao (arg, cao, head, max_l)
        if cao.argv :
            pyk.fprint ()
            pyk.fprint ("%s%-*s  : %s" % (head, max_l, "argv", cao.argv))
    # end def _help_args

    def _help_bun (self, bun, cao, head, indent) :
        pyk.fprint ("%s@%s" % (head, bun._name))
        desc    = bun._description
        if desc :
            pyk.fprint (head, desc, sep = "    ")
        indent += 4
        head    = " " * indent
        max_l   = cao._max_name_length
        for k, v in sorted (pyk.iteritems (bun._kw)) :
            pyk.fprint ("%s%-*s : %s" % (head, max_l, k, v))
    # end def _help_bun

    def _help_buns (self, cao, indent = 0) :
        if cao._bun_dict :
            pyk.fprint \
                ("%sArgument/option bundles of %s" % (" " * indent, cao._name))
            indent += 4
            head    = " " * indent
            for k, b in sorted (pyk.iteritems (cao._bun_dict)) :
                self._help_bun (b, cao, head, indent)
    # end def _help_buns

    def _help_cmds (self, cao, indent = 0, heading = False) :
        cmd = cao._cmd
        if cmd._sub_cmd_choice :
            if heading :
                pyk.fprint ("%sSub commands of %s" % (" " * indent, cao._name))
            indent += 4
            head    = " " * indent
            max_l   = cao._max_name_length
            scs     = sorted \
                ( pyk.iteritems (cmd._sub_cmd_choice.sub_cmds)
                , key = TFL.Getter [0]
                )
            for name, sc in scs :
                pyk.fprint \
                    ("%s%-*s : %s" % (head, max_l, name, sc._description))
        else :
            pyk.fprint \
                ("%s%s doesn't have sub commands" % (" " * indent, cao._name))
    # end def _help_cmds

    def _help_opts (self, cao, indent = 0, heading = False) :
        if heading :
            pyk.fprint ("%sOptions   of %s" % (" " * indent, cao._name))
        indent += 4
        head    = " " * indent
        max_l   = cao._max_name_length - 1
        for name, opt in sorted (pyk.iteritems (cao._opt_dict)) :
            self._help_ao (opt, cao, head, max_l, "-")
    # end def _help_opts

    def _help_summary (self, cao, indent) :
        head = " " * indent
        desc = cao._cmd._description
        pyk.fprint \
            ( "%s%s %s"
            % (head, cao._name, " ".join (self._help_summary_args (cao)))
            )
        if desc :
            pyk.fprint (head, desc, sep = "    ")
        if cao._bun_dict :
            next (self.nl)
            pyk.fprint \
                ( "%sPossible bundles: %s"
                % ( " " * (indent + 4)
                  , ", ".join ("@%s" % b for b in sorted (cao._bun_dict))
                  )
                )
    # end def _help_summary

    def _help_summary_args (self, cao) :
        cmd      = cao._cmd
        min_args = cao._min_args
        max_args = cao._max_args
        if cmd._bun_dict :
            yield "[@bundle]"
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

    def _help_value (self, ao, cao, head, max_l, prefix = "") :
        if ao.hide :
            return
        name = ao.name
        raw_default = pyk.text_type (ao.raw_default)
        try :
            raw = cao ["%s:raw" % name]
        except KeyError :
            raw = None
        if raw is None or raw == []:
            raw = raw_default
        if raw == "" :
            raw = None
        try :
            cooked = cao [name]
        except KeyError :
            cooked = None
        if cooked is None or (isinstance (cooked, list) and cooked == []) :
            cooked = ao.default
        if ao.max_number == 1 and isinstance (cooked, list) :
            cooked = cooked [0]
        pyk.fprint \
            ("%s%s%-*s  = %s" % (head, prefix, max_l, name, raw))
        if pyk.text_type (cooked) != pyk.text_type (raw) :
            if isinstance (cooked, (list, dict)) :
                from _TFL.Formatter import formatted_1, formatted
                pyk.fprint \
                    (formatted (cooked, level = (len (head) // 4 + 1) * 2))
            else :
                pyk.fprint ("%s    %s" % (head, cooked))
    # end def _help_value

    def _help_values (self, cao, indent) :
        pyk.fprint \
            ( "%sActual option and argument values of %s"
            % (" " * indent, cao._name)
            )
        indent += 4
        head    = " " * indent
        max_l   = cao._max_name_length
        for name, opt in sorted (pyk.iteritems (cao._opt_dict)) :
            self._help_value (opt, cao, head, max_l, "-")
        max_l  += 1
        for arg in cao._arg_list :
            self._help_value (arg, cao, head, max_l)
    # end def _help_values

    def _nl_gen (self) :
        while True :
            yield
            pyk.fprint ()
    # end def _nl_gen

    def _set_default (self, default) :
        self.__super._set_default ([])
    # end def _set_default

    def __repr__ (self) :
        return "'%s%s %s'" % \
            ( self.prefix
            , self.name
            , self.description
            )
    # end def __repr__

# end class Help

class Input_Encoding (_Encoding_) :
    """Default encoding for input (files)."""
# end class Input_Encoding

class Int (_Number_) :
    """Argument or option with a integer value"""

    type_abbr     = "I"

    _cook         = int

# end class Int

class Int_X (_Number_) :
    """Argument or option with a integer value, allowing base specification"""

    type_abbr     = "X"

    def _cook (self, value) :
        if isinstance (value, pyk.string_types) :
            return int (value, 0)
        return int (value)
    # end def _cook

# end class Int_X

class Key (_Spec_) :
    """Argument or option that specifies a key of a dictionary `dct`."""

    def __init__ (self, dct, ** kw) :
        assert all (isinstance (k, pyk.string_types) for k in dct)
        self._dict = dct
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    def choices (self) :
        return self._dict
    # end def choices

    def cook (self, value, cao = None) :
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

class Money (Decimal) :
    """Argument or option with a decimal value denoting a monetary amount"""

    auto_split     = None
    type_abbr      = "$"
    comma_dec_pat  = Regexp \
        ( r"([0-9.]+) , (\d{2})$"
        , re.VERBOSE
        )
    period_dec_pat = Regexp \
        ( r"([0-9,]+) \. (\d{2})$"
        , re.VERBOSE
        )

    def _safe_eval (self, value) :
        cdp = self.comma_dec_pat
        pdp = self.period_dec_pat
        if isinstance (value, pyk.string_types) :
            if cdp.match (value) :
                orig  = value
                value = cdp.sub \
                    (r"\g<1>.\g<2>", value.replace (".", ""))
            elif pdp.match (value) :
                value = value.replace (",", "")
        return self.__super._safe_eval (value)
    # end def _safe_eval

# end class Money

class Output_Encoding (_Encoding_) :
    """Default encoding for output."""
# end class Output_Encoding

class Path (_Spec_) :
    """Argument or option with a filename or directory name as value"""

    auto_split    = ":"
    type_abbr     = "P"

    def cook (self, value, cao = None) :
        ### Need to redefine `cook` because instances without `auto_split`
        ### don't go through `_resolve_range`
        if value :
            value = sos.expanded_path (value)
        return value
    # end def cook

    def _resolve_range (self, values, cao) :
        def _gen (values, cao) :
            for value in sos.expanded_globs (* values) :
                for v in self._resolve_range_1 (sos.expanded_path (value), cao):
                    yield v
        for v in TFL.uniq (_gen (values, cao)) :
            yield v
    # end def _resolve_range

# end class Path

class Abs_Path (Path) :
    """Path converted to absolute"""

    type_abbr     = "Q"

    def cook (self, value, cao = None) :
        ### Need to redefine `cook` because instances without `auto_split`
        ### don't go through `_resolve_range`
        result = self.__super.cook (value, cao)
        if result :
            result = sos.path.abspath (result)
        return result
    # end def cook

    def _resolve_range_1 (self, value, cao) :
        yield sos.path.abspath (value)
    # end def _resolve_range_1

# end class Abs_Path

class Rel_Path (Path) :
    """Path that can be relative to a specific base directory."""

    type_abbr     = "R"

    single_match  = False
    _base_dir     = None
    _base_dirs    = ()

    @TFL.Meta.Once_Property
    def base_dirs (self) :
        def _gen (bds) :
            for bd in bds :
                if TFL.callable (bd) :
                    bd = bd ()
                if bd is not None :
                    yield bd
        return tuple (_gen (self._base_dirs or (self._base_dir, )))
    # end def base_dirs

    def _resolve_range_1 (self, value, cao) :
        base_dirs = self.base_dirs
        if base_dirs :
            if not sos.path.isabs (value) :
                def _gen (value, base_dirs, single_match) :
                    not_existing = None
                    for bd in base_dirs :
                        v = sos.path.join (bd, value)
                        if sos.path.exists (v) :
                            not_existing = False
                            yield v
                            if single_match :
                                break
                        elif not_existing is None :
                            not_existing = v
                    if not_existing :
                        yield not_existing
                for v in _gen (value, base_dirs, self.single_match) :
                    yield sos.path.abspath (v)
                return
        yield sos.path.abspath (value)
    # end def _resolve_range_1

# end class Rel_Path

class Config (_Config_, Rel_Path) :
    """Option specifying a config-file"""

    type_abbr     = "C"

    def cook (self, value, cao = None) :
        from _TFL.load_config_file import load_config_file
        path   = self.__super.cook (value, cao)
        result = {}
        if path :
            context = dict (C = cao._cmd if cao else None)
            load_config_file (path, context, result)
        return result
    # end def cook

# end class Config

class Set (_Spec_) :
    """Argument or option that specifies one element of a set of choices"""

    def __init__ (self, choices, ** kw) :
        self.choices = set (choices)
        self.__super.__init__ (** kw)
    # end def __init__

    def cook (self, value, cao = None) :
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

class Time_Zone (_User_Config_Entry_) :
    """Time zone to use."""

    def _get_default (self) :
        return "UTC"
    # end def _get_default

# end class Time_Zone

class Bundle (TFL.Meta.Object) :
    """Model a bundle of values for arguments and options.

       A bundle is defined by creating an instance of :class:`Bundle` with
       the arguments:

       - the name of the bundle,

       - a description of the bundle to be included in the `help`,

       - a number of keyword arguments specifying values for the arguments
         and options defined by the bundle.

    """

    kind          = "bundle"

    def __init__ (self, _name, _description = "", ** _kw) :
        self._name          = _name
        self._description   = _description
        self._kw            = _kw
    # end def __init__

    def __call__ (self, value, cao) :
        assert value == self._name
        cao._use_args (self._kw)
    # end def __call__

    def __contains__ (self, item) :
        return item in self._kw
    # end def __contains__

    def __getattr__ (self, name) :
        return self._kw [name]
    # end def __getattr__

    def __getitem__ (self, key) :
        try :
            return self._kw [key]
        except AttributeError :
            raise KeyError (key)
    # end def __getitem__

# end class Bundle

class Cmd (TFL.Meta.Object) :
    """Model a command with options, arguments, and a handler.

       :meth:`Cmd.parse` and :meth:`Cmd.use` return an instance of
       :class:`CAO`.

       Calling an instance of `Cmd` uses :meth:`parse` (if argument `_argv` is
       specified or no argument at all is given) or :meth:`use` (if `** _kw`
       are specified) and calls the resulting instance of :class:`CAO`.
    """

    _handler      = None
    _helper       = None

    def __init__ \
            ( self
            , handler       = None
            , args          = ()
            , opts          = ()
            , buns          = ()
            , description   = ""
            , name          = ""
            , min_args      = 0
            , max_args      = -1
            , do_keywords   = False
            , put_keywords  = False
            , helper        = None
            , defaults      = {}
            ) :
        assert max_args == -1 or max_args >= min_args
        assert max_args == -1 or max_args >= len (args)
        if handler is not None :
            assert TFL.callable (handler)
            self._handler   = handler
        self._arg_spec      = args
        self._opt_spec      = opts
        self._bun_spec      = buns
        self._min_args      = min_args
        self._max_args      = max_args
        self._description   = \
            description or getattr (handler, "__doc__", "") or ""
        self._name          = name or TFL.Environment.script_name ()
        self._do_keywords   = do_keywords or put_keywords
        self._put_keywords  = put_keywords
        if helper is not None :
            self._helper    = helper
        self.defaults       = dict (defaults)
        self._setup_opts (opts, self.defaults)
        self._setup_args (args)
        self._setup_buns (buns)
    # end def __init__

    def __call__ (self, _argv = None, ** _kw) :
        """Setup and call an instance of :class:`CAO` by calling `use` (if
           `_kw` is given) or `parse` (with `_argv or sys.argv [1:]`).
        """
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
            except Exception as exc :
                if help :
                    pyk.fprint (exc, "\n\nUsage :")
                    cao = CAO (self)
                    self.help (cao, indent = 4)
                    return
                else :
                    raise
        return cao ()
    # end def __call__

    @TFL.Meta.Once_Property
    def _max_name_length (self) :
        result = max \
            (len (k) for k in ichain (self._arg_dict, self._opt_dict))
        if self._sub_cmd_choice :
            result = max (result, self._sub_cmd_choice._max_name_length)
        return result + 1
    # end def _max_name_length

    def parse (self, argv) :
        """Parse arguments, options, and sub-commands specified in `argv`
           (which must not contain the command name, like `sys.argv` would)
           and return an instance of :class:`CAO`.
        """
        result = CAO       (self)
        result._parse_args (argv)
        result._check      ()
        return result
    # end def parse

    def use (self, ** _kw) :
        """Return an instance of :class:`CAO` initialized with the arguments,
           options, and sub-commands specified by the keyword arguments in
           `_kw`.
        """
        result = CAO     (self)
        result._use_args (_kw)
        result._check    ()
        return result
    # end def use

    def _attribute_spec (self, name) :
        if name in self._opt_dict :
            return self._opt_dict [name]
        if name in self._arg_dict :
            return self._arg_dict [name]
        raise AttributeError (name)
    # end def _attribute_spec

    def _setup_args (self, args) :
        self._arg_list = al  = []
        self._arg_dict = ad  = {}
        self._sub_cmd_choice = None
        od = self._opt_dict
        if not args :
            max_args = self._max_args
            if max_args == -1 or max_args > 0 :
                args = (Arg.Str ("__argv"), )
        for i, a in enumerate (args) :
            if isinstance (a, pyk.string_types) :
                a = Arg.from_string (a)
            if isinstance (a.__class__, Opt) :
                raise Err \
                    ("Option type `%s` cannot be used for argument" % a)
            assert a.name not in od
            a.index = i
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
            else :
                a.kind  = "argument"
    # end def _setup_args

    def _setup_buns (self, buns) :
        self._bun_dict = dict ((b._name, b) for b in buns)
    # end def _setup_buns

    def _setup_opt  (self, opt, od, al, index, default = None) :
        od [opt.name]   = opt
        opt.kind        = "option"
        opt.index       = index
        if default is not None :
            opt.default = default
        if opt.alias :
            al [opt.alias] = opt.name
    # end def _setup_opt

    def _setup_opts (self, opts, defaults) :
        self._opt_dict  = od = {}
        self._opt_alias = al = {}
        self._opt_conf  = oc = []
        for i, o in enumerate (opts) :
            if isinstance (o, pyk.string_types) :
                o = Arg.from_string (o.lstrip ("-"))
            elif not isinstance (o.__class__, Arg) :
                raise Err ("Not a valid option `%s`" % o)
            self._setup_opt (o, od, al, i, defaults.get (o.name))
            if isinstance (o, _Config_) :
                oc.append (o)
        oc.sort (key = TFL.Getter.rank)
        if "help" not in od :
            self._setup_opt (Opt.Help (), od, al, -1)
        if "Pdb_on_Exception" not in od :
            self._setup_opt \
                ( Opt.Bool
                    ( "Pdb_on_Exception"
                    , description = "Start python debugger pdb on exception"
                    )
                , self._opt_dict
                , self._opt_alias
                , -1
                )
    # end def _setup_opts

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
    """Command with options and arguments supplied.

       Calling an instance of `CAO` calls the `handler` of the associated
       :class:`Cmd` instance, passing `self` to the `handler`.
    """

    _bun_pat = Regexp \
        ( """@(?P<name> [a-zA-Z0-9_]+)$"""
        , re.VERBOSE
        )
    _key_pat = Regexp \
        ( """\s*"""
          """(?P<name> [^= ]+)"""
          """\s* [=] \s* """
          """(?P<value> .*)"""
        , re.VERBOSE
        )
    _opt_pat = Regexp \
        ( """ -{1,2} (?P<name> [^:= ]+) """
          """ (?: = (?P<quote> [\"\']?) (?P<value> .*) (?P=quote)? )? """
          """ $ """
        , re.VERBOSE
        )

    _pending = TFL.Undef ("pending")

    def __init__ (self, cmd) :
        self._cmd             = cmd
        self._name            = cmd._name
        self._arg_dict        = dict (cmd._arg_dict)
        self._arg_list        = list (cmd._arg_list)
        self._bun_dict        = dict (cmd._bun_dict)
        self._opt_dict        = dict (cmd._opt_dict)
        self._opt_abbr        = Trie (cmd._opt_dict, cmd._opt_alias)
        self._opt_alias       = dict (cmd._opt_alias)
        self._opt_conf        = list (cmd._opt_conf)
        self._min_args        = cmd._min_args
        self._max_args        = cmd._max_args
        self._do_keywords     = cmd._do_keywords
        self._put_keywords    = cmd._put_keywords
        self.argv             = []
        self.argv_raw         = []
        self._max_name_length = cmd._max_name_length
        self._map             = TFL.defaultdict (lambda : self._pending)
        self._raw             = TFL.defaultdict (list)
        self._key_values      = dict ()
    # end def __init__

    def __call__ (self) :
        handler = self._cmd._handler
        if self.Pdb_on_Exception :
            ### Inspired by http://code.activestate.com/recipes/65287/ (r5)
            if hasattr (sys, 'ps1') or not sys.stderr.isatty () :
                ### interactive mode or without terminal
                ### --> leave sys.excepthook unchanged
                pass
            else :
                def info (type, value, tb) :
                    import traceback, pdb
                    traceback.print_exception (type, value, tb)
                    pyk.fprint ()
                    pdb.pm     () # post-mortem mode
                sys.excepthook = info
        if self.help :
            self._cmd.help (self)
        elif handler :
            return handler (self)
        return self
    # end def __call__

    def GET (self, name, default) :
        return getattr (self, name, default)
    # end def GET

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
        if result is self._pending :
            result = map [name] = self._cooked (ao)
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
        min_args = self._min_args
        max_args = self._max_args
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

    def _cooked (self, spec) :
        raw = self._raw.get (spec.name, None)
        if raw is None :
            default = spec.cooked_default (self)
            result  = default if (default is not None) else []
        else :
            result  = list \
                (ichain (* tuple (spec.cooked (r, self) for r in raw)))
        self._map [spec.name] = result
        return result
    # end def _cooked

    def _finish_setup (self) :
        sc = self._cmd._sub_cmd_choice
        for co in self._opt_conf :
            ckds = self._cooked (co)
            for ckd in ckds :
                if sc and sc.name in ckd :
                    self._set_arg (sc, ckd.pop (sc.name))
                for k, v in pyk.iteritems (ckd) :
                    ao = None
                    if k in self._opt_dict :
                        ao = self._opt_dict [k]
                        ao.default = v
                    elif k in self._arg_dict :
                        ao = self._arg_dict [k]
                        ao.default = (v, )
                    elif k not in self._key_values :
                        self._key_values [k] = v
        map = self._map
        pending = self._pending
        for k in self._opt_dict :
            if k not in map or map [k] is pending :
                ### pre-cook un-evaluated options to trigger side effects
                ### if necessary (like _User_Config_Entry_)
                getattr (self, k)
        argv = self.argv
        for spec in self._arg_list :
            ckd = self._cooked (spec)
            if ckd is not None :
                argv.extend (ckd)
    # end def _finish_setup

    def _handle_arg (self, arg, argv_it, check_bun = True) :
        bd  = self._bun_dict
        pat = self._bun_pat
        if check_bun and pat.match (arg) :
            name = pat.name
            if name in bd :
                spec = bd [name]
                arg  = name
            else :
                raise Err \
                    ( "Unknown bundle `%s`, specify one of (%s)"
                    % (arg, ", ".join ("@%s" % b for b in sorted (bd)))
                    )
        else :
            al   = self._arg_list
            spec = al [min (len (self.argv_raw), len (al) - 1)]
        self._set_arg (spec, arg)
    # end def _handle_arg

    def _handle_opt (self, arg, argv_it) :
        pat = self._opt_pat
        if pat.match (arg) :
            k = pat.name
            v = pat.value
            matches, unique = self._opt_abbr.completions (k)
            if unique :
                n = self._opt_alias.get (unique, unique)
                spec = self._opt_dict [n]
                if v is None :
                    if spec.needs_value :
                        try :
                            v = next (argv_it)
                        except StopIteration :
                            raise Err ("Option `%s` needs a value" % n)
                    else :
                        v = spec.implied_value
                self._set_opt  (spec, v)
            else :
                if matches :
                    raise Err \
                        ( "Ambiguous option `%s`, matches any of %s"
                        % (arg, matches)
                        )
                else :
                    raise Err ("Unknown option `%s`" % (arg, ))
    # end def _handle_opt

    def _parse_args (self, argv) :
        argv_it = iter (argv)
        for arg in argv_it :
            if arg == "--" :
                for arg in argv_it :
                    self._handle_arg (arg, argv_it, check_bun = False)
            elif arg.startswith ("-") :
                self._handle_opt (arg, argv_it)
            else :
                self._handle_arg (arg, argv_it)
    # end def _parse_args

    def _set_arg (self, spec, value) :
        kp = self._key_pat
        if isinstance (spec, (Bundle, Cmd_Choice)) :
            if self.argv_raw :
                raise Err \
                    ( "%s `%s` needs to be first argument"
                    % (spec.kind.capitalize (), value)
                    )
            spec (value, self)
        elif self._do_keywords and kp.match (value) :
            self._set_keys ({kp.name : kp.value})
        else :
            self.argv_raw.append (value)
            if spec.name :
                self._map [spec.name] = self._pending
                self._raw [spec.name].append (value)
    # end def _set_arg

    def _set_keys (self, kw) :
        self._key_values.update (kw)
        if self._put_keywords :
           sos.environ.update (kw)
    # end def _set_keys

    def _set_opt (self, spec, value) :
        if value is not None :
            self._raw [spec.name].append (value)
            self._map [spec.name] = self._pending
        else :
            self._map [spec.name] = spec.cooked (value, self)
    # end def _set_opt

    def _use_args (self, _kw) :
        sc = self._cmd._sub_cmd_choice
        if sc and sc.name in _kw :
            self._set_arg (sc, _kw.pop (sc.name))
        ad   = self._arg_dict
        rest = []
        for k, v in pyk.iteritems (_kw) :
            matches, unique = self._opt_abbr.completions (k)
            if unique :
                self._set_opt  (self._opt_dict [unique], v)
            elif k in ad :
                self._set_arg  (ad [k], v)
            elif k == "__rest__" :
                rest = v
            elif k == "__kw__" :
                self._set_keys (v)
            else :
                tail = ""
                if matches :
                    tail = "\n    Ambiguous match for the options: %s" % \
                        (matches, )
                raise Err \
                    ( "Unknown argument or option `%s` [%s] for command %s%s"
                    % (k, v, self._name, tail)
                    )
        argv_it = iter (rest)
        for arg in argv_it :
            self._handle_arg (arg, argv_it)
    # end def _use_args

    def __getattr__ (self, name) :
        try :
            result = self._attribute_value (name)
            setattr (self, name, result)
            return result
        except AttributeError :
            if name == "argn" :
                return len (self.argv)
            else :
                raise
    # end def __getattr__

    def __getitem__ (self, key) :
        if isinstance (key, pyk.string_types) :
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

@TFL.Contextmanager
def expect_except (* Xs) :
    """Hide exception class name differences between Python 2 and 3"""
    try :
        yield
    except Xs as exc :
        print ("%s: %s" % (exc.__class__.__name__, exc))
# end def expect_except

def show (cao) :
    pyk.fprint (cao._name)
    pyk.fprint \
        ("    Arguments  : %s" % (sorted (a.name for a in cao._arg_list),))
    for o in sorted (cao._opt_dict) :
        pyk.fprint ("    -%-9s : %s" % (o, getattr (cao, o)))
    for a in cao._arg_list :
        pyk.fprint ("    %-10s : %s" % (a.name, getattr (cao, a.name)))
    pyk.fprint ("    argv       : %s" % (cao.argv, ))
# end def show

### «text» ### start of documentation
__doc__ = """
Module `CAO`
=============

This module provides classes for defining and processing **commands**,
**arguments**, and **options**. The values for arguments and options can be
parsed from `sys.argv` or supplied by a client via keyword arguments.

A command is defined by creating an instance of :class:`Cmd`
with the arguments

- a callback function `handler` that implements the command,

    `handler` is called with an instance of :class:`CAO` as
    the single argument

- a tuple of :class:`Arg` instances specifying the possible arguments,

- the minimum number of arguments required `min_args`,

- the maximum number of arguments allowed  `max_args`,

    (the default -1 means an unlimited number is allowed)

- a tuple of :class:`Arg` or :class:`Opt` instances specifying the
  possible  options,

- a tuple of :class:`Bundle` instances that define pre-packaged bundles of
  argument- and option-values to support common usage scenarios that can be
  specified simply by using name of the respective bundle,

- a description of the command to be included in the `help`,

    if the `description` argument is undefined, `handler.__doc__` will be
    used if that is defined

- a `name` for the command (by default, the name of the module defining
  the `Command` is used).

For `Arg` and `Opt` arguments, a shortcut string notation can be used:

    `<name>:<type-spec><auto-split-spec>=<default>#<max-number>?<help>`

Calling a :class:`Cmd` instance with an argument array, e.g.,
`sys.argv[1:]`, parses the arguments and options in the array, stores
their values in the instance, and calls the `handler`.

Calling a :class:`Cmd` instance with keyword arguments initializes
the argument and option values from those values and calls the
`handler`.

Alternatively, the methods :meth:`~Cmd.parse` or :meth:`~Cmd.use` can be
called by a client, should explicit flow control be required.

A typical use of :class:`Cmd` looks like::

    >>> def main (cao) :
    ...     "Explanation of the purpose of the command"
    ...     if cao.verbose :
    ...         print ("Starting", cao._name)
    ...     for fn in cao.argv :
    ...         if cao.verbose :
    ...             print ("   processing", fn)
    ...         ### do whatever needs to be done
    ...     if cao.verbose :
    ...         print ("Finished", cao._name)
    ...

    >>> cmd = TFL.CAO.Cmd (
    ...       handler       = main
    ...     , args          = ( "file:P?File(s) to process",)
    ...     , opts          =
    ...         ( "indent:I,=4?Number of spaces to use for indentation"
    ...         , "-output:P"
    ...             "?Name of file to receive output (default: standard output)"
    ...         , "-verbose:B?Print additional information to standard error"
    ...         )
    ...     , min_args      = 2
    ...     , max_args      = 8
    ...     , name          = "cao_example"
    ...     )

    >>> if __name__ == "__main__" :
    ...     cmd ()

`cmd` contains the specification of arguments and options. ::

    >>> type (cmd.indent)
    <class 'CAO.Int'>

    >>> cmd.indent
    'indent:I,=4#0?Number of spaces to use for indentation'

    >>> cmd.indent.name, cmd.indent.default, cmd.indent.description, cmd.indent.auto_split, cmd.indent.max_number
    ('indent', [4], 'Number of spaces to use for indentation', ',', 0)

    >>> type (cmd.verbose)
    <class 'CAO.Bool'>

    >>> cmd.verbose
    '-verbose:B=False#1?Print additional information to standard error'

The methods :meth:`~Cmd.parse` and :meth:`~Cmd.use` return a instance of
:class:`CAO` which provides access to all argument and option values
specified. ::

    >>> with expect_except (Err) :
    ...      cao = cmd.parse (["-verbose"])
    Err: Command/argument/option error: Need at least 2 arguments, got 0

    >>> cao = cmd.parse (["-verbose", "path1", "path2"])

    >>> print (cao.indent, type (cao.indent).__name__)
    [4] list

    >>> print (cao.output)
    None

    >>> print (cao.verbose)
    True

    >>> cao.argn
    2

    >>> cao.argv
    ['path1', 'path2']

    >>> cao.file
    'path1'

    >>> cao ()
    Starting cao_example
       processing path1
       processing path2
    Finished cao_example

    >>> cmd.help (cao)
    cao_example file ...
        Explanation of the purpose of the command
    <BLANKLINE>
        file               : Path
            File(s) to process
    <BLANKLINE>
        argv               : ['path1', 'path2']
    <BLANKLINE>
        cao_example doesn't have sub commands
    <BLANKLINE>
        -Pdb_on_Exception  : Bool
            Start python debugger pdb on exception
        -help              : Help
            Display help about command
        -indent            : Int
            Number of spaces to use for indentation
        -output            : Path
            Name of file to receive output (default: standard output)
        -verbose           : Bool
            Print additional information to standard error
    <BLANKLINE>
        Actual option and argument values of cao_example
            -Pdb_on_Exception   = False
            -help               = []
            -indent             = 4
                [ 4 ]
            -output             = None
                ()
            -verbose            = True
            file                = path1

.. autoclass:: Cmd
   :members: __call__, parse, use
.. autoclass:: CAO

.. autoclass:: Arg
   :members:
.. autoclass:: Opt
   :members:
.. autoclass:: Bundle

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

"""

### «text» ### start of doctest
__test__ = dict \
    ( test = """
Usage examples
----------------

Many of the following tests/examples pass a simple `show` function as
`handler`. `show` just displays some information about the command and the
values passed to it::

    >>> cmd = Cmd (show, name = "Test", args = ("adam:P=/tmp/test?First arg", "bert:I=42"), opts = ("-verbose:B", "-year:I,=2010"))
    >>> cmd._arg_list
    ['adam:P=/tmp/test#1?First arg', 'bert:I=42#1?']
    >>> sorted (str (o) for o in pyk.itervalues (cmd._opt_dict))
    ["'-Pdb_on_Exception:B=False#1?Start python debugger pdb on exception'", "'-help Display help about command'", "'-verbose:B=False#1?'", "'year:I,=2010#0?'"]

    >>> cmd.adam, cmd.verbose
    ('adam:P=/tmp/test#1?First arg', '-verbose:B=False#1?')
    >>> cmd.adam.__class__
    <class 'CAO.Path'>

    >>> cmd (["-year=2000", "-year", "1999", "-v=no", "/tmp/tmp"])
    Test
        Arguments  : ['adam', 'bert']
        -Pdb_on_Exception : False
        -help      : []
       -verbose    : False
        -year      : [2000, 1999]
        adam       : /tmp/tmp
        bert       : 42
        argv       : ['/tmp/tmp', 42]

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
    ['/tmp/tmp', 42]

    >>> cmd (["-year=2000", "-year", "1999", "-verb", "/tmp/tmp", "137"])
    Test
        Arguments  : ['adam', 'bert']
        -Pdb_on_Exception : False
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
    >>> caq = cmd.parse (["/tmp/tmp", "137"])
    >>> caq.verbose
    False

    >>> c1  = Cmd (show, name = "one", args = ("aaa:S", "bbb:S"), opts = ("y:I", "Z:B"))
    >>> c1 ([])
    one
        Arguments  : ['aaa', 'bbb']
        -Pdb_on_Exception : False
        -Z         : False
        -help      : []
        -y         : None
        aaa        : None
        bbb        : None
        argv       : []
    >>> c2  = Cmd (show, name = "two", args = ("ccc:I=3", "ddd:T=D"), opts = ("struct:B", ))
    >>> c2 ([])
    two
        Arguments  : ['ccc', 'ddd']
        -Pdb_on_Exception : False
        -help      : []
        -struct    : False
        ccc        : 3
        ddd        : D
        argv       : [3, 'D']
    >>> coc = Cmd (show,
    ...     name = "Comp", args = (Arg.Cmd_Choice ("sub", c1, c2), ),
    ...     opts = ("verbose:B", "strict:B"))
    >>> coc ([])
    Comp
        Arguments  : ['sub']
        -Pdb_on_Exception : False
        -help      : []
        -strict    : False
        -verbose   : False
        sub        : None
        argv       : []
    >>> coc (["one"])
    Comp one
        Arguments  : ['aaa', 'bbb']
        -Pdb_on_Exception : False
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
        Arguments  : ['ccc', 'ddd']
        -Pdb_on_Exception : False
        -help      : []
        -strict    : False
        -struct    : False
        -verbose   : False
        ccc        : 3
        ddd        : D
        argv       : [3, 'D']
    >>> coc (["-s"])
    Comp
        Arguments  : ['sub']
        -Pdb_on_Exception : False
        -help      : []
        -strict    : True
        -verbose   : False
        sub        : None
        argv       : []
    >>> coc (["-s", "one"])
    Comp one
        Arguments  : ['aaa', 'bbb']
        -Pdb_on_Exception : False
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
        Arguments  : ['ccc', 'ddd']
        -Pdb_on_Exception : False
        -help      : []
        -strict    : True
        -struct    : False
        -verbose   : False
        ccc        : 3
        ddd        : D
        argv       : [3, 'D']
    >>> with expect_except (Err) :
    ...      coc (["two", "-s"])
    Err: Command/argument/option error: Ambiguous option `-s`, matches any of ('strict', 'struct')
    >>> with expect_except (Err) :
    ...      coc (["two", "-t"])
    Err: Command/argument/option error: Unknown option `-t`
    >>> with expect_except (Err) :
    ...      coc (["two", "one"])
    Err: Command/argument/option error: Invalid value `one` for 'ccc:I=3#1?'
    >>> coc (["one", "two"])
    Comp one
        Arguments  : ['aaa', 'bbb']
        -Pdb_on_Exception : False
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
        Arguments  : ['aaa', 'bbb']
        -Pdb_on_Exception : False
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
        Arguments  : ['aaa', 'bbb']
        -Pdb_on_Exception : False
        -Z         : True
        -help      : []
        -strict    : False
        -verbose   : True
        -y         : None
        aaa        : two
        bbb        : three
        argv       : ['two', 'three', 'four']

    >>> ko  = Arg.Key (name = "foo", dct = {"1": "frodo", "a": 42})
    >>> cmd = Cmd (show, name = "dict-test", opts = (ko, ))
    >>> cmd (["-foo", "a"])
    dict-test
        Arguments  : ['__argv']
        -Pdb_on_Exception : False
        -foo       : 42
        -help      : []
        __argv     : None
        argv       : []
    >>> cmd (["-foo=1"])
    dict-test
        Arguments  : ['__argv']
        -Pdb_on_Exception : False
        -foo       : frodo
        -help      : []
        __argv     : None
        argv       : []
    >>> cmd (["a", "b", "c", "d"])
    dict-test
        Arguments  : ['__argv']
        -Pdb_on_Exception : False
        -foo       : None
        -help      : []
        __argv     : a
        argv       : ['a', 'b', 'c', 'd']
    >>> cmd (["-foo", "a", "b", "c", "d"])
    dict-test
        Arguments  : ['__argv']
        -Pdb_on_Exception : False
        -foo       : 42
        -help      : []
        __argv     : b
        argv       : ['b', 'c', 'd']
    >>> cmd (["-foo=1", "a", "b", "c", "d"])
    dict-test
        Arguments  : ['__argv']
        -Pdb_on_Exception : False
        -foo       : frodo
        -help      : []
        __argv     : a
        argv       : ['a', 'b', 'c', 'd']

    >>> _ = coc (["-help"])
    Comp [sub] ...
    <BLANKLINE>
        sub                 : Cmd_Choice
            Possible values: one, two
    <BLANKLINE>
        -Pdb_on_Exception   : Bool
            Start python debugger pdb on exception
        -help               : Help
            Display help about command
        -strict             : Bool
        -verbose            : Bool
    >>> _ = coc (["-help", "one"])
    Comp one [aaa] [bbb] ...
    <BLANKLINE>
        aaa                 : Str
        bbb                 : Str
    <BLANKLINE>
        -Pdb_on_Exception   : Bool
            Start python debugger pdb on exception
        -Z                  : Bool
        -help               : Help
            Display help about command
        -strict             : Bool
        -verbose            : Bool
        -y                  : Int
    >>> _ = coc (["-help", "two"])
    Comp two [ccc] [ddd] ...
    <BLANKLINE>
        ccc                 : Int
        ddd                 : Str_AS
    <BLANKLINE>
        argv                : [3, 'D']
    <BLANKLINE>
        -Pdb_on_Exception   : Bool
            Start python debugger pdb on exception
        -help               : Help
            Display help about command
        -strict             : Bool
        -struct             : Bool
        -verbose            : Bool
    >>> _ = coc (["-help=cmds"])
    Sub commands of Comp
        one :
        two :

    >>> cmd = Cmd (show, name = "Varargs test", max_args = 3)
    >>> cmd ([])
    Varargs test
        Arguments  : ['__argv']
        -Pdb_on_Exception : False
        -help      : []
        __argv     : None
        argv       : []
    >>> cmd (["a"])
    Varargs test
        Arguments  : ['__argv']
        -Pdb_on_Exception : False
        -help      : []
        __argv     : a
        argv       : ['a']
    >>> cmd (["a", "b"])
    Varargs test
        Arguments  : ['__argv']
        -Pdb_on_Exception : False
        -help      : []
        __argv     : a
        argv       : ['a', 'b']
    >>> cmd (["a", "b", "c"])
    Varargs test
        Arguments  : ['__argv']
        -Pdb_on_Exception : False
        -help      : []
        __argv     : a
        argv       : ['a', 'b', 'c']
    >>> with expect_except (Err) :
    ...      cmd (["a", "b", "c", "d"])
    Err: Command/argument/option error: Maximum number of arguments is 3, got 4

    >>> c1b = Bundle ("c1b", sub = "one", Z = True, aaa = "foo")
    >>> c2b = Bundle ("c2b", sub = "two", struct = False, ccc = 42)
    >>> cocb = Cmd (show,
    ...     name = "Comp", args = (Arg.Cmd_Choice ("sub", c1, c2), ),
    ...     opts = ("verbose:B", "strict:B"), buns = (c1b, c2b))
    >>> cocb ([])
    Comp
        Arguments  : ['sub']
        -Pdb_on_Exception : False
        -help      : []
        -strict    : False
        -verbose   : False
        sub        : None
        argv       : []
    >>> cocb (["@c1b"])
    Comp one
        Arguments  : ['aaa', 'bbb']
        -Pdb_on_Exception : False
        -Z         : True
        -help      : []
        -strict    : False
        -verbose   : False
        -y         : None
        aaa        : foo
        bbb        : None
        argv       : ['foo']
    >>> cocb (["@c2b"])
    Comp two
        Arguments  : ['ccc', 'ddd']
        -Pdb_on_Exception : False
        -help      : []
        -strict    : False
        -struct    : False
        -verbose   : False
        ccc        : 42
        ddd        : D
        argv       : [42, 'D']
    >>> with expect_except (Err) :
    ...      cocb (["c2b"])
    Err: Command/argument/option error: Unkown sub-command `c2b`, specify one of: (one, two)
    >>> with expect_except (Err) :
    ...      cocb (["@c3b"])
    Err: Command/argument/option error: Unknown bundle `@c3b`, specify one of (@c1b, @c2b)

    >>> _ = cocb (["-help"])
    Comp [@bundle] [sub] ...
    <BLANKLINE>
        Possible bundles: @c1b, @c2b
    <BLANKLINE>
        sub                 : Cmd_Choice
            Possible values: one, two
    <BLANKLINE>
        -Pdb_on_Exception   : Bool
            Start python debugger pdb on exception
        -help               : Help
            Display help about command
        -strict             : Bool
        -verbose            : Bool
    <BLANKLINE>
        Argument/option bundles of Comp
            @c1b
                Z   : True
                aaa : foo
            @c2b
                ccc    : 42
                struct : False

"""
    )

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.CAO
