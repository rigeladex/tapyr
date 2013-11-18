# -*- coding: utf-8 -*-
from django.template           import Context, RequestContext, loader
from django                    import http
from _DJO.Navigation           import Root

def handler404 (request, template_name='404.html') :
    t = loader.get_template (template_name)
    return http.HttpResponseNotFound \
        ( t.render
            ( RequestContext
                ( request
                , dict
                    ( request_path = request.path
                    , page         = Root.top
                    )
                )
            )
        )
# end def handler404
