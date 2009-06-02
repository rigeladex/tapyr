import _TFL.sos        as     sos
from   _DJO            import DJO
import _DJO.Navigation
from    django.conf    import settings

def handle_500 (request) :
    import sys
    from   django.views import debug
    exc_info = sys.exc_info ()
    return debug.technical_500_response(request, *exc_info)
# end handle_500

ROOT_PATH  = settings.ROOT_PATH
MEDIA_ROOT = settings.MEDIA_ROOT

SRC_ROOT   = ROOT_PATH
NAV        = DJO.Navigation.Root.from_nav_list_file \
        ( SRC_ROOT
        , src_root        = SRC_ROOT
        , copyright_start = 2008
        , encoding        = "iso-8859-15"
        , input_encoding  = "iso-8859-15"
        , hide_marginal   = True
        , language        = "de"
        , owner           = "DJO Test Page"
        , site_prefix     = "/"
        , site_url        = "http://localhost:8000"
        , template        = "static.html"
        , web_links       =
            [ dict
                ( href    = u"http://www.noe.gv.at/externeseiten/wasserstand/wiskiwebpublic/stat_1574033.htm?entryparakey=Q"
                , desc    = u"Wasserstand der Donau in Korneuburg"
                , title   = u"Donau Wasserstand"
                )
            ]
        , url_patterns    =
            ( DJO.Navigation.Static_Files_Pattern
                ( "^media/(?P<path>.*)$"
                , document_root = MEDIA_ROOT
                , show_indexes  = True
                )
            , DJO.Navigation.Static_Files_Pattern
                ( "^images/(?P<path>.*)$"
                , document_root = sos.path.join (MEDIA_ROOT, "..", "images")
                , show_indexes  = True
                )
            )
        , handlers =
            { 404  : "_DJO._tests._Nav.handler_404.handler404"
            , 500  : handle_500
            }
        )

def add_admin_setction () :
    from   _DJO._tests._Nav.model_1.models import News, News_Extender
    DJO.Navigation.Root.top.add_entries \
        ( [ dict
              ( sub_dir      = "Admin"
              , title        = "Admin"
              , models       = (News, News_Extender)
              , Type         = DJO.Navigation.Site_Admin
              )
          ]
        )
# end def add_admin_setction

add_admin_setction ()
