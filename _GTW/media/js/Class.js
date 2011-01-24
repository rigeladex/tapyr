/*
** Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
** Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
** ****************************************************************************
** This file is part of the library GTW.
**
** This file is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**
** This file is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU General Public License for more details.
**
** You should have received a copy of the GNU General Public License
** along with this file. If not, see <http://www.gnu.org/licenses/>.
** ****************************************************************************
**
**++
** Name
**    Class
**
** Purpose
**    Provide a javascript class based on ideas of
**        http://dean.edwards.name/weblog/2006/03/base/
**    and
**        http://ejohn.org/blog/simple-javascript-inheritance/
**
**
** Revision Dates
**    24-Jan-2011 (CT) Creation
**    ««revision-date»»···
**--
*/

( function(scope)
  {
    var Class = function () {};
    var making_prototype = false;
    var super_re   = /\bthis._super\b/;
    var super_test =
        ( super_re.test (function () { this._super; })
        ? super_re.test : function () { return true; }
        );
    Class.extend = function (dict)
      {
        ««statement»»···
      };
    ««statement»»···
    $.GTW.Class = Class;
  }
) ($.GTW);

/* __END__ Class.js */
