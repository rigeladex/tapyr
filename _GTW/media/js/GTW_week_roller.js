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
**    17-Nov-2010 (CT) `init_cal` changed to use AJAX `.load` to fill `div$`
**    19-Nov-2010 (CT) `push_history` called
**    26-Nov-2010 (CT) `init_slider` added and used
**    ««revision-date»»···
**--
*/

( function($)
  {
    $.fn.GTW_week_roller = function (options)
      {
        var options  = $.extend
          ( { apply_button_name : "Apply"
            , cal_selector      : "table.calendar"
            , ctrl_selector     : "form.ctrl"
            , selected_class    : "selected"
            , day_selector      : "td"
            , slider_selector   : ".slider"
            , today_selector    : "td.today"
            , q_day_transformer : function (href)
                { return href.replace (/(\d{4}\/\d{1,2}\/\d{1,2})/, "qx/$1"); }
            , q_url_transformer : function (name)
                { return name.replace (/\/q/, "/qx"); }
            }
          , options || {}
          );
        function change_field (name, context, response, value)
          {
            $("input[name='" + name + "']", context).attr
              ("value", (value != null) ? value : response [name]);
          }
        function init_cal (wr$)
          {
            var cal$   = $(options.cal_selector, wr$);
            var div$   = $("div." + options.selected_class, wr$);
            var today$ = $(options.today_selector, cal$);
            $(options.day_selector, cal$).each
              ( function ()
                  {
                    var day  = this;
                    var day$ = $(day);
                    var href = $("span.date a", day$).attr ("href");
                    if (href)
                      {
                        var qx = options.q_day_transformer (href);
                        day$.click
                          ( function (ev)
                              {
                                div$.load (qx).css ({display : "block"});
                                if (options.selected)
                                  {
                                    $(options.selected).removeClass
                                      (options.selected_class);
                                  }
                                day$.addClass (options.selected_class);
                                options.selected = day;
                                if (ev && ev.preventDefault)
                                  {
                                    ev.preventDefault ();
                                  }
                              }
                          );
                      }
                  }
              );
            today$.triggerHandler ("click");
          }
        function init_ctrl (wr$)
          {
            $(options.ctrl_selector, wr$).each
              ( function ()
                  {
                    var ctrl$ = $(this);
                    var cal$  = $(options.cal_selector, wr$);
                    var q_url = this.action;
                    var x_url = options.q_url_transformer (q_url);
                    $("input[type='submit']", ctrl$).click
                      ( function (ev)
                          {
                            var args = ctrl$.serialize ()
                                  + "&" + this.name + "=" + this.value;
                            $.getJSON
                              ( x_url
                              , args
                              , function (response)
                                  {
                                    if (response)
                                      {
                                        cal$.replaceWith (response.calendar);
                                        change_field ("day",   ctrl$, response);
                                        change_field ("month", ctrl$, response);
                                        change_field ("weeks", ctrl$, response);
                                        change_field ("year",  ctrl$, response);
                                        cal$  = $(options.cal_selector, wr$);
                                        init_cal (wr$);
                                        $.GTW.push_history (q_url + "?" + args);
                                      }
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
        function init_slider (wr$)
          {
            $(options.slider_selector, wr$).each
              ( function ()
                  {
                    var slider$ = $(this);
                    var apply$  =
                        $("input[name='"+options.apply_button_name+"']", wr$);
                    function change (event, ui)
                        {
                          var value = - ui.value;
                          if (value)
                            {
                              change_field          ("delta", wr$, null, value);
                              apply$.triggerHandler ("click");
                              change_field          ("delta", wr$, null, "");
                              slider$.slider        ("value", 0);
                            }
                        }
                    function slide (event, ui)
                        {
                          var value = - ui.value;
                          if (value)
                            {
                              change_field ("delta", wr$, null, value);
                            }
                        }
                    slider$.slider
                      ( { max         : 53
                        , min         : -53
                        , orientation : "vertical"
                        , value       : 0
                        , change      : change
                        , slide       : slide
                        }
                      );
                    slider$.addClass ("enabled");
                  }
              );
          }
        $(this).each
          ( function ()
              {
                init_ctrl   ($(this));
                init_slider ($(this));
              }
          );
        return this;
      }
  }
) (jQuery);

/* __END__ GTW_week_roller.js */
