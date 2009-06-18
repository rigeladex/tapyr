( function ($)
    {
      $.fn.DJO =
        { complete_nested_object_fields : function (options) {}
        , nested_many_2_many_setup      : function (options)
            {
              options = jQuery.extend
                ( {
                  }
                , options
                );
              return this.each
                ( function ()
                    {
                      $(this).addClass ("orange");
                    }
                );
            }
        };
      $.fn.nested_many_2_many_setup = $.fn.DJO.nested_many_2_many_setup;
    }
)(jQuery);
