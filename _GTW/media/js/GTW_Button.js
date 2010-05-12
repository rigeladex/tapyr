/*
** Copyright (C) 2010 Martin Glueck All rights reserved
** Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
** This file is part of the library GTW.
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
**    GTW_Button
**
** Purpose
**    Wrapper around the jQuery UI button to support two state buttons with
**    different icons for each state and some additional features.
**
** Revision Dates
**     9-May-2010 (MG) Creation
**    ««revision-date»»···
**--
*/
(function ($)
{
  var _T;
  var _;
  var _Tn;

  if ($.I18N === undefined)
    {
      _T = _ = _Tn = function (t) { return t; }
    }
  else
    {
      _T = _ = $.I18N._T;
      _Tn    = $.I18N._Tn;
    }

  var GTW_Button =
    { _create : function ()
      {
        var O = this.options;
        if (O.states === undefined)
          {
            var state     = {};
            var attr_list = ["icon", "callback", "label"];
            for (var i = 0; i < attr_list.length; i++)
              state [attr_list [i]] = O [attr_list [i]];
            O.states        = [state];
            O.initial_state = 0;
          }
        O.state  = (O.initial_state || 0) - 1;
        if (O.state < 0) O.state = O.states.length - 1;
        this.element.data ("O", O);
        this.element.bind ("click", this, function (evt)
            {
              var self     = evt.data;
              self._update_icon (evt, true);
              return false;
            }).addClass ("ui-icon");
        this._update_icon (undefined, false);
      }
    , _update_icon : function (evt, trigger)
      {
          var O        = this.element.data ("O");
          var old_icon = O.states [O.state].icon;
          O.state     += 1;
          if (O.state >= O.states.length) O.state = 0;
          var new_icon = O.states [O.state].icon;
          this.element.removeClass (old_icon).addClass (new_icon);
          if (trigger)
            {
              var callback = O.states [O.state].callback;
              callback (evt, O.data);
            }
      }
    };
  $.widget ("ui.GTW_Button", GTW_Button);
  $.extend
      ( $.ui.GTW_Form
      , { "version"      : "0.1"
        , "defaults"     :
          { group        : ""
          , states       : []
          }
        }
      )

})(jQuery);
