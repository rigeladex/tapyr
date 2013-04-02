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

    >>> print (PAP.Association.E_Type.name.description)
    Name of association.

    >>> print (PAP.Company.E_Type.name.description)
    Name of company.

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
    <owner.left.salutation.AQ [Attr.Type.Querier String]> -----
    <owner.left.sex.AQ [Attr.Type.Querier Ckd]> -----
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
    <affiliate.owner.left.salutation.AQ [Attr.Type.Querier String]> -----
    <affiliate.owner.left.sex.AQ [Attr.Type.Querier Ckd]> -----
    <affiliate.registered_in.AQ [Attr.Type.Querier String]> -----
    <affiliate.lifetime.AQ [Attr.Type.Querier Composite]> MOM.Date_Interval
    <affiliate.lifetime.start.AQ [Attr.Type.Querier Date]> -----
    <affiliate.lifetime.finish.AQ [Attr.Type.Querier Date]> -----
    <affiliate.lifetime.alive.AQ [Attr.Type.Querier Boolean]> -----
    <affiliate.short_name.AQ [Attr.Type.Querier String]> -----
    <affiliate.affiliate.AQ [Attr.Type.Querier Id_Entity]> PAP.Company_P

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
    <owner.left.salutation.AQ [Attr.Type.Querier String]>
    <owner.left.sex.AQ [Attr.Type.Querier Ckd]>
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
    <affiliate.owner.left.salutation.AQ [Attr.Type.Querier String]>
    <affiliate.owner.left.sex.AQ [Attr.Type.Querier Ckd]>
    <affiliate.registered_in.AQ [Attr.Type.Querier String]>
    <affiliate.lifetime.start.AQ [Attr.Type.Querier Date]>
    <affiliate.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <affiliate.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <affiliate.short_name.AQ [Attr.Type.Querier String]>

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
                    , { 'name' : 'salutation'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Salutation'
                      }
                    , { 'name' : 'sex'
                      , 'sig_key' : 0
                      , 'ui_name' : 'Sex'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Man'
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
                          , { 'name' : 'salutation'
                            , 'sig_key' : 3
                            , 'ui_name' : 'Salutation'
                            }
                          , { 'name' : 'sex'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Sex'
                            }
                          ]
                      , 'name' : 'left'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Man'
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
              ]
          , 'name' : 'affiliate'
          , 'sig_key' : 2
          , 'ui_name' : 'Affiliate'
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
                  ( attr = String `salutation`
                  , full_name = 'owner.left.salutation'
                  , id = 'owner__left__salutation'
                  , name = 'salutation'
                  , sig_key = 3
                  , ui_name = 'Owner/Man/Salutation'
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
                ]
            , full_name = 'owner.left'
            , id = 'owner__left'
            , name = 'left'
            , sig_key = 2
            , type_name = 'PAP.Person'
            , ui_name = 'Owner/Man'
            )
          ]
      , full_name = 'owner'
      , id = 'owner'
      , name = 'owner'
      , sig_key = 2
      , type_name = 'PAP.Biz_Man'
      , ui_name = 'Owner'
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
                        ( attr = String `salutation`
                        , full_name = 'affiliate.owner.left.salutation'
                        , id = 'affiliate__owner__left__salutation'
                        , name = 'salutation'
                        , sig_key = 3
                        , ui_name = 'Affiliate/Owner/Man/Salutation'
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
                      ]
                  , full_name = 'affiliate.owner.left'
                  , id = 'affiliate__owner__left'
                  , name = 'left'
                  , sig_key = 2
                  , type_name = 'PAP.Person'
                  , ui_name = 'Affiliate/Owner/Man'
                  )
                ]
            , full_name = 'affiliate.owner'
            , id = 'affiliate__owner'
            , name = 'owner'
            , sig_key = 2
            , type_name = 'PAP.Biz_Man'
            , ui_name = 'Affiliate/Owner'
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
            )
          ]
      , full_name = 'affiliate'
      , id = 'affiliate'
      , name = 'affiliate'
      , sig_key = 2
      , type_name = 'PAP.Company_P'
      , ui_name = 'Affiliate'
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

            role_type          = GTW.OMP.PAP.Person
            role_name          = "man"

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

        # end class owner

        class affiliate  (A_Id_Entity) :
            """Affiliate of the company"""

            kind               = Attr.Optional
            P_Type             = "GTW.OMP.PAP.Company_P"

        # end class affiliate

    # end class _Attributes

# end class Company_P

__test__ = Scaffold.create_test_dict \
    ( dict
        ( main          = _test_code
        )
    )

### __END__ GTW.__test__.Company
