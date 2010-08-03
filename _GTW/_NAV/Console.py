# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Nav.
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
#    GTW.Nav.Console
#
# Purpose
#    A ineractive python console in the web browser (inspired by the console
#    of werkzeug (http://werkzeug.pocoo.org/))
#
# Revision Dates
#     2-Aug-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL               import TFL
from   _TFL.predicate     import dusplit
import _TFL.Url
import _TFL.I18N
import _TFL.Py_Interpreter

from   _GTW           import GTW
import _GTW._NAV.Base
import _GTW.Media

from    xml.sax.saxutils import escape
from    traceback        import format_exception_only
import  sys
import  code

import  re
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
RegexType     = type(_paragraph_re)

try:
    from collections import deque
except ImportError :
    deque = None

def _add_subclass_info (inner, obj, base) :
    if isinstance (base, tuple) :
        for base in base :
            if type (obj) is base :
                return inner
    elif type (obj) is base :
        return inner
    module = ''
    if obj.__class__.__module__ not in ("__builtin__", "exceptions") :
        module = '<span class="module">%s.</span>' % obj.__class__.__module__
    return "%s%s(%s)" % (module, obj.__class__.__name__, inner)
# end def _add_subclass_info

class HTML_Repr_Generator (TFL.Meta.Object) :
    """Borrowed from werkzeug: werkzeug.debug.repr"""

    def __init__ (self) :
        self._stack = []
    # end def __init__

    def _sequence_repr_maker (left, right, base = object (), limit = 8) :
        def proxy (self, obj, recursive) :
            if recursive :
                return _add_subclass_info (left + '...' + right, obj, base)
            buf                   = [left]
            have_extended_section = False
            for idx, item in enumerate (obj) :
                if idx :
                    buf.append (', ')
                if idx == limit :
                    buf.append ('<span class="extended">')
                    have_extended_section = True
                buf.append (self.repr (item))
            if have_extended_section :
                buf.append ('</span>')
            buf.append     (right)
            return _add_subclass_info (u''.join (buf), obj, base)
        # end def proxy
        return proxy
    # end def _sequence_repr_maker

    list_repr      = _sequence_repr_maker ('[',           ']',  list)
    tuple_repr     = _sequence_repr_maker ('(',           ')',  tuple)
    set_repr       = _sequence_repr_maker ('set([',       '])', set)
    frozenset_repr = _sequence_repr_maker ('frozenset([', '])', frozenset)

    if deque is not None:
        deque_repr = _sequence_repr_maker \
            ('<span class="module">collections.</span>deque([', '])', deque)
    del _sequence_repr_maker

    def regex_repr (self, obj) :
        pattern = repr (obj.pattern).decode ('string-escape', 'ignore')
        if pattern[:1] == 'u' :
            pattern = 'ur' + pattern [1:]
        else:
            pattern = 'r'  + pattern
        return u're.compile(<span class="string regex">%s</span>)' % pattern
    # end def regex_repr

    def string_repr (self, obj, limit = 70) :
        buf     = ['<span class="string">']
        escaped = escape (obj)
        a       = repr   (escaped [:limit])
        b       = repr   (escaped [limit:])
        if isinstance (obj, unicode) :
            buf.append ('u')
            a = a [1:]
            b = b [1:]
        if b != "''" :
            buf.extend ((a [:-1], '<span class="extended">', b [1:], '</span>'))
        else:
            buf.append (a)
        buf.append     ('</span>')
        return _add_subclass_info (u''.join (buf), obj, (str, unicode))
    # end def string_repr

    def dict_repr (self, d, recursive, limit = 5) :
        if recursive :
            return _add_subclass_info (u'{...}', d, dict)
        buf = ['{']
        have_extended_section = False
        for idx, (key, value) in enumerate (d.iteritems ()) :
            if idx :
                buf.append (', ')
            if idx == (limit - 1) :
                buf.append ('<span class="extended">')
                have_extended_section = True
            buf.append \
                ( '<span class="pair"><span class="key">%s</span>: '
                  '<span class="value">%s</span></span>'
                % (self.repr (key), self.repr (value))
                )
        if have_extended_section :
            buf.append ('</span>')
        buf.append     ('}')
        return _add_subclass_info (u''.join (buf), d, dict)
    # end def dict_repr

    def object_repr (self, obj) :
        return \
            ( u'<span class="object">%s</span>'
            % escape (repr(obj).decode ('utf-8', 'replace'))
            )
    # end def object_repr

    def dispatch_repr (self, obj, recursive) :
        #if obj is helper :
        #    return helper.get_help (None)
        if isinstance (obj, (int, long, float, complex)) :
            return u'<span class="number">%r</span>' % (obj, )
        if isinstance (obj, basestring) :
            return self.string_repr    (obj)
        if isinstance (obj, RegexType) :
            return self.regex_repr     (obj)
        if isinstance (obj, list) :
            return self.list_repr      (obj, recursive)
        if isinstance (obj, tuple) :
            return self.tuple_repr     (obj, recursive)
        if isinstance (obj, set) :
            return self.set_repr       (obj, recursive)
        if isinstance (obj, frozenset) :
            return self.frozenset_repr (obj, recursive)
        if isinstance (obj, dict) :
            return self.dict_repr      (obj, recursive)
        if deque is not None and isinstance (obj, deque) :
            return self.deque_repr     (obj, recursive)
        return self.object_repr        (obj)
    # end def dispatch_repr

    def fallback_repr (self) :
        try:
            info = ''.join (format_exception_only (* sys.exc_info () [:2]))
        except :
            info = '?'
        return \
            ( u'<span class="brokenrepr">&lt;broken repr (%s)&gt;'
              u'</span>' % escape (info.decode ('utf-8', 'ignore').strip ())
            )

    def repr (self, obj) :
        recursive = False
        for item in self._stack :
            if item is obj :
                recursive = True
                break
        self._stack.append (obj)
        try :
            try :
                return self.dispatch_repr (obj, recursive)
            except :
                return self.fallback_repr ()
        finally :
            self._stack.pop ()
    # end der repr

    def dump_object (self, obj) :
        repr = items = None
        if isinstance (obj, dict) :
            title = 'Contents of'
            items = []
            for key, value in obj.iteritems () :
                if not isinstance (key, basestring) :
                    items = None
                    break
                items.append ((key, self.repr (value)))
        if items is None :
            items = []
            repr  = self.repr (obj)
            for key in dir (obj) :
                try:
                    items.append ((key, self.repr (getattr (obj, key))))
                except :
                    pass
            title = 'Details for'
        title    += ' ' + object.__repr__ (obj) [1:-1]
        ### XXX
        return render_template('dump_object.html', items=items,
                               title=title, repr=repr)
    # end def dump_object

    def dump_locals (self, d) :
        items = [(key, self.repr (value)) for key, value in d.items ()]
        ### XXX
        return render_template('dump_object.html', items=items,
                               title='Local variables in frame', repr=None)
    # end def dump_locals

# end class HTML_Repr_Generator

class _Py_Console_ (code.InteractiveInterpreter) :
    """A simple interactive console"""

    class HTML_String_O (TFL.Meta.Object) :
        """A StringO version which escapes HTML entities."""

        def __init__ (self) :
            self._lines   = []
            self.repr_gen = HTML_Repr_Generator ()
        # end def __init__

        def consume (self) :
            result      = "".join (self._lines)
            self._lines = []
            return result
        # end def consume

        def write (self, line) :
            self._write (escape (line))
        # end def write

        def _write (self, line) :
            self._lines.append (line)
        # end def _write

        def displayhook (self, obj) :
            self._write (self.repr_gen.repr (obj))
        # end def displayhook

    # end class HTML_String_O

    def __init__ (self, locls = {}, globls = None) :
        if globls is None :
            globls        = globals ()
        self.globals      = globls
        self._history     = []
        self._histptr     = 0
        self.output       = self.HTML_String_O ()
        self.more         = False
        self.input_buffer = []
        code.InteractiveInterpreter.__init__ (self, locls)
    # end def __init__

    def update_locals (self, ** kw) :
        self.locals.update (kw)
    # end def update_locals

    def runsource (self, source) :
        source = source.rstrip() + '\n'
        prompt = self.more and '... ' or '>>> '
        try :
            source_to_eval = ''.join (self.input_buffer + [source])
            with TFL.Context.attr_let \
                ( sys
                , stdout      = self.output
                , displayhook = self.output.displayhook
                ) :
                if code.InteractiveInterpreter.runsource \
                    (self, source_to_eval, "<debugger>", "single") :
                    self.more = True
                    self.input_buffer.append (source)
                else:
                    self.more          = False
                    self.input_buffer  = []
        finally :
            output = self.output.consume ()
        return prompt + source + output
    # end def runsource

    def runcode (self, code) :
        try:
            exec code in self.globals, self.locals
        except:
            self.showtraceback ()
    # end def runcode

    def showtraceback (self) :
        from werkzeug.debug.tbtools import get_current_traceback
        tb = get_current_traceback(skip=1)
        sys.stdout._write(tb.render_summary())
    # end def showtraceback

    def showsyntaxerror (self, filename = None) :
        from werkzeug.debug.tbtools import get_current_traceback
        tb = get_current_traceback(skip=4)
        sys.stdout._write(tb.render_summary())
    # end def showsyntaxerror

    def write (self, data) :
        sys.stdout.write (data)
    # end def write

    def __call__ (self, cmd) :
        return self.runsource (cmd)
    # end def __call__

# end class _Py_Console_

class Console (GTW.NAV.Page) :
    """Provide a interactive python console `window`."""

    template = "console"

    _Media   = GTW.Media \
        ( css_links   =
            ( GTW.CSS_Link ("/media/GTW/css/python-console.css")
            ,
            )
        , js_on_ready =
            ( "$('div.console').open_shell (null, 0);"
            ,
            )
        , scripts     =
            ( GTW.Script._.jQuery
            , GTW.Script (src = "/media/GTW/js/jquery.debugger.js")
            )
        )

    console           = None
    completion_cutoff = 30

    @TFL.Meta.Once_Property
    def console (self) :
        return _Py_Console_ (dict (NAV  = self.top, page = self))
    # end def console

    def _completion_cand_cahr (self, candidate, pos) :
        try :
            return candidate [pos]
        except IndexError :
            return ""
    # end def _completion_cand_cahr

    def rendered (self, handler) :
        request  = handler.request
        req_data = request.req_data
        cmd      = req_data.get ("cmd")
        complete = req_data.get ("complete")
        if complete :
            console      = self.console
            input, cands = TFL.complete_command \
                (complete, console.globals, console.locals)
            cands        = cands.strip ().split (",")
            completed    = False
            if len (cands) == 1 :
                if len (input) >= len (complete) :
                    completed = True
                else :
                    input     = complete
            elif len (cands) > self.completion_cutoff :
                #cp           = 0 ###len (input)
                #import pdb; pdb.set_trace ()
                #cands_by_apl = dusplit \
                #    (cands, lambda c : self._completion_cand_cahr (c, cp))
                cands        = \
                    [ TFL.I18N._T
                       ("There are %s possible completions" % (len (cands)))
                    ]
                #for cbya in cands_by_apl :
                #    cands.append \
                #        ( TFL.I18N._T
                #            ("%s starting with %s" % (len (cbya, "X")))
                #        )
            return handler.json \
                ( dict ( input     = input
                       , cands     = ", ".join (cands)
                       , completed = completed
                       )
                )
        elif not cmd :
            top      = self.top
            referer  = request.headers.get ("Referer")
            if top and referer :
                url   = TFL.Url (referer)
                self.console.update_locals \
                    ( last_page = top.page_from_href (url.path [1:])
                    , referer   = url
                    )
        else :
            return handler.json \
                (dict (html = self.console (cmd), more = self.console.more))
        return self.__super.rendered (handler, self.template)
    # end def rendered

# end class Console

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.Nav.Console


