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
          var $legend    = this.element.find ("legend");
          var add_class  = this._getData     ("add_class");
          var $m2m_range = this.element.find ("input.many-2-many-range:first");
          var  m2m_range = $m2m_range.attr   ("value").split (":");
          var cur_count  = parseInt (m2m_range [1]);
          var max_count  = parseInt (m2m_range [2]);
          this._setData ("$prototype", this.element.find (".m2m-prototype"));
          this._setData ("$m2m_range", $m2m_range);
          this._setData ("min_count",  parseInt (m2m_range [0]));
          this._setData ("cur_count",  cur_count);
          this._setData ("cur_number", cur_count);
          this._setData ("max_count",  max_count);
          $legend.prepend
              ( '<a href="#add" class="ui-icon ui-icon-plusthick '
              + add_class
              + '" title="Add ' + $legend.attr ("title")
              + '">Add</a> '
              );
          var $forms = this.element.find (".m2m-nested-form");
          for (var i = 0; i < $forms.length; i++)
          {
              this._add_delete_button ($forms.eq (i));
          }
          this._update_button_states ();
      }
    , _add_delete_button : function ($form)
      {
          var $link = $form.find ("a[href=#delete]");
          if (! $link.length)
          {
              var  first_tag = $form.get (0).tagName.toLowerCase ();
              $link          =
                  $('<a href="#delete" class="ui-icon ui-icon-closethick">Delete</a>');
              var $element = $link;
              if (first_tag == "tr")
                  $element = $("<td></td>").append ($link);
              $form.append ($element);
          }
          /* we can only bind callback's once the element is part of the DOM */
          $link.bind ("click", this, this._delete_form);
      }
    , _add_new_form : function (evt)
      {
          var self       = evt.data;
          var $prototype = self._getData    ("$prototype");
          var $new       = $prototype.clone ().removeClass ("m2m-prototype");
          /* now that we have cloned the block, let's change the
          ** name/id/for attributes
          */
          self._setData ("cur_count", self._getData ("cur_count") + 1);
          var cur_number = self._getData ("cur_number") + 1;
          self._setData ("cur_number", cur_number);
          var pattern    = /MP-/;
          var new_no     = "M" + cur_number + "-";
          var $labels    = $new.find     ("label")
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
          self._add_delete_button    ($new);
          self._update_button_states ();
          $prototype.parent          ().append ($new);
          evt.preventDefault         ();
          evt.preventDefault ();
      }
    , _update_button_states : function ()
      {
          var $add_button = this.element.find ("legend a.ui-icon");
          var cur_count = this._getData ("cur_count");
          var max_count = this._getData ("max_count");
          if (cur_count < max_count)
              $add_button.bind ("click", this, this._add_new_form);
          else
              $add_button.addClass ("ui-state-disabled");
      }
    , _forms_equal : function ($l, $r)
      {
          /* Returns whether the values of the two forms are equal */
          var $l_value_elements = $l.find ("[value]");
          var $r_value_elements = $r.find ("[value]");
          if ($l_value_elements.length != $r_value_elements.length)
              return false;
          for (var i = 0; i < $l_value_elements.length; i++)
          {
              if (  $l_value_elements.eq (i).attr ("value")
                 != $r_value_elements.eq (i).attr ("value")
                 )
                  return false;
          }
          return true;
      }
    , _delete_form : function (evt)
      {
          var self       = evt.data;
          var $prototype = self._getData         ("$prototype");
          var $form      = $(evt.target).parents (".m2m-nested-form");
          self._setData ("cur_count", self._getData ("cur_count") + 1);
          if (self._forms_equal ($form, $prototype))
          {
              $form.remove ();
          }
          else
          {
              var $link = $form.find ("a[href=#delete]");
              if ($link.hasClass ("ui-icon-closethick"))
              {
                  $form.find        ("input, textarea, select")
                       .attr        ("disabled","disabled");
                  $link.removeClass ("ui-icon-closethick")
                       .addClass    ("ui-icon-circle-close");
              }
              else
              {
                  $form.find        ("input, textarea, select")
                       .removeAttr  ("disabled");
                  $link.removeClass ("ui-icon-circle-close")
                       .addClass    ("ui-icon-closethick");
              }
          }
          evt.preventDefault ();
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
