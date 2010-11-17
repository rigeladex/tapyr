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
**    16-Nov-2010 (CT) `change_field` factored
**    16-Nov-2010 (CT) `init_cal` added and used
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
            , selected_class    : "selected"
            , day_selector      : "td"
            , q_url_transformer : function (name)
                { return name.replace (/\/q/, "/qx"); }
            }
          , options || {}
          );
        function change_field (name, context, response)
          {
            $("input[name='" + name + "']", context).attr
              ("value", response [name]);
          }
        function init_cal (wr$)
          {
            var cal$  = $(options.cal_selector, wr$);
            var div$  = $("div." + options.selected_class, wr$);
            $(options.day_selector, cal$).click
              ( function (ev)
                  {
                    if (options.selected)
                      {
                        $(options.selected).removeClass
                          (options.selected_class);
                      }
                    $(this).addClass (options.selected_class);
                    options.selected = this;
                    div$.html ("").css ({display : "block"});
                    div$.append ($("<h1>" + $(this).attr ("title") + "</h1>"));
                    $(this).children ().each
                      ( function (n)
                          {
                            if (n > 0)
                              {
                                div$.append
                                  ( $( "<div>"
                                     + $(this).attr ("title")
                                     + " : "
                                     + $(this).html ()
                                     + "</div>"
                                     )
                                  );
                              }
                          }
                      );
                    if (ev && ev.preventDefault)
                      {
                        ev.preventDefault ();
                      }
                  }
              );
          }
        function init_ctrl (wr$)
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
                                    cal$.replaceWith (response.calendar);
                                    change_field ("day",   ctrl$, response);
                                    change_field ("month", ctrl$, response);
                                    change_field ("weeks", ctrl$, response);
                                    change_field ("year",  ctrl$, response);
                                    init_cal (wr$);
                                    cal$  = $(options.cal_selector, wr$);
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
            init_cal (wr$);
          }
        $(this).each
          ( function ()
              {
                init_ctrl ($(this));
              }
          );
        return this;
      }
  }
) (jQuery);

/* __END__ GTW_week_roller.js */
