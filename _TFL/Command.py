# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.Command
#
# Purpose
#    Base class for an interactive command using CAO to define/process
#    arguments and options
#
# Revision Dates
#    17-May-2012 (CT) Creation
#    22-May-2012 (CT) Add `Sub_Command`, `app_dir`, and `app_path`
#    23-May-2012 (CT) Add `lib_dir`, `Sub_Command._handler_prefix`
#    24-May-2012 (CT) Add `_..._to_combine` to `_lists_to_combine`
#    25-May-2012 (CT) Add `sc_map` and `__getitem__`; add `_parent`
#    31-May-2012 (CT) Add `config_defaults`, define `Config` option in `opts`
#     1-Jun-2012 (CT) Fix `__doc__` in `_M_Command_.__new__`
#     1-Jun-2012 (CT) Add `Sub_Command_Combiner`
#     2-Jun-2012 (CT) Use `_TFL._Export_Module`, not `_TFL._Export`
#     2-Jun-2012 (CT) Factor `_Meta_Base_`, add `Option`
#     2-Jun-2012 (CT) Add `Config_Option`, remove `config_defaults`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL                   import TFL

from   _TFL                   import pyk
from   _TFL                   import sos
from   _TFL.I18N              import _, _T, _Tn
from   _TFL.object_globals    import object_module
from   _TFL.predicate         import first

import _TFL.CAO
import _TFL._Meta.M_Auto_Combine
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

class _Meta_Base_ (TFL.Meta.M_Auto_Combine) :

    def __new__ (mcls, name, bases, dct) :
        prefix = dct.get ("_rn_prefix") or first \
            (getattr (b, "_rn_prefix", None) for b in bases)
        if prefix and name.startswith (prefix) and "_real_name" not in dct :
            dct ["_real_name"] = name [len (prefix):]
        if "_name" not in dct :
            dct ["_name"] = dct.get ("_real_name", name).strip ("_").lower ()
        dct.setdefault ("is_partial", False)
        if not dct.get ("__doc__") :
            ### Find the right base to inherit doc-string from
            ### * must be an instance of `_Meta_Base_`
            ### * must contain a non-empty doc-string in its __dict__
            try :
                dct ["__doc__"] = first \
                    (  d for d in
                           (  b.__dict__.get ("__doc__") for b in bases
                           if isinstance (b, _Meta_Base_)
                           )
                    if d
                    )
            except LookupError :
                pass
        return super (_Meta_Base_, mcls).__new__ (mcls, name, bases, dct)
    # end def __new__

# end class _Meta_Base_

class _M_Option_ (_Meta_Base_) :
    ### Meta class for `Option`.

    pass

# end class _M_Option_

class TFL_Option (TFL.Meta.Object) :
    ### Base class for options of interactive commands.

    __metaclass__           = _M_Option_
    _real_name              = "Option"
    _rn_prefix              = "TFL"

    cook              = None
    hide              = False
    max_number        = None
    range_delta       = 1
    rank              = 0
    type              = None

    _auto_split       = None
    _default          = None
    _defaults         = ()
    _name             = None

    _lists_to_combine = ("_defaults", )

    def __init__ (self, cmd) :
        assert self.type, "%s::%s must define `type`" % \
            (cmd, self.__class__.__name__)
        type = self.type
        if isinstance (type, basestring) :
            try :
                type = self.type = TFL.CAO.Opt.Table [type]
            except KeyError :
                type = self.type = getattr (TFL.CAO, type)
        self.cmd = cmd
    # end def __init__

    def __call__ (self) :
        result = self.type (** self.kw)
        return result
    # end def __call__

    @TFL.Meta.Once_Property
    def auto_split (self) :
        result = self._auto_split
        if result is None :
            result = self.type.auto_split
        return result
    # end def auto_split

    @TFL.Meta.Once_Property
    def default (self) :
        result = self._default
        if result is None and self._defaults :
            if self.auto_split :
                result = self.auto_split.join (self._defaults)
            else :
                raise TypeError \
                    ( "%s::%s hs multiple defaults %s, but no `auto_split`"
                    % (cmd, self.__class__.__name__, self._defaults)
                    )
        return result
    # end def default

    @TFL.Meta.Once_Property
    def kw (self) :
        return dict \
            ( name            = self.name
            , default         = self.default
            , description     = self.__doc__
            , auto_split      = self.auto_split
            , max_number      = self.max_number
            , hide            = self.hide
            , range_delta     = self.range_delta
            , cook            = self.cook
            , rank            = self.rank
            )
    # end def kw

    @TFL.Meta.Once_Property
    def name (self) :
        return self._name or self.__class__.__name__.strip ("_").lower ()
    # end def name

Option = TFL_Option # end class

class TFL_Config_Option (Option) :
    """File(s) specifying defaults for options"""

    auto_split              = ":"
    single_match            = False
    type                    = TFL.CAO.Config

    _base_dir               = None
    _base_dirs              = ("$app_dir", )

    @TFL.Meta.Once_Property
    def base_dirs (self) :
        def _gen (self, bds) :
            for bd in bds :
                if isinstance (bd, basestring) and bd.startswith ("$") :
                    bd = getattr (self.cmd, bd [1:])
                if bd is not None :
                    yield bd
        return tuple (_gen (self, self._base_dirs or (self._base_dir, )))
    # end def base_dirs

    @TFL.Meta.Once_Property
    def kw (self) :
        result = self.__super.kw
        if self.base_dirs :
            result ["_base_dirs"] = self.base_dirs
        result ["single_match"] = self.single_match
        return result
    # end def kw

Config_Option = TFL_Config_Option # end class


class _M_Command_ (_Meta_Base_) :
    ### Meta class for `Command`

    def __new__ (mcls, name, bases, dct) :
        mcls._update_set (dct, _M_Command_, "_sub_commands")
        mcls._update_set (dct, _M_Option_,  "_opts_reified")
        return super (_M_Command_, mcls).__new__ (mcls, name, bases, dct)
    # end def __new__

    @classmethod
    def _update_set (cls, dct, T, name) :
        dct [name] = _set = set (dct.get (name, ()))
        _set.update \
            (  v.__name__ for v in dct.itervalues ()
            if isinstance (v, T) and not getattr (v, "is_partial", 0)
            )
    # end def _update_set

# end class _M_Command_

class TFL_Command (TFL.Meta.Object) :
    ### Base class for interactive commands.

    __metaclass__           = _M_Command_
    _rn_prefix              = "TFL"

    _dicts_to_combine       = ("_defaults", )
    _lists_to_combine       = \
        ( "_args", "_buns", "_opts"
        , "_dicts_to_combine", "_lists_to_combine", "_sets_to_combine"
        )
    _sets_to_combine        = ("_opts_reified", "_sub_commands")

    cmd_choice_name         = _ ("command")
    do_keywords             = False
    handler                 = None
    helper                  = None
    min_args                = 0
    max_args                = -1
    put_keywords            = False

    _args                   = ()
    _buns                   = ()
    _defaults               = {}
    _description            = ""
    _name                   = None
    _opts                   = ()
    _opts_reified           = set ()
    _root                   = None
    _sub_commands           = set ()

    def __init__ (self, _name = None, _parent = None, ** kw) :
        if _name is not None :
            self._name      = _name
        self._init_kw       = kw
        self._parent        = _parent
        if _parent is not None :
            self._root      = _parent._root or _parent
        self._cmd           = TFL.CAO.Cmd \
            ( args          = self.args
            , buns          = self.buns
            , defaults      = self.defaults
            , description   = self.description
            , do_keywords   = self.do_keywords
            , handler       = self.handler
            , helper        = self.helper
            , name          = self.name
            , max_args      = self.max_args
            , min_args      = self.min_args
            , opts          = self.opts
            , put_keywords  = self.put_keywords
            )
    # end def __init__

    def __call__ (self, _argv = None, ** _kw) :
        return self._cmd (_argv, ** _kw)
    # end def __call__

    @TFL.Meta.Once_Property
    def app_dir (self) :
        return sos.path.dirname (self.app_path)
    # end def app_dir

    @TFL.Meta.Once_Property
    def app_path (self) :
        return object_module (self).__file__
    # end def app_path

    @TFL.Meta.Once_Property
    def args (self) :
        if self._sub_commands :
            assert not self._args, \
                ( "Cannot specify both args %s and sub-commands %s"
                , (self._args, self._sub_commands)
                )
            name = _T (self.cmd_choice_name)
            scs  = tuple (sc._cmd for sc in self.sub_commands)
            return (TFL.CAO.Cmd_Choice (name, * scs), )
        else :
            return self._args
    # end def args

    @TFL.Meta.Once_Property
    def buns (self) :
        return self._buns
    # end def buns

    @TFL.Meta.Once_Property
    def defaults (self) :
        result = dict (self._defaults)
        result.update (self.dynamic_defaults (result))
        result.update (self._init_kw)
        return result
    # end def defaults

    @TFL.Meta.Once_Property
    def lib_dir (self) :
        return sos.path.dirname (sos.path.dirname (__file__))
    # end def lib_dir

    @TFL.Meta.Once_Property
    def description (self) :
        return self._description or self.__class__.__doc__
    # end def description

    @TFL.Meta.Once_Property
    def name (self) :
        if self._root :
            return self._name or self.__class__.__name__.strip ("_").lower ()
        else :
            return self.app_path
    # end def name

    @TFL.Meta.Once_Property
    def opts (self) :
        def _gen (self) :
            for k in self._opts_reified :
                o = getattr (self, k)
                yield o (self) ()
        result = list (_gen (self))
        result.extend (self._opts)
        return tuple (result)
    # end def opts

    @TFL.Meta.Once_Property
    def sc_map (self) :
        return dict ((sc.name, sc) for sc in self.sub_commands)
    # end def sc_map

    @TFL.Meta.Once_Property
    def sub_commands (self) :
        def _gen (self) :
            defaults = self.defaults
            for sc in self._sub_commands :
                if isinstance (sc, basestring) :
                    sc = getattr  (self, sc)
                if not isinstance (sc, TFL.CAO.Cmd) :
                    sc = sc (_parent = self, ** defaults)
                yield sc
        return tuple (_gen (self))
    # end def sub_commands

    def dynamic_defaults (self, defaults) :
        return {}
    # end def dynamic_defaults

    def __getitem__ (self, key) :
        if " " in key :
            result = self.sc_map
            for k in key.split (" ") :
                result = result [k]
        else :
            result = self.sc_map [key]
        return result
    # end def __getitem__

Command = TFL_Command # end class

class TFL_Sub_Command (Command) :
    ### Base class for sub-commands

    _real_name              = "Sub_Command"
    _handler_prefix         = ""

    def handler (self, cmd) :
        return self._handler (cmd)
    # end def handler

    @TFL.Meta.Once_Property
    def _handler (self) :
        handler_name = "".join (("_handle_", self._handler_prefix, self.name))
        return getattr (self._root, handler_name)
    # end def _handler

Sub_Command = TFL_Sub_Command # end class

class TFL_Sub_Command_Combiner (Command) :
    ### Base class for sub-commands that combine a number of other sub-commands

    _real_name              = "Sub_Command_Combiner"

    ### `_sub_command_seq` can't be auto-combined because a descendent might
    ### want a different sequence
    _sub_command_seq        = []

    @TFL.Meta.Once_Property
    def sub_command_seq (self) :
        def _gen (self) :
            for sc in self._sub_command_seq :
                if isinstance (sc, basestring) :
                    yield [sc]
                else :
                    yield sc
        return tuple (_gen (self))
    # end def sub_command_seq

    def handler (self, cmd) :
        opts   = self._std_opts (cmd)
        parent = self._parent
        for sc in self.sub_command_seq :
            parent (sc + opts)
    # end def handler

    def _std_opts (self, cmd) :
        result = []
        raws   = cmd._raw
        opts   = cmd._opt_dict
        for k, v in cmd._map.iteritems () :
            opt = opts.get (k)
            if opt :
                mk = "-" + k
                if k in raws :
                    result.extend ((mk, opt.auto_split.join (raws [k])))
                elif v and (not isinstance (v, list) or any (v)) :
                    result.append (mk)
        return result
    # end def _std_opts

Sub_Command_Combiner = TFL_Sub_Command_Combiner # end class

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Command
