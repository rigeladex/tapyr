# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
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
#    GTW.__test__._SAS_test_functions
#
# Purpose
#    Support functions for testings SAS features
#
# Revision Dates
#    18-Jun-2013 (CT) Creation (factor from SAS.SQL)
#    27-Jun-2013 (CT) Factor `formatted_column`
#    ««revision-date»»···
#--

from   __future__ import print_function
from   __future__ import unicode_literals

from   _MOM.inspect        import children_trans_iter
from   _TFL.predicate      import split_hst

nl     = chr (10)
indent = "  " * 2
sk     = lambda x : (x.type_name, x.i_rank, )

def formatted_select (T, nl, indent) :
    sep            = nl + indent
    text           = str        (T._sa_table.select ())
    head, _, tail  = split_hst  (text, " ")
    lines          = tail.split (nl)
    def _gen () :
        s = "," + sep + (" " * 7)
        for l in lines :
            if "," in l :
                comps = sorted (c.strip () for c in l.split (","))
                yield s.join (comps)
            else :
                yield l
    result = " ".join ((head, sep.join (x.rstrip () for x in _gen ())))
    return result
# end def formatted_select

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
    return \
        ( "Column %-25s : %-20s %s"
        % (c.name, str (c.type).capitalize (), " ".join (tail))
        ).strip ()
# end def formatted_column

def formatted_table (T, nl, indent) :
    sep   = nl + indent
    SQ    = T._SAQ
    ST    = T._sa_table
    def _gen () :
        for c in ST.columns :
            yield formatted_column (c)
    return sep.join (x.rstrip () for x in sorted (_gen ()))
# end def formatted_table

def show_joins (scope) :
    for T, l in (children_trans_iter (scope.MOM.Id_Entity, sort_key = sk)) :
        SAS = getattr (T, "_SAS", None)
        if SAS and len (SAS.joined_tables) > 1 :
            tn  = T.type_name
            ETM = scope [tn]
            print (tn, sorted (str (t) for t in SAS.joined_tables))
            print (" " * 3, ETM.query ())
# end def show_joins

def show_select (scope) :
    for T, l in (children_trans_iter (scope.MOM.Id_Entity, sort_key = sk)) :
        if T.relevant_root and T.show_in_ui :
            second = "" if T.relevant_root is T \
                      else T.relevant_root.type_name
            head   = ("%s %s" % (T.type_name, second)).strip ()
            print ("%s%s" % (head, nl), "  ", formatted_select (T, nl, indent))
# end def show_select

def show_tables (scope) :
    for T, l in (children_trans_iter (scope.MOM.Id_Entity, sort_key = sk)) :
        if T.relevant_root and T.show_in_ui :
            ST = T._sa_table
            second = "" if T.relevant_root is T \
                      else T.relevant_root.type_name
            head   = ("%s %s" % (T.type_name, second)).strip ()
            head   = ("%s <Table %s>" % (head, T._sa_table)).strip ()
            print ("%s%s" % (head, nl), "  ", formatted_table (T, nl, indent))
# end def show_tables

### __END__ GTW.__test__._SAS_test_functions
