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
#    ««revision-date»»···
#--
"""
>>> scope = MOM.Scope.new (apt, None)
>>> PAP   = scope.PAP
>>> simp_per_form_cls = GTW.Form.MOM.Instance.New (PAP.Person)

Each form class has a fields NO-List containing all fields of all field groups.

    >>> [f.name for f in simp_per_form_cls.fields]
    ['last_name', 'first_name', 'middle_name', 'title', 'lifetime', 'instance_state']
    >>> fields_of_field_groups (simp_per_form_cls)
    ['last_name', 'first_name', 'middle_name', 'title', 'lifetime']

It is also possible to use field group descriptions to define which fields
and in what order the fields should be part of the form:

    >>> form_cls = GTW.Form.MOM.Instance.New \\
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

    >>> form_cls = GTW.Form.MOM.Instance.New \\
    ...     ( PAP.Person
    ...     , FGD ("title")
    ...     , FGD ("first_name", "last_name", WF  ())
    ...     )
    >>> [f.name for f in form_cls.fields]
    ['title', 'first_name', 'last_name', 'middle_name', 'lifetime', 'instance_state']
    >>> fields_of_field_groups (form_cls)
    ['title']
    ['first_name', 'last_name', 'middle_name', 'lifetime']

    >>> form_cls = GTW.Form.MOM.Instance.New \\
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

    >>> form_cls = GTW.Form.MOM.Instance.New \\
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
    ('Person__instance_state', 'KGRwMQpTJ2xpZmV0aW1lJwpwMgpWCnNTJ2ZpcnN0X25hbWUnCnAzClYKc1MnbGFzdF9uYW1lJwpwNApWCnNTJ21pZGRsZV9uYW1lJwpwNQpWCnNTJ3RpdGxlJwpwNgpWCnMu')
    ('Person__last_name', u'')
    ('Person__lifetime', u'')
    ('Person__middle_name', u'')
    ('Person__title', u'')

Once we receive the data from the browser we *call* the form instance and
pass along the request_data
    >>> request_data = dict ()
    >>> #form (request_data)
    #0

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
    >>> form.instance
    GTW.OMP.PAP.Person (u'last name', u'first name', u'', u'')

Now let's come back to the change use case. Just pass the instance just
created to the new form instance.

    >>> form = form_cls ("/post-url/", form.instance)
    >>> for i in sorted (form.raw_values.iteritems ()) : print i
    ('Person__first_name', 'First name')
    ('Person__instance_state', 'KGRwMQpTJ2xpZmV0aW1lJwpwMgpWCnNTJ2ZpcnN0X25hbWUnCnAzClMnRmlyc3QgbmFtZScKcDQKc1MnbGFzdF9uYW1lJwpwNQpTJ0xhc3QgbmFtZScKcDYKc1MnbWlkZGxlX25hbWUnCnA3ClYKc1MndGl0bGUnCnA4ClYKcy4=')
    ('Person__last_name', 'Last name')
    ('Person__lifetime', u'')
    ('Person__middle_name', u'')
    ('Person__title', u'')

    >>> form = form_cls ("/post-url/", form.instance)
    >>> request_data ["Person__first_name"] = "New first name"
    >>> form (request_data)
    0
    >>> form.instance
    GTW.OMP.PAP.Person (u'last name', u'new first name', u'', u'')

We have choosen the PAP.Person object for a good reason. It has a so called
`Composite` attribute: *lifetime*. This attribute is actually an object by
itself which has two attributes: the *start* and the *end* of the date
interval (which would be the brith and deathdate of the person):

    >>> form.instance.lifetime
    MOM.Date_Interval ()
"""

"""

### let's use or simple form and simpulate a `POST`. For this, we need to
### create an nstance of or form class speicifing the POST url and than call
### this instance with a request data dictinary:
>>> form = simp_per_form_cls ("/post/")

### An empty data dict not is treated as an error but no instance is created
### as well (and we can see that the form stores the error count internally
### as well)
>>> form.error_count, form.instance
(0, None)

### Now, let's try to pas along some real data:
>>> request_data ["last_name"] = "Last Name"
>>> form (request_data)
1

### this time, the form reports 1 error
>>> dump_form_errors (form) #doctest: +ELLIPSIS
Non field errors:
  epkified_raw() takes at least 3 non-keyword arguments (2 given)
    GTW.OMP.PAP.Person needs the arguments: (last_name, first_name, middle_name = u'', title = u'', ** kw)
    Instead it got: (raw = True, last_name = 'Last Name', on_error = <built-in method append of list object at 0x...>)

### now we try to pass all required data to the form and let the form create a
### instance for us
>>> request_data ["first_name"] = "First Name"
>>> form = simp_per_form_cls ("/post/")
>>> form (request_data)
0
>>> form.instance
GTW.OMP.PAP.Person (u'Last Name', u'First Name', u'', u'')
>>> form_instance_states (form)
[('lifetime', u''), ('first_name', 'First Name'), ('last_name', 'Last Name'), ('middle_name', ''), ('title', '')]

### to make sure we check if the instance is stored in the scope
>>> PAP.Person.query ().all ()
[GTW.OMP.PAP.Person (u'Last Name', u'First Name', u'', u'')]

### now, if what to change an existing instance we can do this by passing the
### instance to the form constructor:
>>> person = PAP.Person.query ().one ()
>>> form   = simp_per_form_cls ("/post/", person)
>>> request_data ["title"] = "Dr. Dr"
>>> form (request_data)
0
>>> form.instance
GTW.OMP.PAP.Person (u'Last Name', u'First Name', u'', u'Dr. Dr')
>>> PAP.Person.query ().one () == form.instance
True
>>> form_instance_states (form)
[('lifetime', u''), ('first_name', 'First Name'), ('last_name', 'Last Name'), ('middle_name', ''), ('title', 'Dr. Dr')]

### form can also be used to rename an instance
>>> form   = simp_per_form_cls ("/post/", person)
>>> request_data ["last_name"] = "New Last Name"
>>> form (request_data)
0
>>> form.instance
GTW.OMP.PAP.Person (u'New Last Name', u'First Name', u'', u'Dr. Dr')
>>> PAP.Person.query ().all ()
[GTW.OMP.PAP.Person (u'New Last Name', u'First Name', u'', u'Dr. Dr')]

### let's go back to the error handling:
>>> form   = simp_per_form_cls ("/post/")
>>> form (request_data)
1
>>> dump_form_errors (form)
Non field errors:
  new definition of (u'New Last Name', u'First Name', u'', u'Dr. Dr') clashes with existing (u'New Last Name', u'First Name', u'', u'Dr. Dr')
>>> form   = simp_per_form_cls ("/post/")
>>> request_data ["first_name"] = "New First Name"
>>> request_data ["lifetime"] = "not a birth date"
>>> form (request_data) ### XXX remove this output, comes from the framework
`not a birth date` for : `lifetime`
     expected type  : `Date`
     got      value : `not a birth date -> not a birth date`
     of       type  : `<type 'unicode'>`
1
>>> dump_form_errors (form)
lifetime
  Can't set optional attribute <(u'New Last Name', u'New First Name', u'', u'Dr. Dr')>.lifetime to `not a birth date`
    `not a birth date` for : `lifetime`
     expected type  : `Date`
     got      value : `not a birth date -> not a birth date`
     of       type  : `<type 'unicode'>`

### before we continue, let's rollback the scope to start with a new, empty
### scope
>>> scope.rollback ()
>>> scope.MOM.Id_Entity.query ().all ()
[]

### forms also be used to edit an object and link's oto this object in one
### form using so called `inlines` (Link_Inline_Description and for the roles
### Attribute_Inline_Description).
>>> form_cls = GTW.Form.MOM.Instance.New \\
...     ( PAP.Person
...     , FGD (WF ("primary"))
...     , FGD ()
...     , LID
...         ( "PAP.Person_has_Address"
...         , FGD ("desc")
...         , AID ("address", FGD (WF ("primary")))
...         )
...     )

### let's see how the structure of such a for looks like.
### We can see the the main form has normal vields but in addition an
### sub-form for `Person_has_Address` which itself has a field for `desc` and
### an additional form for `Address` which again has some fields on it's own::
>>> fields_of_field_groups (form_cls)
['last_name', 'first_name', 'middle_name', 'title', 'instance_state']
['lifetime']
Person_has_Address
  ['desc', 'instance_state', '_lid_a_state_']
  Address
    ['street', 'zip', 'city', 'country', 'region', 'instance_state', '_lid_a_state_']

### in addition to the already seen `instance_state` field we find a new
### internal field called `_lid_a_state_` which is used by the Javascript
### code in the browser to handle the deletion/copy/rename/add link features.

### So, lets see how we can create a instance based on this new form.
### Let's begin with the simple case: Just creating a Person object.
### This acrually works the same way as before:
>>> request_data = \\
...   { "first_name" : "First Name"
...   , "last_name"  : "Last Name"
...   }
>>> form = form_cls ("/post/")
>>> form (request_data)
0
>>> dump_form_errors (form)
>>> scope.MOM.Id_Entity.query ().all ()
[GTW.OMP.PAP.Person (u'Last Name', u'First Name', u'', u'')]
>>> form_instance_states (form)
[('lifetime', u''), ('first_name', 'First Name'), ('last_name', 'Last Name'), ('middle_name', ''), ('title', '')]
  [('desc', u'')]
    [('city', u''), ('country', u''), ('region', u''), ('street', u''), ('zip', u'')]

>>> scope.rollback () ### delete the create person again

### so, this was easy.... now let's try to add a link as well:
>>> request_data.update \\
...     ( { "Person_has_Address-M0-desc"               : "home"
...       , "Person_has_Address-M0-Address-street"     : "Street"
...       , "Person_has_Address-M0-Address-zip"        : "0000"
...       , "Person_has_Address-M0-Address-city"       : "City"
...       , "Person_has_Address-M0-Address-country"    : "Country"
...       }
...     )
>>> valid_data = request_data.copy () ### save for later
>>> form = form_cls ("/post/")
>>> form (request_data)
0
>>> scope.MOM.Id_Entity.query ().all ()
[GTW.OMP.PAP.Person_has_Address ((u'Last Name', u'First Name', u'', u''), (u'Street', u'0000', u'City', u'Country', u'')), GTW.OMP.PAP.Person (u'Last Name', u'First Name', u'', u''), GTW.OMP.PAP.Address (u'Street', u'0000', u'City', u'Country', u'')]

### now, lets try to introducte errors on somewhere in the data
>>> scope.rollback ()
>>> error_data = dict \\
...     (request_data, ** {"Person_has_Address-M0-Address-zip" : ""})
>>> form = form_cls ("/post/")
>>> form (error_data)
1
>>> dump_form_errors (form)  #doctest: +ELLIPSIS
Person_has_Address-M0
  Person_has_Address-M0-Address
    Non field errors:
      epkified_raw() takes at least 5 non-keyword arguments (2 given)
    GTW.OMP.PAP.Address needs the arguments: (street, zip, city, country, region = u'', ** kw)
    Instead it got: (country = 'Country', raw = True, street = 'Street', on_error = <built-in method append of list object at 0x...>, city = 'City')
>>> scope.MOM.Id_Entity.query ().all ()
[GTW.OMP.PAP.Person (u'Last Name', u'First Name', u'', u'')]

>>> scope.rollback ()
>>> error_data = dict \\
...     (request_data, ** {"Person_has_Address-M0-desc" : Non_Stringable (1)})
>>> form = form_cls ("/post/")
>>> form (error_data) ### XXX remove the Unicode error once it is removed from the framework
coercing to Unicode: need string or buffer, int found
1
>>> dump_form_errors (form)
Person_has_Address-M0
  Non field errors:
    coercing to Unicode: need string or buffer, int found
>>> scope.MOM.Id_Entity.query ().all ()
[GTW.OMP.PAP.Person (u'Last Name', u'First Name', u'', u''), GTW.OMP.PAP.Address (u'Street', u'0000', u'City', u'Country', u'')]

### now, let's try to `rename` a link (change one role without creating a
### new link)
>>> scope.rollback ()
>>> form = form_cls ("/post/")
>>> form (valid_data)
0
>>> person = form.instance

### to be able to find the instances which have populate the original form
### the _lid_a_state_ fields will be used.
>>> int_data = internal_field_values (form)
>>> sorted (int_data.iteritems ())
[('Person_has_Address-M0-Address-_lid_a_state_', '2:L'), ('Person_has_Address-M0-Address-instance_state', 'KGRwMQpTJ2NpdHknCnAyClMnQ2l0eScKcDMKc1MncmVnaW9uJwpwNApTJycKc1Mnc3RyZWV0JwpwNQpTJ1N0cmVldCcKcDYKc1MnemlwJwpwNwpTJzAwMDAnCnA4CnNTJ2NvdW50cnknCnA5ClMnQ291bnRyeScKcDEwCnMu'), ('Person_has_Address-M0-_lid_a_state_', '3:L'), ('Person_has_Address-M0-instance_state', 'KGRwMQpTJ2Rlc2MnCnAyClMnaG9tZScKcDMKcy4='), ('instance_state', 'KGRwMQpTJ2JpcnRoX2RhdGUnCnAyClYKc1MnZmlyc3RfbmFtZScKcDMKUydGaXJzdCBOYW1lJwpwNApzUydsYXN0X25hbWUnCnA1ClMnTGFzdCBOYW1lJwpwNgpzUydtaWRkbGVfbmFtZScKcDcKUycnCnNTJ3RpdGxlJwpwOApTJycKcy4=')]
>>> rename_data = dict \\
...     (valid_data, ** { "Person_has_Address-M0-Address-zip" : "1111"
...                     })
>>> del int_data ["Person_has_Address-M0-Address-instance_state"]
>>> int_data ["Person_has_Address-M0-Address-_lid_a_state_"] = ":N"
>>> int_data ["Person_has_Address-M0-_lid_a_state_"]         = "3:C"
>>> rename_data.update (int_data)
>>> form = form_cls ("/post/", person)
>>> form (rename_data)
0
>>> PAP.Person.count, PAP.Address.count, PAP.Person_has_Address.count
(1, 2, 1)
>>> form_instance_states (form)
[('lifetime', u''), ('first_name', 'First Name'), ('last_name', 'Last Name'), ('middle_name', ''), ('title', '')]
  [('desc', 'home')]
    [('city', 'City'), ('country', 'Country'), ('region', ''), ('street', 'Street'), ('zip', '1111')]

### and now we try to delete a link via a `form`
>>> scope.rollback  ()
>>> form = form_cls ("/post/")
>>> form            (valid_data)
0
>>> person = form.instance
>>> int_data = internal_field_values (form)
>>> rename_data = dict (valid_data)
>>> old_lid = int_data ["Person_has_Address-M0-_lid_a_state_"]
>>> int_data ["Person_has_Address-M0-_lid_a_state_"] = \\
...     "%s:U" % old_lid.split (":") [0]
>>> rename_data.update (int_data)
>>> form = form_cls ("/post/", person)
>>> form (rename_data)
0
>>> PAP.Person.count, PAP.Address.count, PAP.Person_has_Address.count
(1, 1, 0)
"""
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
### we use the PAP OMP for our tests
import _GTW._OMP._PAP.import_PAP
### define an app type
apt = MOM.App_Type \
    (u"HWO", GTW, PNS_Aliases = dict (PAP = GTW.OMP.PAP)
    ).Derived (EMS, DBW)

### define some helper functions
def fields_of_field_groups (form, indent = "") :
    for fg in form.field_groups :
        if isinstance (fg, GTW.Form.MOM._Inline_) :
            print "%s%s" % (indent, fg.form_cls.et_man.type_base_name)
            fields_of_field_groups (fg.form_cls, indent + "  ")
        else :
            print "%s%s" % (indent, [f.name for f in fg.fields])
# end def fields_of_field_groups

def dump_form_errors (form, indent = "") :
    if form.errors :
        print "%sNon field errors:" % (indent, )
        print "\n".join ("  %s%s" % (indent, e) for e in form.errors)
    for f, errors in form.field_errors.iteritems () :
        print str (f)
        print "\n".join ("  %s%s" % (indent, e) for e in errors)
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
    def __init__ (self, value) :
        self.value = value
    # end def __init__

    def __str__ (self) :
        return 1
    # end def __str__

# end class Non_Stringable

### __END__ GTW.Form.MOM.__test__


