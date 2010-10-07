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
**    GTW_Gallery
**
** Purpose
**    jQuery plugin for a photo gallery
**
**
** Revision Dates
**     7-Oct-2010 (CT) Creation
**    ««revision-date»»···
**--
*/

( function($)
  {
    $.fn.GTW_Gallery = function (options)
      {
        var options = $.extend
          ( { controls        :
                { head        : ".button.head"
                , next        : ".button.next"
                , play        : ".button.play"
                , prev        : ".button.prev"
                , tail        : ".button.tail"
                }
            , delay           : 3000
            , inline_selector : ".gallery .inline"
            , photo_selector  : ".photo img"
            , play_class      : "playing"
            , url_transformer : function (name)
                { return name.replace (/\/th\//, "/im/"); }
            }
          , options || {}
          );
        function show (index, event)
          {
            if (index < 0)
              {
                index += options.thumbnails$.length
              }
            $(options.photo_selector).attr
                ( "src"
                , options.url_transformer (options.thumbnails$ [index].src)
                );
            options.current = index;
            if (event != null)
              {
                event.preventDefault ();
              }
          }
        function next (event)
          {
            show ((options.current + 1) % options.thumbnails$.length, event);
          }
        function prev (event)
          {
            show
              ( (options.thumbnails$.length + options.current - 1)
              % (options.thumbnails$.length)
              , event
              );
          }
        options.current     = 0;
        options.thumbnails$ = $("img", this);
        options.thumbnails$.each
          ( function (n)  { $(this).data ("GTW-gallery-index", n); }
          ).click
          ( function (ev) { show ($(this).data ("GTW-gallery-index"), ev); });
        this.addClass ("inline");
        $(options.inline_selector).show ();
        $(options.photo_selector).click (next);
        $(options.controls.next).click  (next);
        $(options.controls.prev).click  (prev);
        $(options.controls.head).click  (function (ev) { show (0, ev); });
        $(options.controls.tail).click  (function (ev) { show (-1, ev); });
        $(options.controls.play).toggle
          ( function (event)
              {
                options.play_cb = window.setInterval
                  ( function ()
                      { $(options.controls.next).triggerHandler ("click"); }
                  , options.delay
                  );
                $(event.target).addClass (options.play_class);
                $(options.controls.next).click ();
              }
          , function (event)
              {
                window.clearInterval (options.play_cb);
                $(event.target).removeClass (options.play_class);
              }
          );
        show (0);
        return this;
      }
  }
) (jQuery);

/* __END__ GTW_Gallery.js */
