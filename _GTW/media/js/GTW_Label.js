/*
** Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
** Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
** ****************************************************************************
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
**    GTW_Label
**
** Purpose
**    jQuery plugin for improving labels
**
**
** Revision Dates
**    12-Jan-2011 (CT) Creation
**    ««revision-date»»···
**--
*/

( function($)
  {
    function label_target (label$)
      {
        var id = label$.attr ("for");
        var result;
        if (id)
          {
            result = $("#" + id).get (0);
          }
        return result;
      }
    $.fn.gtw_label_as_placeholder = function (options)
      {
        var options  = $.extend
          ( { hide_parent : false
            }
          , options || {}
          );
        this.each
          ( function ()
              {
                var label$ = $(this);
                var target = label_target (label$);
                if (target)
                  {
                    var target$ = $(target);
                    var placeholder = target$.attr ("placeholder");
                    if (! placeholder)
                      {
                        target$.attr ("placeholder", label$.text ());
                        var to_hide$ = options.hide_parent
                          ? label$.closest (options.hide_parent) : label$;
                        to_hide$.css ("display", "none");
                      }
                  }
              }
          );
        return this;
      }
    $.fn.gtw_label_clicker = function (options)
      {
        var options  = $.extend
          ( { l_class : "clickable"
            }
          , options || {}
          );
        this.each
          ( function ()
              {
                var label$ = $(this);
                var target = label_target (label$);
                if (target)
                  {
                    label$.click (function (ev) { target.focus (); });
                    options.l_class && label$.addClass (options.l_class);
                  }
              }
          );
        return this;
      }
  }
) (jQuery);

/* __END__ GTW_Label.js */
