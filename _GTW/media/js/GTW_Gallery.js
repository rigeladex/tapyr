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
**    GTW_Gallery
**
** Purpose
**    jQuery plugin for a photo gallery
**
**
** Revision Dates
**     7-Oct-2010 (CT) Creation
**     8-Oct-2010 (CT) Creation continued
**    30-Nov-2010 (CT) Calls to `.button` added
**    30-Nov-2010 (CT) `scroll` added and used
**    ««revision-date»»···
**--
*/

( function($)
  {
    $.fn.GTW_Gallery = function (options)
      {
        var controls = $.extend
          ( { head        : "button.first"
            , next        : "button.next"
            , play        : "button.play"
            , prev        : "button.prev"
            , tail        : "button.last"
            }
          , options.controls || {}
          );
        var options  = $.extend
          ( { delay           : 3000
            , inline_selector : ".gallery .inline"
            , photo_selector  : ".photo img"
            , play_class      : "playing"
            , selected_class  : "selected"
            , url_transformer : function (name)
                { return name.replace (/\/th\//, "/im/"); }
            }
          , options || {}
          , { controls        : controls }
          );
        function scroll (thumb$)
          {
            var w1  = options.th_div$.width ();
            var w2  = options.th_box$.width ();
            var pos, left;
            if ((w1 < w2))
              {
                options.th_box$.css    ("margin-left", 0);
                pos  = thumb$.position ();
                if ((pos.left + thumb$.width ()) > w1)
                  {
                    left = Math.min (pos.left, w2 - w1);
                    options.th_box$.css ("margin-left", "-" + left + "px");
                  }
              }
          }
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
            $(options.thumbnails$ [options.current]).removeClass ("selected");
            index = options.current = index % len;
            thumb = options.thumbnails$ [index];
            url   = options.url_transformer (thumb.src);
            photo.attr
              ( { src   : url
                , title :
                    (alt ? alt + ":" : "Photo") + " " + (index+1) + "/" + len
                }
              );
            scroll ($(thumb));
            $(thumb).addClass ("selected");
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
              .click    (stop)
              .button
                ({ icons : { primary : "ui-icon-pause" }, text : false });
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
                  .removeClass (options.play_class)
                  .button
                    ({ icons : { primary : "ui-icon-play" }, text : false });
              }
          }
        this.addClass ("inline");
        options.current = 0;
        options.th_div$     = this;
        options.th_box$     = $(".box", this);
        options.thumbnails$ = $("img",  this);
        options.th_div$.css ("overflow", "hidden");
        options.thumbnails$
          .each
            ( function (n)
                { $(this).data ("GTW-gallery-index", n); }
            )
          .click
            ( function (ev)
                { stop (ev); show ($(this).data ("GTW-gallery-index"), ev); }
            );
        $(options.controls.next)
          .click
            (function (ev) { stop (ev); next (ev); })
          .button
            ({ icons : { primary : "ui-icon-seek-next" }, text : false });
        $(options.controls.prev)
          .click
            (function (ev) { stop (ev); prev (ev); })
          .button
            ({ icons : { primary : "ui-icon-seek-prev" }, text : false });
        $(options.controls.head)
          .click
            (function (ev) { stop (ev); show (0, ev); })
          .button
            ({ icons : { primary : "ui-icon-seek-start" }, text : false });
        $(options.controls.tail)
          .click
            (function (ev) { stop (ev); show (-1, ev); })
          .button
            ({ icons : { primary : "ui-icon-seek-end" }, text : false });
        $(options.controls.play)
          .click (start)
          .button
            ({ icons : { primary : "ui-icon-play" }, text : false });
        $(options.inline_selector).show ();
        show (0);
        return this;
      }
  }
) (jQuery);

/* __END__ GTW_Gallery.js */
