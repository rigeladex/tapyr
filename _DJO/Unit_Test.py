# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2008 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin.glueck@gmail.com
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
#    FJO.Unit_Test
#
# Purpose
#    Base class for test cases
#
# Revision Dates
#    30-Nov-2007 (MG) Creation
#     2-Dec-2007 (MG) `Input_Has_Value` added
#    15-Dec-2007 (MG) Missing import added
#     9-May-2008 (MG) `Redirect_to_Login` added, `Check_Context` and
#                     `Input_Has_Value` fixed
#     9-May-2008 (MG) `Test_Case.login` factored
#    ««revision-date»»···
#--

import django.test.testcases           as     unittest
from   django.contrib.auth.models      import User
from   django.core.urlresolvers        import reverse, NoReverseMatch
from   django.db.models.fields         import FieldDoesNotExist
from   django.db.models.manager        import Manager
from   django.conf                     import settings
import pdb
import re

class _Check_ (object) :
    pass
# end class _Check_

class Contains_Text (_Check_) :

    def __init__ (self, text, count = 1, status_code = None) :
        self.text        = text
        self.count       = count
        self.status_code = status_code
    # end def __init__

    def __call__ (self, test_case, response, status_code = None) :
        if self.status_code is not None :
            status_code = self.status_code
        test_case.assertContains \
            (response, self.text, count = self.count, status_code = status_code)
    # end def __call__

# end class Contains_Text

class Contains_Tag (Contains_Text) :

    def __init__ (self, tag_name, count = 1, status_code = None) :
        super (Contains_Tag, self).__init__ \
            ("<%s" % (tag_name, ), count, status_code)
    # end def __init__

# end class Contains_Tag

class Check_Context (_Check_) :

    def __init__ (self, * conditions, ** context) :
        self.conditions = conditions
        self.context    = context
    # end def __init__

    def __call__ (self, test_case, response, status_code = None) :
        if self.context :
            CT           = {}
            res_contexts = unittest.to_list (response.context)
            for name, how in self.context.iteritems () :
                for ct in res_contexts :
                    if how in ct :
                        value = ct [how]
                        break
                else :
                    raise test_case.failureException, \
                        ("`%s` bot found in any context" % (how, ))
                CT [name] = value
        else :
            CT = (response.context and response.context [0]) or {}
        for cond in self.conditions :
            try :
                result    = eval (cond, globals (), CT)
                if not result :
                    msg = "%s not fulfilled in %r" % (cond, CT)
                    raise test_case.failureException, msg
            except :
                raise
    # end def __call__

# end class Check_Context

class Input_Has_Value (_Check_) :

    tag_pattern    = re.compile ("<input.*?name=[\"'](\w+)[\"'].*?>", re.I)
    value_patttern = re.compile ("value=[\"'](.+?)[\"']",             re.I)
    type_patttern  = re.compile ("type=[\"'](\w+)[\"']",              re.I)

    def __init__ (self, field_name, value, type = "text") :
        self.field_name = field_name
        self.value      = value
        self.type       = type
    # end def __init__

    def __call__ (self, test_case, response, status_code = None) :
        side = response.content
        for match in self.tag_pattern.finditer (side) :
            if match.group (1) == self.field_name :
                ### we found the input tag, group (0) is the whole match
                tag         = match.group (0)
                value_req   = self.value is not None
                value_match = self.value_patttern.search (tag)
                type_match  = self.type_patttern. search (tag)
                if not value_match and value_req :
                    test_case.fail \
                        ( "Input tag `%s` has no value attribute."
                        % (self.field_name)
                        )
                elif value_req and (self.value != value_match.group (1)) :
                    test_case.fail \
                        ( "Value of input tag `%s` is `%s` but `%s` was "
                          "expected."
                        % (self.field_name, value_match.group (1), self.value)
                        )
                elif self.type and (type_match.group (1) != self.type) :
                    test_case.fail \
                        ( "Input tag `%s` is of type `%s` but type `%s` was "
                          "expected."
                        % (self.field_name, type_match.group (1), self.type)
                        )
                break
        else :
            test_case.fail \
                ( "Input tag `%s` not found in response form."
                % (self.field_name, )
                )
    # end def __call__

# end class Input_Has_Value

class Field_Choices (_Check_) :

    def __init__ ( self, field_name, count
                 , initial            = None
                 , form_variable_name = "form"
                 ) :
        self.field_name         = field_name
        self.count              = count
        self.initial            = initial
        self.form_variable_name = form_variable_name
    # end def __init__

    def __call__ (self, test_case, response, status_code = None) :
        form     = self.form_variable_name
        contexts = unittest.to_list(response.context)
        for i, context in enumerate (contexts) :
            if form in context :
                field = context [form].fields.get (self.field_name, None)
                if field is None :
                    test_case.fail \
                        ( "The form `%s` in context %d does not contain the "
                          "field `%s`" % (form, i, field)
                        )
                else :
                    field_choices = getattr (field, "choices", None)
                    field_initial = getattr (field, "initial", None)
                    if field_choices is None :
                        test_case.fail \
                            ( "The field `%s` of form `%s` in context %d has "
                              "no `choices` attribute."
                            % (self.field_name, form, i)
                            )
                    else :
                        field_choices = tuple (field_choices)
                        if field_initial is None :
                            field_initial = context [form].initial.get \
                                (self.field_name, None) or ()
                        try :
                            field_initial = tuple (field_initial)
                        except TypeError :
                            field_initial = (field_initial, )
                        field_initial = tuple (sorted (field_initial))
                        if len (field_choices) != self.count :
                            test_case.fail \
                                ( "The choices of field `%s` of form `%s` in "
                                  "context %d have %d entries but %d where "
                                  "expected %r"
                                % ( self.field_name, form, i
                                  , len (field_choices), self.count
                                  , field_choices
                                  )
                                )
                        elif (   (self.initial  is not None)
                             and (field_initial !=     tuple (self.initial))
                             ) :
                            test_case.fail \
                                ( "The initials of field `%s` of form `%s` in "
                                  "context %d has %s entries but %s where "
                                  "expected %r"
                                % ( self.field_name, form, i
                                  , len (field_initial), self.initial
                                  , field_initial
                                  )
                                )
                break
        else :
            test_case.fail \
                ("The form '%s' was not used to render the response" % (form, ))
    # end def __call__

# end class Field_Choices

class Form_Error (_Check_) :

    def __init__ (self, field_name, error_msg, form_variable_name = "form") :
        self.field_name         = field_name
        self.error_msg          = error_msg
        self.form_variable_name = form_variable_name
    # end def __init__

    def __call__ (self, test_case, response, status_code = None) :
        test_case.assertFormError \
            ( response, self.form_variable_name
            , self.field_name, self.error_msg
            )
    # end def __call__

# end class Form_Error

class Required_Field (Form_Error) :

    def __init__ (self, field_name, form_variable_name = "form") :
        super (Required_Field, self).__init__ \
            (field_name, u"This field is required.", form_variable_name)
    # end def __init__

# end class Required_Field

class Call (_Check_) :

    def __init__ (self, callable, * args, ** kw) :
        self.callable = callable
        self.args     = args
        self.kw       = kw
    # end def __init__

    def __call__ (self, test_case, response, status_code = None) :
        return self.callable (* self.args, ** self.kw)
    # end def __call__

# end class Call

class Call_Result (Call) :

    def __init__ (self, callable, result, * args, ** kw) :
        self.result   = result
        super (Call_Result, self).__init__ (callable, * args, ** kw)
    # end def __init__

    def __call__ (self, test_case, response, status_code = None) :
        fct_result = super (Call_Result, self).__call__ \
            (test_case, response, test_case)
        result     = eval ("%s == %s"% (self.result, fct_result))
        if not result :
            msg = "%s (* %r, ** %r) did not return %r but %r" % \
                      ( self.callable, self.args, self.kw
                      , self.result, fct_result
                      )
            raise test_case.failureException, msg
    # end def __call__

# end class Call

class Check_Object (_Check_) :

    def __init__ (self, cls, ** query) :
        self.cls           = cls
        self.query         = query
        self.instance_data = query.pop ("instance_data", {})
    # end def __init__

    def __call__ (self, test_case, response, status_code = None) :
        try :
            obj = self.cls.objects.get (** self.query)
        except self.cls.DoesNotExist :
            msg = "Object of `%s` with query %r does not exist" % \
                (self.cls.__new__, self.query)
            raise test_case.failureException, msg
        errors = []
        for attr, value in self.instance_data.iteritems () :
            inst_value = getattr (obj, attr)
            if isinstance (inst_value, Manager) :
                inst_value = sorted (o.pk for o in inst_value.all ())
                value      = sorted (value)
            if value != inst_value :
                errors.append \
                    ( "`%s` should be `%s` but is `%s`"
                    % (attr, value, inst_value)
                    )
        if errors :
            msg = "Attribute value missmatch %s" % (", ".join (errors))
            raise test_case.failureException, msg
    # end def __call__

# end class Check_Object

class Redirect (_Check_) :

    def __init__ (self, reverse = None, url = None) :
        self.url     = url
        self.reverse = reverse
    # end def __init__

    def __call__ (self, test_case, response, status_code = None) :
        url = self.url
        if self.reverse and self.url is None :
            url = test_case.reverse (self.reverse)
        test_case.assertRedirects (response, url)
    # end def __call__

# end class Redirect

class Redirect_to_Login (Redirect) :

    def __init__ (self, name, * args, ** kw) :
        try :
            next = reverse (name, args = args, kwargs = kw)
        except NoReverseMatch :
            next = name
        super (Redirect_to_Login, self).__init__ \
            (url = "%s?next=%s" % (settings.LOGIN_URL, next))
    # end def __init__

# end class Redirect_to_Login

class Test_Case (unittest.TestCase) :
    """Common test functions."""

    Break_On_Failure = False
    #Break_On_Failure = True

    def BREAK (self) :
        if self.Break_On_Failure :
            pdb.set_trace ()
    # end def BREAK

    def STOP (self) :
        pdb.set_trace ()
    # end def STOP

    def login (self, name, password = None) :
        self.client.login (username = name, password = password or name)
    # end def login

    def _create_user (self, name, password = None, login = False) :
        password = password or name
        user     = User.objects.create_user \
           (name, "%s@test.org" % (name, ), password)
        if login :
            self.login (name, password)
        return user
    # end def _create_user

    def reverse (self, name, * args, ** kw) :
        try :
            return reverse (name, args = args, kwargs = kw)
        except NoReverseMatch :
            return name
    # end def reverse

    def _test_get (self, url, status_code = 200, * tests, ** data) :
        response = self.client.get (self.reverse (url), data = data)
        self._test_response (response, status_code, * tests)
        return response
    # end def _test_get

    def _test_post (self, url, status_code = 200, * tests, ** data) :
        response = self.client.post (self.reverse (url), data = data)
        self._test_response (response, status_code, * tests)
        return response
    # end def _test_get

    def _test_response (self, response, status_code = 200, * tests) :
        if status_code is not None :
            try :
                self.failUnlessEqual (response.status_code, status_code)
            except :
                self.BREAK ()
                raise
        for test in tests :
            try :
                test (self, response, status_code)
            except :
                self.BREAK ()
                raise
    # end def _test_response

# end class Test_Case

if __name__ != "__main__" :
    from _DJO import DJO
    DJO._Export ("*")
### __END__ DJO.Unit_Test
