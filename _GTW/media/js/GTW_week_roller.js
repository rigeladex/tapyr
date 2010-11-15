/*
** Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
**    GTW_week_roller
**
** Purpose
**    jQuery plugin for a calendar displayed as week_roller
**
**
** Revision Dates
**    15-Nov-2010 (CT) Creation
**    ««revision-date»»···
**--
*/

( function($)
  {
    $.fn.GTW_week_roller = function (options)
      {
        var options  = $.extend
          ( { cal_selector      : "table.calendar"
            , ctrl_selector     : "form.ctrl"
            , q_url_transformer : function (name)
                { return name.replace (/\/q/, "/qx"); }
            }
          , options || {}
          );
        function _init_ctrl (wr$)
          {
            $(options.ctrl_selector, wr$).each
              ( function ()
                  {
                    var ctrl$ = $(this);
                    var cal$  = $(options.cal_selector, wr$);
                    var url   = options.q_url_transformer (this.action);
                    $("input[type='submit']", ctrl$).click
                      ( function (ev)
                          {
                            stop (ev);
                            $.getJSON
                              ( url
                              , ctrl$.serialize ()
                                  + "&" + this.name + "=" + this.value
                              , function (response)
                                  {
                                    cal$.html (response.calendar);
                                    $("input[name='day']",   ctrl$).attr ("value", response.day);
                                    $("input[name='month']", ctrl$).attr ("value", response.month);
                                    $("input[name='weeks']", ctrl$).attr ("value", response.weeks);
                                    $("input[name='year']",  ctrl$).attr ("value", response.year);
                                  }
                              )
                            if (ev && ev.preventDefault)
                              {
                                ev.preventDefault ();
                              }
                          }
                      );
                  }
              );
          }
        $(this).each
          ( function ()
              {
                _init_ctrl ($(this));
              }
          );
        return this;
      }
  }
) (jQuery);

/* __END__ GTW_week_roller.js */
