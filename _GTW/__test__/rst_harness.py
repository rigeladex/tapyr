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
#    GTW.__test__.rst_harness
#
# Purpose
#    Harness for testing RESTful apis
#
# Revision Dates
#     9-Jan-2013 (CT) Creation (factor from RST)
#    31-Jan-2013 (CT) Change `_main` to use `Backend_Default_Path`
#    31-Jan-2013 (CT) Use `url.scheme` as default `db_name` extension in
#                     `run_server`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW.__test__.Test_Command import *

from   posixpath import join as pp_join

import multiprocessing
import requests
import subprocess
import sys
import time

def req_json (r) :
    if r is not None and r.content :
        result = r.json
        if TFL.callable (result) :
            try :
                result = result ()
            except Exception :
                result = None
        return result
# end def req_json

def _run_server (Scaffold, args = []) :
    print (["run_server"] + server_args + args)
    result = Scaffold (["run_server"] + server_args + args)
    return result
# end def run_server

def run_server (test_module_name, db_url = "hps://", db_name = None) :
    import socket
    import tempfile
    import _TFL.Url
    url = TFL.Url (db_url)
    if not db_name :
        db_name = "test.%s" % (url.scheme, )
    cmd = \
        [ sys.executable, "-c"
        , "; ".join
            ( ( "import %s" % (test_module_name, )
              , "%s.Scaffold " % (test_module_name, )
              + "( "
              + repr
                  ( ["run_server"]
                  + server_args
                  + ["-db_url", db_url, "-db_name", db_name]
                  )
              + ")"
              )
            )
        ]
    tf = tempfile.NamedTemporaryFile (delete = False)
    print ("Using", tf.name, "as stdout/stderr for server process", file=sys.stderr)
    p = subprocess.Popen (cmd, stderr = tf, stdout = tf)
    s = socket.socket    (socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout         (1.0)
    i   = 0
    while True :
        try :
            s.connect (("localhost", 9999))
        except socket.error as exc :
            if i < 20 :
                i += 1
                time.sleep (1)
            else :
                break
        else :
            exc = None
            break
    s.close ()
    if exc is not None :
        print  ("Socket connect gave exception:", exc)
        p.kill ()
    return p
# end def run_server

def _normal (k, v) :
    if k in ("date", "last-modified") :
        v = "<datetime instance>"
    elif k in ("etag",) :
        v = "ETag value"
    elif k == "content-length" and int (v) != 0 :
        v = "<length>"
    elif k == "server" :
        v = "<server>"
    return k, v
# end def _normal

def show (r, ** kw) :
    json = req_json (r)
    if json is not None :
        kw ["json"] = json
    elif r.content :
        kw ["content"] = r.content.replace ("\r", "").strip ().split ("\n")
    output = formatted \
        ( dict
            ( status  = r.status_code
            , url     = r.url
            , ** kw
            )
        )
    print (output)
    return r
# end def show

def showf (r, ** kw) :
    return show \
        ( r
        , headers = dict (_normal (k, v) for k, v in r.headers.iteritems ())
        , ** kw
        )
# end def showf

def traverse (url, level = 0, seen = None) :
    if seen is None :
        seen = set ()
    rg    = requests.get     (url)
    ro    = requests.options (url)
    path  = requests.utils.urlparse (url).path or "/"
    if ro.ok :
        allow = ro.headers ["allow"]
        if allow not in seen :
            print (path, ":", allow)
            seen .add (allow)
    else :
        print (path, ":", ro.status_code, ro.content)
    if rg.ok :
        json = req_json (rg)
        if json :
            l = level + 1
            for e in json.get ("entries", ()) :
                traverse ("http://localhost:9999" + str (e), l, seen)
# end def traverse

class Requester (TFL.Meta.Object) :
    """Wrapper for `requests`"""

    class W (TFL.Meta.Object) :

        def __init__ (self, name, prefix) :
            self.method = getattr (requests, name)
            self.prefix = prefix
        # end def __init__

        def __call__ (self, path, * args, ** kw) :
            kw.setdefault ("headers", { "Content-Type": "application/json" })
            url = pp_join (self.prefix, path.lstrip ("/"))
            return self.method (url, * args, ** kw)
        # end def __call__

    # end class W

    def __init__ (self, prefix) :
        self.prefix = prefix
    # end def __init__

    def __getattr__ (self, name) :
        return self.W (name, self.prefix)
    # end def __getattr__

# end class Requester

R = Requester ("http://localhost:9999")

server_args = \
    [ "-UTP=RST"
    , "-auto_reload=no"
    , "-debug=no"
    , "-load_I18N=no"
    , "-log_level=0"
    , "-port=9999"
    ]

def _main (Scaffold) :
    backend = sos.environ.get \
        ("GTW_test_backends", "HPS").split (":") [0].strip ()
    db_url  = Scaffold.Backend_Parameters.get   (backend, "hps://").strip ("'")
    db_name = Scaffold.Backend_Default_Path.get \
        (backend, "test.%s" % (back.lower (), ))
    _run_server \
        (Scaffold, ["-db_url", db_url, "-db_name", db_name, "-debug", "no"])
# end def _main

### __END__ GTW.__test__.rst_harness
