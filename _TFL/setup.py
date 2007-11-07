#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria.
# Web: http://www.c-tanzer.at/en/ Email: tanzer@swing.co.at
# All rights reserved
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************

import os
import sys
from   distutils.core import setup

os.chdir (os.path.dirname (__file__))

name    = 'TFL'
license = 'GNU Library or Lesser General Public License (LGPL)'
version = os.popen ('svnversion').read ().strip ()
if version.isdigit () :
    pkgs    = []
    # path-walking probably only works in Unix due to hardcoded '/'
    for root, dirs, files in os.walk ('../_' + name) :
        # ugly: need to modify dirs in place!
        dd = set (d for d in dirs if d.startswith ('_'))
        for d in dirs :
            if d not in dd :
                dirs.remove (d)
        pkgs.append (root.replace ('/', '.') [3:])
    setup \
        ( name             = name
        , version          = version
        , description      =
            "Library with lots of useful stuff (says Ralf Schlatterbeck)"
        # long_description =
        , license          = license
        , author           = "Christian Tanzer and others"
        , author_email     = "tanzer@swing.co.at"
        , url              = "http://www.c-tanzer.at/en"
        , packages         = pkgs
        , package_dir      = {'_' + name : ''}
        , platforms        = 'Any'
        , classifiers      = \
            [ 'Development Status :: 6 - Mature'
            , 'License :: OSI Approved :: ' + license
            , 'Operating System :: OS Independent'
            , 'Programming Language :: Python'
            , 'Intended Audience :: Developers'
            , 'Topic :: Software Development :: Libraries'
            , 'Topic :: Software Development :: Libraries :: '
                'Application Frameworks'
            , 'Topic :: Software Development :: Libraries :: Python Modules'
            ]
        )
else :
    print "SVN version `%s` is not amenable to using setup" % (version, )
    print "   Please check-in your changes, if any, and update your sandbox"
