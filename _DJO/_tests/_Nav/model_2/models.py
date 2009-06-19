# -*- coding: iso-8859-15 -*-

from   __future__                 import with_statement

from   _DJO                       import DJO
import _DJO.Models
import _DJO.Model_Field           as     MF
import _DJO.Model_Form
import _DJO.Permission

from   _TFL.Decorator             import Attributed
from   _TFL.Function              import Function

import datetime

from   django.db                  import models
from   django.contrib.auth.models import User
from   django.template            import defaultfilters

from   django.utils.translation   import gettext_lazy as _

try :
    from django.contrib.markup.templatetags.markup import markdown
except ImportError :
    pass

try :
    from django.contrib.markup.templatetags.markup import restructuredtext
except ImportError :
    pass

class Entry (DJO.Model) :

    _Formats = dict \
        ( R  = "reST"
        # M  = "Markdown"
        , H  ="Html"
        )
    _Kinds   = dict \
        ( C  = "Club"
        , J  = "Jugend"
        , S  = "Seitenblicke"
        )

    class Meta :
        ordering       = ["-date_pub", "title"]
    # end class Meta

    slug               = MF.Auto_Slug \
        ( "Url"
        , from_fields  = "date_pub"
        , field_fmt_kw = dict (date_pub = dict (output_format  = "%Y%m%d"))
        , help_text    =
            "Kurzbezeichnung des Newseintrags (wird für Url verwendet)"
        , max_length   = 24
        )
    kind               = MF.Choice \
        ( MF.Char, "Kategorie"
        , blank        = True
        , choices      = _Kinds.items ()
        , editable     = False
        , help_text    = "Kategorie des Newseintrags"
        , max_length   = 1
        )
    title              = MF.Char \
        ( "Titel"
        , help_text    =
            "Titel des Newseintrags"
        , max_length   = 80
        )
    text               = MF.Text \
        ( "Text"
        , help_text    =
            "Inhalt des Newseintrags"
        , widget_attrs = dict (cols = 80, rows = 40)
        )
    desc               = MF.Text \
        ( "Beschreibung"
        , blank        = True
        , help_text    =
            "Die Beschreibung wird als Hilfetext angezeigt"
        , widget_attrs = dict (cols = 80, rows = 2)
        )
    creator            = MF.Foreign_Key \
        ( User
        , blank        = True
        , editable     = False
        , null         = True
        , verbose_name = "Eingabe durch"
        )
    date_cre           = MF.Date_Time \
        ( "Eingabe-Datum"
        , blank        = True
        , editable     = False
        , default      = datetime.datetime.now
        , null         = True
        )
    date_pub           = MF.Date_Time \
        ( "Erscheinungs-Datum"
        , blank          = True
        , default        = datetime.datetime.now
        , help_text      =
            "Wenn nichts eingetragen ist, wird das Datum der Eingabe verwendet"
        , null           = True
        )
    date_exp           = MF.Date_Time \
        ( "Ablauf-Datum"
        , blank        = True
        , help_text    =
            "Nach dem Ablaufdatum wird der Newseintrag nicht mehr in den "
            "aktuellen News angezeigt (nur mehr im Archiv)"
        , null         = True
        )
    author             = MF.Char     \
        ( "Autor"
        , blank        = True
        , help_text    =
            "Autor des Newseintrags (wenn von der Person verschieden, "
            "die die Eingabe macht)"
        , max_length   = 80
        )
    format             = MF.Choice \
        ( MF.Char, "Text-Format"
        , choices      = _Formats.items ()
        , default      = "R"
        , help_text    =
            "Format, in dem der Text eingegeben wird."
        , max_length   = 1
        )

    class Entry_Form_Mixin (DJO.Creator_Form_Mixin, DJO.Kind_Name_Form_Mixin) :

        def clean (self) :
            result = self.__super.clean ()
            text   = result.get         ("text")
            format = result.get         ("format")
            if text and format :
                result ["text"] = Entry._cleaned_text (text, format)
            return result
        # end def clean

    # end class Entry_Form_Mixin

    def save (self) :
        if not self.date_cre :
            self.date_cre = datetime.datetime.now ().replace (microsecond = 0)
        if not self.date_pub :
            self.date_pub = self.date_cre
        if self.creator and not self.author :
            c = self.creator
            self.author = " ".join \
                (   n.capitalize ()
                for n in (c.first_name, c.last_name or c.username) if n
                )
        self.__super.save ()
    # end def save

    @property
    def contents (self) :
        result = self.text
        if self.format in ("M", "Markdown") :
            result = markdown (result)
        elif self.format in ("R", "reST") :
            result = restructuredtext (result)
        return result
    # end def contents

    @Function
    def _cleaned_html (text) :
        forbidden = "applet frame frameset head html iframe input object script"
        result    = defaultfilters.removetags (text, forbidden)
        if result != text :
            from django.forms.util import ValidationError
            raise ValidationError \
                ("`text` contains a forbidden tag (one of: `%s`)" % forbidden)
        return result
    # end def _cleaned_html

    @Function
    def _cleaned_markdown (text) :
        result = Entry._cleaned_html (text)
        try :
            markdown (result)
        except StandardError, exc :
            raise ValueError (exc)
        else :
            return result
    # end def _cleaned_markdown

    @Function
    def _cleaned_rest (text) :
        try :
            restructuredtext (text)
        except StandardError, exc :
            raise ValueError (exc)
        else :
            return text
    # end def _cleaned_rest

    @classmethod
    def _cleaned_text (cls, text, format) :
        return cls._cleaner [format] (text)
    # end def _cleaned_text

    _cleaner = dict \
        ( H                = _cleaned_html
        , Html             = _cleaned_html
        , M                = _cleaned_markdown
        , Markdown         = _cleaned_markdown
        , R                = _cleaned_rest
        , reST             = _cleaned_rest
        )

    def __unicode__(self):
        return self.title
    # end def __unicode__

    NAV_admin_args     = dict \
        ( list_display = \
            ("slug", "title", "desc", "date_pub", "date_exp", "author")
        , Form_Mixins  = (Entry_Form_Mixin, )
        , field_group_descriptions =
            ( DJO.Field_Group_Description
                ("title", "text", "desc", "author", "format")
            , DJO.Field_Group_Description
                ( "date_cre", "date_pub", "date_exp"
                , legend    = _("Publication dates")
                , template  = "field_group_horizontal.html"
                )
            )
#        , _permission  = DJO.In_Page_Group ()
        )

    NAV_manager_args   = dict \
        ( attr_map     = dict
            ( date         = "date_pub"
            , src_contents = "text"
            )
        , template     = "news.html"
        )

# end class Entry

### __END__ news/models
