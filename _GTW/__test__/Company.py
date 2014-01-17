# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Company
#
# Purpose
#    Test PAP.Company and descendents
#
# Revision Dates
#    26-Feb-2013 (CT) Creation
#     4-Mar-2013 (CT) Add tests for `PAP.Association`
#     6-Mar-2013 (CT) Adapt to new attribute `Company.registered_in`
#     6-Mar-2013 (CT) Add test for `polymorphic_epk` using `children_trans_iter`
#    19-Mar-2013 (CT) Add test for `AQ` for recursive attribute `affiliate`
#    19-Mar-2013 (CT) Add test for `AQ.Atoms`, `AQ.Unwrapped_Atoms`
#    11-May-2013 (CT) Add `test_entity_attr`
#    15-May-2013 (CT) Add test for `link_ref_attr`
#    24-Jul-2013 (CT) Add `test_saw`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> p1 = PAP.Person ("Doe", "Jane", lifetime = ("20010101", ), raw = True)
    >>> bm = PAP.Biz_Man (p1)
    >>> cp = PAP.Company_P ("Doe, Inc.", bm, raw = True)
    >>> ta = PAP.Association ("Towel Carriers Association", short_name = "TCA", raw = True)

    >>> print (p1.ui_repr)
    PAP.Person (u'Doe', u'Jane', u'', u'')

    >>> print (bm.ui_repr)
    PAP.Biz_Man ((u'Doe', u'Jane', u'', u'', 'PAP.Person'),)

    >>> print (cp.ui_repr)
    PAP.Company_P (u'Doe, Inc.', ((u'Doe', u'Jane', u'', u'', 'PAP.Person'), 'PAP.Biz_Man'), u'')

    >>> print (ta.ui_repr)
    PAP.Association (u'Towel Carriers Association',)

    >>> scope.commit ()

    >>> PAP.Person.sorted_by_epk
    <Sorted_By: Getter function for `.last_name`, Getter function for `.first_name`, Getter function for `.middle_name`, Getter function for `.title`>

    >>> PAP.Biz_Man.sorted_by_epk
    <Sorted_By: Getter function for `.left.last_name`, Getter function for `.left.first_name`, Getter function for `.left.middle_name`, Getter function for `.left.title`>

    >>> PAP.Company_P.sorted_by_epk
    <Sorted_By: Getter function for `.name`, Getter function for `.owner.left.last_name`, Getter function for `.owner.left.first_name`, Getter function for `.owner.left.middle_name`, Getter function for `.owner.left.title`, Getter function for `.registered_in`>

    >>> PAP.Person.query (sort_key = TFL.Sorted_By ("pid")).count ()
    1
    >>> PAP.Biz_Man.query (sort_key = TFL.Sorted_By ("pid")).count ()
    1
    >>> PAP.Company_P.query (sort_key = TFL.Sorted_By ("pid")).count ()
    1

    >>> PAP.Person.query ().count ()
    1

    >>> PAP.Person.query (sort_key = PAP.Person.sorted_by_epk).count ()
    1
    >>> PAP.Biz_Man.query (sort_key = PAP.Biz_Man.sorted_by_epk).count ()
    1
    >>> PAP.Company_P.query (sort_key = PAP.Company_P.sorted_by_epk).count ()
    1

    >>> cq = PAP.Company_P ("Jane's, Inc.", bm)

    >>> PAP.Company_P.query (sort_key = TFL.Sorted_By ("pid")).count ()
    2

    >>> PAP.Company_P.query (sort_key = PAP.Company_P.sorted_by_epk).count ()
    2

    >>> print (PAP.Association.E_Type.attr_prop ("name").description)
    Name of association.

    >>> print (PAP.Company.E_Type.attr_prop ("name").description)
    Name of company.

    >>> for s in PAP.Subject.query ().order_by (TFL.Sorted_By ("type_name", "pid")) :
    ...     print (s.ui_repr)
    PAP.Association (u'Towel Carriers Association',)
    PAP.Company_P (u'Doe, Inc.', ((u'Doe', u'Jane', u'', u'', 'PAP.Person'), 'PAP.Biz_Man'), u'')
    PAP.Company_P (u"Jane's, Inc.", ((u'Doe', u'Jane', u'', u'', 'PAP.Person'), 'PAP.Biz_Man'), u'')
    PAP.Person (u'Doe', u'Jane', u'', u'')

    >>> for s in PAP.Subject.query_s () :
    ...     print (s.ui_repr)
    PAP.Person (u'Doe', u'Jane', u'', u'')
    PAP.Company_P (u'Doe, Inc.', ((u'Doe', u'Jane', u'', u'', 'PAP.Person'), 'PAP.Biz_Man'), u'')
    PAP.Company_P (u"Jane's, Inc.", ((u'Doe', u'Jane', u'', u'', 'PAP.Person'), 'PAP.Biz_Man'), u'')
    PAP.Association (u'Towel Carriers Association',)

    >>> sk = lambda x : (not bool (x.children), x.i_rank)
    >>> for i, (T, l) in enumerate (children_trans_iter (PAP.Subject, sort_key = sk)) :
    ...     if not i :
    ...         print ("%%-50s %%5s %%5s %%5s" %% ("type_name", "relev", "p_epk", "p_epks"))
    ...         print ("=" * 70)
    ...     et = T.E_Type
    ...     fs = (et.is_relevant, et.polymorphic_epk, et.polymorphic_epks)
    ...     if any (fs) :
    ...         hd  = "%%s%%s" %% ("  " * l, et.type_name)
    ...         hdl = len (hd)
    ...         sep = (" " if hdl %% 2 else "") + ". " * ((50 - hdl) // 2)
    ...         r, p, s = ((x or "") for x in fs)
    ...         print ("%%s %%s %%5s %%5s %%5s" %% (hd, sep, r, p, s))
    type_name                                          relev p_epk p_epks
    ======================================================================
    PAP.Subject  . . . . . . . . . . . . . . . . . . .         True  True
      PAP.Legal_Entity . . . . . . . . . . . . . . . .         True  True
        PAP.Company  . . . . . . . . . . . . . . . . .   True  True  True
          PAP.Company_P  . . . . . . . . . . . . . . .   True
        PAP.Association  . . . . . . . . . . . . . . .   True
      PAP.Person . . . . . . . . . . . . . . . . . . .   True

    >>> AQ = PAP.Company_P.E_Type.AQ

    >>> for aq in AQ.Attrs_Transitive :
    ...     print (aq, aq.E_Type.type_name if aq.E_Type else "-"*5)
    <name.AQ [Attr.Type.Querier String]> -----
    <owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Biz_Man
    <owner.left.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <owner.left.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <owner.left.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <owner.left.middle_name.AQ [Attr.Type.Querier String]> -----
    <owner.left.title.AQ [Attr.Type.Querier String]> -----
    <owner.left.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <owner.left.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <owner.left.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <owner.left.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <owner.left.sex.AQ [Attr.Type.Querier Ckd]> -----
    <owner.left.last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <owner.left.pid.AQ [Attr.Type.Querier Ckd]> -----
    <owner.left.type_name.AQ [Attr.Type.Querier String]> -----
    <owner.last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <owner.pid.AQ [Attr.Type.Querier Ckd]> -----
    <owner.type_name.AQ [Attr.Type.Querier String]> -----
    <registered_in.AQ [Attr.Type.Querier String]> -----
    <lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <short_name.AQ [Attr.Type.Querier String]> -----
    <affiliate.AQ [Attr.Type.Querier Id_Entity]> PAP.Company_P
    <affiliate.name.AQ [Attr.Type.Querier String]> -----
    <affiliate.owner.AQ [Attr.Type.Querier Id_Entity]> PAP.Biz_Man
    <affiliate.owner.left.AQ [Attr.Type.Querier Id_Entity]> PAP.Person
    <affiliate.owner.left.last_name.AQ [Attr.Type.Querier String_FL]> -----
    <affiliate.owner.left.first_name.AQ [Attr.Type.Querier String_FL]> -----
    <affiliate.owner.left.middle_name.AQ [Attr.Type.Querier String]> -----
    <affiliate.owner.left.title.AQ [Attr.Type.Querier String]> -----
    <affiliate.owner.left.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <affiliate.owner.left.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <affiliate.owner.left.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <affiliate.owner.left.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <affiliate.owner.left.sex.AQ [Attr.Type.Querier Ckd]> -----
    <affiliate.owner.left.last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <affiliate.owner.left.pid.AQ [Attr.Type.Querier Ckd]> -----
    <affiliate.owner.left.type_name.AQ [Attr.Type.Querier String]> -----
    <affiliate.owner.last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <affiliate.owner.pid.AQ [Attr.Type.Querier Ckd]> -----
    <affiliate.owner.type_name.AQ [Attr.Type.Querier String]> -----
    <affiliate.registered_in.AQ [Attr.Type.Querier String]> -----
    <affiliate.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <affiliate.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <affiliate.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <affiliate.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <affiliate.short_name.AQ [Attr.Type.Querier String]> -----
    <affiliate.affiliate.AQ [Attr.Type.Querier Id_Entity]> PAP.Company_P
    <affiliate.last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <affiliate.pid.AQ [Attr.Type.Querier Ckd]> -----
    <affiliate.type_name.AQ [Attr.Type.Querier String]> -----
    <last_cid.AQ [Attr.Type.Querier Ckd]> -----
    <pid.AQ [Attr.Type.Querier Ckd]> -----
    <type_name.AQ [Attr.Type.Querier String]> -----

    >>> AQ
    <Attr.Type.Querier.E_Type for PAP.Company_P>

    >>> for aq in AQ.Atoms :
    ...     print (aq)
    <name.AQ [Attr.Type.Querier String]>
    <owner.left.last_name.AQ [Attr.Type.Querier String_FL]>
    <owner.left.first_name.AQ [Attr.Type.Querier String_FL]>
    <owner.left.middle_name.AQ [Attr.Type.Querier String]>
    <owner.left.title.AQ [Attr.Type.Querier String]>
    <owner.left.lifetime.start.AQ [Attr.Type.Querier Date]>
    <owner.left.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <owner.left.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <owner.left.sex.AQ [Attr.Type.Querier Ckd]>
    <owner.left.last_cid.AQ [Attr.Type.Querier Ckd]>
    <owner.left.pid.AQ [Attr.Type.Querier Ckd]>
    <owner.left.type_name.AQ [Attr.Type.Querier String]>
    <owner.last_cid.AQ [Attr.Type.Querier Ckd]>
    <owner.pid.AQ [Attr.Type.Querier Ckd]>
    <owner.type_name.AQ [Attr.Type.Querier String]>
    <registered_in.AQ [Attr.Type.Querier String]>
    <lifetime.start.AQ [Attr.Type.Querier Date]>
    <lifetime.finish.AQ [Attr.Type.Querier Date]>
    <lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <short_name.AQ [Attr.Type.Querier String]>
    <affiliate.name.AQ [Attr.Type.Querier String]>
    <affiliate.owner.left.last_name.AQ [Attr.Type.Querier String_FL]>
    <affiliate.owner.left.first_name.AQ [Attr.Type.Querier String_FL]>
    <affiliate.owner.left.middle_name.AQ [Attr.Type.Querier String]>
    <affiliate.owner.left.title.AQ [Attr.Type.Querier String]>
    <affiliate.owner.left.lifetime.start.AQ [Attr.Type.Querier Date]>
    <affiliate.owner.left.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <affiliate.owner.left.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <affiliate.owner.left.sex.AQ [Attr.Type.Querier Ckd]>
    <affiliate.owner.left.last_cid.AQ [Attr.Type.Querier Ckd]>
    <affiliate.owner.left.pid.AQ [Attr.Type.Querier Ckd]>
    <affiliate.owner.left.type_name.AQ [Attr.Type.Querier String]>
    <affiliate.owner.last_cid.AQ [Attr.Type.Querier Ckd]>
    <affiliate.owner.pid.AQ [Attr.Type.Querier Ckd]>
    <affiliate.owner.type_name.AQ [Attr.Type.Querier String]>
    <affiliate.registered_in.AQ [Attr.Type.Querier String]>
    <affiliate.lifetime.start.AQ [Attr.Type.Querier Date]>
    <affiliate.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <affiliate.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <affiliate.short_name.AQ [Attr.Type.Querier String]>
    <affiliate.last_cid.AQ [Attr.Type.Querier Ckd]>
    <affiliate.pid.AQ [Attr.Type.Querier Ckd]>
    <affiliate.type_name.AQ [Attr.Type.Querier String]>
    <last_cid.AQ [Attr.Type.Querier Ckd]>
    <pid.AQ [Attr.Type.Querier Ckd]>
    <type_name.AQ [Attr.Type.Querier String]>

    >>> for aq in AQ.Unwrapped_Atoms :
    ...     print (aq)
    <name.AQ [Attr.Type.Querier String]>
    <owner.left.last_name.AQ [Attr.Type.Querier String_FL]>
    <owner.left.first_name.AQ [Attr.Type.Querier String_FL]>
    <owner.left.middle_name.AQ [Attr.Type.Querier String]>
    <owner.left.title.AQ [Attr.Type.Querier String]>
    <registered_in.AQ [Attr.Type.Querier String]>
    <lifetime.start.AQ [Attr.Type.Querier Date]>
    <lifetime.finish.AQ [Attr.Type.Querier Date]>
    <short_name.AQ [Attr.Type.Querier String]>
    <affiliate.name.AQ [Attr.Type.Querier String]>
    <affiliate.owner.left.last_name.AQ [Attr.Type.Querier String_FL]>
    <affiliate.owner.left.first_name.AQ [Attr.Type.Querier String_FL]>
    <affiliate.owner.left.middle_name.AQ [Attr.Type.Querier String]>
    <affiliate.owner.left.title.AQ [Attr.Type.Querier String]>
    <affiliate.registered_in.AQ [Attr.Type.Querier String]>
    <last_cid.AQ [Attr.Type.Querier Ckd]>
    <pid.AQ [Attr.Type.Querier Ckd]>
    <type_name.AQ [Attr.Type.Querier String]>

    >>> print (formatted (AQ.As_Json_Cargo))
    { 'filters' :
        [ { 'name' : 'name'
          , 'sig_key' : 3
          , 'ui_name' : 'Name'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'last_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Last name'
                      }
                    , { 'name' : 'first_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'First name'
                      }
                    , { 'name' : 'middle_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Middle name'
                      }
                    , { 'name' : 'title'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Academic title'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'start'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Start'
                            }
                          , { 'name' : 'finish'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Finish'
                            }
                          , { 'name' : 'alive'
                            , 'sig_key' : 1
                            , 'ui_name' : 'Alive'
                            }
                          ]
                      , 'name' : 'lifetime'
                      , 'ui_name' : 'Lifetime'
                      }
                    , { 'name' : 'sex'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Sex'
                      }
                    , { 'name' : 'last_cid'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Last cid'
                      }
                    , { 'name' : 'pid'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Pid'
                      }
                    , { 'name' : 'type_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Type name'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Man'
                }
              , { 'name' : 'last_cid'
                , 'sig_key' : 0
                , 'ui_name' : 'Last cid'
                }
              , { 'name' : 'pid'
                , 'sig_key' : 0
                , 'ui_name' : 'Pid'
                }
              , { 'name' : 'type_name'
                , 'sig_key' : 3
                , 'ui_name' : 'Type name'
                }
              ]
          , 'name' : 'owner'
          , 'sig_key' : 2
          , 'ui_name' : 'Owner'
          }
        , { 'name' : 'registered_in'
          , 'sig_key' : 3
          , 'ui_name' : 'Registered in'
          }
        , { 'attrs' :
              [ { 'name' : 'start'
                , 'sig_key' : 0
                , 'ui_name' : 'Start'
                }
              , { 'name' : 'finish'
                , 'sig_key' : 0
                , 'ui_name' : 'Finish'
                }
              , { 'name' : 'alive'
                , 'sig_key' : 1
                , 'ui_name' : 'Alive'
                }
              ]
          , 'name' : 'lifetime'
          , 'ui_name' : 'Lifetime'
          }
        , { 'name' : 'short_name'
          , 'sig_key' : 3
          , 'ui_name' : 'Short name'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'name' : 'name'
                , 'sig_key' : 3
                , 'ui_name' : 'Name'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'Class' : 'Entity'
                      , 'attrs' :
                          [ { 'name' : 'last_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Last name'
                            }
                          , { 'name' : 'first_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'First name'
                            }
                          , { 'name' : 'middle_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Middle name'
                            }
                          , { 'name' : 'title'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Academic title'
                            }
                          , { 'attrs' :
                                [ { 'name' : 'start'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Start'
                                  }
                                , { 'name' : 'finish'
                                  , 'sig_key' : 0
                                  , 'ui_name' : 'Finish'
                                  }
                                , { 'name' : 'alive'
                                  , 'sig_key' : 1
                                  , 'ui_name' : 'Alive'
                                  }
                                ]
                            , 'name' : 'lifetime'
                            , 'ui_name' : 'Lifetime'
                            }
                          , { 'name' : 'sex'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Sex'
                            }
                          , { 'name' : 'last_cid'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Last cid'
                            }
                          , { 'name' : 'pid'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Pid'
                            }
                          , { 'name' : 'type_name'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Type name'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Man'
                      }
                    , { 'name' : 'last_cid'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Last cid'
                      }
                    , { 'name' : 'pid'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Pid'
                      }
                    , { 'name' : 'type_name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Type name'
                      }
                    ]
                , 'name' : 'owner'
                , 'sig_key' : 2
                , 'ui_name' : 'Owner'
                }
              , { 'name' : 'registered_in'
                , 'sig_key' : 3
                , 'ui_name' : 'Registered in'
                }
              , { 'attrs' :
                    [ { 'name' : 'start'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Start'
                      }
                    , { 'name' : 'finish'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Finish'
                      }
                    , { 'name' : 'alive'
                      , 'sig_key' : 1
                      , 'ui_name' : 'Alive'
                      }
                    ]
                , 'name' : 'lifetime'
                , 'ui_name' : 'Lifetime'
                }
              , { 'name' : 'short_name'
                , 'sig_key' : 3
                , 'ui_name' : 'Short name'
                }
              , { 'Class' : 'Entity'
                , 'name' : 'affiliate'
                , 'sig_key' : 2
                , 'ui_name' : 'Affiliate'
                }
              , { 'name' : 'last_cid'
                , 'sig_key' : 0
                , 'ui_name' : 'Last cid'
                }
              , { 'name' : 'pid'
                , 'sig_key' : 0
                , 'ui_name' : 'Pid'
                }
              , { 'name' : 'type_name'
                , 'sig_key' : 3
                , 'ui_name' : 'Type name'
                }
              ]
          , 'name' : 'affiliate'
          , 'sig_key' : 2
          , 'ui_name' : 'Affiliate'
          }
        , { 'name' : 'last_cid'
          , 'sig_key' : 0
          , 'ui_name' : 'Last cid'
          }
        , { 'name' : 'pid'
          , 'sig_key' : 0
          , 'ui_name' : 'Pid'
          }
        , { 'name' : 'type_name'
          , 'sig_key' : 3
          , 'ui_name' : 'Type name'
          }
        ]
    , 'name_sep' : '__'
    , 'op_map' :
        { 'CONTAINS' :
            { 'desc' : 'Select entities where the attribute contains the specified value'
            , 'sym' : 'contains'
            }
        , 'ENDSWITH' :
            { 'desc' : 'Select entities where the attribute value ends with the specified value'
            , 'sym' : 'ends-with'
            }
        , 'EQ' :
            { 'desc' : 'Select entities where the attribute is equal to the specified value'
            , 'sym' : '=='
            }
        , 'EQS' :
            { 'desc' : 'Select entities where the attribute is equal to the specified string value'
            , 'sym' : 'EQS'
            }
        , 'GE' :
            { 'desc' : 'Select entities where the attribute is greater than, or equal to, the specified value'
            , 'sym' : '>='
            }
        , 'GT' :
            { 'desc' : 'Select entities where the attribute is greater than the specified value'
            , 'sym' : '>'
            }
        , 'IN' :
            { 'desc' : 'Select entities where the attribute is a member of the specified list of values'
            , 'sym' : 'in'
            }
        , 'LE' :
            { 'desc' : 'Select entities where the attribute is less than, or equal to, the specified value'
            , 'sym' : '<='
            }
        , 'LT' :
            { 'desc' : 'Select entities where the attribute is less than the specified value'
            , 'sym' : '<'
            }
        , 'NE' :
            { 'desc' : 'Select entities where the attribute is not equal to the specified value'
            , 'sym' : '!='
            }
        , 'NES' :
            { 'desc' : 'Select entities where the attribute is not equal to the specified string value'
            , 'sym' : 'NES'
            }
        , 'STARTSWITH' :
            { 'desc' : 'Select entities where the attribute value starts with the specified value'
            , 'sym' : 'starts-with'
            }
        }
    , 'op_sep' : '___'
    , 'sig_map' :
        { 0 :
            ( 'EQ'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            )
        , 1 :
    ( 'EQ' ,)
        , 2 :
            ( 'EQ'
            , 'IN'
            , 'NE'
            )
        , 3 :
            ( 'CONTAINS'
            , 'ENDSWITH'
            , 'EQ'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            , 'STARTSWITH'
            )
        }
    , 'ui_sep' : '/'
    }

    >>> print (formatted (AQ.As_Template_Elem))
    [ Record
      ( attr = String `name`
      , full_name = 'name'
      , id = 'name'
      , name = 'name'
      , sig_key = 3
      , ui_name = 'Name'
      )
    , Record
      ( Class = 'Entity'
      , attr = Entity `owner`
      , attrs =
          [ Record
            ( Class = 'Entity'
            , attr = Person `left`
            , attrs =
                [ Record
                  ( attr = String `last_name`
                  , full_name = 'owner.left.last_name'
                  , id = 'owner__left__last_name'
                  , name = 'last_name'
                  , sig_key = 3
                  , ui_name = 'Owner/Man/Last name'
                  )
                , Record
                  ( attr = String `first_name`
                  , full_name = 'owner.left.first_name'
                  , id = 'owner__left__first_name'
                  , name = 'first_name'
                  , sig_key = 3
                  , ui_name = 'Owner/Man/First name'
                  )
                , Record
                  ( attr = String `middle_name`
                  , full_name = 'owner.left.middle_name'
                  , id = 'owner__left__middle_name'
                  , name = 'middle_name'
                  , sig_key = 3
                  , ui_name = 'Owner/Man/Middle name'
                  )
                , Record
                  ( attr = String `title`
                  , full_name = 'owner.left.title'
                  , id = 'owner__left__title'
                  , name = 'title'
                  , sig_key = 3
                  , ui_name = 'Owner/Man/Academic title'
                  )
                , Record
                  ( attr = Date_Interval `lifetime`
                  , attrs =
                      [ Record
                        ( attr = Date `start`
                        , full_name = 'owner.left.lifetime.start'
                        , id = 'owner__left__lifetime__start'
                        , name = 'start'
                        , sig_key = 0
                        , ui_name = 'Owner/Man/Lifetime/Start'
                        )
                      , Record
                        ( attr = Date `finish`
                        , full_name = 'owner.left.lifetime.finish'
                        , id = 'owner__left__lifetime__finish'
                        , name = 'finish'
                        , sig_key = 0
                        , ui_name = 'Owner/Man/Lifetime/Finish'
                        )
                      , Record
                        ( attr = Boolean `alive`
                        , choices =
                            [ 'no'
                            , 'yes'
                            ]
                        , full_name = 'owner.left.lifetime.alive'
                        , id = 'owner__left__lifetime__alive'
                        , name = 'alive'
                        , sig_key = 1
                        , ui_name = 'Owner/Man/Lifetime/Alive'
                        )
                      ]
                  , full_name = 'owner.left.lifetime'
                  , id = 'owner__left__lifetime'
                  , name = 'lifetime'
                  , ui_name = 'Owner/Man/Lifetime'
                  )
                , Record
                  ( attr = Sex `sex`
                  , choices =
                      [
                        ( 'F'
                        , 'Female'
                        )
                      ,
                        ( 'M'
                        , 'Male'
                        )
                      ]
                  , full_name = 'owner.left.sex'
                  , id = 'owner__left__sex'
                  , name = 'sex'
                  , sig_key = 0
                  , ui_name = 'Owner/Man/Sex'
                  )
                , Record
                  ( attr = Int `last_cid`
                  , full_name = 'owner.left.last_cid'
                  , id = 'owner__left__last_cid'
                  , name = 'last_cid'
                  , sig_key = 0
                  , ui_name = 'Owner/Man/Last cid'
                  )
                , Record
                  ( attr = Surrogate `pid`
                  , full_name = 'owner.left.pid'
                  , id = 'owner__left__pid'
                  , name = 'pid'
                  , sig_key = 0
                  , ui_name = 'Owner/Man/Pid'
                  )
                , Record
                  ( attr = String `type_name`
                  , full_name = 'owner.left.type_name'
                  , id = 'owner__left__type_name'
                  , name = 'type_name'
                  , sig_key = 3
                  , ui_name = 'Owner/Man/Type name'
                  )
                ]
            , full_name = 'owner.left'
            , id = 'owner__left'
            , name = 'left'
            , sig_key = 2
            , type_name = 'PAP.Person'
            , ui_name = 'Owner/Man'
            , ui_type_name = 'Person'
            )
          , Record
            ( attr = Int `last_cid`
            , full_name = 'owner.last_cid'
            , id = 'owner__last_cid'
            , name = 'last_cid'
            , sig_key = 0
            , ui_name = 'Owner/Last cid'
            )
          , Record
            ( attr = Surrogate `pid`
            , full_name = 'owner.pid'
            , id = 'owner__pid'
            , name = 'pid'
            , sig_key = 0
            , ui_name = 'Owner/Pid'
            )
          , Record
            ( attr = String `type_name`
            , full_name = 'owner.type_name'
            , id = 'owner__type_name'
            , name = 'type_name'
            , sig_key = 3
            , ui_name = 'Owner/Type name'
            )
          ]
      , full_name = 'owner'
      , id = 'owner'
      , name = 'owner'
      , sig_key = 2
      , type_name = 'PAP.Biz_Man'
      , ui_name = 'Owner'
      , ui_type_name = 'Biz_Man'
      )
    , Record
      ( attr = String `registered_in`
      , full_name = 'registered_in'
      , id = 'registered_in'
      , name = 'registered_in'
      , sig_key = 3
      , ui_name = 'Registered in'
      )
    , Record
      ( attr = Date_Interval `lifetime`
      , attrs =
          [ Record
            ( attr = Date `start`
            , full_name = 'lifetime.start'
            , id = 'lifetime__start'
            , name = 'start'
            , sig_key = 0
            , ui_name = 'Lifetime/Start'
            )
          , Record
            ( attr = Date `finish`
            , full_name = 'lifetime.finish'
            , id = 'lifetime__finish'
            , name = 'finish'
            , sig_key = 0
            , ui_name = 'Lifetime/Finish'
            )
          , Record
            ( attr = Boolean `alive`
            , choices = <Recursion on list...>
            , full_name = 'lifetime.alive'
            , id = 'lifetime__alive'
            , name = 'alive'
            , sig_key = 1
            , ui_name = 'Lifetime/Alive'
            )
          ]
      , full_name = 'lifetime'
      , id = 'lifetime'
      , name = 'lifetime'
      , ui_name = 'Lifetime'
      )
    , Record
      ( attr = String `short_name`
      , full_name = 'short_name'
      , id = 'short_name'
      , name = 'short_name'
      , sig_key = 3
      , ui_name = 'Short name'
      )
    , Record
      ( Class = 'Entity'
      , attr = Entity `affiliate`
      , attrs =
          [ Record
            ( attr = String `name`
            , full_name = 'affiliate.name'
            , id = 'affiliate__name'
            , name = 'name'
            , sig_key = 3
            , ui_name = 'Affiliate/Name'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `owner`
            , attrs =
                [ Record
                  ( Class = 'Entity'
                  , attr = Person `left`
                  , attrs =
                      [ Record
                        ( attr = String `last_name`
                        , full_name = 'affiliate.owner.left.last_name'
                        , id = 'affiliate__owner__left__last_name'
                        , name = 'last_name'
                        , sig_key = 3
                        , ui_name = 'Affiliate/Owner/Man/Last name'
                        )
                      , Record
                        ( attr = String `first_name`
                        , full_name = 'affiliate.owner.left.first_name'
                        , id = 'affiliate__owner__left__first_name'
                        , name = 'first_name'
                        , sig_key = 3
                        , ui_name = 'Affiliate/Owner/Man/First name'
                        )
                      , Record
                        ( attr = String `middle_name`
                        , full_name = 'affiliate.owner.left.middle_name'
                        , id = 'affiliate__owner__left__middle_name'
                        , name = 'middle_name'
                        , sig_key = 3
                        , ui_name = 'Affiliate/Owner/Man/Middle name'
                        )
                      , Record
                        ( attr = String `title`
                        , full_name = 'affiliate.owner.left.title'
                        , id = 'affiliate__owner__left__title'
                        , name = 'title'
                        , sig_key = 3
                        , ui_name = 'Affiliate/Owner/Man/Academic title'
                        )
                      , Record
                        ( attr = Date_Interval `lifetime`
                        , attrs =
                            [ Record
                              ( attr = Date `start`
                              , full_name = 'affiliate.owner.left.lifetime.start'
                              , id = 'affiliate__owner__left__lifetime__start'
                              , name = 'start'
                              , sig_key = 0
                              , ui_name = 'Affiliate/Owner/Man/Lifetime/Start'
                              )
                            , Record
                              ( attr = Date `finish`
                              , full_name = 'affiliate.owner.left.lifetime.finish'
                              , id = 'affiliate__owner__left__lifetime__finish'
                              , name = 'finish'
                              , sig_key = 0
                              , ui_name = 'Affiliate/Owner/Man/Lifetime/Finish'
                              )
                            , Record
                              ( attr = Boolean `alive`
                              , choices = <Recursion on list...>
                              , full_name = 'affiliate.owner.left.lifetime.alive'
                              , id = 'affiliate__owner__left__lifetime__alive'
                              , name = 'alive'
                              , sig_key = 1
                              , ui_name = 'Affiliate/Owner/Man/Lifetime/Alive'
                              )
                            ]
                        , full_name = 'affiliate.owner.left.lifetime'
                        , id = 'affiliate__owner__left__lifetime'
                        , name = 'lifetime'
                        , ui_name = 'Affiliate/Owner/Man/Lifetime'
                        )
                      , Record
                        ( attr = Sex `sex`
                        , choices = <Recursion on list...>
                        , full_name = 'affiliate.owner.left.sex'
                        , id = 'affiliate__owner__left__sex'
                        , name = 'sex'
                        , sig_key = 0
                        , ui_name = 'Affiliate/Owner/Man/Sex'
                        )
                      , Record
                        ( attr = Int `last_cid`
                        , full_name = 'affiliate.owner.left.last_cid'
                        , id = 'affiliate__owner__left__last_cid'
                        , name = 'last_cid'
                        , sig_key = 0
                        , ui_name = 'Affiliate/Owner/Man/Last cid'
                        )
                      , Record
                        ( attr = Surrogate `pid`
                        , full_name = 'affiliate.owner.left.pid'
                        , id = 'affiliate__owner__left__pid'
                        , name = 'pid'
                        , sig_key = 0
                        , ui_name = 'Affiliate/Owner/Man/Pid'
                        )
                      , Record
                        ( attr = String `type_name`
                        , full_name = 'affiliate.owner.left.type_name'
                        , id = 'affiliate__owner__left__type_name'
                        , name = 'type_name'
                        , sig_key = 3
                        , ui_name = 'Affiliate/Owner/Man/Type name'
                        )
                      ]
                  , full_name = 'affiliate.owner.left'
                  , id = 'affiliate__owner__left'
                  , name = 'left'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'Affiliate/Owner/Man'
                  , ui_type_name = 'Person'
                  )
                , Record
                  ( attr = Int `last_cid`
                  , full_name = 'affiliate.owner.last_cid'
                  , id = 'affiliate__owner__last_cid'
                  , name = 'last_cid'
                  , sig_key = 0
                  , ui_name = 'Affiliate/Owner/Last cid'
                  )
                , Record
                  ( attr = Surrogate `pid`
                  , full_name = 'affiliate.owner.pid'
                  , id = 'affiliate__owner__pid'
                  , name = 'pid'
                  , sig_key = 0
                  , ui_name = 'Affiliate/Owner/Pid'
                  )
                , Record
                  ( attr = String `type_name`
                  , full_name = 'affiliate.owner.type_name'
                  , id = 'affiliate__owner__type_name'
                  , name = 'type_name'
                  , sig_key = 3
                  , ui_name = 'Affiliate/Owner/Type name'
                  )
                ]
            , full_name = 'affiliate.owner'
            , id = 'affiliate__owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Biz_Man'
            , ui_name = 'Affiliate/Owner'
            , ui_type_name = 'Biz_Man'
            )
          , Record
            ( attr = String `registered_in`
            , full_name = 'affiliate.registered_in'
            , id = 'affiliate__registered_in'
            , name = 'registered_in'
            , sig_key = 3
            , ui_name = 'Affiliate/Registered in'
            )
          , Record
            ( attr = Date_Interval `lifetime`
            , attrs =
                [ Record
                  ( attr = Date `start`
                  , full_name = 'affiliate.lifetime.start'
                  , id = 'affiliate__lifetime__start'
                  , name = 'start'
                  , sig_key = 0
                  , ui_name = 'Affiliate/Lifetime/Start'
                  )
                , Record
                  ( attr = Date `finish`
                  , full_name = 'affiliate.lifetime.finish'
                  , id = 'affiliate__lifetime__finish'
                  , name = 'finish'
                  , sig_key = 0
                  , ui_name = 'Affiliate/Lifetime/Finish'
                  )
                , Record
                  ( attr = Boolean `alive`
                  , choices = <Recursion on list...>
                  , full_name = 'affiliate.lifetime.alive'
                  , id = 'affiliate__lifetime__alive'
                  , name = 'alive'
                  , sig_key = 1
                  , ui_name = 'Affiliate/Lifetime/Alive'
                  )
                ]
            , full_name = 'affiliate.lifetime'
            , id = 'affiliate__lifetime'
            , name = 'lifetime'
            , ui_name = 'Affiliate/Lifetime'
            )
          , Record
            ( attr = String `short_name`
            , full_name = 'affiliate.short_name'
            , id = 'affiliate__short_name'
            , name = 'short_name'
            , sig_key = 3
            , ui_name = 'Affiliate/Short name'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `affiliate`
            , full_name = 'affiliate.affiliate'
            , id = 'affiliate__affiliate'
            , name = 'affiliate'
            , sig_key = 2
            , type_name = 'PAP.Company_P'
            , ui_name = 'Affiliate/Affiliate'
            , ui_type_name = 'Company_P'
            )
          , Record
            ( attr = Int `last_cid`
            , full_name = 'affiliate.last_cid'
            , id = 'affiliate__last_cid'
            , name = 'last_cid'
            , sig_key = 0
            , ui_name = 'Affiliate/Last cid'
            )
          , Record
            ( attr = Surrogate `pid`
            , full_name = 'affiliate.pid'
            , id = 'affiliate__pid'
            , name = 'pid'
            , sig_key = 0
            , ui_name = 'Affiliate/Pid'
            )
          , Record
            ( attr = String `type_name`
            , full_name = 'affiliate.type_name'
            , id = 'affiliate__type_name'
            , name = 'type_name'
            , sig_key = 3
            , ui_name = 'Affiliate/Type name'
            )
          ]
      , full_name = 'affiliate'
      , id = 'affiliate'
      , name = 'affiliate'
      , sig_key = 2
      , type_name = 'PAP.Company_P'
      , ui_name = 'Affiliate'
      , ui_type_name = 'Company_P'
      )
    , Record
      ( attr = Int `last_cid`
      , full_name = 'last_cid'
      , id = 'last_cid'
      , name = 'last_cid'
      , sig_key = 0
      , ui_name = 'Last cid'
      )
    , Record
      ( attr = Surrogate `pid`
      , full_name = 'pid'
      , id = 'pid'
      , name = 'pid'
      , sig_key = 0
      , ui_name = 'Pid'
      )
    , Record
      ( attr = String `type_name`
      , full_name = 'type_name'
      , id = 'type_name'
      , name = 'type_name'
      , sig_key = 3
      , ui_name = 'Type name'
      )
    ]

    >>> QR  = GTW.RST.TOP.MOM.Query_Restriction
    >>> print (formatted (QR.Filter_Atoms (QR.Filter (PAP.Company_P, "affiliate"))))
    ( Record
      ( AQ = <name.AQ [Attr.Type.Querier String]>
      , attr = String `name`
      , edit = None
      , full_name = 'name'
      , id = 'name___AC'
      , name = 'name___AC'
      , op = Record
          ( desc = 'Select entities where the attribute value starts with the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 3
      , ui_name = 'Name'
      , value = None
      )
    , Record
      ( AQ = <owner.left.last_name.AQ [Attr.Type.Querier String_FL]>
      , attr = String `last_name`
      , edit = None
      , full_name = 'owner.left.last_name'
      , id = 'owner__left__last_name___AC'
      , name = 'owner__left__last_name___AC'
      , op = Record
          ( desc = 'Select entities where the attribute value starts with the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 3
      , ui_name = 'Owner/Man/Last name'
      , value = None
      )
    , Record
      ( AQ = <owner.left.first_name.AQ [Attr.Type.Querier String_FL]>
      , attr = String `first_name`
      , edit = None
      , full_name = 'owner.left.first_name'
      , id = 'owner__left__first_name___AC'
      , name = 'owner__left__first_name___AC'
      , op = Record
          ( desc = 'Select entities where the attribute value starts with the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 3
      , ui_name = 'Owner/Man/First name'
      , value = None
      )
    , Record
      ( AQ = <owner.left.middle_name.AQ [Attr.Type.Querier String]>
      , attr = String `middle_name`
      , edit = None
      , full_name = 'owner.left.middle_name'
      , id = 'owner__left__middle_name___AC'
      , name = 'owner__left__middle_name___AC'
      , op = Record
          ( desc = 'Select entities where the attribute value starts with the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 3
      , ui_name = 'Owner/Man/Middle name'
      , value = None
      )
    , Record
      ( AQ = <owner.left.title.AQ [Attr.Type.Querier String]>
      , attr = String `title`
      , edit = None
      , full_name = 'owner.left.title'
      , id = 'owner__left__title___AC'
      , name = 'owner__left__title___AC'
      , op = Record
          ( desc = 'Select entities where the attribute value starts with the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 3
      , ui_name = 'Owner/Man/Academic title'
      , value = None
      )
    , Record
      ( AQ = <registered_in.AQ [Attr.Type.Querier String]>
      , attr = String `registered_in`
      , edit = None
      , full_name = 'registered_in'
      , id = 'registered_in___AC'
      , name = 'registered_in___AC'
      , op = Record
          ( desc = 'Select entities where the attribute value starts with the specified value'
          , label = 'auto-complete'
          )
      , sig_key = 3
      , ui_name = 'Registered in'
      , value = None
      )
    )

"""

_test_entity_attr = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> MOM = scope.MOM
    >>> PAP = scope.PAP
    >>> sk = lambda x : (not bool (x.children), x.i_rank)

    >>> show_T_attrs (PAP.Subject, "%%s%%-15s %%-10s %%-25.25s %%s", None, sk)
    PAP.Subject
        address_links   query      PAP.Subject_has_Address   PAP.Subject_has_Address
        addresses       query      PAP.Address               PAP.Subject_has_Address
        created_by      computed   MOM.Id_Entity
        email_links     query      PAP.Subject_has_Email     PAP.Subject_has_Email
        emails          query      PAP.Email                 PAP.Subject_has_Email
        last_changed_by computed   MOM.Id_Entity
        phone_links     query      PAP.Subject_has_Phone     PAP.Subject_has_Phone
        phones          query      PAP.Phone                 PAP.Subject_has_Phone
        property_links  query      PAP.Subject_has_Property  PAP.Subject_has_Property
        url_links       query      PAP.Subject_has_Url       PAP.Subject_has_Url
        urls            query      PAP.Url                   PAP.Subject_has_Url
    .PAP.Legal_Entity
        address_links   query      PAP.Subject_has_Address   PAP.Subject_has_Address
        addresses       query      PAP.Address               PAP.Subject_has_Address
        created_by      computed   MOM.Id_Entity
        email_links     query      PAP.Subject_has_Email     PAP.Subject_has_Email
        emails          query      PAP.Email                 PAP.Subject_has_Email
        last_changed_by computed   MOM.Id_Entity
        phone_links     query      PAP.Subject_has_Phone     PAP.Subject_has_Phone
        phones          query      PAP.Phone                 PAP.Subject_has_Phone
        property_links  query      PAP.Subject_has_Property  PAP.Subject_has_Property
        url_links       query      PAP.Subject_has_Url       PAP.Subject_has_Url
        urls            query      PAP.Url                   PAP.Subject_has_Url
    ..PAP.Company
        address_links   query      PAP.Company_has_Address   PAP.Company_has_Address
        addresses       query      PAP.Address               PAP.Company_has_Address
        created_by      computed   MOM.Id_Entity
        email_links     query      PAP.Company_has_Email     PAP.Company_has_Email
        emails          query      PAP.Email                 PAP.Company_has_Email
        last_changed_by computed   MOM.Id_Entity
        phone_links     query      PAP.Company_has_Phone     PAP.Company_has_Phone
        phones          query      PAP.Phone                 PAP.Company_has_Phone
        property_links  query      PAP.Subject_has_Property  PAP.Subject_has_Property
        url_links       query      PAP.Company_has_Url       PAP.Company_has_Url
        urls            query      PAP.Url                   PAP.Company_has_Url
    ...PAP.Company_P
        address_links   query      PAP.Company_has_Address   PAP.Company_has_Address
        addresses       query      PAP.Address               PAP.Company_has_Address
        affiliate       optional   PAP.Company_P
        created_by      computed   MOM.Id_Entity
        email_links     query      PAP.Company_has_Email     PAP.Company_has_Email
        emails          query      PAP.Email                 PAP.Company_has_Email
        last_changed_by computed   MOM.Id_Entity
        owner           primary    PAP.Biz_Man
        phone_links     query      PAP.Company_has_Phone     PAP.Company_has_Phone
        phones          query      PAP.Phone                 PAP.Company_has_Phone
        property_links  query      PAP.Subject_has_Property  PAP.Subject_has_Property
        url_links       query      PAP.Company_has_Url       PAP.Company_has_Url
        urls            query      PAP.Url                   PAP.Company_has_Url
    ..PAP.Association
        address_links   query      PAP.Association_has_Addre PAP.Association_has_Address
        addresses       query      PAP.Address               PAP.Association_has_Address
        created_by      computed   MOM.Id_Entity
        email_links     query      PAP.Association_has_Email PAP.Association_has_Email
        emails          query      PAP.Email                 PAP.Association_has_Email
        last_changed_by computed   MOM.Id_Entity
        phone_links     query      PAP.Association_has_Phone PAP.Association_has_Phone
        phones          query      PAP.Phone                 PAP.Association_has_Phone
        property_links  query      PAP.Subject_has_Property  PAP.Subject_has_Property
        url_links       query      PAP.Association_has_Url   PAP.Association_has_Url
        urls            query      PAP.Url                   PAP.Association_has_Url
    .PAP.Person
        account_links   query      PAP.Person_has_Account    PAP.Person_has_Account
        accounts        query      Auth.Account              PAP.Person_has_Account
        address_links   query      PAP.Person_has_Address    PAP.Person_has_Address
        addresses       query      PAP.Address               PAP.Person_has_Address
        biz_man         query      PAP.Biz_Man               PAP.Biz_Man
        created_by      computed   MOM.Id_Entity
        email_links     query      PAP.Person_has_Email      PAP.Person_has_Email
        emails          query      PAP.Email                 PAP.Person_has_Email
        last_changed_by computed   MOM.Id_Entity
        phone_links     query      PAP.Person_has_Phone      PAP.Person_has_Phone
        phones          query      PAP.Phone                 PAP.Person_has_Phone
        property_links  query      PAP.Subject_has_Property  PAP.Subject_has_Property
        sailors         query      SRM.Sailor                SRM.Sailor
        url_links       query      PAP.Person_has_Url        PAP.Person_has_Url
        urls            query      PAP.Url                   PAP.Person_has_Url

    >>> seen = set ()
    >>> show_T_attrs (MOM.Id_Entity, "%%s%%-35s %%-10s %%-25.25s %%s", set (), sk)
    MOM.Id_Entity
        created_by                          computed   MOM.Id_Entity
        last_changed_by                     computed   MOM.Id_Entity
    .MOM.Link
    ..MOM.Link1
    ...Auth.Link1
    ....Auth._Account_Action_
        left                                primary    Auth.Account              Auth._Account_Action_
    .....Auth._Account_Token_Action_
    ...EVT.Link1
    ....EVT._Recurrence_Mixin_
    .....EVT.Recurrence_Spec
        left                                primary    EVT.Event                 EVT.Recurrence_Spec
        rules                               query      EVT.Recurrence_Rule       EVT.Recurrence_Rule
    .....EVT.Recurrence_Rule
        left                                primary    EVT.Recurrence_Spec       EVT.Recurrence_Rule
    ....EVT.Event
        calendar                            primary    EVT.Calendar
        left                                primary    SWP.Page                  EVT.Event
        occurs                              query      EVT.Event_occurs          EVT.Event_occurs
        recurrence                          query      EVT.Recurrence_Spec       EVT.Recurrence_Spec
    ....EVT.Event_occurs
        essence                             computed   MOM.Id_Entity
    ...PAP.Link1
    ....PAP.Address_Position
        left                                primary    PAP.Address               PAP.Address_Position
    ....PAP.Biz_Man
        left                                primary    PAP.Person                PAP.Biz_Man
        owns                                query      PAP.Company_P             PAP.Company_P
    ...SRM.Link1
    ....SRM._Regatta_
        boat_class                          primary    SRM._Boat_Class_
        left                                primary    SRM.Regatta_Event         SRM._Regatta_
    .....SRM.Regatta
        boats                               query      SRM.Boat_in_Regatta       SRM.Boat_in_Regatta
    ......SRM.Regatta_C
        boat_class                          primary    SRM.Boat_Class
        teams                               query      SRM.Team                  SRM.Team
    ......SRM.Regatta_H
        boat_class                          primary    SRM.Handicap
    ....SRM.Boat
        left                                primary    SRM.Boat_Class            SRM.Boat
        regatta_links                       query      SRM.Boat_in_Regatta       SRM.Boat_in_Regatta
    ....SRM.Sailor
        boat_in_regatta_links               query      SRM.Crew_Member           SRM.Crew_Member
        club                                primary    SRM.Club
    ....SRM.Race_Result
        left                                primary    SRM.Boat_in_Regatta       SRM.Race_Result
    ....SRM.Team
        boat_links                          query      SRM.Team_has_Boat_in_Rega SRM.Team_has_Boat_in_Regatta
        leader                              optional   PAP.Person
        left                                primary    SRM.Regatta_C             SRM.Team
    ...SWP.Link1
    ....SWP.Clip_O
        left                                primary    SWP.Object_PN             SWP.Clip_O
    ....SWP.Picture
        left                                primary    SWP.Gallery               SWP.Picture
    ..MOM._MOM_Link_n_
    ...MOM.Link2
    ....Auth.Link2
    .....Auth.Account_in_Group
        right                               primary    Auth.Group                Auth.Account_in_Group
    ....PAP.Link2
    .....PAP.Subject_has_Property
        left                                primary    PAP.Subject               PAP.Subject_has_Property
        right                               primary    PAP.Property              PAP.Subject_has_Property
    ......PAP.Subject_has_Address
        right                               primary    PAP.Address               PAP.Subject_has_Address
    .......PAP.Company_has_Address
        left                                primary    PAP.Company               PAP.Company_has_Address
    .......PAP.Association_has_Address
        left                                primary    PAP.Association           PAP.Association_has_Address
    ......PAP.Subject_has_Email
        right                               primary    PAP.Email                 PAP.Subject_has_Email
    ......PAP.Subject_has_Phone
        right                               primary    PAP.Phone                 PAP.Subject_has_Phone
    ......PAP.Subject_has_Url
        right                               primary    PAP.Url                   PAP.Subject_has_Url
    .....PAP.Person_has_Account
        right                               primary    Auth.Account              PAP.Person_has_Account
    ....SRM.Link2
    .....SRM.Boat_in_Regatta
        _crew                               query      SRM.Sailor                SRM.Crew_Member
        left                                primary    SRM.Boat                  SRM.Boat_in_Regatta
        race_results                        query      SRM.Race_Result           SRM.Race_Result
        right                               primary    SRM.Regatta               SRM.Boat_in_Regatta
        sailor_links                        query      SRM.Crew_Member           SRM.Crew_Member
        skipper                             required   SRM.Sailor
        team_links                          query      SRM.Team_has_Boat_in_Rega SRM.Team_has_Boat_in_Regatta
    .....SRM.Crew_Member
        right                               primary    SRM.Sailor                SRM.Crew_Member
    .....SRM.Team_has_Boat_in_Regatta
        left                                primary    SRM.Team                  SRM.Team_has_Boat_in_Regatta
        right                               primary    SRM.Boat_in_Regatta       SRM.Team_has_Boat_in_Regatta
    ...Auth._MOM_Link_n_
    ...PAP._MOM_Link_n_
    ...SRM._MOM_Link_n_
    ..Auth.Link
    ..EVT.Link
    ..PAP.Link
    ..SRM.Link
    ..SWP.Link
    .MOM.Object
    ..Auth.Object
    ...Auth._Account_
    ....Auth.Account
        _account_action_s                   query      Auth._Account_Action_     Auth._Account_Action_
        _account_token_action_s             query      Auth._Account_Token_Actio Auth._Account_Token_Action_
        account_email_verifications         query      Auth.Account_EMail_Verifi Auth.Account_EMail_Verification
        account_password_resets             query      Auth.Account_Password_Res Auth.Account_Password_Reset
        activation                          query      Auth.Account_Activation   Auth.Account_Activation
        activations                         query      Auth.Account_Activation   Auth.Account_Activation
        group_links                         query      Auth.Account_in_Group     Auth.Account_in_Group
        groups                              query      Auth.Group                Auth.Account_in_Group
        password_change_required            query      Auth.Account_Password_Cha Auth.Account_Password_Change_Required
        password_change_requireds           query      Auth.Account_Password_Cha Auth.Account_Password_Change_Required
        person                              query      PAP.Person                PAP.Person_has_Account
        person_link                         query      PAP.Person_has_Account    PAP.Person_has_Account
        person_links                        query      PAP.Person_has_Account    PAP.Person_has_Account
    ...Auth.Group
        account_links                       query      Auth.Account_in_Group     Auth.Account_in_Group
        accounts                            query      Auth.Account              Auth.Account_in_Group
    ..EVT.Object
    ..SWP.Object
    ...SWP.Object_PN
        clips                               query      SWP.Clip_O                SWP.Clip_O
    ....SWP.Page
        events                              query      EVT.Event                 EVT.Event
    .....SRM.Page
        event                               primary    SRM.Regatta_Event
    ....SWP.Gallery
        pictures                            query      SWP.Picture               SWP.Picture
    ..PAP.Object
    ...PAP.Property
        subject_links                       query      PAP.Subject_has_Property  PAP.Subject_has_Property
    ....PAP.Address
        association_links                   query      PAP.Association_has_Addre PAP.Association_has_Address
        associations                        query      PAP.Association           PAP.Association_has_Address
        companies                           query      PAP.Company               PAP.Company_has_Address
        company_links                       query      PAP.Company_has_Address   PAP.Company_has_Address
        gps                                 query      PAP.Address_Position      PAP.Address_Position
        person_links                        query      PAP.Person_has_Address    PAP.Person_has_Address
        persons                             query      PAP.Person                PAP.Person_has_Address
        subject_links                       query      PAP.Subject_has_Address   PAP.Subject_has_Address
    ....PAP.Email
        association_links                   query      PAP.Association_has_Email PAP.Association_has_Email
        company_links                       query      PAP.Company_has_Email     PAP.Company_has_Email
        person_links                        query      PAP.Person_has_Email      PAP.Person_has_Email
        subject_links                       query      PAP.Subject_has_Email     PAP.Subject_has_Email
    ....PAP.Phone
        association_links                   query      PAP.Association_has_Phone PAP.Association_has_Phone
        company_links                       query      PAP.Company_has_Phone     PAP.Company_has_Phone
        person_links                        query      PAP.Person_has_Phone      PAP.Person_has_Phone
        subject_links                       query      PAP.Subject_has_Phone     PAP.Subject_has_Phone
    ....PAP.Url
        association_links                   query      PAP.Association_has_Url   PAP.Association_has_Url
        company_links                       query      PAP.Company_has_Url       PAP.Company_has_Url
        person_links                        query      PAP.Person_has_Url        PAP.Person_has_Url
        subject_links                       query      PAP.Subject_has_Url       PAP.Subject_has_Url
    ...PAP.Subject
        address_links                       query      PAP.Subject_has_Address   PAP.Subject_has_Address
        addresses                           query      PAP.Address               PAP.Subject_has_Address
        email_links                         query      PAP.Subject_has_Email     PAP.Subject_has_Email
        emails                              query      PAP.Email                 PAP.Subject_has_Email
        phone_links                         query      PAP.Subject_has_Phone     PAP.Subject_has_Phone
        phones                              query      PAP.Phone                 PAP.Subject_has_Phone
        property_links                      query      PAP.Subject_has_Property  PAP.Subject_has_Property
        url_links                           query      PAP.Subject_has_Url       PAP.Subject_has_Url
        urls                                query      PAP.Url                   PAP.Subject_has_Url
    ....PAP.Legal_Entity
    .....PAP.Company
        address_links                       query      PAP.Company_has_Address   PAP.Company_has_Address
        email_links                         query      PAP.Company_has_Email     PAP.Company_has_Email
        phone_links                         query      PAP.Company_has_Phone     PAP.Company_has_Phone
        url_links                           query      PAP.Company_has_Url       PAP.Company_has_Url
    ......PAP.Company_P
        affiliate                           optional   PAP.Company_P
        owner                               primary    PAP.Biz_Man
    .....PAP.Association
        address_links                       query      PAP.Association_has_Addre PAP.Association_has_Address
        email_links                         query      PAP.Association_has_Email PAP.Association_has_Email
        phone_links                         query      PAP.Association_has_Phone PAP.Association_has_Phone
        url_links                           query      PAP.Association_has_Url   PAP.Association_has_Url
    ....PAP.Person
        account_links                       query      PAP.Person_has_Account    PAP.Person_has_Account
        address_links                       query      PAP.Person_has_Address    PAP.Person_has_Address
        biz_man                             query      PAP.Biz_Man               PAP.Biz_Man
        email_links                         query      PAP.Person_has_Email      PAP.Person_has_Email
        phone_links                         query      PAP.Person_has_Phone      PAP.Person_has_Phone
        sailors                             query      SRM.Sailor                SRM.Sailor
        url_links                           query      PAP.Person_has_Url        PAP.Person_has_Url
    ..SRM.Object
    ...SRM._Boat_Class_
    ....SRM.Boat_Class
        boats                               query      SRM.Boat                  SRM.Boat
    ...SRM.Regatta_Event
        regattas                            query      SRM._Regatta_             SRM._Regatta_
    .Auth.Id_Entity
    .EVT.Id_Entity
    .SWP.Id_Entity
    .PAP.Id_Entity
    .SRM.Id_Entity

    >>> for T, l in sorted (children_trans_iter (MOM.Id_Entity), key = TFL.Getter [0].type_name):
    ...     if T.link_ref_attr and not T.is_partial :
    ...         print (T.type_name)
    ...         for a in T.link_ref_attr :
    ...             if a.Ref_Type.show_in_ui :
    ...                  print (" " * 3, a.name)
    Auth.Account
        group_links
        person_links
    Auth.Group
        account_links
    EVT.Event
        occurs
    EVT.Recurrence_Spec
        rules
    PAP.Address
        subject_links
        company_links
        person_links
        association_links
    PAP.Association
        property_links
        url_links
        phone_links
        email_links
        address_links
    PAP.Company
        property_links
        url_links
        phone_links
        email_links
        address_links
    PAP.Company_P
        property_links
        url_links
        phone_links
        email_links
        address_links
    PAP.Email
        subject_links
        company_links
        person_links
        association_links
    PAP.Person
        property_links
        account_links
        sailors
        url_links
        phone_links
        email_links
        address_links
    PAP.Phone
        subject_links
        company_links
        person_links
        association_links
    PAP.Url
        subject_links
        company_links
        person_links
        association_links
    SRM.Boat
        regatta_links
    SRM.Boat_Class
        boats
    SRM.Boat_in_Regatta
        race_results
        sailor_links
        team_links
    SRM.Page
        events
        clips
    SRM.Regatta_C
        boats
        teams
    SRM.Regatta_Event
        regattas
    SRM.Regatta_H
        boats
    SRM.Sailor
        boat_in_regatta_links
    SRM.Team
        boat_links
    SWP.Clip_X
        events
        clips
    SWP.Gallery
        clips
        pictures
    SWP.Page
        events
        clips
    SWP.Page_Y
        events
        clips

    >>> for T, l in sorted (children_trans_iter (MOM.Id_Entity), key = TFL.Getter [0].type_name):
    ...     if T.rev_ref_attr and not T.is_partial :
    ...         print (T.type_name)
    ...         for a in T.rev_ref_attr :
    ...             if a.Ref_Type.show_in_ui :
    ...                  print (" " * 3, a.name)
    Auth.Account
        creation
        last_change
        group_links
        groups
        person
        person_links
        person_link
    Auth.Account_Activation
        creation
        last_change
    Auth.Account_Anonymous
        creation
        last_change
    Auth.Account_EMail_Verification
        creation
        last_change
    Auth.Account_Password_Change_Required
        creation
        last_change
    Auth.Account_Password_Reset
        creation
        last_change
    Auth.Account_in_Group
        creation
        last_change
    Auth.Certificate
        creation
        last_change
    Auth.Group
        creation
        last_change
        accounts
        account_links
    EVT.Calendar
        creation
        last_change
    EVT.Event
        creation
        last_change
        occurs
        recurrence
    EVT.Event_occurs
        creation
        last_change
    EVT.Recurrence_Rule
        creation
        last_change
    EVT.Recurrence_Spec
        creation
        last_change
        rules
    PAP.Address
        creation
        last_change
        gps
        subject_links
        companies
        company_links
        persons
        person_links
        associations
        association_links
    PAP.Address_Position
        creation
        last_change
    PAP.Association
        creation
        last_change
        property_links
        url_links
        urls
        phone_links
        phones
        email_links
        emails
        address_links
        addresses
    PAP.Association_has_Address
        creation
        last_change
    PAP.Association_has_Email
        creation
        last_change
    PAP.Association_has_Phone
        creation
        last_change
    PAP.Association_has_Url
        creation
        last_change
    PAP.Biz_Man
        creation
        last_change
        owns
    PAP.Company
        creation
        last_change
        property_links
        url_links
        urls
        phone_links
        phones
        email_links
        emails
        address_links
        addresses
    PAP.Company_P
        creation
        last_change
        property_links
        url_links
        urls
        phone_links
        phones
        email_links
        emails
        address_links
        addresses
    PAP.Company_has_Address
        creation
        last_change
    PAP.Company_has_Email
        creation
        last_change
    PAP.Company_has_Phone
        creation
        last_change
    PAP.Company_has_Url
        creation
        last_change
    PAP.Email
        creation
        last_change
        subject_links
        companies
        company_links
        persons
        person_links
        associations
        association_links
    PAP.Person
        creation
        last_change
        property_links
        account_links
        accounts
        sailors
        biz_man
        url_links
        urls
        phone_links
        phones
        email_links
        emails
        address_links
        addresses
    PAP.Person_has_Account
        creation
        last_change
    PAP.Person_has_Address
        creation
        last_change
    PAP.Person_has_Email
        creation
        last_change
    PAP.Person_has_Phone
        creation
        last_change
    PAP.Person_has_Url
        creation
        last_change
    PAP.Phone
        creation
        last_change
        subject_links
        companies
        company_links
        persons
        person_links
        associations
        association_links
    PAP.Url
        creation
        last_change
        subject_links
        companies
        company_links
        persons
        person_links
        associations
        association_links
    SRM.Boat
        creation
        last_change
        regatta_links
    SRM.Boat_Class
        creation
        last_change
        boats
    SRM.Boat_in_Regatta
        creation
        last_change
        race_results
        sailor_links
        _crew
        teams
        team_links
    SRM.Club
        creation
        last_change
    SRM.Crew_Member
        creation
        last_change
    SRM.Handicap
        creation
        last_change
    SRM.Page
        creation
        last_change
        events
        clips
    SRM.Race_Result
        creation
        last_change
    SRM.Regatta_C
        creation
        last_change
        boats
        teams
    SRM.Regatta_Event
        creation
        last_change
        regattas
    SRM.Regatta_H
        creation
        last_change
        boats
    SRM.Sailor
        creation
        last_change
        boat_in_regatta_links
    SRM.Team
        creation
        last_change
        boat_links
        boats
    SRM.Team_has_Boat_in_Regatta
        creation
        last_change
    SWP.Clip_O
        creation
        last_change
    SWP.Clip_X
        creation
        last_change
        events
        clips
    SWP.Gallery
        creation
        last_change
        clips
        pictures
    SWP.Page
        creation
        last_change
        events
        clips
    SWP.Page_Y
        creation
        last_change
        events
        clips
    SWP.Picture
        creation
        last_change

    >>> for T, l in sorted (children_trans_iter (MOM.Id_Entity), key = TFL.Getter [0].type_name):
    ...     print ("%%-40s %%s" %% (T.type_name, T.show_in_ui))
    Auth.Account                             True
    Auth.Account_Activation                  False
    Auth.Account_Anonymous                   False
    Auth.Account_EMail_Verification          False
    Auth.Account_Password_Change_Required    False
    Auth.Account_Password_Reset              False
    Auth.Account_in_Group                    True
    Auth.Certificate                         True
    Auth.Group                               True
    Auth.Id_Entity                           True
    Auth.Link                                True
    Auth.Link1                               True
    Auth.Link2                               True
    Auth.Object                              True
    Auth._Account_                           True
    Auth._Account_Action_                    False
    Auth._Account_Token_Action_              False
    Auth._MOM_Link_n_                        True
    EVT.Calendar                             True
    EVT.Event                                True
    EVT.Event_occurs                         True
    EVT.Id_Entity                            True
    EVT.Link                                 True
    EVT.Link1                                True
    EVT.Object                               True
    EVT.Recurrence_Rule                      True
    EVT.Recurrence_Spec                      True
    EVT._Recurrence_Mixin_                   True
    MOM.Id_Entity                            True
    MOM.Link                                 True
    MOM.Link1                                True
    MOM.Link2                                True
    MOM.Link3                                False
    MOM.Object                               True
    MOM._MOM_Link_n_                         True
    PAP.Address                              True
    PAP.Address_Position                     True
    PAP.Association                          True
    PAP.Association_has_Address              True
    PAP.Association_has_Email                True
    PAP.Association_has_Phone                True
    PAP.Association_has_Url                  True
    PAP.Biz_Man                              True
    PAP.Company                              True
    PAP.Company_P                            True
    PAP.Company_has_Address                  True
    PAP.Company_has_Email                    True
    PAP.Company_has_Phone                    True
    PAP.Company_has_Url                      True
    PAP.Email                                True
    PAP.Id_Entity                            True
    PAP.Legal_Entity                         True
    PAP.Link                                 True
    PAP.Link1                                True
    PAP.Link2                                True
    PAP.Object                               True
    PAP.Person                               True
    PAP.Person_has_Account                   True
    PAP.Person_has_Address                   True
    PAP.Person_has_Email                     True
    PAP.Person_has_Phone                     True
    PAP.Person_has_Url                       True
    PAP.Phone                                True
    PAP.Property                             True
    PAP.Subject                              True
    PAP.Subject_has_Address                  True
    PAP.Subject_has_Email                    True
    PAP.Subject_has_Phone                    True
    PAP.Subject_has_Property                 True
    PAP.Subject_has_Url                      True
    PAP.Url                                  True
    PAP._MOM_Link_n_                         True
    SRM.Boat                                 True
    SRM.Boat_Class                           True
    SRM.Boat_in_Regatta                      True
    SRM.Club                                 True
    SRM.Crew_Member                          True
    SRM.Handicap                             True
    SRM.Id_Entity                            True
    SRM.Link                                 True
    SRM.Link1                                True
    SRM.Link2                                True
    SRM.Object                               True
    SRM.Page                                 True
    SRM.Race_Result                          True
    SRM.Regatta                              True
    SRM.Regatta_C                            True
    SRM.Regatta_Event                        True
    SRM.Regatta_H                            True
    SRM.Sailor                               True
    SRM.Team                                 True
    SRM.Team_has_Boat_in_Regatta             True
    SRM._Boat_Class_                         True
    SRM._MOM_Link_n_                         True
    SRM._Regatta_                            True
    SWP.Clip_O                               True
    SWP.Clip_X                               True
    SWP.Gallery                              True
    SWP.Id_Entity                            True
    SWP.Link                                 True
    SWP.Link1                                True
    SWP.Object                               True
    SWP.Object_PN                            True
    SWP.Page                                 True
    SWP.Page_Y                               True
    SWP.Picture                              True

"""

_test_saw = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP

    >>> print (PAP.Biz_Man.query ())
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_biz_man."left" AS pap_biz_man_left,
           pap_biz_man.pid AS pap_biz_man_pid
         FROM mom_id_entity
           JOIN pap_biz_man ON mom_id_entity.pid = pap_biz_man.pid


    >>> print (PAP.Subject._SAW.sa_joins_strict)
    mom_id_entity

    >>> print (PAP.Subject._SAW.sa_joins)
    mom_id_entity
      LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
      LEFT OUTER JOIN pap_company_p ON pap_company.pid = pap_company_p.pid
      LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
      LEFT OUTER JOIN pap_association ON mom_id_entity.pid = pap_association.pid

    >>> print (PAP.Subject.query ())
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_association.__raw_name AS pap_association___raw_name,
           pap_association.__raw_short_name AS pap_association___raw_short_name,
           pap_association.lifetime__finish AS pap_association_lifetime__finish,
           pap_association.lifetime__start AS pap_association_lifetime__start,
           pap_association.name AS pap_association_name,
           pap_association.pid AS pap_association_pid,
           pap_association.short_name AS pap_association_short_name,
           pap_company.__raw_name AS pap_company___raw_name,
           pap_company.__raw_registered_in AS pap_company___raw_registered_in,
           pap_company.__raw_short_name AS pap_company___raw_short_name,
           pap_company.lifetime__finish AS pap_company_lifetime__finish,
           pap_company.lifetime__start AS pap_company_lifetime__start,
           pap_company.name AS pap_company_name,
           pap_company.pid AS pap_company_pid,
           pap_company.registered_in AS pap_company_registered_in,
           pap_company.short_name AS pap_company_short_name,
           pap_company_p.affiliate AS pap_company_p_affiliate,
           pap_company_p.owner AS pap_company_p_owner,
           pap_company_p.pid AS pap_company_p_pid,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
           LEFT OUTER JOIN pap_company_p ON pap_company.pid = pap_company_p.pid
           LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
           LEFT OUTER JOIN pap_association ON mom_id_entity.pid = pap_association.pid
         WHERE mom_id_entity.pid = pap_company.pid
            OR mom_id_entity.pid = pap_company_p.pid
            OR mom_id_entity.pid = pap_person.pid
            OR mom_id_entity.pid = pap_association.pid

    >>> p1 = PAP.Person ("Doe", "Jane", lifetime = ("20010101", ), raw = True)
    >>> bm = PAP.Biz_Man (p1)
    >>> cp = PAP.Company_P ("Doe, Inc.", bm, raw = True)
    >>> ta = PAP.Association ("Towel Carriers Association", short_name = "TCA", raw = True)
    >>> cq = PAP.Company_P ("Jane's, Inc.", bm)


"""

from   _GTW.__test__.model      import *
from   _MOM.import_MOM          import Q
from   _MOM.inspect             import children_trans_iter

import _GTW._OMP._PAP.Association
import _GTW._RST._TOP._MOM.Query_Restriction

_Ancestor_Essence = GTW.OMP.PAP.Link1

class Biz_Man (_Ancestor_Essence) :
    """Russian in business"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Network device the interface is connected to."""

            role_type           = GTW.OMP.PAP.Person
            role_name           = "man"
            max_links           = 1
            link_ref_singular   = True

        # end class left

    # end class _Attributes

# end class Biz_Man

_Ancestor_Essence = GTW.OMP.PAP.Company

class Company_P (_Ancestor_Essence) :
    """Company owned and operated by a single person"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class owner (A_Id_Entity) :
            """Owner of the company"""

            kind               = Attr.Primary
            P_Type             = Biz_Man
            rev_ref_attr_name  = "owns"

        # end class owner

        class affiliate  (A_Id_Entity) :
            """Affiliate of the company"""

            kind               = Attr.Optional
            P_Type             = "GTW.OMP.PAP.Company_P"

        # end class affiliate

    # end class _Attributes

# end class Company_P

def T_attrs (T, seen = None) :
    if seen is None :
        seen = set ()
    Ref_Attr_Types = \
        ( MOM.Attr._A_Id_Entity_
        , MOM.Attr._A_Id_Entity_Collection_
        )
    def _gen () :
        for n, a in sorted (T.attributes.iteritems ()) :
            attr = a.attr
            PT   = attr.P_Type
            if PT and isinstance (attr, Ref_Attr_Types) :
                key = (attr.name, PT.type_name)
                if key not in seen :
                    seen.add (key)
                    yield n, a, PT
    return sorted (_gen ())
# end def T_attrs

def show_T_attrs (Root, format, seen, sk, lead = ".") :
    for (T, l) in children_trans_iter (Root, sort_key = sk) :
        attrs = T_attrs (T, seen)
        if attrs or T.children :
            print ("%s%s" % (lead * l, T.type_name))
            for n, a, PT in attrs :
                RT = getattr (getattr (a, "Ref_Type", None), "type_name", "")
                if not RT :
                    RT = getattr (a, "assoc", "")
                    if not isinstance (RT, basestring) :
                        RT = getattr (RT, "type_name", "")
                if RT.startswith ("GTW.OMP.") :
                    RT = RT [len ("GTW.OMP."):]
                line = format % (" " * 4, a.name, a.kind, PT.type_name, RT)
                print (line.rstrip ())
# end def show_T_attrs

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_main        = _test_code
        , test_entity_attr = _test_entity_attr
        )
    )

__test__.update \
    ( Scaffold.create_test_dict \
        ( dict
            ( test_saw     = _test_saw
            )
        , ignore           = ("HPS", "MYS")
        )
    )

### __END__ GTW.__test__.Company
