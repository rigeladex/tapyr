/*
** Copyright (C) 2009 Martin Glück All rights reserved
** Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
**
** This library is free software; you can redistribute it and/or
** modify it under the terms of the GNU Library General Public
** License as published by the Free Software Foundation; either
** version 2 of the License, or (at your option) any later version.
**
** This library is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
** Library General Public License for more details.
**
** You should have received a copy of the GNU Library General Public
** License along with this library; if not, write to the Free
** Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
** ****************************************************************************
**
**++
** Name
**    model_edit_ui
**
** Purpose
**    Define a jQuery UI widget handling the nested many to many forms
**
** Revision Dates
**    20-Jun-2009 (MG) Creation
**    ««revision-date»»···
**--
*/

(function ($)
{
  var Many2Many =
    { _init : function ()
      {
          var $legend    = $("legend", this.element);
          var add_class  = this._getData ("add_class");
          var $m2m_range = this.element.find ("input.many-2-many-range:first");
          var  m2m_range = $m2m_range.attr ("value").split (":");
          var cur_count  = parseInt (m2m_range [1]);
          var max_count  = parseInt (m2m_range [2]);
          this._setData ("$m2m_range", $m2m_range);
          this._setData ("min_count", parseInt (m2m_range [0]));
          this._setData ("cur_count", cur_count);
          this._setData ("max_count", max_count);
          $legend.prepend
              ( '<a href="#add" class="ui-icon ui-icon-circle-plus '
              + add_class
              + '" title="Add ' + $legend.attr ("title")
              + '">Add</a> '
              );
          var $forms = this.element.find (".m2m-clone");
          for (var i = 0; i < $forms.length; i++)
          {
              var $form = $forms.eq (i);
              var  first_tag = $form.get (0).tagName.toUpperCase ();
              var $link      =
                  $('<a href="#delete" class="ui-icon ui-icon-circle-close">Delete</a>');
              if (first_tag == "TR")
                  $link = $("<td></td>").append ($link);
              $form.append ($link);
          }
          this._update_add_button ();
      }
    , _add_new_form : function (evt)
      {
          var self = evt.data;
          /* find the block which will be cloned */
          var $old = self.element.find (".m2m-clone:first");
          var $new = $old.clone ()
          /* now that we have cloned the block, let's change the
          ** name/id/for attributes
          */
          var cur_count = self._getData ("cur_count");
          self._setData ("cur_count", cur_count + 1);
          var pattern   = /M(\d+)-/;
          var new_no    = "M" + cur_count + "-";
          var $labels   = $new.find     ("label")
          for (var i = 0; i < $labels.length; i++)
          {
              var $l = $labels.eq (i);
              $l.attr ("for", $l.attr ("for").replace (pattern, new_no));
          }
          var $edit_elements = $new.find ("input, textarea, select");
          var  edit_mod_list = ["id", "name"];
          for (var i = 0; i < $edit_elements.length; i++)
          {
              var $e = $edit_elements.eq (i);
              for (var j = 0; j < edit_mod_list.length; j++)
              {
                  var n = edit_mod_list [j];
                  $e.attr (n, $e.attr (n).replace (pattern, new_no));
              }
          }
          /* we are ready to add the new block at the end */
          $old.parent ().append ($new);
          self._update_add_button ();
          evt.preventDefault ();
      }
    , _update_add_button : function ()
      {
          var $add_button = this.element.find ("legend a.ui-icon");
          var cur_count = this._getData ("cur_count");
          var max_count = this._getData ("max_count");
          if (cur_count < max_count)
              $add_button.bind ("click", this, this._add_new_form);
          else
              $add_button.addClass ("ui-state-disabled");
      }
    }
  $.widget ("ui.many2many", Many2Many);
  $.extend
    ( $.ui.many2many
    , { version                          : "0.1"
      , defaults                         :
        { add_class                      : "m2m-add"
        }
      }
    );
})(jQuery);
