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
**     8-Oct-2010 (CT) Creation continued
**    ««revision-date»»···
**--
*/

( function($)
  {
    $.fn.GTW_Gallery = function (options)
      {
        var controls = $.extend
          ( { head        : ".button.head"
            , next        : ".button.next"
            , play        : ".button.play"
            , prev        : ".button.prev"
            , tail        : ".button.tail"
            }
          , options.controls || {}
          );
        var options  = $.extend
          ( { delay           : 3000
            , inline_selector : ".gallery .inline"
            , photo_selector  : ".photo img"
            , play_class      : "playing"
            , url_transformer : function (name)
                { return name.replace (/\/th\//, "/im/"); }
            }
          , options || {}
          , { controls        : controls }
          );
        function show (index, event)
          {
            var len   = options.thumbnails$.length;
            var photo = $(options.photo_selector);
            var alt   = photo.attr ("alt");
            var thumb, url;
            if (index < 0)
              {
                index += len;
              }
            index = options.current = index % len;
            thumb = options.thumbnails$ [index];
            url   = options.url_transformer (thumb.src);
            photo.attr
              ( { src   : url
                , title :
                    (alt ? alt + ":" : "Photo") + " " + (index+1) + "/" + len
                }
              );
            if (event && event.preventDefault)
              {
                event.preventDefault ();
              }
          }
        function next (event)
          {
            show (options.current + 1, event);
          }
        function prev (event)
          {
            show (options.current - 1, event);
          }
        function start (event)
          {
            options.play_cb = window.setInterval (next, options.delay);
            $(options.controls.play)
              .addClass (options.play_class)
              .unbind   ("click")
              .click    (stop);
            next ();
          }
        function stop (event)
          {
            if ($(options.controls.play).hasClass (options.play_class))
              {
                window.clearInterval (options.play_cb);
                $(options.controls.play)
                  .unbind      ("click")
                  .click       (start)
                  .removeClass (options.play_class);
              }
          }
        this.addClass ("inline");
        options.current = 0;
        options.thumbnails$ = $("img", this);
        options.thumbnails$
          .each
            ( function (n)
                { $(this).data ("GTW-gallery-index", n); }
            )
          .click
            ( function (ev)
                { stop (ev); show ($(this).data ("GTW-gallery-index"), ev); }
            );
        $(options.controls.next).click
            (function (ev) { stop (ev); next (ev); });
        $(options.controls.prev).click
            (function (ev) { stop (ev); prev (ev); });
        $(options.controls.head).click
            (function (ev) { stop (ev); show (0, ev); });
        $(options.controls.tail).click
            (function (ev) { stop (ev); show (-1, ev); });
        $(options.controls.play).click (start);
        $(options.inline_selector).show ();
        show (0);
        return this;
      }
  }
) (jQuery);

/* __END__ GTW_Gallery.js */
