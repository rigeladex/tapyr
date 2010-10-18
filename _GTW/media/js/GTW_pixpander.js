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
**    GTW_pixpander
**
** Purpose
**    jQuery plugin for expanding linked images in place
**
**
** Revision Dates
**    18-Oct-2010 (CT) Creation
**    ««revision-date»»···
**--
*/

( function($)
  {
    $.fn.GTW_pixpander = function (options)
      {
        var options  = $.extend
          ( { x_class     : "pixpanded"
            }
          , options || {}
          );
        $(this).each
          ( function ()
              {
                var img  = this;
                var img$ = $(img);
                var a    = img$.closest ("a");
                var src  = img.src;
                var sty  = img.style;
                function show (event, url, style)
                  {
                    img$.attr
                      ( { src   : url
                        , style : style
                        }
                      );
                    options.x_class && img$.toggleClass (options.x_class);
                    if (event && event.preventDefault)
                      {
                        event.preventDefault ();
                      }
                  }
                img$.toggle
                  ( function (ev) { show (ev, a.attr ("href"), ""); }
                  , function (ev) { show (ev, src, sty); }
                  )

              }
          );
        return this;
      }
  }
) (jQuery);

/* __END__ GTW_pixpander.js */
