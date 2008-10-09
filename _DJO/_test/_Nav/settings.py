# -*- coding: iso-8859-15 -*-
# Django settings for scams project.

from   _DJO             import DJO
import _DJO.Navigation
from   _TFL             import sos
from   _TFL.Filename    import Filename

ROOT_PATH      = sos.path.dirname (__file__)

DEBUG          = False # or True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'djo_nav_test' # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Vienna"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#     http://www.iana.org/assignments/language-tags
LANGUAGE_CODE = 'de-AT-1901' ### de-AT-1996

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = sos.path.join (ROOT_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8000/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = "'thisisthesecretkeyandshouldnotbetoldanyonetokeepi"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'nav_test.urls'

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = \
    ( sos.path.join (ROOT_PATH, "templates")
    ,
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    "_DJO",
    ### add a few test models
    "_DJO._test._Nav.model_1",
    "_DJO._test._Nav.model_2"
)

DATE_FORMAT                      = "Y/m/d"
DATE_TIME_FORMAT                 = "Y/m/d H:i"
MONTH_DAY_FORMAT                 = "j. N"
TIME_FORMAT                      = "H:i"
YEAR_MONTH_FORMAT                = "Y/m"

DEFAULT_CHARSET                  = "iso-8859-15"
DEFAULT_CONTENT_TYPE             = "text/html"
FILE_CHARSET                     = "iso-8859-15"

SEND_BROKEN_LINK_EMAILS          = False
SESSION_COOKIE_AGE               = 86400 // 2
SESSION_COOKIE_SECURE            = False ### True --> set only for https
SESSION_EXPIRE_AT_BROWSER_CLOSE  = True

if not DJO.Navigation.Root.top :
    def handle_500 (request) :
        import sys
        from   django.views import debug
        exc_info = sys.exc_info ()
        return debug.technical_500_response(request, *exc_info)
    # end handle_500
    SRC_ROOT  = ROOT_PATH
    NAV       = DJO.Navigation.Root.from_nav_list_file \
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
                { 404  : "_DJO._test._Nav.handler_404.handler404"
                , 500  : handle_500
                }
            )
    ### bypass the standard django URL resolving based on regular expressions
    DJO.Navigation.Bypass_URL_Resolver ()

    def add_admin_setction () :
        from   _DJO._test._Nav.model_1.models import News
        DJO.Navigation.Root.top.add_entries \
            ( [ dict
                  ( sub_dir      = "Admin"
                  , title        = "Admin"
                  , models       = (News, )
                  , Type         = DJO.Navigation.Site_Admin
                  )
              ]
            )
    # end def add_admin_setction

    DJO.Navigation.Root.pre_first_request_hooks.append (add_admin_setction)
