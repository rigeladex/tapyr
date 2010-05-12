# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.MOM.__test__
#
# Purpose
#    Basic test for the MOM based form handling
#
# Revision Dates
#     5-Feb-2010 (MG) Creation
#     6-Feb-2010 (MG) Doctest for renaming a link fixed
#    12-May-2010 (CT) Use `pid`, not `lid`
#    ««revision-date»»···
#--

_object_test = r"""
    >>> scope = MOM.Scope.new (apt, None)
    >>> PAP   = scope.PAP
    >>> simp_per_form_cls = GTW.Form.MOM.Instance.New (PAP.Person)

Each form class has a fields NO-List containing all fields of all field groups.

    >>> [f.name for f in simp_per_form_cls.fields]
    ['last_name', 'first_name', 'middle_name', 'title', 'lifetime', 'instance_state']
    >>> fields_of_field_groups (simp_per_form_cls)
    ['last_name', 'first_name', 'middle_name', 'title', 'lifetime']

As wen can see, for each user editable attribute a field will be added to the
form.
In addtion, a field called *instance_state* will be added as well. This field
is used to check whether the user has actually changed any value.

It is also possible to use field group descriptions to define which fields
and in what order the fields should be part of the form:

    >>> form_cls = GTW.Form.MOM.Instance.New \
    ...     ( PAP.Person
    ...     , FGD ("title")
    ...     , FGD ("first_name", "last_name", "middle_name")
    ...     , FGD (AID ("lifetime"))
    ...     )
    >>> [f.name for f in form_cls.fields]
    ['title', 'first_name', 'last_name', 'middle_name', 'lifetime', 'instance_state']
    >>> fields_of_field_groups (form_cls)
    ['title']
    ['first_name', 'last_name', 'middle_name']
    ['lifetime']

Instead of listing the field names it is possible to use wildcard field
descriptions:

    >>> form_cls = GTW.Form.MOM.Instance.New \
    ...     ( PAP.Person
    ...     , FGD ("title")
    ...     , FGD ("first_name", "last_name", WF  ())
    ...     )
    >>> [f.name for f in form_cls.fields]
    ['title', 'first_name', 'last_name', 'middle_name', 'lifetime', 'instance_state']
    >>> fields_of_field_groups (form_cls)
    ['title']
    ['first_name', 'last_name', 'middle_name', 'lifetime']

    >>> form_cls = GTW.Form.MOM.Instance.New \
    ...     ( PAP.Person
    ...     , FGD (WF ("primary"))
    ...     , FGD ()
    ...     )
    >>> [f.name for f in form_cls.fields]
    ['last_name', 'first_name', 'middle_name', 'title', 'lifetime', 'instance_state']
    >>> fields_of_field_groups (form_cls)
    ['last_name', 'first_name', 'middle_name', 'title']
    ['lifetime']

The wildcard field can now be place anywhere in the list of field and will
only expand to the fields not explicitly list in any other field group
description.

    >>> form_cls = GTW.Form.MOM.Instance.New \
    ...     ( PAP.Person
    ...     , FGD ("title")
    ...     , FGD ("first_name", WF ())
    ...     , FGD ("lifetime")
    ...     )
    >>> [f.name for f in form_cls.fields]
    ['title', 'first_name', 'last_name', 'middle_name', 'lifetime', 'instance_state']
    >>> fields_of_field_groups (form_cls)
    ['title']
    ['first_name', 'last_name', 'middle_name']
    ['lifetime']

Now that we have learned how the create form classes, let's see what we can
do with instance of such forms. The form itself expects the post url as first
parameter and a possible exiting object (for an edit operation) as second
parameter. But for now, we just consider the create case.

    >>> form = form_cls ("/post-url/")

The raw_values dict holdes the values which will be used as default values
for the HTML fields
    >>> for i in sorted (form.raw_values.iteritems ()) : print i
    ('Person__first_name', u'')
    ('Person__instance_state', 'KGRwMQpTJ2xpZmV0aW1lJwpwMgooZHAzClMncmF3JwpwNApJMDEKc3NTJ2ZpcnN0X25hbWUnCnA1ClYKc1MnbGFzdF9uYW1lJwpwNgpWCnNTJ21pZGRsZV9uYW1lJwpwNwpWCnNTJ3RpdGxlJwpwOApWCnMu')
    ('Person__last_name', u'')
    ('Person__lifetime', {'raw': True})
    ('Person__middle_name', u'')
    ('Person__title', u'')

Once we receive the data from the browser we *call* the form instance and
pass along the request_data
    >>> request_data = dict ()
    >>> form (request_data)
    0
    >>> dump_form_errors (form)

Since we did not pass any request data the process does not report any error
but will not create any instance as well:
    >>> form.instance is None
    True

Now, let's pass some real data to the form:
    >>> form = form_cls ("/post-url/")
    >>> request_data ["Person__instance_state"] = "KGRwMQpTJ2xpZmV0aW1lJwpwMgpWCnNTJ2ZpcnN0X25hbWUnCnAzClYKc1MnbGFzdF9uYW1lJwpwNApWCnNTJ21pZGRsZV9uYW1lJwpwNQpWCnNTJ3RpdGxlJwpwNgpWCnMu"
    >>> request_data ["Person__last_name"]      = "Last name"
    >>> form (request_data)
    1

We have one error...
    >>> dump_form_errors (form)
    Non field errors:
      epkified_ckd() takes at least 3 non-keyword arguments (2 given)
        GTW.OMP.PAP.Person needs the arguments: (last_name, first_name, middle_name = '', title = '', ** kw)
        Instead it got: (last_name = 'Last name')

Ah, so we need a first name as well.
    >>> form = form_cls ("/post-url/")
    >>> request_data ["Person__first_name"] = "First name"
    >>> form (request_data)
    0
    >>> dump_form_errors (form)
    >>> form.instance
    GTW.OMP.PAP.Person (u'last name', u'first name', u'', u'')

Now let's come back to the change use case. Just pass the instance just
created to the new form instance.

    >>> form = form_cls ("/post-url/", form.instance)
    >>> for i in sorted (form.raw_values.iteritems ()) : print i
    ('Person__first_name', 'First name')
    ('Person__instance_state', 'KGRwMQpTJ2xpZmV0aW1lJwpwMgooZHAzClMncmF3JwpwNApJMDEKc3NTJ2ZpcnN0X25hbWUnCnA1ClMnRmlyc3QgbmFtZScKcDYKc1MnbGFzdF9uYW1lJwpwNwpTJ0xhc3QgbmFtZScKcDgKc1MnbWlkZGxlX25hbWUnCnA5ClYKc1MndGl0bGUnCnAxMApWCnMu')
    ('Person__last_name', 'Last name')
    ('Person__lifetime', {'raw': True})
    ('Person__middle_name', u'')
    ('Person__title', u'')

    >>> form = form_cls ("/post-url/", form.instance)
    >>> request_data ["Person__first_name"] = "New first name"
    >>> form (request_data)
    0
    >>> dump_form_errors (form)
    >>> form.instance
    GTW.OMP.PAP.Person (u'last name', u'new first name', u'', u'')

We have choosen the PAP.Person object for a good reason. It has a so called
`Composite` attribute: *lifetime*. This attribute is actually an object by
itself which has two attributes: the *start* and the *finish* of the date
interval (which would be the brith- and deathdate of the person):

    >>> form.instance.lifetime
    MOM.Date_Interval ()

Editing of objects inside of a form for an other object is called *inline
editing*. So let' check which inlines we have:

    >>> [ai.name for ai in form.inline_fields]
    ['lifetime']

Each inline has an embedded form for it's own:

    >>> inline_form_cls = form.inline_fields [0].form_cls
    >>> [f.name for f in inline_form_cls.fields]
    ['start', 'finish', 'instance_state', '_pid_a_state_']

The result is not what we execpted.... There is a new fields called
*_pid_a_state_*. This field is used by the javascript on the client side to
commiunicate chanes made to this *inline* object.

Now that we know that we have an inline form, let's try to pass some data for
the fields of the inline from;

    >>> request_data ["Person__lifetime__start"] = "16.03.1976"
    >>> form = form_cls ("/post-url/", form.instance)
    >>> form (request_data)
    0
    >>> dump_form_errors (form)
    >>> form.instance
    GTW.OMP.PAP.Person (u'last name', u'new first name', u'', u'')
    >>> form.instance.lifetime
    MOM.Date_Interval (start = 1976/03/16)
    >>> dump_instance (form.instance)
    last_name            = u'last name'
    first_name           = u'new first name'
    middle_name          = u''
    title                = u''
    lifetime:
      start              = datetime.date(1976, 3, 16)
      finish             = None

Now, let's try to change the value of a composite:
    >>> request_data ["Person__lifetime__finish"] = "16.03.2142"
    >>> form = form_cls ("/post-url/", form.instance)
    >>> form (request_data)
    0
    >>> dump_form_errors (form)
    >>> dump_instance (form.instance)
    last_name            = u'last name'
    first_name           = u'new first name'
    middle_name          = u''
    title                = u''
    lifetime:
      start              = datetime.date(1976, 3, 16)
      finish             = datetime.date(2142, 3, 16)

Up the now, we have always changed an existing object. Now, Lets check if we
can rename an existing object as well:

    >>> scope.PAP.Person.count
    1
    >>> request_data ["Person__last_name"] = "Test"
    >>> form = form_cls ("/post-url/", form.instance)
    >>> form (request_data)
    0
    >>> dump_form_errors (form)
    >>> dump_instance (form.instance)
    last_name            = u'test'
    first_name           = u'new first name'
    middle_name          = u''
    title                = u''
    lifetime:
      start              = datetime.date(1976, 3, 16)
      finish             = datetime.date(2142, 3, 16)
    >>> scope.PAP.Person.count
    1
    >>> saved_instance = form.instance

OK, so what happens if we try to create an instance with the same primary key
a second time:
    >>> form = form_cls ("/post-url/")
    >>> form (request_data)
    1
    >>> dump_form_errors (form)
    Non field errors:
      new definition of (u'test', u'new first name', u'', u'') clashes with existing (u'test', u'new first name', u'', u'')

OK, let's see how an error in a composite is handled:
    >>> request_data ["Person__lifetime__finish"] = "16.03.1900"
    >>> form = form_cls ("/post-url/", saved_instance)
    >>> form (request_data)
    2
    >>> dump_form_errors (form)
    start
        Condition `finish_after_start` : The finish date must be later than the start date (start <= finish)
        start = datetime.date(1976, 3, 16)
        finish = datetime.date(1900, 3, 16)
    finish
        Condition `finish_after_start` : The finish date must be later than the start date (start <= finish)
        start = datetime.date(1976, 3, 16)
        finish = datetime.date(1900, 3, 16)
"""

_link_test = r"""
    >>> scope = MOM.Scope.new (apt, None)
    >>> EVT   = scope.EVT
    >>> SWP   = scope.SWP
    >>> page  = SWP.Page \
    ...    ( "test_page"
    ...    , text = "Test page"
    ...    , date = scope.MOM.Date_Interval_N (start = "1.1.2010", raw = True)
    ...    )

Up to now we have not touch links in any way. Let's change that. For a start
we use the *Link1* *Event*:

    >>> form_cls = GTW.Form.MOM.Instance.New \
    ...     ( EVT.Event
    ...     , FGD (AID ("left", FGD("perma_name", "text", "date")), WF ())
    ...     )
    >>> form     = form_cls ("/post/")
    >>> for i in sorted (form.raw_values.iteritems ()) : print i
    ('Event__date', {'raw': True})
    ('Event__detail', u'')
    ('Event__instance_state', 'KGRwMQpTJ2RldGFpbCcKcDIKVgpzUydzaG9ydF90aXRsZScKcDMKVgpzUydyZWN1cnJlbmNlJwpwNAooZHA1ClMncmF3JwpwNgpJMDEKc3NTJ3RpbWUnCnA3CihkcDgKZzYKSTAxCnNzUydkYXRlJwpwOQooZHAxMApnNgpJMDEKc3NTJ2xlZnQnCnAxMQoodHMu')
    ('Event__left', ())
    ('Event__recurrence', {'raw': True})
    ('Event__short_title', u'')
    ('Event__time', {'raw': True})
    >>> [f.name for f in form_cls.fields]
    ['left', 'date', 'time', 'detail', 'recurrence', 'short_title', 'instance_state']
    >>> fields_of_field_groups (form_cls)
    ['left', 'date', 'time', 'detail', 'recurrence', 'short_title']
    >>> [ai.name for ai in form.inline_fields]
    ['left', 'date', 'time', 'recurrence']
    >>> [f.name for f in form.inline_fields [0].form.fields]
    ['perma_name', 'text', 'date', 'instance_state', '_pid_a_state_']

As we can see we have multiple inlines here. date, time and recurrence are of
the *composite* type we have already seen in the person example.
But the *left* is a different animal. It's the role of a link, also handled
by an inline. The difference now is that this inline does handle a
*Id_Entity* instead of an *An_Entity*.
So, let's try to create a new *Event*. First, we need to know which **keys**
we would need for the *left* part:
    >>> ilf = form.inline_fields [0].form
    >>> ilf.prefix
    'Event__left'

So *Event__left* is the prefix. Ok, so let's try to create an *Event*:
    >>> form     = form_cls ("/post/")
    >>> request_data = dict (Event__instance_state = "KGRwMQpTJ2RldGFpbCcKcDIKVgpzUydzaG9ydF90aXRsZScKcDMKVgpzUydyZWN1cnJlbmNlJwpwNAooZHA1ClMncmF3JwpwNgpJMDEKc3NTJ3RpbWUnCnA3CihkcDgKZzYKSTAxCnNzUydkYXRlJwpwOQooZHAxMApnNgpJMDEKc3NTJ2xlZnQnCnAxMQoodHMu")
    >>> request_data ["Event__left__perma_name"]  = "Permaname"
    >>> request_data ["Event__left__text"]        = "Text"
    >>> request_data ["Event__left__date__start"] = "1.1.2010"
    >>> form (request_data)  ### 1
    0
    >>> dump_form_errors (form) ### 1
    >>> dump_instance (form.instance)
    left:
      perma_name         = u'Permaname'
      text               = u'Text'
      creator            = None
      date:
        start            = datetime.date(2010, 1, 1)
        finish           = None
      short_title        = u''
      title              = u''
      format             = <class '_GTW._OMP._SWP.Format.ReST'>
      head_line          = u''
      prio               = 0
    date:
      start              = None
      finish             = None
    time:
      start              = None
      finish             = None
    detail               = u''
    recurrence:
      period             = 1
      unit               = 2
      week_day           = None
      count              = None
      restrict_pos       = None
      month_day          = None
      month              = None
      week               = None
      year_day           = None
      easter_offset      = None
    short_title          = u''
    >>> EVT.Event.count, SWP.Page.count
    (1, 2)

Up to now we have not touch links in any way. Let's change that. For a start
we use the *Link1* *Event*:

    >>> form_cls = GTW.Form.MOM.Instance.New (EVT.Event)

Ok, so we have create a new event together with a new page object in one
step. But how would be reuse an existing page to create a new page. That the
reason the **_pid_a_state_** field exists (we saw this field already for the
composite inlines but had no real use for them there). So, if we what to
reuse an existing page for a new event we just specify the **_pid_a_state_**
to reference the page we what:
    >>> request_data = dict (Event__instance_state = "KGRwMQpTJ2RldGFpbCcKcDIKVgpzUydzaG9ydF90aXRsZScKcDMKVgpzUydyZWN1cnJlbmNlJwpwNAooZHA1ClMncmF3JwpwNgpJMDEKc3NTJ3RpbWUnCnA3CihkcDgKZzYKSTAxCnNzUydkYXRlJwpwOQooZHAxMApnNgpJMDEKc3NTJ2xlZnQnCnAxMQoodHMu")
    >>> request_data ["Event__left___pid_a_state_"] = "1:L"
    >>> form     = form_cls ("/post/")
    >>> form (request_data) ### 2
    0
    >>> dump_form_errors (form) ### 2
    >>> dump_instance (form.instance)
    left:
      perma_name         = u'test_page'
      text               = u'Test page'
      creator            = None
      date:
        start            = datetime.date(2010, 1, 1)
        finish           = None
      short_title        = u''
      title              = u''
      format             = <class '_GTW._OMP._SWP.Format.ReST'>
      head_line          = u''
      prio               = 0
    date:
      start              = None
      finish             = None
    time:
      start              = None
      finish             = None
    detail               = u''
    recurrence:
      period             = 1
      unit               = 2
      week_day           = None
      count              = None
      restrict_pos       = None
      month_day          = None
      month              = None
      week               = None
      year_day           = None
      easter_offset      = None
    short_title          = u''
    >>> EVT.Event.count, SWP.Page.count
    (2, 2)

But what if we don't have a smart client that know's how to handle the
**_pid_a_state_** field:

    >>> request_data = dict (Event__instance_state = "KGRwMQpTJ2RldGFpbCcKcDIKVgpzUydzaG9ydF90aXRsZScKcDMKVgpzUydyZWN1cnJlbmNlJwpwNAooZHA1ClMncmF3JwpwNgpJMDEKc3NTJ3RpbWUnCnA3CihkcDgKZzYKSTAxCnNzUydkYXRlJwpwOQooZHAxMApnNgpJMDEKc3NTJ2xlZnQnCnAxMQoodHMu")
    >>> request_data ["Event__left__perma_name"] = "Permaname"
    >>> request_data ["Event__left__text"]       = "Text"
    >>> request_data ["Event__date__start"]      = "1.1.2010"
    >>> form     = form_cls ("/post/")
    >>> form (request_data) ### 3
    0
    >>> dump_form_errors (form) ### 3
    >>> dump_instance (form.instance)
    left:
      perma_name         = u'Permaname'
      text               = u'Text'
      creator            = None
      date:
        start            = datetime.date(2010, 1, 1)
        finish           = None
      short_title        = u''
      title              = u''
      format             = <class '_GTW._OMP._SWP.Format.ReST'>
      head_line          = u''
      prio               = 0
    date:
      start              = datetime.date(2010, 1, 1)
      finish             = None
    time:
      start              = None
      finish             = None
    detail               = u''
    recurrence:
      period             = 1
      unit               = 2
      week_day           = None
      count              = None
      restrict_pos       = None
      month_day          = None
      month              = None
      week               = None
      year_day           = None
      easter_offset      = None
    short_title          = u''
    >>> EVT.Event.count, SWP.Page.count
    (3, 2)

As we can see that form try to find the reference object by matching all the
data provided by the client against the database to find the object. If it is
found, this object will be used instead of creating a new object.

Up to now we only showed how the good cases work, so let's  look at a bad
case too. We try to generate the same event as before, which is not allowed:
    >>> form     = form_cls ("/post/")
    >>> form (request_data) ### 4
    1
    >>> dump_form_errors (form) ### 4
    Non field errors:
      <class 'GTW.OMP.EVT.Event' [HWO__Hash__HPS]>, ((u'Permaname', ), dict (start = '2010/01/01'), dict ())


Now suprise here. The error is detected and reported correctly.
"""

_link2_test = """
    >>> scope = MOM.Scope.new (apt, None)
    >>> PAP   = scope.PAP

Now we know how a link-1 is handled, let's look at a link with more than one
role, a link-2. We choose the Person_has_Address for the reason that the
*Person* itself has a composite **lifetime** (and *Address* has a composite
too, **position**). Just to make it a bit more interesting and challanging
for the form code.

    >>> form_cls = GTW.Form.MOM.Instance.New (PAP.Person_has_Address)
    >>> form     = form_cls ("/post/")
    >>> for i in sorted (form.raw_values.iteritems ()) : print i
    ('Person_has_Address__desc', u'')
    ('Person_has_Address__instance_state', 'KGRwMQpTJ2Rlc2MnCnAyClYKc1MncmlnaHQnCnAzCih0c1MnbGVmdCcKcDQKKHRzLg==')
    ('Person_has_Address__left', ())
    ('Person_has_Address__right', ())
    >>> [f.name for f in form_cls.fields]
    ['left', 'right', 'desc', 'instance_state']
    >>> fields_of_field_groups (form_cls)
    ['left', 'right', 'desc']
    >>> [ai.name for ai in form.inline_fields]
    ['left', 'right']

As we can see the form basically has 3 user editable fields. The **left** and
**right** roles of the link and the **desc**. **left** and **right** are
inline fields, **desc** is a normal field.
So let's look at inline fields in more detail:
    >>> for ilf in form.inline_fields :
    ...     print ilf.name
    ...     [f.name for f in ilf.form.fields]
    ...     [ii.name for ii in ilf.form.inline_fields]
    left
    ['last_name', 'first_name', 'middle_name', 'title', 'instance_state', '_pid_a_state_']
    []
    right
    ['street', 'zip', 'city', 'country', 'region', 'instance_state', '_pid_a_state_']
    []

It's goin to be intersting to see how the key in the request data have to
look like for all attributes:
    >>> dump_field_ids (form)
    P left:
     P last_name         = 'Person_has_Address__left__last_name'
     P first_name        = 'Person_has_Address__left__first_name'
     p middle_name       = 'Person_has_Address__left__middle_name'
     p title             = 'Person_has_Address__left__title'
     i instance_state    = 'Person_has_Address__left__instance_state'
     i _pid_a_state_     = 'Person_has_Address__left___pid_a_state_'
    P right:
     P street            = 'Person_has_Address__right__street'
     P zip               = 'Person_has_Address__right__zip'
     P city              = 'Person_has_Address__right__city'
     P country           = 'Person_has_Address__right__country'
     p region            = 'Person_has_Address__right__region'
     i instance_state    = 'Person_has_Address__right__instance_state'
     i _pid_a_state_     = 'Person_has_Address__right___pid_a_state_'
    U desc               = 'Person_has_Address__desc'
    i instance_state     = 'Person_has_Address__instance_state'

Ok, that's a lot of options we have. Luckily not all of them are primary
(indecated by the *P*).

So let's create request_data dict.
    >>> request_data = dict ()
    >>> request_data ["Person_has_Address__left__last_name"]  = "Last name"
    >>> request_data ["Person_has_Address__left__first_name"] = "First name"
    >>> request_data ["Person_has_Address__right__street"]    = "Street"
    >>> request_data ["Person_has_Address__right__zip"]       = "1010"
    >>> request_data ["Person_has_Address__right__city"]      = "Vienna"
    >>> request_data ["Person_has_Address__right__country"]   = "Austria"
    >>> form     = form_cls ("/post/")
    >>> form (request_data)
    0
    >>> dump_form_errors (form)
    >>> dump_instance (form.instance)
    left:
      last_name          = u'last name'
      first_name         = u'first name'
      middle_name        = u''
      title              = u''
      lifetime:
        start            = None
        finish           = None
    right:
      street             = u'street'
      zip                = u'1010'
      city               = u'vienna'
      country            = u'austria'
      region             = u''
      desc               = u''
      position:
        lat              = None
        lon              = None
        height           = None
    desc                 = u''
"""

_object_with_link_test = r"""
    >>> scope = MOM.Scope.new (apt, None)
    >>> PAP   = scope.PAP

So now it's time to introduce the next feature of the forms. The ability to
edit links to an object as part of the form of the object itselt. This is
limited to links where the object the main form is for as a role of the link.

Creating the form class is a little bit more effort here.
    >>> form_cls = GTW.Form.MOM.Instance.New \
    ...     ( PAP.Person
    ...     , FGD ()
    ...     , LID
    ...         ( "PAP.Person_has_Address"
    ...         )
    ...     )

As we can see, in the form for the link the inline for the left role (->
person) is missing. This is because this form is part of the toplevel form
for a person -> the person role is taken from the toplevel form.
So, let's try to create a person together with an address linked to this
person.
    >>> form = form_cls ("/post/")
    >>> request_data = dict ()
    >>> request_data ["Person__last_name"]                             = "Last"
    >>> request_data ["Person__first_name"]                            = "First"
    >>> request_data ["Person__Person_has_Address-M0__right__street"]  = "Street"
    >>> request_data ["Person__Person_has_Address-M0__right__zip"]     = "1010"
    >>> request_data ["Person__Person_has_Address-M0__right__city"]    = "Vienna"
    >>> request_data ["Person__Person_has_Address-M0__right__country"] = "Austria"
    >>> form (request_data) ### 1
    0
    >>> dump_instance (form.instance) ### 1
    last_name            = u'last'
    first_name           = u'first'
    middle_name          = u''
    title                = u''
    lifetime:
      start              = None
      finish             = None
    >>> for i in sorted (form.instance.addresses) :
    ...     dump_instance (i) ### 1
    street               = u'street'
    zip                  = u'1010'
    city                 = u'vienna'
    country              = u'austria'
    region               = u''
    desc                 = u''
    position:
      lat                = None
      lon                = None
      height             = None
   >>> for ad in form.instance.addresses :
   ...     ad.pid
   1

Ok, so with one form we created a person, an address and a link between the
person and the address.
With this kind of form's it is also possible to delete links (but not the
object which is linked) using the **_pid_a_state_** field of the link:

    >>> form = form_cls ("/post/", form.instance)
    >>> request_data = dict ()
    >>> request_data ["Person__last_name"]                             = "Last"
    >>> request_data ["Person__first_name"]                            = "First"
    >>> request_data ["Person__Person_has_Address-M0___pid_a_state_"]  = "3:U"
    >>> form (request_data) ### 2
    0
    >>> dump_instance (form.instance) ### 2
    last_name            = u'last'
    first_name           = u'first'
    middle_name          = u''
    title                = u''
    lifetime:
      start              = None
      finish             = None
    >>> for i in sorted (form.instance.addresses) :
    ...     dump_instance (i) ### 2
    >>> PAP.Address.query ().all ()
    [GTW.OMP.PAP.Address (u'street', u'1010', u'vienna', u'austria', u'')]

The link has been deleted but the address object itself is still there.
So, let's try to link to this object again:
    >>> form = form_cls ("/post/", form.instance)
    >>> request_data = dict ()
    >>> request_data ["Person__last_name"]                             = "Last"
    >>> request_data ["Person__first_name"]                            = "First"
    >>> request_data ["Person__Person_has_Address-M0__right___pid_a_state_"] = "1:L"
    >>> form (request_data) ### 3
    0
    >>> dump_form_errors (form) ### 3
    >>> dump_instance (form.instance)
    last_name            = u'last'
    first_name           = u'first'
    middle_name          = u''
    title                = u''
    lifetime:
      start              = None
      finish             = None
    >>> for i in sorted (form.instance.addresses) :
    ...     dump_instance (i)
    street               = u'street'
    zip                  = u'1010'
    city                 = u'vienna'
    country              = u'austria'
    region               = u''
    desc                 = u''
    position:
      lat                = None
      lon                = None
      height             = None

    >>> PAP.Person_has_Address.query ().first ().pid
    4

Now, let's try to set the attribute of the link itself
    >>> form = form_cls ("/post/", form.instance)
    >>> request_data = dict ()
    >>> request_data ["Person__last_name"]                             = "Last"
    >>> request_data ["Person__first_name"]                            = "First"
    >>> request_data ["Person__Person_has_Address-M0___pid_a_state_"]  = "4:R"
    >>> request_data ["Person__Person_has_Address-M0__desc"]           = "link-desc"
    >>> request_data ["Person__Person_has_Address-M0__right___pid_a_state_"] = "2:r"
    >>> request_data ["Person__Person_has_Address-M0__right__street"]  = "Street"
    >>> request_data ["Person__Person_has_Address-M0__right__zip"]     = "1010"
    >>> request_data ["Person__Person_has_Address-M0__right__city"]    = "Vienna"
    >>> request_data ["Person__Person_has_Address-M0__right__country"] = "Austria"
    >>> form (request_data) ### 4
    0
    >>> PAP.Person.count, PAP.Address.count, PAP.Person_has_Address.count
    (1, 1, 1)
    >>> PAP.Person_has_Address.query ().one ().desc
    u'link-desc'

The last thing we can do is **rename** the link (link to a different
address):
    >>> form = form_cls ("/post/", form.instance)
    >>> request_data = dict ()
    >>> request_data ["Person__last_name"]                             = "Last"
    >>> request_data ["Person__first_name"]                            = "First"
    >>> request_data ["Person__Person_has_Address-M0___pid_a_state_"]  = "4:R"
    >>> request_data ["Person__Person_has_Address-M0__desc"]           = "link-desc"
    >>> request_data ["Person__Person_has_Address-M0__right___pid_a_state_"] = "2:r"
    >>> request_data ["Person__Person_has_Address-M0__right__street"]  = "New Street"
    >>> request_data ["Person__Person_has_Address-M0__right__zip"]     = "1010"
    >>> request_data ["Person__Person_has_Address-M0__right__city"]    = "Vienna"
    >>> request_data ["Person__Person_has_Address-M0__right__country"] = "Austria"
    >>> form (request_data) ### 5
    0
    >>> dump_form_errors (form) ### 5
    >>> for i in sorted (form.instance.addresses) :
    ...     dump_instance (i)  ### 5
    street               = u'new street'
    zip                  = u'1010'
    city                 = u'vienna'
    country              = u'austria'
    region               = u''
    desc                 = u''
    position:
      lat                = None
      lon                = None
      height             = None
    >>> PAP.Person.count, PAP.Address.count, PAP.Person_has_Address.count
    (1, 2, 1)
    >>> for a in sorted (PAP.Address.query (), key = lambda a : a.pid) : print a
    (u'street', u'1010', u'vienna', u'austria', u'')
    (u'new street', u'1010', u'vienna', u'austria', u'')

Ok, here we created a new address, but can we also rename a link to an
existing address object?
    >>> PAP.Address.query (street = "street").one ().pid
    1
    >>> form = form_cls ("/post/", form.instance)
    >>> request_data = dict ()
    >>> request_data ["Person__last_name"]                             = "Last"
    >>> request_data ["Person__first_name"]                            = "First"
    >>> request_data ["Person__Person_has_Address-M0___pid_a_state_"]  = "4:R"
    >>> request_data ["Person__Person_has_Address-M0__desc"]           = ""
    >>> request_data ["Person__Person_has_Address-M0__right___pid_a_state_"] = "1:L"
    >>> request_data ["Person__Person_has_Address-M0__right__street"]  = "Street"
    >>> request_data ["Person__Person_has_Address-M0__right__zip"]     = "1010"
    >>> request_data ["Person__Person_has_Address-M0__right__city"]    = "Vienna"
    >>> request_data ["Person__Person_has_Address-M0__right__country"] = "Austria"
    >>> form (request_data) ### 6
    0
    >>> dump_form_errors (form) ### 6
    >>> PAP.Person.count, PAP.Address.count, PAP.Person_has_Address.count
    (1, 2, 1)
    >>> for i in sorted (form.instance.addresses) :
    ...     dump_instance (i) ### 6
    street               = u'street'
    zip                  = u'1010'
    city                 = u'vienna'
    country              = u'austria'
    region               = u''
    desc                 = u''
    position:
      lat                = None
      lon                = None
      height             = None
"""

if 1 :
    __test__ = dict \
        ( object_with_link = _object_with_link_test
        , link2            = _link2_test
        , link             = _link_test
        , object           = _object_test
        )
else :
    __doc__ = _link_test

from   _MOM._EMS.Hash                           import Manager as EMS
from   _MOM._DBW._HPS.Manager                   import Manager as DBW
from   _GTW                                     import GTW
import _GTW._Form._MOM.Instance
from   _GTW._Form._MOM.Inline_Description       import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
    )
from   _GTW._Form._MOM.Field_Group_Description  import \
    ( Field_Group_Description as FGD
    , Field_Prefixer          as FP
    , Wildcard_Field          as WF
    )

from   _MOM                      import MOM
from   _MOM.Product_Version      import Product_Version, IV_Number
import  itertools

GTW.Version = Product_Version \
    ( productid           = u"GTW MOM Form Test"
    , productnick         = u"GTW"
    , productdesc         = u"Test cases for MOM form handling"
    , date                = " 5-Feb-2010"
    , major               = 0
    , minor               = 5
    , patchlevel          = 42
    , author              = u"Martin Glück"
    , copyright_start     = 2010
    , db_version          = IV_Number
        ( "db_version"
        , ("MOM FOrm tests", )
        , ("MOM FOrm tests", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".mft"
        )
    )
### import the models we use for the test
import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._EVT.import_EVT

### define an app type
apt = MOM.App_Type \
    ( u"HWO", GTW
    , PNS_Aliases = dict
       (PAP = GTW.OMP.PAP, EVT = GTW.OMP.EVT, SWP = GTW.OMP.SWP)
    ).Derived (EMS, DBW)

### define some helper functions
def fields_of_field_groups (form, indent = "") :
    for fg in form.field_groups :
        if isinstance (fg, GTW.Form.MOM.Link_Inline) :
            print "%s%s" % (indent, fg.form_cls.et_man.type_base_name)
            fields_of_field_groups (fg.form_cls, indent + "  ")
        else :
            print "%s%s" % (indent, [f.name for f in fg.fields])
# end def fields_of_field_groups

def dump_form_errors (form, indent = "", Break = False) :
    if form.errors :
        if Break : import pdb; pdb.set_trace ()
        print "%sNon field errors:" % (indent, )
        print "\n".join ("  %s%s" % (indent, e) for e in form.errors)
    for f, errors in form.field_errors.iteritems () :
        print str (f)
        print "\n".join ("  %s%s" % (indent, e) for e in errors)
    for ifl in form.inline_fields :
        dump_form_errors (ifl.form, indent + "  ")
    for fg in form.inline_groups :
        for ifo in fg.forms :
            if getattr (ifo, "error_count", 1) :
                print "%s%s" % (indent, ifo.prefix)
                dump_form_errors (ifo, indent + "  ")
# end def dump_form_errors

def internal_field_values (form) :
    result = {}
    for f in form.fields :
        if f.hidden :
            result [form.get_id (f)] = form.get_raw (f)
    for ig in form.inline_groups :
        for ifo in ig.forms :
            result.update (internal_field_values (ifo))
    return result
# end def internal_field_values

def form_instance_states (form, indent = "") :
    field = form.instance_state_field
    fisd  = field.decode (form.get_raw (field))
    print "%s%s" % (indent, sorted (fisd.iteritems ()))
    for ig in form.inline_groups :
        for ifo in ig.forms :
            form_instance_states (ifo, indent + "  ")
# end def form_instance_states

class Non_Stringable (object) :
    ### Use to generate a form error
    def __init__ (self, value) :
        self.value = value
    # end def __init__

    def __str__ (self) :
        return 1
    # end def __str__

# end class Non_Stringable

def dump_instance (instance, indent = "") :
    if instance is None :
        print "%sNone" % (indent, )
    else :
        name_len = 20 - len (indent)
        for attr in itertools.chain (instance.primary, instance.user_attr) :
            value = getattr (instance, attr.name)
            if isinstance (value, MOM.Entity) :
                print "%s%s:" % (indent, attr.name, )
                dump_instance (value, indent + "  ")
            else :
                print "%s%-*s = %r" % (indent, name_len, attr.name, value)
# end def dump_instance

def dump_field_ids (form, indent = "") :
    name_len = 18 - len (indent)
    et_man   = form.et_man
    for f in form.fields :
        attr_kind = getattr (et_man, f.name, None)
        if attr_kind :
            kind = "U"
            if isinstance (attr_kind, MOM.Attr.Primary) :
                kind = "P"
            elif isinstance (attr_kind, MOM.Attr.Primary_Optional) :
                kind = "p"
            elif isinstance (attr_kind, MOM.Attr.Mandatory) :
                kind = "M"
        else :
            kind = "i"
        if not isinstance (f, GTW.Form.MOM._Attribute_Inline_) :
            print "%s%s %-*s = %r" % (indent, kind, name_len, f.name, form.get_id (f))
        else :
            print "%s%s %s:" % (indent, kind, f.name)
            dump_field_ids (f.form, indent + " ")
    for ifg in form.inline_groups :
        print "%s%s:" % (indent, ifg.name)
        for no, f in enumerate (ifg.forms) :
            dump_field_ids (f, indent + " ")
# end def dump_field_ids

def test (form) :
    import pdb; pdb.set_trace ()
# end def test

### __END__ GTW.Form.MOM.__test__


