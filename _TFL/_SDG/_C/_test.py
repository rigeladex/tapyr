from   _TFL._SDG._C.import_C import C
C.Comment.out_level = 5
m = C.Module  (name = "test", header_comment = "Simple test module", author = "FooBar")
c = C.Comment ("This is a comment", stars = 2)
s = C.Struct ( "TDFT_Sign_Mask"
             , "unsigned long bit_mask    = 42 // mask for value"
             , "unsigned long extend_mask // mask for sign extension"
             , "char qux = 040"
             )
t = C.Struct ( "TDFT_Sign_Mask2"
             , "unsigned long bit_mask    = 42 // mask for value"
             , "unsigned long extend_mask // mask for sign extension "
                  "with an extra long comment spanning multiple lines "
                  "without containing any sensible information -- "
                  "remember the guy who inserted lots of these into the "
                  "code without paying attention?"
             , C.Struct
                 ( "nested"
                 , "int a // first nested field"
                 , "char b // second nested field"
                 )
             )
a1 = C.Array ("int", "ar", 2, init = (0, 1), static = True)
a2 = C.Array ( "TDFT_Sign_Mask", "fubars", 3
             , init = [ dict (bit_mask = "57 % 2",  extend_mask = 137, qux = 040)
                      , dict (bit_mask = "142 % 4", extend_mask = -1, qux = 060)
                      , dict (bit_mask = "95",      extend_mask = 0, qux = 077)
                      ]
             )
#c.write_to_c_stream (); s.write_to_c_stream  ();
#a1.write_to_c_stream ();
a2.write_to_c_stream ()
m.add ( C.Function ( "int", "bar", "void"
                   , c, s, t, a1, a2
                   )
      )
#m.write_to_c_stream ()

