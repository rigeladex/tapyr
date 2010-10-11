/*
** Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
** Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
** ****************************************************************************
**
**
** This file is free software: you can redistribute it and/or modify
** it under the terms of the GNU Affero General Public License as published by
** the Free Software Foundation, either version 3 of the License, or
** (at your option) any later version.
**
** This file is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU Affero General Public License for more details.
**
** You should have received a copy of the GNU Affero General Public License
** along with this file. If not, see <http://www.gnu.org/licenses/>.
** ****************************************************************************
**
**++
** Name
**    GTW_util
**
** Purpose
**    Utility javascript functions for GTW
**
**
** Revision Dates
**     3-Aug-2010 (CT) Creation (`as_int_array`)
**     4-Aug-2010 (CT) `fix_a_nospam` added (factored from GTW.jQuery)
**    10-Oct-2010 (CT) `GTW_Externalize` added
      ��revision-date�����
**--
*/

( function($)
  {
    $.GTW = $.GTW || {};
    $.extend
      ( $.GTW
      , { as_int_array : function (data)
          {
            var list   = data.split (",");
            var pat    = /^\s*\d+\s*([-+]\s*\d+)?\s*$/;
            var result = new Array ();
            for (i = 0; i < list.length; i+= 1)
              {
                var x = list [i];
                if (x.search (pat) != null)
                  {
                    result.push (eval (x));
                  }
              }
            return result;
          }
        , fix_a_nospam : function ($)
          {
            $("a.nospam").each
              ( function (i)
                {
                  var rel = $(this).attr ("rel");
                  if (rel != null)
                    {
                      var aia = $.GTW.as_int_array (rel);
                      $(this).replaceWith
                          (String.fromCharCode.apply (null, aia));
                    }
                }
              );
          }
        }
      );
    $.fn.GTW_Externalize = function ()
      {
        this.click
          ( function (event)
              {
                window.open (this.href).focus ();
                if (event && event.preventDefault)
                  {
                    event.preventDefault ();
                  }
              }
          ).addClass ("external");
        return this;
      };
  }
) (jQuery);

/* __END__ GTW_util.js */
