# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.Attr.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Attr.Type
#
# Purpose
#    Model attribute types of MOM meta object model
#
# Revision Dates
#    28-Sep-2009 (CT) Creation (factored from TOM.Attr.Type)
#     7-Oct-2009 (CT) Class attribute `syntax` removed (added by `M_Attr_Type`
#                     if necessary)
#     7-Oct-2009 (CT) `_A_Named_Value_` and `A_Boolean` added
#     9-Oct-2009 (CT) `raw_default` and `_symbolic_default` added
#    13-Oct-2009 (CT) Guard for empty string added to `_to_cooked`
#    20-Oct-2009 (MG) `check_ascii` added as it is used for String attributes
#    22-Oct-2009 (CT) `needs_raw_value` added
#    22-Oct-2009 (CT) `max_length` added to `A_String` and its descendents
#    22-Oct-2009 (CT) Signatures of `_from_string_prepare` and
#                     `_from_string_eval` fixed
#    27-Oct-2009 (CT) `_A_Object_` changed to use `epk` instead of `name`
#    28-Oct-2009 (CT) I18N
#    28-Oct-2009 (CT) `A_Link_Role` and descendents added
#    29-Oct-2009 (CT) `_t_rank` added
#     3-Nov-2009 (CT) Fixed `as_string` and `_to_cooked` of `_A_Object_`
#     3-Nov-2009 (CT) `A_Link_Role` derived from `_A_Object_`
#     4-Nov-2009 (CT) `__all__` defined and used
#    19-Nov-2009 (CT) `_A_Object_._get_scope` changed to use
#                     `MOM.Scope.active` as default
#    23-Nov-2009 (CT) `__cmp__` and `__hash__` removed (breaks hashing of
#                     Link_Role attributes)
#    24-Nov-2009 (CT) `_A_Object_.cooked` added to check value agains `Class`
#    25-Nov-2009 (CT) `invariant` removed
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    26-Nov-2009 (CT) `A_Object`, `A_Cached_Role`, and `A_Cached_Role_DFC` added
#    26-Nov-2009 (CT) `_A_Object_.etype_manager` factored and used
#    18-Dec-2009 (CT) Use `unicode` instead of `str`
#    21-Dec-2009 (CT) `_A_Object_._get_object` factored
#    22-Dec-2009 (CT) `_A_Link_Role_Seq_No_` removed
#    30-Dec-2009 (CT) `A_Decimal` added
#     5-Jan-2010 (CT) `_Number_.min_value` and `_Number_.max_value` added
#     5-Jan-2010 (CT) `_checkers` added to `A_Attr_Type` and `_Number_`
#    14-Jan-2010 (CT) `ui_name` added
#    18-Jan-2010 (CT) `_A_Typed_Collection_`, `_A_Typed_List_`,
#                     `_A_Typed_Set_`, and `_A_Object_Set_` added
#    18-Jan-2010 (CT) `A_Cached_Role_Set` added
#    18-Jan-2010 (CT) `_A_Object_._check_type` factored
#    18-Jan-2010 (CT) `A_Link_Role`: redefined `cooked` (performance) and
#                     `_check_type` (to check `refuse_links`)
#    19-Jan-2010 (CT) `_A_String_` factored
#    19-Jan-2010 (CT) `A_Char` added
#    21-Jan-2010 (CT) `as_arg_ckd` and `as_arg_raw` added
#    21-Jan-2010 (CT) `cooked` and `_to_cooked` redefined for `_A_String_`
#    31-Jan-2010 (CT) `computed_default` added
#    31-Jan-2010 (CT) `A_Date_Slug` added
#     2-Feb-2010 (CT) `Pickler = None` added to `_A_Attr_Type_`
#     2-Feb-2010 (CT) `_A_Named_Object_` added
#     2-Feb-2010 (CT) `auto_up_depends` added
#     3-Feb-2010 (CT) `A_Email` added
#     4-Feb-2010 (CT) `_A_String_.default` added (`""`)
#     4-Feb-2010 (CT) `_A_Composite_` added
#     4-Feb-2010 (CT) Argument `e_type` added to `_checkers`
#                     `_A_Composite_._checkers` added
#     5-Feb-2010 (CT) `_A_Composite_.cooked` added
#     6-Feb-2010 (MG) `_A_Date_.as_string` typo fixed
#     9-Feb-2010 (CT) `now` added to `A_Date`, `A_Date_Time`, and `A_Time`
#    10-Feb-2010 (CT) `_A_Date_.needs_raw_value = False` added
#    12-Feb-2010 (CT) `A_Blob` added
#    22-Feb-2010 (CT) `A_Attr_Type.cooked` changed to guard agains `None`
#    22-Feb-2010 (CT) `_A_String_.cooked` removed, `._from_string_eval` and
#                     `._to_cooked` changed to call `simple_cooked`
#    22-Feb-2010 (CT) `_A_String_.__metaclass__` set to `M_Attr_Type_String`
#    24-Feb-2010 (CT) `ui_length` added
#    28-Feb-2010 (CT) `_A_String_Base_` factored, `A_Numeric_String` added
#     3-Mar-2010 (CT) `_checkers` changed to take additional argument `kind`
#     3-Mar-2010 (CT) `_A_Composite_._checkers` changed to honor `kind.electric`
#     4-Mar-2010 (CT) `_A_String_Base_._checkers` redefined to add a check
#                     for `max_length`, if any
#     4-Mar-2010 (CT) `max_length = 0` added to `_A_String_Base_`
#    10-Mar-2010 (CT) `A_Int_List` and `A_Date_List` added
#    11-Mar-2010 (CT) `epk_def_set_ckd` and `epk_def_set_raw` added
#    11-Mar-2010 (CT) `_A_Typed_Set_` corrected
#    12-Mar-2010 (CT) `_A_Composite_.from_string` corrected
#                     (s/s/t/ after assignment)
#    12-Mar-2010 (CT) Interface of `Pickler` changed
#    13-Mar-2010 (CT) `_A_Typed_Collection_.needs_raw_value = False`
#    13-Mar-2010 (CT) `_A_Binary_String_` added
#    15-Mar-2010 (CT) Interface of `attr.Pickler` changed again (`attr_type`)
#    22-Mar-2010 (CT) `A_Dirname` and `A_Filename` added (+ `_A_Filename_`)
#     9-Apr-2010 (CT) `A_Url` added
#    20-Apr-2010 (CT) Default `Type` added to `_A_Named_Object_.Pickler`
#    26-Apr-2010 (CT) `_A_Object_._to_cooked` changed to accept a single value
#                     as plain string instead of as a 1-tuple
#    26-Apr-2010 (CT) `_A_Typed_Collection_.from_string` redefined
#    26-Apr-2010 (CT) `_fix_C_Type` added
#    26-Apr-2010 (CT) `_A_Typed_Collection_._checkers` redefined to call
#                     `_fix_C_Type`
#    27-Apr-2010 (CT) Default for `glob` and `locl` changed from `None` to `{}`
#    27-Apr-2010 (CT) Default for `needs_raw_value` changed to `False`
#    28-Apr-2010 (CT) `_A_Collection_` factored from `_A_Typed_Collection_`
#    28-Apr-2010 (CT) `_A_Composite_Collection_` added
#    30-Apr-2010 (CT) `_A_Object_._get_object` changed to improve the message
#                     passed to `MOM.Error.No_Such_Object`
#    30-Apr-2010 (CT) `_A_Composite_.from_string` changed to set `raw = True`
#    30-Apr-2010 (CT) `A_Date.cooked` and `A_Date_Time.cooked` added to
#                     enforce the right type
#     4-May-2010 (CT) `ac_query` and `Q` added
#    11-May-2010 (CT) `A_Date_Time.cooked` corrected (an instance of
#                     `datetime.datetime` is also an instance of
#                     `datetime.date`!)
#    19-May-2010 (CT) `_A_Object_._check_type` changed to check against
#                     `etype.Essence`
#     7-Jun-2010 (CT) `_A_Named_Object_.Pickler` methods guarded against `None`
#    18-Jun-2010 (CT) `_A_String_Base_.default` changed from `""` to `u""`
#    21-Jun-2010 (CT) `_A_Filename_.simple_cooked` changed to use
#                     `I18N.encode_f` instead of hard-coded `encode` to `ascii`
#    22-Jun-2010 (CT) `is_mandatory` added
#    24-Jun-2010 (CT) `db_sig` added
#    29-Jun-2010 (CT) s/from_pickle_cargo/from_attr_pickle_cargo/
#                     s/as_pickle_cargo/as_attr_pickle_cargo/
#    18-Aug-2010 (CT) `A_Date_Time_List` added
#    19-Aug-2010 (CT) `_A_Date_._from_string_eval` changed into
#                     `Class_and_Instance_Method`
#    19-Aug-2010 (CT) `A_Date.cooked` and `A_Date_Time.cooked` changed to
#                     accept strings, too
#    26-Aug-2010 (CT) Ballast dumped
#                     * `from_code` removed
#                     * `symbolic_ref_pat` removed
#                     * `from_string` drastically simplified (symbolic...)
#                     * `P_Type` added and used, `simple_cooked` removed
#    30-Aug-2010 (CT) `A_Url.max_length` increased from 96 to 160
#    30-Aug-2010 (CT) `__future__` imports added to improve 3-compatibility
#     2-Sep-2010 (CT) Signatures of `Pickler.as_cargo` and `.from_cargo` changed
#     6-Sep-2010 (CT) `A_Boolean._from_string` redefined to allow empty strings
#     6-Sep-2010 (CT) `_A_Composite_Collection_` removed
#     6-Sep-2010 (CT) `_A_Typed_Tuple_` added
#    13-Oct-2010 (CT) `example` added
#    13-Oct-2010 (CT) `A_Date_Time.as_string` redefined to not output `0:0`
#    14-Oct-2010 (CT) Last vestiges of `_symbolic_default` removed
#    28-Oct-2010 (CT) `_A_Object_._get_object` changed to take type-name from
#                     `epk`, if possible
#    17-Nov-2010 (CT) `sort_rank` added
#    22-Nov-2010 (CT) `A_Euro_Amount` and `A_Year` added, `_A_Decimal_` factored
#     8-Feb-2011 (CT) s/Required/Necessary/, s/Mandatory/Required/
#     9-Feb-2011 (CT) `ui_allow_new` added to `_A_Object_` and `A_Link_Role`
#    24-Feb-2011 (CT) s/A_Object/A_Entity/
#     6-Mar-2011 (CT) `_A_Date_.as_string`: convert result to `unicode`
#     8-Mar-2011 (CT) `_A_Entity_.from_string` changed to check
#                     `isinstance (s, self.Class)`
#     8-Mar-2011 (CT) `_cls_attr` added
#    30-May-2011 (CT) `from_string` changed to except "" for `s`
#     5-Jul-2011 (CT) `e_completer` and `f_completer` added to `A_Attr_Type`
#    16-Jul-2011 (CT) `_AC_Query_S_` added and used
#    17-Jul-2011 (CT) s/f_completer/completer/, removed `e_completer`
#    20-Jul-2011 (CT) `A_Date_Time` changed to use UTC for cooked value
#    20-Jul-2011 (CT) `_A_Date_._output_format` added and used
#    26-Jul-2011 (CT) `ckd_query_eq` and `raw_query_eq` added
#    28-Jul-2011 (CT) `ckd_query` and `raw_query` added
#     9-Sep-2011 (CT) Use `etm.E_Type` instead of `etm._etype`
#    12-Sep-2011 (CT) `_AC_Query_` changed to use init-arg `attr_name`
#                     instead of `q` and to use `prefix` in `__call__`
#    12-Sep-2011 (CT) `_AC_Query_C_` added and used for `_A_Composite_.ac_query`
#    13-Sep-2011 (CT) `ac_ui_display` added
#    15-Sep-2011 (CT) `_AC_Query_E_` added and used for `_A_Entity_.ac_query`
#    15-Sep-2011 (CT) `_A_Entity_.C_Type` added (Alias_Property) to fix
#                     `ac_query`
#    21-Sep-2011 (CT) `_AC_Query_Date_` added and used for `A_Date.ac_query`
#    21-Sep-2011 (CT) `_A_Composite_.__getattr__` added
#    22-Sep-2011 (CT) s/Object_Reference_Mixin/Id_Entity_Reference_Mixin/
#    22-Sep-2011 (CT) s/A_Entity/A_Id_Entity/
#    22-Sep-2011 (CT) s/Class/P_Type/ for _A_Id_Entity_ attributes
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#    22-Sep-2011 (CT) `_A_Entity_` factored from `_A_Composite_` and
#                     `_A_Id_Entity_`
#    23-Sep-2011 (CT) `needs_raw_value` and `ignore_case` added to `db_sig`
#    23-Sep-2011 (CT) `_A_Id_Entity_.as_code` robustified
#     4-Nov-2011 (CT) Redefine `_A_Typed_Collection_.ui_length`
#     8-Nov-2011 (CT) Change `_checkers` to yield check only, not `(check, ())`
#    11-Nov-2011 (CT) Factor `MOM.Attr.Filter`, replace `ac_query` by `Q.AC`
#    16-Nov-2011 (CT) Add `sorted_by` to `_A_Composite_` and `_A_Id_Entity_`
#    17-Nov-2011 (CT) Add `E_Type`
#    21-Nov-2011 (CT) Add `ui_name_T`
#     2-Dec-2011 (CT) Add `A_Boolean.Q_Ckd_Type`
#     4-Dec-2011 (CT) Replace `MOM.Attr.Filter` by `MOM.Attr.Querier`
#     4-Dec-2011 (CT) Add `Boolean.cooked` (to fix `Boolean.Q.EQ ("no")`)
#     4-Dec-2011 (CT) Add `Choices`
#    20-Dec-2011 (CT) Change `_A_Composite_.as_code` to use `attr_as_code`
#    20-Dec-2011 (CT) s/Q/AQ/
#    20-Dec-2011 (CT) Remove `ckd_query` and `ckd_query_eq`
#    22-Dec-2011 (CT) Add `A_Date.completer`
#    15-Feb-2012 (CT) Change unlimited `A_Link_Role.max_links` from `0` to `-1`
#     6-Mar-2012 (CT) Use `_` at class level, not `_T`
#     6-Mar-2012 (CT) Factor `Syntax_Re_Mixin`
#     7-Mar-2012 (CT) Change ancestor of `A_Attr_Type` from `object` to
#                     `TFL.Meta.Object` (to avoid MRO conflict for
#                     Syntax_Re_Mixin [which derives from `TFL.Meta.Object`])
#    14-Mar-2012 (CT) Add `Eval_Mixin` and `_A_String_Ascii_`
#    27-Mar-2012 (CT) Add `electric` to mark framework-generated attributes
#    28-Mar-2012 (CT) Add `A_Freqency`
#    29-Mar-2012 (CT) Change `_A_Unit_._unit_pattern` to not force whitespace
#                     between a plain number and the unit
#    11-Apr-2012 (CT) Add `A_Url_X`
#    15-Apr-2012 (CT) Adapted to changes of `MOM.Error`
#    19-Apr-2012 (CT) Use translated `.ui_name` instead of `.type_name` for
#                     exceptions
#    22-Apr-2012 (CT) Adapt to signature change of `is_correct`
#                     (`kind` -->`_kind`)
#    10-May-2012 (CT) Add `A_Angle`
#    11-May-2012 (CT) `_A_Number_._from_string` changed to raise `ValueError`
#                     if `_call_eval` fails
#    14-May-2012 (CT) Add `_A_Filename_.P_Type`
#    23-May-2012 (RS) Make docstrings useable for end-user
#     6-Jun-2012 (CT) Change `_A_Entity_.E_Type` to `Alias_Property`
#     7-Jun-2012 (CT) Use `TFL.r_eval`
#    19-Jul-2012 (RS) Factor `plain_number_pat`
#                     Add degree/minute/second parsing to `A_Angle`
#     3-Aug-2012 (CT) Redefine `A_Link_Role.E_Type` and `.P_Type` as aliases
#                     for `role_type`
#     5-Aug-2012 (CT) Change `_A_Id_Entity_.from_string` to allow pid
#     7-Aug-2012 (CT) Add `_A_Composite_.example`
#     8-Aug-2012 (CT) Robustify `A_Link_Role.ui_name`
#     8-Aug-2012 (CT) Guard against exceptions in `example`
#    11-Aug-2012 (CT) Define `_A_Id_Entity_.example` as `property`,
#                     not `Once_Property` (result might be `rollback`-ed)
#    17-Aug-2012 (CT) Add `is_link_role` to `_A_Id_Entity_`, `A_Link_Role`
#    20-Aug-2012 (RS) Fix typo, now `A_Frequency`
#     8-Sep-2012 (CT) Add `A_Enum`
#     8-Sep-2012 (CT) Convert more `_from_string` definitions to
#                     Class_and_Instance_Method
#    12-Sep-2012 (CT) Add `A_Link_Role.auto_derive_np`, `.auto_cache_np`
#    12-Sep-2012 (CT) Add `__init__` argument `e_type`
#    13-Sep-2012 (CT) Add `fix_doc`
#    19-Sep-2012 (CT) Add `A_Link_Role.force_role_name`
#    10-Oct-2012 (CT) Move parsing from `A_Angle.cooked` to `._from_string`
#    11-Oct-2012 (CT) Add `A_Url_X.example`
#    11-Oct-2012 (CT) Change `_A_Number_.code_format` to "%s" (inherits "%r")
#    11-Oct-2012 (CT) Add and use `A_Boolean.Table_X`
#    11-Oct-2012 (CT) Add `sig_rank`
#    12-Oct-2012 (CT) Remove `_call_eval` from `_A_Composite_.from_string`
#    12-Oct-2012 (CT) Add `signified` to `_A_Composite_.cooked`, `.from_string`
#    12-Oct-2012 (CT) Remove `dict ` from output of `_A_Composite_.as_code`
#    16-Oct-2012 (CT) Add `as_rest_cargo_ckd`, `as_rest_cargo_raw`;
#                     add `Atomic_Json_Mixin`
#     9-Nov-2012 (CT) Change arguments to `MOM.Error.Link_Type`
#    12-Dec-2012 (CT) Add clause for `MOM.Entity` to `A_Id_Entity.from_string`
#    13-Dec-2012 (CT) Set `A_Angle.needs_raw_value` to `True`
#    14-Dec-2012 (CT) Robustify `_A_Id_Entity_._check_type`
#    11-Jan-2013 (CT) Add `A_AIS_Value`
#    16-Jan-2013 (CT) Add `Init_Only_Mixin` to `A_AIS_Value.Kind_Mixins`
#    24-Jan-2013 (CT) Add guards to `A_Enum.cooked`
#    25-Feb-2013 (CT) Add `query_preconditions`
#    27-Feb-2013 (CT) Add `sort_skip`
#    27-Feb-2013 (CT) Move `_fix_P_Type` into `_A_Entity_.__init__`
#     6-Mar-2013 (CT) Change `_A_Unit_.eligible_raw_values, `._from_string` to
#                     `Class_and_Instance_Method`, redefine `_A_Unit_.cooked`
#     7-Mar-2013 (CT) Add `A_Frequency.completer`
#    11-Mar-2013 (CT) Factor `fix_doc` to `MOM.Prop.Type`
#    15-Apr-2013 (CT) Add `_A_Id_Entity_.allow_e_types`, `.refuse_e_types`
#    16-Apr-2013 (CT) Change `_A_Id_Entity_.check_type` to check against
#                     `.refuse_e_types_transitive`, too
#    17-Apr-2013 (CT) Move calls of `check_type` to `Kind._set_cooked_value`
#                     Remove `A_Link_Role.cooked` and `._check_type`
#    17-Apr-2013 (CT) Change `as_arg_ckd` and `as_arg_raw` to normal methods
#    18-Apr-2013 (CT) Raise `MOM.Error.Wrong_Type` or `.Attribute_Syntax`,
#                     not `ValueError`
#    18-Apr-2013 (CT) Add `_A_Id_Entity_.eligible_e_types` and
#                     `.selectable_e_types_unique_epk`
#    19-Apr-2013 (CT) Remove `_A_Id_Entity_.eligible_objects`,
#                     `.eligible_raw_values`
#    26-Apr-2013 (CT) Remove `A_AIS_Value`
#     1-May-2013 (CT) Add `Email._syntax_re`
#     8-May-2013 (CT) Add `A_Link_Ref` and `A_Link_Ref_Set`
#    10-May-2013 (CT) Add `link_ref_singular`
#    11-May-2013 (CT) Factor `_A_Rev_Ref_`, add `A_Rev_Ref_Set`
#    12-May-2013 (CT) Add `A_Role_Ref` and `A_Role_Ref_Set`
#    13-May-2013 (CT) Factor `_A_Id_Entity_Collection_`,
#                     add `_A_Id_Entity_List_`
#    15-May-2013 (CT) Rename `auto_cache` to `auto_rev_ref`
#    17-May-2013 (CT) Add `sort_key` to `_A_Rev_Ref_.query`, `.query_x`
#     3-Jun-2013 (CT) Change `_A_Id_Entity_.example` to return example
#                     instance, not `.as_string`
#     3-Jun-2013 (CT) Change `A_Email.example` to be syntactically valid
#     3-Jun-2013 (CT) Get attribute descriptors from `etype.attributes`
#     4-Jun-2013 (CT) Add `A_Surrogate`
#     5-Jun-2013 (CT) Add `q_able`
#     5-Jun-2013 (CT) Add `is_attr_type`
#     5-Jun-2013 (CT) Dry `M_Attr_Type` names
#     5-Jun-2013 (CT) Add metaclass to `A_Surrogate`
#     6-Jun-2013 (CT) Add `A_Surrogate.q_name`
#     6-Jun-2013 (CT) Use `pyk.int_types`, not `int`;
#                     `pyk.string_types`, not `basestring`
#    14-Jun-2013 (CT) Set `det_base` and `det_root`
#    19-Jun-2013 (CT) Add `det` and `det_kind`
#    26-Jun-2013 (CT) Add `max_ui_length`
#    26-Jun-2013 (CT) Add numeric properties, e.g., `max_digits`, to `db_sig`
#    26-Jun-2013 (CT) Add `Pickled_Type`, use `Class_and_Instance_Once_Property`
#    27-Jun-2013 (CT) Change `_A_Binary_String_.max_length` from `None` to `0`
#     1-Jul-2013 (CT) Factor `q_name` from `A_Surrogate` to `A_Attr_Type`
#     3-Jul-2013 (CT) Add `q_able_names`
#     4-Jul-2013 (CT) DRY `Pickled_Type`, fix `Pickled_Type_Raw`
#    10-Jul-2013 (CT) Change `_A_Rev_Ref_.kind` to `_Rev_Query_`
#    10-Jul-2013 (CT) Factor `_A_Rev_Ref_.sqx`, use `MOM.SQ`
#    12-Jul-2013 (CT) Derive `A_Role_Ref_Set` from `A_Rev_Ref_Set`,
#                     not `_A_Id_Entity_Set_`
#    12-Jul-2013 (CT) Add `A_Rev_Ref`
#    12-Jul-2013 (CT) Add support for `sqx_filter` to `_A_Rev_Ref_`
#     1-Aug-2013 (CT) Factor `_A_SPK_Entity_`, add `_A_MD_Change_`
#    21-Aug-2013 (CT) Add `_A_Rev_Ref_.finished_query_first`, `.sort_key`
#    ««revision-date»»···
#--

from   __future__            import absolute_import, division
from   __future__            import print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

from   _MOM._Attr.Filter     import Q
from   _MOM.SQ               import SQ

import _MOM._Attr.Coll
import _MOM._Attr.Completer
import _MOM._Attr.Kind
import _MOM._Attr.Querier
import _MOM._Attr.Selector
import _MOM._Meta.M_Attr_Type
import _MOM._Prop.Type

from   _TFL.I18N             import _, _T
from   _TFL.predicate        import uniq
from   _TFL.Regexp           import *
from   _TFL                  import sos

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL._Meta.Property
import _TFL.Decorator
import _TFL.Currency
import _TFL.r_eval

import datetime
import decimal
import itertools
import logging
import math
import time

plain_number_pat = r"\d+ (?: \.\d*)? (?: [eE]\d+)? \s*"

def is_attr_type (x) :
    return isinstance (x, MOM.Meta.M_Attr_Type.Root)
# end def is_attr_type

@TFL.Decorator
def _pts_prop (f) :
    name = f.__name__
    def _ (self) :
        result = getattr (self._Pickler_Type, name, None)
        if result is None :
            result = getattr (self._attr_type, name, None)
        return result
    return _
# end def _pts_prop

@pyk.adapt__bool__
class Pickled_Type_Spec (TFL.Meta.Object) :

    def __init__ (self, p_type, attr_type, Pickler_Type = None) :
        self.p_type        = p_type
        self.__name__      = p_type and p_type.__name__
        self._Pickler_Type = Pickler_Type
        self._attr_type    = attr_type
    # end def __init__

    @TFL.Meta.Once_Property
    @_pts_prop
    def decimal_places (self) : pass

    @TFL.Meta.Once_Property
    @_pts_prop
    def ignore_case (self) : pass

    @TFL.Meta.Once_Property
    def length (self) :
        result = self.max_length
        if result is None :
            result = self.max_ui_length
        return result
    # end def length

    @TFL.Meta.Once_Property
    @_pts_prop
    def max_digits (self) : pass

    @TFL.Meta.Once_Property
    @_pts_prop
    def max_length (self) : pass

    @TFL.Meta.Once_Property
    @_pts_prop
    def max_ui_length (self) : pass

    @TFL.Meta.Once_Property
    @_pts_prop
    def max_value (self) : pass

    @TFL.Meta.Once_Property
    @_pts_prop
    def min_value (self) : pass

    def __bool__ (self) :
        return self.p_type is not None
    # end def __bool__

# end class Pickled_Type_Spec

class A_Attr_Type (MOM.Prop.Type) :
    """Root class for attribute types for the MOM meta object model."""

    __metaclass__       = MOM.Meta.M_Attr_Type.Root
    _doc_properties     = ("syntax", )
    _sets_to_combine    = MOM.Prop.Type._sets_to_combine  + ("check", )
    _lists_to_combine   = MOM.Prop.Type._lists_to_combine + ("Kind_Mixins", )

    auto_up_depends     = ()
    check               = set ()
    check_syntax        = None
    Choices             = None
    code_format         = "%r"
    completer           = None
    computed            = None
    computed_default    = None
    db_sig_version      = 0
    default             = None
    description         = ""
    E_Type              = None  ### E_Type of `_A_Entity_`, if any
    electric            = False ### True if created by framework
    explanation         = ""
    format              = "%s"
    group               = ""
    hidden              = False
    kind                = None
    Kind_Mixins         = ()
    needs_raw_value     = False
    Pickler             = None
    P_Type              = None  ### Python type of attribute values
    Q_Ckd_Type          = MOM.Attr.Querier.Ckd
    Q_Raw_Type          = MOM.Attr.Querier.Raw
    q_able              = True
    query               = None
    query_fct           = None
    query_preconditions = ()
    rank                = 0
    raw_default         = ""
    record_changes      = True
    sort_rank           = 0
    sort_skip           = False ### don't include in sorted_by_epk if True
    store_default       = False
    typ                 = None
    ui_name             = TFL.Meta.Class_and_Instance_Once_Property \
        (lambda s : s.name.capitalize ().replace ("_", " "))
    ui_length           = 20

    _t_rank             = 0

    @TFL.Meta.Once_Property
    def AQ (self) :
        return self.Q_Raw if self.needs_raw_value else self.Q_Ckd
    # end def AQ

    @TFL.Meta.Class_and_Instance_Once_Property
    def Pickled_Type (self) :
        args = (self.P_Type, self)
        if self.Pickler :
            PT = getattr (self.Pickler, "Type", None)
            if is_attr_type (PT) :
                args = (PT.P_Type, self, PT)
            elif PT is not None :
                args = (PT, self)
        return Pickled_Type_Spec (* args)
    # end def Pickled_Type

    @TFL.Meta.Class_Property
    @TFL.Meta.Once_Property
    def Pickled_Type_Raw (self) :
        if self.needs_raw_value :
            return Pickled_Type_Spec (unicode, self)
    # end def Pickled_Type_Raw

    @TFL.Meta.Class_and_Instance_Once_Property
    def Q_Ckd (self) :
        return self.Q_Ckd_Type (self)
    # end def Q_Ckd

    @TFL.Meta.Class_and_Instance_Once_Property
    def Q_Raw (self) :
        return self.Q_Raw_Type (self)
    # end def Q_Raw

    @TFL.Meta.Once_Property
    def q_able_names (self) :
        return tuple (uniq (itertools.chain ((self.name, ), self.renameds)))
    # end def q_able_names

    @TFL.Meta.Once_Property
    def q_name (self) :
        ### use `_type_name` here because `type_name` property isn't set up
        ### properly when attribute is instantiated
        tn = self.e_type._type_name
        return "%s.%s" % (tn, self.name)
    # end def q_name

    @TFL.Meta.Class_and_Instance_Once_Property
    def example (self) :
        return self.raw_default
    # end def example

    @TFL.Meta.Class_Property
    @TFL.Meta.Class_and_Instance_Method
    def max_ui_length (self) :
        result = self._max_ui_length
        if result is None :
            result = self._max_ui_length = max \
                (self.ui_length, (getattr (self, "max_length", 0) or 0) + 1)
        return result
    # end def max_ui_length

    @TFL.Meta.Once_Property
    def raw_query (self) :
        result = getattr (Q, self.raw_name)
        return result
    # end def raw_query

    @TFL.Meta.Once_Property
    def raw_query_eq (self) :
        return self.AQ.EQ
    # end def raw_query_eq

    @TFL.Meta.Class_and_Instance_Once_Property
    def sig_rank (soc) :
        """Rank of attribute in signature of `__init__`."""
        k_rank = getattr (soc.kind, "_k_rank", 0)
        return (k_rank, soc._t_rank, soc.rank, soc._d_rank)
    # end def sig_rank

    @property
    def ui_name_T (self) :
        """Localized `ui_name`."""
        ### Must not be a `Once_Property`, because `language` can change
        return _T (self.ui_name)
    # end def ui_name_T

    def __init__ (self, kind, e_type) :
        self.e_type       = e_type
        self.kind         = kind
        self.is_required  = kind.is_required
        if kind.save_to_db and not issubclass (e_type, MOM.An_Entity) :
            et_map        = e_type.app_type.etypes
            DT            = self.DET
            DB            = self.DET_Base
            DR            = self.DET_Root
            self.det_base = et_map [DB] if DB else None
            self.det_root = et_map [DR] if DR else None
            self.det = dt = et_map [DT] if DT else e_type
            self.det_kind = (dt.attr_prop (self.name) or kind) \
                if DT != e_type.type_name else kind
    # end def __init__

    def ac_ui_display (self, value) :
        if self.needs_raw_value :
            result = value
        elif isinstance (value, MOM.Entity) :
            result = value.ui_display
        else :
            try :
                result = self.as_string (value)
            except (TypeError, ValueError) :
                result = value
        return result
    # end def ac_ui_display

    def as_arg_ckd (self) :
        return self.kind.as_arg_ckd (self)
    # end def as_arg_ckd

    def as_arg_raw (self) :
        return self.kind.as_arg_raw (self)
    # end def as_arg_raw

    def as_code (self, value) :
        return self.code_format % (value, )
    # end def as_code

    def as_rest_cargo_ckd (self, obj, * args, ** kw) :
        return self.kind.get_raw_pid (obj)
    # end def as_rest_cargo_ckd

    def as_rest_cargo_raw (self, obj, * args, ** kw) :
        return self.kind.get_raw_pid (obj)
    # end def as_rest_cargo_raw

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return soc.format % (value, )
        return ""
    # end def as_string

    def check_invariant (self, obj, value) :
        errors = obj._pred_man.check_attribute (obj, self, value)
        if len (errors) == 1 :
            raise errors [0]
        elif errors :
            raise MOM.Error.Invariants (errors)
    # end def check_invariant

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if value is not None and soc.P_Type :
            return soc.P_Type (value)
        return value
    # end def cooked

    @TFL.Meta.Class_and_Instance_Once_Property
    def db_sig (self) :
        max_length = getattr (self, "max_length", 0)
        return (self.typ, self.db_sig_version, max_length, self.needs_raw_value)
    # end def db_sig

    def epk_def_set_ckd (self) :
        pass
    # end def epk_def_set_ckd

    def epk_def_set_raw (self) :
        pass
    # end def epk_def_set_raw

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        try :
            if s is not None :
                return self._from_string (s, obj, glob, locl)
        except StandardError as exc :
            if s :
                if isinstance (exc, MOM.Error.Attribute_Syntax) :
                    ### don't wrap Attribute_Syntax inside Attribute_Syntax
                    raise
                raise MOM.Error.Attribute_Syntax (obj, self, s, str (exc))
    # end def from_string

    @TFL.Meta.Class_and_Instance_Method
    def _call_eval (soc, s, ** kw) :
        return TFL.r_eval (s, ** kw)
    # end def _call_eval

    def _checkers (self, e_type, kind) :
        for c in sorted (self.check) :
            yield c
    # end def _checkers

    @TFL.Meta.Class_and_Instance_Method
    def _cls_attr (soc, name) :
        result = getattr (soc, name, None)
        if result is None :
            result = getattr (soc.__class__, name, None)
        return result
    # end def _cls_attr

    def _fix_det (self, kind, e_type) :
        if kind.save_to_db and not issubclass (e_type, MOM.An_Entity) :
            base  = self.det_base or self.det_root
            bdk   = base.attr_prop (self.name)
            b_det = getattr (bdk, "det", None)
            if b_det and self.det_kind.db_sig == bdk.det_kind.db_sig :
                self.det      = b_det
                self.det_kind = b_det.attr_prop (self.name) or bdk
    # end def _fix_det

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, s, obj, glob, locl) :
        return soc.cooked (s)
    # end def _from_string

    def __repr__ (self) :
       return "%s `%s`" % (self.typ, self.name)
    # end def __repr__

    def __str__ (self) :
        return self.name
    # end def __str__

# end class A_Attr_Type

class Atomic_Json_Mixin (TFL.Meta.Object) :
    """Mixin for attribute types that map directly to JSON types"""

    def as_rest_cargo_ckd (self, obj, * args, ** kw) :
        return self.kind.get_value (obj)
    # end def as_rest_cargo_ckd

# end class Atomic_Json_Mixin

class Eval_Mixin (TFL.Meta.Object) :
    """Mixin to use `eval` the raw value to convert the raw value."""

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if value is not None :
            result = TFL.r_eval (value)
            return super (Eval_Mixin, soc).cooked (result)
        return value
    # end def cooked

# end class Eval_Mixin

class Syntax_Re_Mixin (TFL.Meta.Object) :
    """Mixin to check the syntax of a raw value via a regular expression
       `_syntax_re`.
    """

    _syntax_re = None

    def check_syntax (self, obj, value) :
        if value :
            super = self.__super.check_syntax
            if super is not None :
                super (obj, value)
            v = value.strip ()
            if not self._syntax_re.match (v) :
                raise MOM.Error.Attribute_Syntax (obj, self, value)
    # end def check_syntax

# end class Syntax_Re_Mixin

A_Attr_Type.Syntax_Re_Mixin = Syntax_Re_Mixin

class _A_Binary_String_ (A_Attr_Type) :
    """Base type for attributes written to database as binary string."""

    hidden              = True
    max_length          = 0
    P_Type              = bytes

    def as_code (self, value) :
        return repr (value)
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        return value or ""
    # end def as_string

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        return value or ""
    # end def cooked

# end class _A_Binary_String_

class _A_Collection_ (A_Attr_Type) :
    """Base class for attributes that hold a collection of values."""

    C_Type          = None ### Type of entities held by collection
    C_sep           = ","
    R_Type          = None ### Type of collection
    P_Type          = TFL.Meta.Alias_Property ("R_Type")

    needs_raw_value = False

    def __init__ (self, kind, e_type) :
        self.__super.__init__     (kind, e_type)
        self.C_Type = self.C_Type (kind, e_type)
    # end def __init__

    def as_code (self, value) :
        if value is not None :
            return self.__super.as_code \
              (self.C_sep.join (self._C_as_code (value)))
        return ""
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, val) :
        return soc.R_Type (soc.C_Type.cooked (v) for v in val)
    # end def cooked

    @TFL.Meta.Class_and_Instance_Once_Property
    def db_sig (self) :
        return \
            ( self.__super.db_sig
            + (self.C_Type and self.C_Type.db_sig, )
            )
    # end def db_sig

    def _C_as_code (self, value) :
        return (self.C_Type.as_code (v) for v in value)
    # end def _C_as_code

    def _C_split (self, s) :
        if s in ("[]", "") :
            return []
        if s.startswith ("[") and s.endswith ("]") :
            s = s [1:-1]
        elif s.startswith ("(") and s.endswith (")") :
            s = s [1:-1]
        return (x for x in (r.strip () for r in s.split (self.C_sep)) if x)
    # end def _C_split

# end class _A_Collection_

class _A_Entity_ (A_Attr_Type) :
    """Common base class for _A_Composite_ and _A_Id_Entity_"""

    ### Type of composite attribute
    ###     (derived from MOM.An_Entity or MOM.Id_Entity)
    P_Type            = None
    E_Type            = TFL.Meta.Alias_Property ("P_Type")

    needs_raw_value   = False

    def __init__ (self, kind, e_type) :
        P_Type = self.P_Type
        if P_Type :
            tn = P_Type if isinstance (P_Type, pyk.string_types) \
                else P_Type.type_name
            self.P_Type = e_type.app_type.etypes [tn]
        self.__super.__init__ (kind, e_type)
    # end def __init__

    def __getattr__ (self, name) :
        ### to support calls like `scope.PAP.Person.lifetime.start.AQ
        P_Type = self.P_Type
        try :
            return P_Type.attributes [name]
        except LookupError :
            return getattr (P_Type, name)
    # end def __getattr__

# end class _A_Entity_

class _A_Composite_ (_A_Entity_) :
    """Common base class for composite attributes of an object."""

    Kind_Mixins         = (MOM.Attr._Composite_Mixin_, )

    Q_Ckd_Type          = MOM.Attr.Querier.Composite

    @TFL.Meta.Class_and_Instance_Once_Property
    def db_sig (self) :
        return \
            ( self.__super.db_sig
            + (self.P_Type and self.P_Type.db_sig, )
            )
    # end def db_sig

    @TFL.Meta.Class_and_Instance_Once_Property
    def sorted_by (self) :
        return self.P_Type.sorted_by
    # end def sorted_by

    def as_code (self, value) :
        if value is not None :
            return "(%s)" % (value.attr_as_code (), )
        return ""
    # end def as_code

    def as_rest_cargo_ckd (self, obj, * args, ** kw) :
        v = self.kind.get_value (obj)
        if v is not None :
            v_attrs = v.attr_tuple_to_save ()
            return dict ((a.name, a.as_rest_cargo_ckd (v)) for a in v_attrs)
    # end def as_rest_cargo_ckd

    def as_rest_cargo_raw (self, obj, * args, ** kw) :
        v = self.kind.get_value (obj)
        if v is not None :
            v_attrs = v.attr_tuple_to_save ()
            return dict ((a.name, a.as_rest_cargo_raw (v)) for a in v_attrs)
    # end def as_rest_cargo_raw

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return value.as_string ()
        return ""
    # end def as_string

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        P_Type = soc.P_Type
        if isinstance (value, tuple) :
            try :
                value = dict (value)
            except (TypeError, ValueError) :
                value = P_Type.signified (* value)
        if isinstance (value, dict) :
            value = P_Type (** value)
        if value is not None and not isinstance (value, P_Type) :
            raise MOM.Error.Wrong_Type \
                (_T ("Value `%r` is not of type %s") % (value, P_Type))
        return value
    # end def cooked

    def epk_def_set_ckd (self) :
        ### this becomes part of a `classmethod` of the owning `e_type`
        form = \
            ( "if %(name)s is None "
              ": %(name)s = cls.attr_prop ('%(name)s').P_Type ()"
            )
        return self.kind.epk_def_set (form % dict (name = self.name))
    # end def epk_def_set_ckd

    @TFL.Meta.Class_and_Instance_Once_Property
    def example (self) :
        E_Type = self.E_Type
        if E_Type :
            result = E_Type.example_attrs (True)
            if result :
                return result
    # end def example

    @TFL.Meta.Class_and_Instance_Method
    def from_string (soc, s, obj = None, glob = {}, locl = {}) :
        P_Type = soc.P_Type
        t = s or {}
        if isinstance (t, tuple) :
            try :
                t = dict (t)
            except (TypeError, ValueError) :
                t = P_Type.signified (* t)
        t.setdefault ("raw", True)
        return P_Type (** t)
    # end def from_string

    def _checkers (self, e_type, kind) :
        for c in self.__super._checkers (e_type, kind) :
            yield c
        name = self.name
        for k, ps in self.P_Type._Predicates._pred_kind.iteritems () :
            if kind.electric :
                k = kind.kind
                p_kind = MOM.Pred.System
            else :
                p_kind = MOM.Pred.Kind.Table [k]
            if ps :
                p_name = "AC_check_%s_%s" % (name, k)
                check  = MOM.Pred.Condition.__class__ \
                    ( p_name, (MOM.Pred.Condition, )
                    , dict
                        ( assertion  = "%s.is_correct (_kind = %r)" % (name, k)
                        , attributes = (name, )
                        , kind       = p_kind
                        , name       = p_name
                        , __doc__    = " "
                          ### Space necessary to avoid inheritance of `__doc__`
                        )
                    )
                yield check
    # end def _checkers

# end class _A_Composite_

class _A_Date_ (A_Attr_Type) :
    """Common base class for date-valued attributes of an object."""

    needs_raw_value    = False
    _tuple_off         = 0

    @property
    def output_format (self) :
        return self._output_format ()
    # end def output_format

    def as_code (self, value) :
        return self.__super.as_code (self.as_string (value))
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return unicode (value.strftime (soc._output_format ()))
        return ""
    # end def as_string

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, s, obj = None, glob = {}, locl = {}) :
        s = s.strip ()
        if s :
            for f in soc.input_formats :
                try :
                    result = time.strptime (s, f)
                except ValueError :
                    pass
                else :
                    break
            else :
                raise MOM.Error.Attribute_Syntax (obj, soc, s)
            return soc.P_Type (* result [soc._tuple_off:soc._tuple_len])
    # end def _from_string

    @TFL.Meta.Class_and_Instance_Method
    def _output_format (soc) :
        return soc.input_formats [0]
    # end def _output_format

# end class _A_Date_

class _A_Named_Value_ (A_Attr_Type) :
    """Common base class for attributes holding named values."""

    __metaclass__     = MOM.Meta.M_Attr_Type.Named_Value

    C_Type            = None ### Attribute type applicable to cooked values

    needs_raw_value   = False

    def as_code (self, value) :
        return self.code_format % (self.__class__.Elbat [value], )
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        Elbat = soc._cls_attr ("Elbat")
        try :
            return soc.format % (Elbat [value], )
        except KeyError :
            Table = soc._cls_attr ("Table")
            if value in Table :
                return value
            raise
    # end def as_string

    @TFL.Meta.Class_and_Instance_Once_Property
    def Choices (self) :
        return sorted (self.Table)
    # end def Choices

    @TFL.Meta.Class_and_Instance_Method
    def eligible_raw_values (soc, obj = None) :
        return sorted (soc.Table)
    # end def eligible_raw_values

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, s, obj, glob, locl) :
        try :
            return soc.Table [s]
        except KeyError :
            msg = "%s not in %s" % (s, soc.eligible_raw_values ())
            raise MOM.Error.Attribute_Syntax (obj, soc, s, msg)
    # end def _from_string

# end class _A_Named_Value_

class _A_Number_ (A_Attr_Type) :
    """Common base class for number-valued attributes of an object."""

    code_format         = "%s"
    math_dict           = dict \
        ( dict
            (  (k, v) for k, v in math.__dict__.iteritems ()
            if not k.startswith ("_")
            )
        , Decimal = decimal.Decimal
        )

    min_value           = None
    max_value           = None

    _string_fixer       = None

    @TFL.Meta.Class_and_Instance_Once_Property
    def db_sig (self) :
        return self.__super.db_sig + (self.min_value, self.max_value)
    # end def db_sig

    @TFL.Meta.Class_and_Instance_Once_Property
    def example (self) :
        if self.min_value is not None :
            if self.max_value is not None :
                result = self.min_value + (self.max_value - self.min_value) / 2
            else :
                result = self.min_value + 42
        elif self.max_value is not None :
            result = self.max_value - 42
        else :
            result = 42
        return self.as_string (self.cooked (result))
    # end def example

    @TFL.Meta.Class_Property
    @TFL.Meta.Class_and_Instance_Method
    def max_ui_length (self) :
        result = self._max_ui_length
        if result is None :
            mv = max (abs (self.max_value or 0), abs (self.min_value or 0))
            if not mv :
                mv = _A_Int_.max_value_64
            result = self._max_ui_length = \
                int (math.ceil (math.log (mv, 10)) + 1)
        return result
    # end def max_ui_length

    @TFL.Meta.Class_and_Instance_Once_Property
    def ui_length (self) :
        mv = max (abs (self.max_value or 0), abs (self.min_value or 0))
        if not mv :
            mv = _A_Int_.max_value_32
        return int (math.ceil (math.log (mv, 10) + 1))
    # end def ui_length

    def _checkers (self, e_type, kind) :
        if self.min_value is not None :
            if self.max_value is not None :
                yield "%s <= value <= %s" % (self.min_value, self.max_value)
            else :
                yield "%s <= value" % (self.min_value, )
        elif self.max_value :
            yield "value <= %s" % (self.max_value, )
        for c in self.__super._checkers (e_type, kind) :
            yield c
    # end def _checkers

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, value, obj, glob, locl) :
        if value :
            try :
                return soc.P_Type (value)
            except (ValueError, TypeError) as exc :
                val = soc._string_fixer (value) if soc._string_fixer else value
                try :
                    return soc._call_eval (val, ** soc.math_dict)
                except (NameError, ValueError, TypeError, SyntaxError) :
                    raise MOM.Error.Attribute_Syntax (obj, soc, value)
    # end def _from_string

# end class _A_Number_

class _A_Decimal_ (_A_Number_) :
    """Decimal-number valued attribute of an object."""

    typ               = _ ("Decimal")
    P_Type            = decimal.Decimal
    code_format       = "%s"
    decimal_places    = 2
    max_digits        = 12

    _string_fixer     = Re_Replacer \
        ( r"([-+]?\d*\.\d+([eE][-+]?\d+)?)"
        , r"""Decimal("\1")"""
        )

    @TFL.Meta.Class_and_Instance_Once_Property
    def db_sig (self) :
        return self.__super.db_sig + (self.decimal_places, self.max_digits)
    # end def db_sig

    @TFL.Meta.Class_Property
    @TFL.Meta.Class_and_Instance_Method
    def max_ui_length (self) :
        result = self._max_ui_length
        if result is None :
            max_digits = self.max_digits
            if max_digits :
                self._max_ui_length = result = max_digits + 2
            else :
                result = super (_A_Decimal_, self).max_ui_length
        return result
    # end def max_ui_length

# end class _A_Decimal_

class _A_Float_ (Atomic_Json_Mixin, _A_Number_) :
    """Floating-point attribute."""

    typ               = _ ("Float")
    P_Type            = float
    max_ui_length     = 22

# end class _A_Float_

class _A_Int_ (Atomic_Json_Mixin, _A_Number_) :
    """Integer attribute."""

    typ               = _ ("Int")
    P_Type            = int

    max_value_8       = +0x7F
    max_value_16      = +0x7FFF
    max_value_32      = +0x7FFFFFFF
    max_value_64      = +0x7FFFFFFFFFFFFFFF
    min_value_8       = -0x80
    min_value_16      = -0x8000
    min_value_32      = -0x80000000
    min_value_64      = -0x8000000000000000

# end class _A_Int_

class _A_Link_Role_Left_ (A_Attr_Type) :
    """Left role of a link."""

    generic_role_name = "left"
    rank              = 0
    role_abbreviation = "l"
    typ               = _ ("Left")

# end class _A_Link_Role_Left_

class _A_Link_Role_L_Middle_ (A_Attr_Type) :
    """Left-middle role of a link."""

    generic_role_name = "l_middle"
    rank              = 1
    role_abbreviation = "lm"
    typ               = _ ("L_Middle")

# end class _A_Link_Role_L_Middle_

class _A_Link_Role_Middle_ (A_Attr_Type) :
    """Middle role of a link."""

    generic_role_name = "middle"
    rank              = 2
    role_abbreviation = "m"
    typ               = _ ("Middle")

# end class _A_Link_Role_Middle_

class _A_Link_Role_R_Middle_ (A_Attr_Type) :
    """Right-middle role of a link."""

    generic_role_name = "r_middle"
    rank              = 3
    role_abbreviation = "rm"
    typ               = _ ("R_Middle")

# end class _A_Link_Role_R_Middle_

class _A_Link_Role_Right_ (A_Attr_Type) :
    """Right role of a link."""

    generic_role_name = "right"
    rank              = 4
    role_abbreviation = "r"
    typ               = _ ("Right")

# end class _A_Link_Role_Right_

class _A_SPK_Entity_ (_A_Entity_) :
    """Attribute referring to an entity identified by a spk"""

    rev_ref_attr_name   = None
    rev_ref_singular    = False

    def as_code (self, value) :
        if value is not None :
            return tuple \
                (a.as_code (a.get_value (value)) for a in value.primary)
        return repr ("")
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return soc.format % \
                ( tuple
                    (a.as_string (a.get_value (value)) for a in value.primary)
                ,
                )
        return ""
    # end def as_string

    def check_type (self, value) :
        E_Type = self.E_Type
        if not isinstance (value, E_Type.Essence) :
            typ       = _T (getattr (value, "ui_name", value.__class__))
            v_display = getattr (value, "ui_display", unicode (value))
            raise MOM.Error.Wrong_Type \
                ( _T
                    ( "%s '%s' not eligible for attribute %s,"
                      "\n"
                      "    must be instance of %s"
                    )
                % (typ, v_display, self.name, _T (E_Type.ui_name))
                )
        tn = value.type_name
        if tn in self.refuse_e_types_transitive :
            typ = _T (value.E_Type.ui_name)
            raise MOM.Error.Wrong_Type \
                ( _T
                    ( "%s '%s' not eligible for attribute %s,"
                      "\n"
                      "    must be instance of %s, but not %s"
                    )
                % (typ, value.ui_display, self.name, _T (E_Type.ui_name), typ)
                )
        return value
    # end def check_type

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        return value
    # end def cooked

    @TFL.Meta.Class_and_Instance_Method
    def etype_manager (soc, obj = None) :
        if soc.P_Type :
            return getattr (soc._get_scope (obj), soc.P_Type.type_name, None)
    # end def etype_manager

    @TFL.Meta.Class_and_Instance_Method
    def _get_scope (soc, obj) :
        return obj.home_scope if obj else MOM.Scope.active
    # end def _get_scope

# end class _A_SPK_Entity_

class _A_Id_Entity_ (_A_SPK_Entity_) :
    """Attribute referring to an entity."""

    _sets_to_combine    = \
        _A_Entity_._sets_to_combine + ("allow_e_types", "refuse_e_types")

    Q_Ckd_Type          = MOM.Attr.Querier.Id_Entity

    is_link_role        = False

    allow_e_types       = set ()
    refuse_e_types      = set ()

    ### allow creation of new entity for this attribute
    ui_allow_new        = True

    def __init__ (self, kind, e_type) :
        self.__super.__init__ (kind, e_type)
        ### copy from class to instance
        self.allow_e_types  = set (self.allow_e_types)
        self.refuse_e_types = set (self.refuse_e_types)
    # end def __init__

    @TFL.Meta.Once_Property
    def allow_e_types_transitive (self) :
        return set (self._gen_etypes_transitive (self.allow_e_types))
    # end def allow_e_types_transitive

    @TFL.Meta.Once_Property
    def eligible_e_types (self) :
        """Set of eligible e_types that this attribute can refer to"""
        return \
            ( set (self.E_Type.children_np_transitive)
            - self.refuse_e_types_transitive
            )
    # end def eligible_e_types

    @property
    def example (self) :
        etm = self.etype_manager ()
        if etm and etm.is_partial :
            etm = etm.default_child
        if etm :
            try :
                result = etm.example ()
            except Exception as exc :
                if __debug__ :
                    logging.exception \
                        ("\n    %s [%s] .example", self, self.E_Type)
            else :
                return result
        else :
            raise MOM.Error.Partial_Type \
                ( "Partial E_Type %s needs a default child"
                % self.E_Type.type_name
                )
    # end def example

    @TFL.Meta.Once_Property
    def refuse_e_types_transitive (self) :
        return \
            ( set (self._gen_etypes_transitive (self.refuse_e_types))
            - self.allow_e_types_transitive
            )
    # end def refuse_e_types_transitive

    @TFL.Meta.Once_Property
    def selectable_e_types_unique_epk (self) :
        """Set of eligible partial or non-partial e-types with unique epk"""
        def _gen (ET) :
            if ET.polymorphic_epk :
                for c in ET.children.itervalues () :
                    for x in _gen (c) :
                        yield x
            else :
                yield ET.type_name
        return set (_gen (self.E_Type)) - self.refuse_e_types_transitive
    # end def selectable_e_types_unique_epk

    @TFL.Meta.Class_and_Instance_Once_Property
    def sorted_by (self) :
        return self.P_Type.sorted_by_epk
    # end def sorted_by

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        if isinstance (s, MOM.Entity) :
            return s ### `check_type` called by `kind._set_cooked_value`
        elif isinstance (s, pyk.int_types) :
            scope = self._get_scope (obj)
            return scope.pid_query (s)
        elif s :
            assert self.P_Type, "%s needs to define `P_Type`" % self
            if isinstance (s, tuple) :
                t = s
            else :
                try :
                    t = self._call_eval (s)
                except (NameError, SyntaxError) :
                    t = (s, )
            return self._get_object  (obj, t, raw = True)
    # end def from_string

    def _gen_etypes_transitive (self, e_types) :
        apt = self.e_type.app_type
        for ret in e_types :
            ET = apt.etypes.get (ret)
            if ET :
                for c in ET.children_np_transitive :
                    yield c
    # end def _gen_etypes_transitive

    def _get_object (self, obj, epk, raw = False) :
        if epk and isinstance (epk [-1], self.P_Type.Type_Name_Type) :
            tn = epk [-1]
        else :
            tn = self.P_Type.type_name
        scope  = self._get_scope (obj)
        etm    = scope [tn]
        result = etm.instance (* epk, raw = raw)
        if result is not None :
            return self.cooked  (result)
        else :
            raise MOM.Error.No_Such_Entity \
                (  _T ("No object of type %s with epk %s in scope %s")
                % (tn, epk, scope.name)
                )
    # end def _get_object

# end class _A_Id_Entity_

class _A_MD_Change_ (_A_SPK_Entity_) :
    """Attribute referring to a MD_Change instance"""

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        if isinstance (s, MOM.Entity) :
            return s ### `check_type` called by `kind._set_cooked_value`
        elif isinstance (s, pyk.int_types) :
            scope = self._get_scope (obj)
            return scope.MOM.MD_Change.query (Q.cid == s).first ()
        elif s :
            raise ValueError (s)
    # end def from_string

# end class _A_MD_Change_

class _A_Rev_Ref_ (A_Attr_Type) :

    ### need to recompute each time value is accessed ### ???
    kind                = MOM.Attr._Rev_Query_
    Kind_Mixins         = (MOM.Attr.Computed, )

    ### set by meta machinery
    P_Type              = None
    E_Type              = TFL.Meta.Alias_Property ("P_Type")
    Ref_Type            = None
    ref_name            = None
    sort_key            = None
    sqx_filter          = None

    electric            = True
    hidden              = True

    def __init__ (self, kind, e_type) :
        for k in ("P_Type", "Ref_Type") :
            T = getattr (self, k, None)
            if T :
                tn = T if isinstance (T, pyk.string_types) else T.type_name
                setattr (self, k, e_type.app_type.etypes [tn])
        self.__super.__init__ (kind, e_type)
    # end def __init__

    @TFL.Meta.Once_Property
    def ref_filter (self) :
      return getattr (Q, self.ref_name)
    # end def ref_filter

    def finished_query_all (self, q) :
        return q.all ()
    # end def finished_query_all

    def finished_query_first (self, q) :
        try :
            return q.first ()
        except IndexError :
            pass
    # end def finished_query_first

    def finished_query_one (self, q) :
        try :
            return q.one ()
        except IndexError :
            pass
    # end def finished_query_one

    def query (self, obj, sort_key = None) :
        result = self.query_x (obj, sort_key)
        return self.finished_query (result)
    # end def query

    def query_x (self, obj, sort_key = None) :
        sq = self.sqx (obj, sort_key)
        return sq.apply (obj.home_scope)
    # end def query_x

    def sqx (self, obj, sort_key = None) :
        if sort_key is None :
            sort_key = self.sort_key
        result = SQ [self.Ref_Type].filter \
            (self.ref_filter == obj, sort_key = sort_key)
        if self.sqx_filter is not None :
            result = result.filter (self.sqx_filter)
        return result
    # end def sqx

# end class _A_Rev_Ref_

class _A_String_Base_ (A_Attr_Type) :
    """Base class for string-valued attributes of an object."""

    default           = ""
    example           = "foo"
    max_length        = 0
    Q_Ckd_Type        = MOM.Attr.Querier.String
    ui_length         = TFL.Meta.Class_and_Instance_Once_Property \
        (lambda s : s.max_length or 120)

    @TFL.Meta.Once_Property
    def AQ (self) :
        return self.Q_Ckd
    # end def AQ

    def _checkers (self, e_type, kind) :
        for c in self.__super._checkers (e_type, kind) :
            yield c
        if self.max_length :
            name   = self.name
            p_kind = [MOM.Pred.Object, MOM.Pred.System] [kind.electric]
            p_name = "AC_check_%s_length" % (name, )
            check = MOM.Pred.Condition.__class__ \
                ( p_name, (MOM.Pred.Condition, )
                , dict
                    ( assertion  = "length <= %s" % (self.max_length, )
                    , attributes = (name, )
                    , bindings   = dict
                        ( length = "len (%s)" % (name, )
                        )
                    , kind       = p_kind
                    , name       = p_name
                    , __doc__    = "Value for %s must not be longer than %s"
                      % (name, self.max_length)
                    )
                )
            yield check
    # end def _checkers

# end class _A_String_Base_

class _A_Filename_ (_A_String_Base_) :
    """Base class for attributes holding filenames."""

    needs_raw_value   = False
    P_Type            = str

    open_mode         = "w"
    """`open_mode` defines the mode to use for opening the file specified
       by the value of the attribute.
       """

    do_check         = True
    """`do_check` specifies whether the existence of a file as specified by
       the attribute's value is checked by `from_string`.
       """

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, s) :
        if s :
            return TFL.I18N.encode_f (s)
    # end def cooked

    def _check_dir (self, d) :
        if not sos.path.isdir (d) :
            raise MOM.Error.No_Such_Directory (d)
    # end def _check_dir

    def _check_read (self, s) :
        if "r" in self.open_mode and not sos.path.isfile (s):
            raise MOM.Error.No_Such_File (s)
    # end def _check_read

    def _check_open (self, s, mode) :
        if "w" in self.open_mode or "a" in self.open_mode :
            exists = sos.path.isfile (s)
            file   = open (s, mode)
            file.close ()
            if not exists :
                sos.remove (s)
    # end def _check_open

    def _check_write (self, s) :
        if self.do_check :
            self._check_open (s, self.open_mode)
    # end def _check_write

# end class _A_Filename_

class _A_String_ (Atomic_Json_Mixin, _A_String_Base_) :
    """Base class for string-valued attributes of an object."""

    __metaclass__     = MOM.Meta.M_Attr_Type.String

    ignore_case       = False
    needs_raw_value   = False
    P_Type            = unicode

    @TFL.Meta.Class_and_Instance_Once_Property
    def db_sig (self) :
        return self.__super.db_sig + (self.ignore_case, )
    # end def db_sig

# end class _A_String_

class _A_String_Ascii_ (_A_String_) :
    """Base class for ascii-string-valued attributes of an object."""

    P_Type            = str
    _cooked_re        = Regexp \
        ( "^[\x00-\x7F]*$"
        , re.VERBOSE
        )

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if value is not None :
            value = super (_A_String_Ascii_, soc).cooked (value)
            if not self._cooked_re.match (value) :
                raise MOM.Error.Attribute_Syntax (obj, soc, value)
        return value
    # end def cooked

# end class _A_String_Ascii_

class _A_Named_Object_ (_A_Named_Value_) :
    """Common base class for attributes holding named objects (that cannot be
       directly put into a database).
    """

    __metaclass__     = MOM.Meta.M_Attr_Type.Named_Object

    class Pickler (TFL.Meta.Object) :

        Type = _A_String_

        @classmethod
        def as_cargo (cls, attr_kind, attr_type, value) :
            if value is not None :
                return attr_type.as_string (value)
        # end def as_cargo

        @classmethod
        def from_cargo (cls, scope, attr_kind, attr_type, cargo) :
            if cargo is not None :
                Table = attr_type.__class__.Table
                try :
                    return Table [cargo]
                except KeyError :
                    raise ValueError ("%s not in %s" % (cargo, sorted (Table)))
        # end def from_cargo

    # end class Pickler

    @TFL.Meta.Class_and_Instance_Once_Property
    def Choices (self) :
        return sorted \
            ( ((k, str (v)) for k, v in self.Table.iteritems ())
            , key = TFL.Getter [1]
            )
    # end def Choices

# end class _A_Named_Object_

class _A_Typed_Collection_ (_A_Collection_) :
    """Base class for attributes that hold a collection of strictly typed
       values.
    """

    __metaclass__     = MOM.Meta.M_Attr_Type.Typed_Collection
    Kind_Mixins       = (MOM.Attr._Typed_Collection_Mixin_, )

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        ### when called for the class, `soc.__super` doesn't
        ### work while `super (_A_Typed_Collection_, soc)` does
        if value is not None :
            return super (_A_Typed_Collection_, soc).as_string \
                (soc.C_sep.join (soc._C_as_string (value)))
        return ""
    # end def as_string

    def from_string (self, s, obj = None, glob = {}, locl = {}) :
        result = None
        t      = s or []
        if isinstance (t, pyk.string_types) :
            result = self._from_string (s, obj, glob, locl)
        elif t :
            C_fs   = self.C_Type.from_string
            result = self.R_Type (C_fs (c, obj, glob, locl) for c in t)
        return result
    # end def from_string

    @TFL.Meta.Class_and_Instance_Once_Property
    def ui_length (self) :
        return (self.C_Type.ui_length + 2) * 5
    # end def ui_length

    def _checkers (self, e_type, kind) :
        C_Type = self.C_Type
        if C_Type :
            if __debug__ :
                if isinstance (C_Type, _A_Composite_) :
                    raise TypeError \
                        ( "Collection %s of composite %s must be modelled "
                          "as Link1"
                        % (self, C_Type)
                        )
            pass ### XXX Predicate checking each component for `C_Type._checkers`
        return ()
    # end def _checkers

    @TFL.Meta.Class_and_Instance_Method
    def _C_as_string (soc, value) :
        return (soc.C_Type.as_string (v) for v in value)
    # end def _C_as_string

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, s, obj, glob, locl) :
        C_fs  = soc.C_Type._from_string
        comps = soc._C_split (s.strip ())
        return soc.R_Type (C_fs (c, obj, glob, locl) for c in comps)
    # end def _from_string

# end class _A_Typed_Collection_

class _A_Typed_List_ (_A_Typed_Collection_) :
    """Base class for list-valued attributes with strict type."""

    R_Type         = list

# end class _A_Typed_List_

class _A_Typed_Set_ (_A_Typed_Collection_) :
    """Base class for set-valued attributes with strict type."""

    R_Type         = set

# end class _A_Typed_Set_

class _A_Typed_Tuple_ (_A_Typed_Collection_) :
    """Base class for tuple-valued attributes with strict type."""

    R_Type         = tuple

# end class _A_Typed_Tuple_

class _A_Id_Entity_Collection_ (_A_Typed_Collection_) :

    C_Type         = _A_Id_Entity_

    def _C_as_code (self, value) :
        sk = MOM.Scope.active.MOM.Id_Entity.sort_key
        return self.__super._C_as_code (sorted (value, key = sk))
    # end def _C_as_code

    def _C_as_string (self, value) :
        sk = MOM.Scope.active.MOM.Id_Entity.sort_key
        return self.__super._C_as_string (sorted (value, key = sk))
    # end def _C_as_string

# end class _A_Id_Entity_Collection_

class _A_Id_Entity_List_ (_A_Typed_List_, _A_Id_Entity_Collection_) :

    pass

# end class _A_Id_Entity_List_

class _A_Id_Entity_Set_ (_A_Typed_Set_, _A_Id_Entity_Collection_) :

    pass

# end class _A_Id_Entity_Set_

class _A_Unit_ (A_Attr_Type) :
    """Mixin for attributes describing physical quantities with optional
       units.
    """

    __metaclass__  = MOM.Meta.M_Attr_Type.Unit
    _default_unit  = None ### set by meta class
    _unit_dict     = {}
    _unit_pattern  = Regexp \
        ( r"(?: ^"
        + plain_number_pat
        + r"|"
              r"[])a-zA-Z_0-9] \s+" ### expression followed by whitespace(s)
          r")"
          r"(?P<unit> [a-zA-Z]+ (?: / [a-zA-Z]+)?)"
          r"\s*"
          r"$"
        , re.VERBOSE
        )

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        ### beware: `as_string` can be used as class method, too;
        ### when called for the class, `soc.__super` doesn't
        ### work while `super (_A_Unit_, soc)` does
        if value is not None :
            return "%s %s" % \
               (super (_A_Unit_, soc).as_string (value), soc._default_unit)
        return ""
    # end def as_string

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        val = soc.from_string (value) \
            if isinstance (value, pyk.string_types) else value
        return super (_A_Unit_, soc).cooked (val)
    # end def cooked

    @TFL.Meta.Class_and_Instance_Method
    def eligible_raw_values (soc, obj = None) :
        return sorted (soc._unit_dict.iterkeys ())
    # end def eligible_raw_values

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, s, obj, glob, locl) :
        factor = 1
        pat    = soc._unit_pattern
        if pat.search (s) :
            unit = pat.unit
            s    = s [: pat.start ("unit")]
            try :
                factor = soc._unit_dict [unit]
            except KeyError :
                msg = \
                    ( _T ("Invalid unit %s, specify one of %s")
                    % (unit, soc.eligible_raw_values ())
                    )
                raise MOM.Error.Attribute_Syntax (obj, soc, s, msg)
        return super (_A_Unit_, soc)._from_string (s, obj, glob, locl) * factor
    # end def _from_string

# end class _A_Unit_

class A_Angle (_A_Float_) :
    """Angle in degrees."""

    typ              = _ ("Angle")
    max_value        = 360
    min_value        = 0
    needs_raw_value  = True

    _dms_pattern     = Regexp \
        ( r"^\s*"
          r"(?P<sign> [-+])?"
          r"(?:(?P<degrees> \d+) \s* d \s*)?"
          r"(?:(?P<minutes> \d+) \s* m \s*)?"
          r"(?:(?P<seconds> " + plain_number_pat + ") \s* s \s*)?"
          r"$"
        , re.VERBOSE
        )

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if value is not None :
            value = super (A_Angle, soc).cooked (value)
            if soc.max_value == value == 360 and soc.min_value <= 0 :
                value -= 360
        return value
    # end def cooked

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, value, obj, glob, locl) :
        if value is not None :
            pat = soc._dms_pattern
            if soc._dms_pattern.search (value) :
                result = \
                    ( (float (pat.degrees or 0.))
                    + (float (pat.minutes or 0.)) /   60.
                    + (float (pat.seconds or 0.)) / 3600.
                    )
                if pat.sign == '-' :
                    result = -result
            else :
                result = super (A_Angle, soc)._from_string \
                    (value, obj, glob, locl)
        return soc.cooked (result)
    # end def _from_string

# end class A_Angle

class A_Binary_String_P (_A_Binary_String_) :
    """Binary attribute that is written to the database as a pickle."""

    typ                 = _ ("Binary_Pickled")

# end class A_Binary_String_P

class A_Blob (A_Attr_Type) :
    """Generic type for binary attributes that aren't set by the user."""

    typ                 = _ ("Blob")
    kind                = MOM.Attr._Cached_
    hidden              = True

# end class A_Blob

class A_Boolean (Atomic_Json_Mixin, _A_Named_Value_) :
    """Boolean attribute."""

    example           = "no"
    typ               = _ ("Boolean")
    Q_Ckd_Type        = MOM.Attr.Querier.Boolean
    P_Type            = bool
    ui_length         = 5

    Table             = dict \
        ( no          = False
        , yes         = True
        )

    ### allow additional raw values without changing `eligible_raw_values`
    ### (want only canonical values in UI and documentation)
    Table_X           = dict \
        ( Table
        , false       = False
        , true        = True
        )

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if isinstance (value, pyk.string_types) :
            try :
                return soc.Table_X [value.lower ()]
            except KeyError :
                msg = "%s not in %s" % (value, sorted (soc.Table))
                raise MOM.Error.Attribute_Syntax (None, soc, value, msg)
        else :
            return soc.P_Type (value)
    # end def cooked

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, s, obj, glob, locl) :
        return soc.cooked (s)
    # end def _from_string

# end class A_Boolean

class A_Cached_Role (_A_Id_Entity_) :
    """Attribute referring to an object linked via an association.
    """

    electric       = True
    kind           = MOM.Attr.Cached_Role
    typ            = _ ("Cached_Role")
    hidden         = True

# end class A_Cached_Role

class A_Cached_Role_DFC (A_Cached_Role) :
    """Attribute referring to an object linked via an association or derived
       from a container.
    """

    kind           = MOM.Attr.Cached_Role_DFC

# end class A_Cached_Role_DFC

class A_Cached_Role_Set (_A_Id_Entity_Set_) :
    """Attribute referring to a set of objects linked via an association.
    """

    electric       = True
    kind           = MOM.Attr.Cached_Role_Set
    typ            = _ ("Cached_Role_Set")
    hidden         = True

    def __init__ (self, kind, e_type) :
        for k in ("P_Type", ) :
            T = getattr (self, k, None)
            if T :
                tn = T if isinstance (T, pyk.string_types) else T.type_name
                setattr (self, k, e_type.app_type.etypes [tn])
        self.__super.__init__ (kind, e_type)
    # end def __init__

# end class A_Cached_Role_Set

class A_Char (_A_String_) :
    """A single character."""

    example        = "X"
    typ            = _ ("Character")
    max_length     = 1

# end class A_Char

class A_Date (_A_Date_) :
    """Date value."""

    example        = "2010/10/10"
    completer      = MOM.Attr.Completer_Spec  (4)
    typ            = _ ("Date")
    P_Type         = datetime.date
    Q_Ckd_Type     = MOM.Attr.Querier.Date
    ui_length      = 12
    input_formats  = \
        ( "%Y/%m/%d", "%Y%m%d", "%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y")
    _tuple_len     = 3

    def as_rest_cargo_ckd (self, obj, * args, ** kw) :
        value = self.kind.get_value (obj)
        if value is not None :
            return unicode (value.strftime ("%Y-%m-%d"))
    # end def as_rest_cargo_ckd

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if isinstance (value, datetime.datetime) :
            value = value.date ()
        elif isinstance (value, pyk.string_types) :
            try :
                value = soc._from_string (value)
            except ValueError :
                msg = "Date expected, got %r" % (value, )
                raise MOM.Error.Attribute_Syntax (None, soc, value, msg)
        elif not isinstance (value, datetime.date) :
            raise TypeError ("Date expected, got %r" % (value, ))
        return value
    # end def cooked

    @classmethod
    def now (cls) :
        return datetime.datetime.now ().date ()
    # end def now

# end class A_Date

class A_Date_List (_A_Typed_List_) :
    """List of dates."""

    typ            = _ ("Date_List")
    C_Type         = A_Date

# end class A_Date_List

class A_Date_Slug (_A_String_) :
    """Unique value based on the date/time of entity creation.
    """

    example        = "20101010_000042_137"
    typ            = _ ("Date-Slug")
    ui_length      = 22
    max_length     = 32

    def computed_default (self) :
        now    = datetime.datetime.utcnow ()
        now   += TFL.user_config.time_zone.utcoffset (now)
        result = "%s_%06d_%s" % \
            ( now.strftime ("%Y%m%d_%H%M%S")
            , now.microsecond
            , sos.getpid ()
            )
        return result
    # end def computed_default

# end class A_Date_Slug

class A_Date_Time (_A_Date_) :
    """Date-time value."""

    example        = "2010/10/10 06:42"
    typ            = _ ("Date-Time")
    P_Type         = datetime.datetime
    ui_length      = 22
    input_formats  = tuple \
        ( itertools.chain
            ( * (  (f + " %H:%M:%S", f + " %H:%M", f)
                for f in A_Date.input_formats
                )
            )
        )
    _tuple_len     = 6

    def as_rest_cargo_ckd (self, obj, * args, ** kw) :
        value = self.kind.get_value (obj)
        if value is not None :
            if not value.time () :
                return unicode (value.strftime ("%Y-%m-%d"))
            else :
                v = value + TFL.user_config.time_zone.utcoffset (value)
                return v.strftime ("%Y-%m-%d %H:%M")
    # end def as_rest_cargo_ckd

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            if not value.time () :
                return value.strftime (A_Date.input_formats [0])
            else :
                v = value + TFL.user_config.time_zone.utcoffset (value)
                return v.strftime (soc._output_format ())
        return ""
    # end def as_string

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if not isinstance (value, datetime.datetime) :
            if isinstance (value, datetime.date) :
                value = datetime.datetime (value.year, value.month, value.day)
            elif isinstance (value, pyk.string_types) :
                try :
                    value = soc._from_string (value)
                except ValueError :
                    raise TypeError \
                        (_T ("Date/time expected, got %r") % (value, ))
            else :
                raise TypeError (_T ("Date/time expected, got %r") % (value, ))
        return value
    # end def cooked

    @classmethod
    def now (cls) :
        return datetime.datetime.utcnow ()
    # end def now

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, s, obj = None, glob = {}, locl = {}) :
        result = super (A_Date_Time, soc)._from_string (s, obj, glob, locl)
        result -= TFL.user_config.time_zone.utcoffset (result)
        return result
    # end def _from_string

# end class A_Date_Time

class A_Date_Time_List (_A_Typed_List_) :
    """List of date/time elements."""

    typ            = _ ("Date_Time_List")
    C_Type         = A_Date_Time

# end class A_Date_Time_List

class A_Decimal (_A_Decimal_) :
    """Decimal number."""

    __metaclass__  = MOM.Meta.M_Attr_Type.Decimal

    rounding       = decimal.ROUND_HALF_UP

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        D = soc.P_Type
        if not isinstance (value, D) :
            if isinstance (value, float) :
                value = str (value)
            value = D (value, soc.D_Context)
        return value.quantize (soc.D_Quant)
    # end def cooked

    @TFL.Meta.Class_and_Instance_Once_Property
    def db_sig (self) :
        return self.__super.db_sig + (self.decimal_places, self.max_digits)
    # end def db_sig

# end class A_Decimal

class A_Dirname (_A_Filename_) :
    """Directory in the file system."""

    typ         = _ ("Directory")

    def _from_string (self, s, obj, glob, locl) :
        s = self.__super._from_string (s, obj, glob, locl)
        if s :
            if sos.altsep :
                s = s.replace (sos.altsep, sos.sep)
            if not s.endswith (sos.sep) :
                s += sos.sep
            if self.do_check :
                self._check_dir   (s)
                self._check_write (s + ".ignore")
        return sos.path.normpath (s)
    # end def _from_string

# end class A_Dirname

class A_Email (Syntax_Re_Mixin, _A_String_) :
    """An email address"""

    typ                = _ ("Email")
    example            = "foo@bar.baz"
    max_length         = 80
    _syntax_re         = Regexp \
        ( r"^[-_#=!?$&'+*/^~a-z0-9.]+"
          r"@"
          r"[-a-z0-9.]+$"
        , re.IGNORECASE | re.VERBOSE
        )

# end class A_Email

class A_Enum (A_Attr_Type) :
    """Base class for enumeration attributes. An enumeration is defined by a
       `Table` mapping the keys (used as raw and cooked values) to their
       description.
    """

    __metaclass__     = MOM.Meta.M_Attr_Type.Enum

    C_Type            = None ### Attribute type applicable to cooked values
    needs_raw_value   = False

    @property
    def Choices (self) :
        ### cannot cache this because of L10N
        ### XXX cache by language
        return sorted \
            ((k, "%s [%s]" % (k, _T (v))) for k, v in self.Table .iteritems ())
    # end def Choices

    def as_code (self, value) :
        if value is not None :
            return self.C_Type.code_format % (value, )
        return "''"
    # end def as_code

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if value == "" :
            result = None
        else :
            Table = soc.Table
            try :
                result = soc.C_Type.cooked (value)
            except Exception as exc :
                msg = \
                    ( "Invalid value for %s, got %s %r, expected one of %s"
                    % (soc, type (value), value, sorted (Table))
                    )
                raise MOM.Error.Attribute_Syntax (None, soc, s, msg)
            if not result in Table :
                msg = ("%s not in %s" % (result, sorted (Table)))
                raise MOM.Error.Attribute_Syntax (None, soc, s, msg)
        return result
    # end def cooked

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, s, obj, glob, locl) :
        if s :
            Table  = soc.Table
            result = soc.cooked (soc.C_Type._from_string (s, obj, glob, locl))
            if result in Table :
                return result
            else :
                msg = ("%s not in %s" % (s, sorted (Table)))
                raise MOM.Error.Attribute_Syntax (obj, soc, s, msg)
    # end def _from_string

# end class A_Enum

class A_Euro_Amount (_A_Decimal_) :
    """Amount in Euro."""

    typ              = _ ("Decimal")
    P_Type           = TFL.Currency

    _string_cleaner  = Re_Replacer \
        ( r"\s*(%s|%s)\s*" % (TFL.Currency._symbol, TFL.Currency.name)
        , r""
        )

    class Pickler (TFL.Meta.Object) :

        Type = _A_String_

        @classmethod
        def as_cargo (cls, attr_kind, attr_type, value) :
            if value is not None :
                return value.amount
        # end def as_cargo

        @classmethod
        def from_cargo (cls, scope, attr_kind, attr_type, cargo) :
            if cargo is not None :
                return attr_type.P_Type (cargo)
        # end def from_cargo

    # end class Pickler

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, value, obj, glob, locl) :
        ### when called for the class, `soc.__super` doesn't
        ### work while `super (A_Euro_Amount, soc)` does
        if value :
            return super (A_Euro_Amount, soc)._from_string \
                (soc._string_cleaner (value), obj, glob, locl)
    # end def _from_string

# end class A_Euro_Amount

class A_Filename (_A_Filename_) :
    """Name of file in the file system."""

    typ         = _ ("Filename")

    def _from_string (self, s, obj, glob, locl) :
        s = self.__super._from_string (s, obj, glob, locl)
        if s and self.do_check :
            self._check_dir   (sos.path.dirname (s))
            self._check_read  (s)
            self._check_write (s)
        return sos.path.normpath (s)
    # end def _from_string

# end class A_Filename

class A_Float (_A_Float_) :
    code_format    = "%s"
# end class A_Float

class A_Frequency (_A_Unit_, _A_Float_) :
    """Frequency with unit information (e.g. 2.437 GHz)."""

    typ              = _ ("Frequency")
    completer        = MOM.Attr.Completer_Spec  (2)
    needs_raw_value  = True
    _unit_dict       = dict \
        ( Hz         = 1
        , kHz        = 1.E3
        , MHz        = 1.E6
        , GHz        = 1.E9
        , THz        = 1.E12
        )

# end class A_Frequency

class A_Int (_A_Int_) :
    pass
# end class A_Int

class A_Int_List (_A_Typed_List_) :
    """List of integer elements."""

    typ            = _ ("Int_List")
    C_Type         = A_Int

# end class A_Int_List

class A_Length (_A_Unit_, _A_Float_) :
    """Length with unit information."""

    typ            = _ ("Length")
    _unit_dict     = dict \
        ( { "in"   : 0.0254 }
        , cm       = 1.e-2
        , ft       = 0.3048000
        , km       = 1.e3
        , m        = 1.0
        , mi       = 1609.344
        , mm       = 1.e-3
        , Nm       = 1852.0
        , nm       = 1.e-9
        , um       = 1.e-6
        , yd       = 0.9144000
        )

# end class A_Length

class _A_Link_Ref_ (_A_Rev_Ref_) :

    role_filter         = TFL.Meta.Alias_Property ("ref_filter")
    role_name           = TFL.Meta.Alias_Property ("ref_name")

# end class _A_Link_Ref_

class A_Link_Ref (_A_Link_Ref_, _A_Id_Entity_) :
    """Reverse reference to link referring to an `entity`"""

    typ                 = _ ("Link_Ref")
    q_able              = True

    finished_query      = _A_Link_Ref_.finished_query_one

# end class A_Link_Ref

class A_Link_Ref_List (_A_Link_Ref_, _A_Id_Entity_List_) :
    """Reverse reference to set of links referring to an `entity`."""

    typ                 = _ ("Link_Ref_List")

    finished_query      = _A_Link_Ref_.finished_query_all

# end class A_Link_Ref_List

class A_Link_Role (_A_Id_Entity_) :
    """Link-role."""

    __metaclass__       = MOM.Meta.M_Attr_Type.Link_Role

    auto_rev_ref        = False
    auto_rev_ref_np     = False
    auto_derive_np      = False
    auto_derive_npt     = False
    Cacher_Type         = None
    dfc_synthesizer     = None
    force_role_name     = None
    is_link_role        = True
    link_ref_attr_name  = None
    link_ref_singular   = False
    link_ref_suffix     = TFL.Undef ("suffix")
    kind                = MOM.Attr.Link_Role
    max_links           = -1
    role_name           = None
    role_type           = None
    E_Type = P_Type     = TFL.Meta.Alias_Property ("role_type")
    ### by default, don't allow creation of new object for this attribute
    ui_allow_new        = False

    _t_rank                   = -100

    @TFL.Meta.Once_Property
    def q_able_names (self) :
        base_role_names = \
            (getattr (b, "role_name", None) for b in self.__class__.__bases__)
        return tuple \
            (uniq
                (   name for name in itertools.chain
                    ( self.__super.q_able_names
                    , (self.role_name, self.generic_role_name)
                    , base_role_names
                    )
                if  name
                )
            )
    # end def q_able_names

    @TFL.Meta.Class_and_Instance_Once_Property
    def ui_name (self) :
        role_name = self.role_name
        if role_name :
            return role_name.capitalize ().replace ("_", " ")
        else :
            return self.__super.ui_name
    # end def ui_name

# end class A_Link_Role

class A_Link_Role_AB (A_Link_Role) :
    """Link-role of an attribute-based link."""

    attr_name         = None

# end class A_Link_Role_AB

class A_Link_Role_EB (A_Link_Role) :
    """Link-role of an entity-based link."""

# end class A_Link_Role_EB

class A_Name (Syntax_Re_Mixin, _A_String_) :
    """Name of an object."""

    typ                = _ ("Name")
    max_length         = 32
    _syntax_re         = Regexp ("^ [a-zA-Z_] [a-zA-Z0-9_]* $", re.X)
    syntax             = _ \
        ( "A name must start with a letter or underscore and continue with "
          "letters, digits, and underscores."
        )

# end class A_Name

class A_Numeric_String (_A_String_Base_) :
    """String that holds a numeric value.
    """

    example           = "42"
    typ               = _ ("Numeric_String")

    P_Type            = unicode
    as_number         = int

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if isinstance (value, pyk.string_types) :
            value = value.replace (" ", "").lstrip ("+-")
        if value :
            value = soc.as_number (value)
        return soc.P_Type (value)
    # end def cooked

# end class A_Numeric_String

class A_Id_Entity (_A_Id_Entity_) :
    """An entity."""

    typ                = _ ("Entity")
    Kind_Mixins        = (MOM.Attr.Id_Entity_Reference_Mixin, )

# end class A_Id_Entity

class A_Rev_Ref (_A_Rev_Ref_) :
    """Reverse reference to a single entity referring to an `entity`."""

    typ                 = _ ("Rev_Ref")

    finished_query      = _A_Rev_Ref_.finished_query_one

# end class A_Rev_Ref

class A_Rev_Ref_Set (_A_Rev_Ref_, _A_Id_Entity_Set_) :
    """Reverse reference to set of entities referring to an `entity`."""

    typ                 = _ ("Rev_Ref_Set")

    finished_query      = _A_Rev_Ref_.finished_query_all

# end class A_Rev_Ref_Set

class _A_Role_Ref_ (_A_Rev_Ref_) :

    role_filter         = TFL.Meta.Alias_Property ("ref_filter")
    role_name           = TFL.Meta.Alias_Property ("ref_name")

    def sqx (self, obj, sort_key = None) :
        return self.__super.sqx (obj, sort_key).attr (self.other_role_name)
    # end def sqx

# end class _A_Role_Ref_

class A_Role_Ref (_A_Role_Ref_, _A_Id_Entity_) :
    """Reverse reference to role linked to an `entity`"""

    typ                 = _ ("Role_Ref")
    q_able              = True

    def finished_query (self, q) :
        result = self.finished_query_one (q)
        try :
            return result._VALUE
        except Exception :
            return result
    # end def finished_query

# end class A_Role_Ref

class A_Role_Ref_Set (_A_Role_Ref_, A_Rev_Ref_Set) :
    """Reverse reference to set of roles linked to an `entity`."""

    typ                 = _ ("Role_Ref_Set")

    def finished_query (self, q) :
        result = self.finished_query_all (q)
        try :
            return list (r._VALUE for r in result)
        except Exception :
            return result
    # end def finished_query

# end class A_Role_Ref_Set

class A_String (_A_String_) :
    """A string."""

    typ            = _ ("String")
    max_length     = 64

# end class A_String

class A_Surrogate (_A_Int_) :
    """A surrogate key. There can be only one per class."""

    __metaclass__  = MOM.Meta.M_Attr_Type.Surrogate

    typ            = _ ("Surrogate")
    kind           = MOM.Attr.Internal
    Kind_Mixins    = (MOM.Attr.Just_Once_Mixin, )
    default        = None
    min_value      = 0
    if "you need **really** many entities" == "true" :
        max_value  = _A_Int_.max_value_64
    record_changes = False

    surrogate_id   = None

# end class A_Surrogate

class A_Text (_A_String_) :
    """Arbitrary-length text.
    """

    typ            = _ ("Text")
    max_length     = 0

# end class A_Text

class A_Time (_A_Date_) :
    """Time value."""

    example        = "06:42"
    typ            = _ ("Time")
    P_Type         = datetime.time
    ui_length      = 8
    input_formats  = ("%H:%M:%S", "%H:%M")
    _tuple_len     = 6
    _tuple_off     = 3

    def as_rest_cargo_ckd (self, obj, * args, ** kw) :
        value = self.kind.get_value (obj)
        if value is not None :
            return unicode (value.strftime ("%H:%M:%S"))
    # end def as_rest_cargo_ckd

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if isinstance (value, datetime.datetime) :
            value = value.time ()
        elif isinstance (value, pyk.string_types) :
            try :
                value = soc._from_string (value)
            except ValueError :
                raise TypeError (_T ("Time expected, got %r") % (value, ))
        elif not isinstance (value, datetime.time) :
            raise TypeError (_T ("Time expected, got %r") % (value, ))
        return value
    # end def cooked

    @classmethod
    def now (cls) :
        return datetime.datetime.now ().time ()
    # end def now

# end class A_Time

class A_Url (_A_String_) :
    """URL (including local file name)."""

    example        = "/bar"
    typ            = _ ("Url")
    max_length     = 160
    check          = ("""value.startswith (("/", "http://", "https://"))""", )

# end class A_Url

class A_Url_X (A_Url) :
    """External URL."""

    example        = "http://www.example.com/foo"
    check          = ("""value.startswith (("http://", "https://"))""", )

# end class A_Url_X

class A_Year (A_Int) :
    """Year value."""

    example        = "2000"
    typ            = _ ("Year")
    min_value      = 1900
    max_value      = 2100

# end class A_Year

__doc__ = """
Class `MOM.Attr.A_Attr_Type`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: A_Attr_Type

    `MOM.Attr.A_Attr_Type` provides the framework for defining the
    type of essential or non-essential attributes of essential objects
    and links. It is the root class for a hierarchy of classes defining
    abstract attribute types like `A_Int`, `A_String`, `A_Name` and
    many more. All classes specifying abstract attribute types should
    be named following the convention `A_«type-name»` and must define
    a class attribute `typ` that defines the human-readable name of
    the abstract attribute type, e.g., `int`, `string`, or `name`.

    Concrete attribute definitions for essential classes are then
    specified by defining a class derived from the appropriate class
    defining the attribute type, e.g., `A_Int`. The names of classes
    defining concrete attributes **must** not start with `A_` to avoid
    terminal confusion.

    Abstract attribute types are characterized by the properties:

    .. attribute:: name

      Specified by the name of the class.

    .. attribute:: syntax

      Provides information about the syntax required for the
      attribute.

    .. attribute:: typ

      Defines the human-readable name of
      the abstract attribute type, e.g., `int`, `string`, or `name`.

    .. attribute:: needs_raw_value

      Specifies if the raw value needs to be stored for
      this attribute type.

    Concrete attribute types are characterized by the properties:

    .. attribute:: name

      Specified by the name of the class.

    .. attribute:: description

      A short description of the attribute in question.
      This is for example used for displaying a short help text.

      Normally specified via the doc-string of the
      class (but can also be defined by defining a class attribute
      `description`).

    .. attribute:: explanation

      A long description of the attribute in question
      (optional). This is used for the documentation of the attribute
      (together with `description`) and is for example displayed by
      an attribute browser.

    .. attribute:: kind

      Refers to the specific class defining the
      :class:`~_MOM._Attr.Kind.Kind` of the attribute in question.

    .. attribute:: Kind_Mixins

      A number of mixins for the `kind` to be used for this
      attribute. Some of the possible mixins are
      :class:`~_MOM._Attr.Kind.Computed_Mixin`,
      :class:`~_MOM._Attr.Kind.Sticky_Mixin`, and
      :class:`~_MOM._Attr.Kind.Init_Only_Mixin`.

      This is optional and defaults to `()`.

    .. attribute:: check

      Specifies a tuple of expressions that constrain the possible
      values of the attribute. e.g. '0 <= this <= 100'.

      This is optional and defaults to `()`.

    .. attribute:: default

      Defines the default value to be used for the
      attribute when no explicit value is defined by the tool's user.

      This is optional and defaults to `None`.

      `default` **must** not be specified for
      :class:`~_MOM._Attr.Kind.Primary` and
      :class:`~_MOM._Attr.Kind.Necessary` attributes.

    .. attribute:: computed

      A method that's used to compute a value if none is
      specified by the tool user for
      :class:`~_MOM._Attr.Kind.Optional` attributes with the
      :class:`~_MOM._Attr.Kind.Computed_Mixin` or
      one of the internal attributes kinds
      :class:`~_MOM._Attr.Kind.Sync_Cached`,
      :class:`~_MOM._Attr.Kind.Query`,
      :class:`~_MOM._Attr.Kind.Once_Cached`, or
      :class:`~_MOM._Attr.Kind.Computed`.

    .. attribute:: group

      A string that can be used to group a set of attributes
      together. For instance, editors display attributes sorted
      alphabetically by `(group, name)`.

    .. attribute:: rank

      Used when sorting attributes.

    .. attribute:: store_default

      Specifies whether the default value should be
      stored in the database (unless explicitly specified, it isn't).

    Attribute types provide the computed property:

    .. attribute:: db_sig

      Specifies the database signature of the attribute type. This includes
      properties like `max_length`, `needs_raw_value`, etc.

"""

__all__  = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if is_attr_type (v)
    )

__all__ += \
    ( "decimal"
    , "is_attr_type"
    , "Eval_Mixin"
    , "Q"
    , "Pickled_Type_Spec"
    , "Syntax_Re_Mixin"
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Type
