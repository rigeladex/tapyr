#! /swing/bin/python
# Copyright (C) 2003 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    bayesian
#
# Purpose
#    Calculate conditional probabilities using Rev. Thomas Bayes' formula
#
# Revision Dates
#     3-Aug-2003 (CT) Creation
#    ««revision-date»»···
#--

from _TFL import TFL

def bayesian (p_h, p_o_h, p_o_not_h) :
    """Calculate the probability of hypothesis `h` given the new observation
       `o`, where
       - `p_h` is the probability before the new observation was made,
       - `p_o_h` is the probability of the observation when the
         hypothesis `h` is true,
       - `p_o_not_h` is the probability of the observation when the
         hypothesis `h` is false.

       Consider a disease that appears in 1% of the population and a test for
       that disease is positive 80% (or 85%, or 90%) of the time when the
       disease is present and 10% (or 5%, or 1%) of the time when the disease
       is not present:

       >>> "%5.3f" % bayesian (0.01, 0.80, 0.10)
       '0.075'

       >>> "%5.3f" % bayesian (0.01, 0.85, 0.05)
       '0.147'

       >>> "%5.3f" % bayesian (0.01, 0.90, 0.01)
       '0.476'

       Because so many people don't have the disease, the false positives far
       exceed the small percentage of those tested who actually have the
       disease.

       >>> "%5.3f" % bayesian (0.50, 0.80, 0.10)
       '0.889'
       >>> "%5.3f" % bayesian (0.50, 0.85, 0.05)
       '0.944'
       >>> "%5.3f" % bayesian (0.50, 0.90, 0.01)
       '0.989'
    """
    p_not_h         = 1.0 - p_h
    p_h_times_p_o_h = p_h * p_o_h
    return p_h_times_p_o_h / (p_h_times_p_o_h + (p_not_h * p_o_not_h))
# end def bayesian

def _command_spec (arg_array = None) :
    from Command_Line import Command_Line
    return Command_Line \
        ( arg_spec    =
            ( "p_h:F"
                "?probability of hypothesis"
                " before the new observation was made"
            , "p_o_h:F"
                "?probability of the observation"
                " when the hypothesis `h` is true"
            , "p_o_not_h:F"
                "?probability of the observation"
                " when the hypothesis `h` is false"
            )
        , max_args    = 3
        , min_args    = 3
        , arg_array   = arg_array
        )
# end def _command_spec

def _main (cmd) :
    print "%5.3f" % bayesian (cmd.p_h, cmd.p_o_h, cmd.p_o_not_h)
# end def _main

### unit-test code ############################################################
if __debug__ :
    import U_Test

    def _doc_test () :
        import bayesian
        return U_Test.run_module_doc_tests (bayesian)
    # end def _doc_test

    def _test () :
        _doc_test  ()
    # end def _test
# end if __debug__
### end unit-test code ########################################################

if __name__ == "__main__" :
    _main (_command_spec ())
else :
    TFL._Export ("*")
### __END__ bayesian
