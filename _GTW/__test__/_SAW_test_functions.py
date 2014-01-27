# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package _GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    _GTW.__test__._SAW_test_functions
#
# Purpose
#    Support functions for testings SAW features
#
# Revision Dates
#    14-Aug-2013 (CT) Creation
#    26-Aug-2013 (CT) Add `show_key_o_p`, `show_sequence`
#    18-Sep-2013 (CT) Add `show_query` (uses `compile` to show `params`)
#    27-Jan-2014 (CT) Factor `formatted` to `MOM.DBW.SAW.Q_Result`
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM.import_MOM  import MOM, Q

from   _TFL             import TFL
from   _TFL.pyk         import pyk
from   _TFL.predicate   import split_hst, rsplit_hst

import _TFL.Regexp

import itertools
nl     = chr (10)
indent = "  " * 2
sk     = lambda x   : (x.type_name, x.i_rank, )
pred   = lambda ETW : True

def formatted_column (c) :
    tail = []
    c_MOM_Kind = getattr (c, "MOM_Kind", None)
    if c_MOM_Kind :
        tail.append \
            ( "%s %s %s"
            % ( c_MOM_Kind.__class__.__name__
              , c_MOM_Kind.typ
              , getattr (c_MOM_Kind, "name", c_MOM_Kind)
              )
            )
    else :
        tail.append ("-" * 10)
    if c.primary_key :
        tail.append ("primary")
    if c.foreign_keys :
        tail.extend (str (fk) for fk in sorted (c.foreign_keys))
    if c_MOM_Kind and isinstance (c_MOM_Kind.attr, MOM.Attr._A_Id_Entity_) :
        tail.append (repr (c.type))
    try :
        typ = str (c.type).capitalize ()
    except Exception :
        typ = c.type.__class__.__name__
    return ("Column %-25s : %-20s %s" % (c.name, typ, " ".join (tail))).strip ()
# end def formatted_column

def formatted_select (ETW, name = "select", select = None) :
    sep = nl + indent
    if select is None :
        select = getattr (ETW, name, None)
    if select is None :
        return "No '%s'" % (name, )
    text = str (select)
    def _gen (lines, indent = 7) :
        s = "," + sep + (" " * indent)
        inner_indent = " " * (indent - 7)
        inner_sep    = "\n" + inner_indent
        for l in lines :
            if "," in l :
                comps = sorted (c.strip () for c in l.split (","))
                yield s.join (comps)
            elif "JOIN" in l :
                rerep = TFL.Re_Replacer \
                    ( "((?:[A-Z]+ )*JOIN)"
                    , "\n       \\1"
                    )
                p  = rerep (l)
                ps = list (x.rstrip () for x in p.split ("\n"))
                p  = inner_indent + inner_sep.join (ps)
                yield p
            elif "WHERE" in l :
                rerep = TFL.Re_Replacer \
                    ( "((?:\s+)*(?:AND|OR)\s+)"
                    , "\n       \\1"
                    )
                p  = rerep (l)
                ps = list (x.rstrip () for x in p.split ("\n"))
                p  = inner_indent + inner_sep.join (ps)
                yield p
            else :
                yield l
    gindent = 7
    head, _, tail  = split_hst  (text, " ")
    t_head, t_sep, t_tail = split_hst (tail, "\nFROM (SELECT")
    if t_sep :
        head = sep.join ((" ".join ((head, t_head)), t_sep.strip ()))
        tail, t_sep, t_tail_tip = rsplit_hst (t_tail, ")")
        ttt_lines = t_tail_tip.split (nl)
        gindent += 6
    lines  = tail.split (nl)
    result = " ".join \
        ((head, sep.join (x.rstrip () for x in _gen (lines, gindent))))
    if t_sep :
        r_tail = sep.join (x.rstrip () for x in _gen (ttt_lines))
        result = sep.join (( result, " " * 5 + t_sep + r_tail))
    return result.rstrip ()
# end def formatted_select

def formatted_table (ST, nl, indent) :
    sep   = nl + indent
    def _gen () :
        for c in ST.columns :
            yield formatted_column (c)
    return sep.join (x.rstrip () for x in sorted (_gen ()))
# end def formatted_table

def show_ancestors (apt, pred = pred) :
    sk = lambda x : (x.e_type.i_rank, )
    for ETW in sorted (pyk.itervalues (apt._SAW.et_map), key = sk) :
        if not pred (ETW) :
            continue
        T = ETW.e_type
        xs = ("%-36s" % (T.type_name), )
        if ETW.ancestors :
            xs += ("<" , " < ".join ("%-16s" % (a.type_name, ) for a in ETW.ancestors).rstrip ())
        print (" ".join (xs).rstrip ())
# end def show_ancestors

_ignore_kinds = set \
    (( "_Co_Base_", "_Computed_Mixin_", "_Query_", "_Typed_Collection_Mixin_"
     , "Id_Entity_Reference_Mixin", "Kind"
    ))

def _kind_mro (kind, ignore = _ignore_kinds) :
    return \
        ( c.__name__ for c in kind.__class__.__mro__
        if  issubclass (c, MOM.Attr.Kind)
        and "__" not in c.__name__
        and c.__name__ not in ignore
        )
# end def _kind_mro

def show_attr_mro (ET) :
    def show (ET, level = 1) :
        in0 = "  " * (level)
        in1 = "  " * (level + 1)
        for name, kind in sorted (pyk.iteritems (ET.attributes)) :
            if isinstance (kind, MOM.Attr.Auto_Cached) :
                continue
            amro  = ", ".join (_kind_mro (kind))
            tail  = ("-> %s" % (kind.E_Type.type_name, )) if kind.E_Type else ""
            lin1  = ("%s%-20s %s" % (in0, name, tail)).rstrip ()
            print ("%s\n%s%s" % (lin1, in1, amro))
            if kind.is_composite :
                show (kind.attr.E_Type, level + 1)
    print (ET.type_name)
    show (ET)
# end def show_attr_mro

def show_attr_wrappers (apt, pred = pred) :
    def show (W, level = 0) :
        qas = W.q_able_attrs_o
        in0 = "  " * (level + bool (level))
        if qas :
            in1 = in0 + " " * (level + 1 + (not level))
            in2 = in1 + "    "
            print ("%s%s" % (in0, W.type_name))
            for name, aw in sorted (pyk.iteritems (qas)) :
                amro = ", ".join (_kind_mro (aw.kind))
                print \
                    ( "%s%s : %s\n%s%s"
                    % (in1, aw.__class__.__name__, aw.kind, in2, amro)
                    )
                if aw.q_able_attrs_o :
                    show (aw, level + 1)
        elif W.e_type.relevant_root :
            print ("%s%s <-- %s" % (in0, W.type_name, W.parent.type_name))
    sk = lambda x : (x.e_type.i_rank, )
    for ETW in sorted (pyk.itervalues (apt._SAW.et_map), key = sk) :
        if not pred (ETW) :
            continue
        show (ETW)
# end def show_attr_wrappers

def show_key_o_p (apt) :
    def _show (k) :
        return getattr (k, "name", None)
    for ETW in apt._SAW.e_types_t :
        if ETW.key_o or ETW.key_p :
            print \
                ( "%-40s : %-15s %-15s"
                % (ETW.type_name, _show (ETW.key_o), _show (ETW.key_p))
                )
# end def show_key_o_p

def show_q_able (apt, pred = pred) :
    def _gen (ETW) :
        for k, q in sorted (pyk.iteritems (ETW.q_able_attrs)) :
            if k == q.attr.name :
                ### filter attribute-aliases
                yield str (q)
                if q.q_able_attrs :
                    for k, q in sorted (pyk.iteritems (q.q_able_attrs)) :
                        if not q.columns :
                            yield str (q)
    sk = lambda x : (x.e_type.i_rank, )
    for ETW in sorted (pyk.itervalues (apt._SAW.et_map), key = sk):
        if not pred (ETW) :
            continue
        print (ETW)
        print (" ", "\n  ".join (_gen (ETW)))
# end def show_q_able

def show_q_able_names (apt, pred = pred) :
    def _gen (q_able_attrs, level = 0) :
        for k, q in sorted (pyk.iteritems (q_able_attrs)) :
            if k == q.attr.name :
                ### filter attribute-aliases
                yield "%s%-30s: %s" % ("    " * level, k, ", ".join (q.q_able_names))
                if q.q_able_attrs :
                    for x in _gen (q.q_able_attrs, level + 1) :
                        yield x
    sk = lambda x : (x.e_type.i_rank, )
    for ETW in sorted (pyk.itervalues (apt._SAW.et_map), key = sk):
        if not pred (ETW) :
            continue
        print (ETW)
        print (" ", "\n  ".join (_gen (ETW.q_able_attrs)))
# end def show_q_able_names

def show_qc_map (apt, pred = pred) :
    def _show (QC, indent = 4) :
        if QC.Map :
            for k, v in sorted (pyk.iteritems (QC.Map)) :
                print (("%-30s: %.80s" % (" " * indent + k, v)).rstrip ())
                if isinstance (v, QC.__class__) :
                    _show (v, indent + 4)
    sk = lambda x : (x.e_type.i_rank, )
    for ETW in sorted (pyk.itervalues (apt._SAW.et_map), key = sk):
        if not pred (ETW) :
            continue
        if ETW.sa_tables :
            print (ETW)
            _show (ETW.QC)
# end def show_qc_map

def show_query (qr) :
    print (qr.formatted ())
# end def show_query

def show_root_table (apt, pred = pred) :
    sk = lambda x : (x.e_type.i_rank, )
    for ETW in sorted (pyk.itervalues (apt._SAW.et_map), key = sk):
        if not pred (ETW) :
            continue
        T = ETW.e_type
        print (("%-36s %s" % (T.type_name, ETW.root_table)).rstrip ())
# end def show_root_table

def show_selects (apt, name = "select", pred = pred) :
    sk = lambda x : (x.e_type.i_rank, )
    for ETW in sorted (pyk.itervalues (apt._SAW.et_map), key = sk):
        if not pred (ETW) :
            continue
        T = ETW.e_type
        if ETW.has_relevant_tables :
            second = "" if T.relevant_root is T \
                else (T.relevant_root.type_name if T.relevant_root else "")
            head   = ("%s %s" % (T.type_name, second)).strip ()
            print ("%s%s" % (head, nl), "  ", formatted_select (ETW, name = name))
# end def show_selects

def show_sequence (apt) :
    for ETW in apt._SAW.e_types_t :
        seq = ETW.sequence
        if seq:
            print ("%-40s : %s" % (ETW.type_name, seq.seq_name))
# end def show_sequence

def show_sequences (apt) :
    for ETW in apt._SAW.e_types_t :
        seqs = ", ".join (s.seq_name for s in ETW.sequences)
        if seqs :
            print ("%-40s : %s" % (ETW.type_name, seqs))
# end def show_sequences

def show_tables (apt, pred = pred) :
    for ETW in apt._SAW.e_types_t :
        if not pred (ETW) :
            continue
        T = ETW.e_type
        ST = ETW.sa_table
        second = ("(%s)" % (ETW.parent.type_name, )) if ETW.parent else ""
        third  = "" if T.relevant_root is T \
                  else (T.relevant_root and T.relevant_root.type_name)
        head   = (" ".join ((T.type_name, second, third or ""))).strip ()
        head   = ("%s <Table %s>" % (head, ETW.sa_table)).strip ()
        print ("%s%s" % (head, nl), "  ", formatted_table (ETW.sa_table, nl, indent))
    for seq in apt._SAW.sequences :
        print ("<Table for %s>%s" % (seq.attr, nl), "  ", formatted_table (seq.sa_table, nl, indent))
# end def show_tables

### __END__ _GTW.__test__._SAW_test_functions
