# -*- coding: iso-8859-1 -*-
# simple example to test if a redirect works
from   _TFL            import TFL
import _TFL.I18N
from   _GTW            import GTW
import _GTW._NAV.Base

class Redirect (GTW.NAV.Page) :
    """Always redirect"""

    def _view (self, handler) :
        cls = self.top.HTTP.Status.Table [self.code]
        raise cls (self.redirect_to)
    # end def _view

# end class Redirect

class Error (GTW.NAV.Page) :
    """Display error"""

    def _view (self, handler) :
        cls = self.top.HTTP.Status.Table [self.code]
        raise cls
    # end def _view

# end class Error

class E_Type_Form (GTW.NAV.Page) :

    def rendered (self, handler, template = None) :
        et_man  = self.form.et_man
        context = handler.context
        request = handler.request
        context ["objects"] = et_man.query ().limit (10).all ()
        pid     = request.arguments.get ("obj")
        form    = None
        if pid :
            instance = self.form.et_man.query (pid = pid [0]).one ()
        if request.method == "POST" :
            pass
        else :
            if request.arguments.get ("new") :
                form = self.form (self.abs_href)
        context ["form"] = form
        return self.__super.rendered (handler, template)
    # end def rendered

# end class E_Type_Form

class I18N_Test (GTW.NAV.Page) :

    def rendered (self, handler, template = None) :
        context  = handler.context
        request  = handler.request
        lang     = request.arguments.get ("lang")
        if lang :
            handler.session ["language"] = lang
            TFL.I18N.use (* lang)
        context ["lang"] = handler.session.language
        return self.__super.rendered (handler, template)
    # end def rendered

# end class I18N_Test

### __END__ Redirect
