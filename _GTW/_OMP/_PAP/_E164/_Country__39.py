# -*- coding: utf-8 -*-
# Copyright (C) 2015 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.PAP.E164.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.PAP.E164._Country__39
#
# Purpose
#    Provide phone number mapping for Italy
#
# Revision Dates
#    28-Jul-2015 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                         import GTW
from   _TFL                         import TFL

from   _TFL.defaultdict             import defaultdict

import _GTW._OMP._PAP._E164.Country

class Country__39 (GTW.OMP.PAP.E164.Country_M) :
    """Provide phone number mapping for Italy."""

    generated_from     = \
        """https://en.wikipedia.org/wiki/Telephone_numbers_in_Italy
           https://en.wikipedia.org/wiki/List_of_dialling_codes_in_Italy
        """
    generation_date    = "28-Jul-2015 09:55"

    formatted_sn       = lambda x : x

    ndc_prefix         = ""

    ndc_info_map       = \
        {   "010" : "City of Genoa and surroundings"
        ,   "011" : "City of Turin and surroundings"
        ,  "0122" : "Province of Turin, Susa Valley area"
        ,  "0123" : "Province of Turin, Lanzo Valleys area"
        ,  "0124" : "Province of Turin, Rivarolo Canavese and Orco Valley areas"
        ,  "0125" : "Province of Turin, Ivrea area"
        ,  "0131" : "Province of Alessandria"
        ,  "0141" : "Province of Asti"
        ,   "015" : "Province of Biella"
        ,  "0161" : "Province of Vercelli"
        ,  "0163" : "Province of Vercelli – Valsesia"
        ,  "0165" : "Aosta Valley, regional capital and Courmayeur"
        ,  "0166" : "Aosta Valley - Cervinia"
        ,  "0171" : "Province of Cuneo"
        ,  "0183" : "Province of Imperia"
        ,  "0185" : "Province of Genoa, except the provincial/regional capital"
        ,  "0187" : "Province of La Spezia and Cinque Terre"
        ,    "02" : "City of Milan and surroundings, parts of the Province of Varese and Province of Como"
        ,   "030" : "City of Brescia, Franciacorta, valle Trompia and southern province"
        ,   "031" : "Province of Como"
        ,  "0321" : "Province of Novara, including provincial capital"
        ,  "0322" : "Province of Novara - Borgomanero area"
        ,  "0324" : "Province of Verbano-Cusio-Ossola"
        ,  "0331" : "Province of Varese – Busto Arsizio area"
        ,  "0332" : "Province of Varese"
        ,  "0341" : "Province of Lecco"
        ,  "0342" : "Province of Sondrio, including provincial capital"
        ,  "0343" : "Province of Sondrio – area of Chiavenna"
        ,  "0344" : "Province of Como – area of Menaggio"
        ,  "0346" : "Province of Bergamo"
        ,   "035" : "Province of Bergamo, including provincial capital"
        ,  "0362" : "Province of Cremona"
        ,  "0362" : "Province of Monza - area of Seregno"
        ,  "0363" : "Provinces of Bergamo and Cremona"
        ,  "0364" : "Province of Brescia – aresa of Valle Camonica and Breno"
        ,  "0365" : "Province of Brescia – Lake Garda and Valle Sabbia, area of Salò"
        ,  "0371" : "Province of Lodi and a few villages in Province of Milan"
        ,  "0372" : "Province of Cremona including provincial capital"
        ,  "0373" : "Province of Cremona - area of Crema"
        ,  "0375" : "Province of Cremona and part of Province of Mantua"
        ,  "0376" : "Province of Mantua"
        ,  "0382" : "Province of Pavia"
        ,   "039" : "Province of Monza, including provincial capital"
        ,   "040" : "Province of Trieste, including provincial/regional capital"
        ,   "041" : "City of Venice, including landside Mestre area"
        ,  "0421" : "Province of Venice - area of San Donà di Piave"
        ,  "0422" : "Province of Treviso"
        ,  "0423" : "Province of Treviso - area of Montebelluna"
        ,  "0424" : "Province of Vicenza - area of Bassano del Grappa"
        ,  "0425" : "Province of Rovigo - area of Rovigo"
        ,  "0426" : "Province of Rovigo - area of Adria"
        ,  "0432" : "Province of Udine"
        ,  "0444" : "Province of Vicenza, including provincial capital"
        ,  "0445" : "Province of Vicenza - area of Schio"
        ,   "045" : "Province of Verona"
        ,  "0461" : "Province of Trento"
        ,  "0471" : "Province of Bolzano"
        ,  "0481" : "Province of Gorizia"
        ,   "049" : "Province of Padova"
        ,   "050" : "Province of Pisa"
        ,   "051" : "Province of Bologna"
        ,  "0522" : "Province of Reggio Emilia"
        ,  "0521" : "Province of Parma"
        ,  "0523" : "Province of Piacenza"
        ,  "0532" : "Province of Ferrara"
        ,  "0535" : "Mirandola and surroundings"
        ,  "0536" : "Industrial district of Sassuolo, Formigine, Fiorano Modenese, Maranello and Prigniano sulla Secchia and for the comunità montana (lit. mountain district) of Frignano"
        ,  "0541" : "Province of Rimini"
        ,  "0543" : "Province of Forlì-Cesena"
        ,  "0544" : "Province of Ravenna"
        ,  "0545" : "Province of Ravenna"
        ,  "0549" : "Republic of San Marino (only Telecom Italia San Marino landlines)"
        ,   "055" : "City of Florence and surroundings"
        ,  "0565" : "Province of Livorno"
        ,  "0574" : "Province of Prato"
        ,  "0575" : "Province of Arezzo"
        ,  "0577" : "Province of Siena"
        ,  "0583" : "Province of Lucca"
        ,  "0585" : "Province of Massa and Carrara"
        ,  "0586" : "Province of Livorno"
        ,   "059" : "Province of Modena"
        ,    "06" : "City of Rome and surroundings, the Vatican City and parts of Province of Rome"
        ,   "070" : "Province of Cagliari"
        ,   "071" : "Province of Ancona"
        ,  "0721" : "Province of Pesaro and Urbino"
        ,  "0731" : "Province of Ancona - area of Jesi"
        ,  "0732" : "Province of Ancona - area of Fabriano"
        ,  "0733" : "Province of Macerata, including provincial capital"
        ,  "0734" : "Province of Fermo"
        ,  "0735" : "Province of Ascoli Piceno - area of San Benedetto del Tronto"
        ,  "0736" : "Province of Ascoli Piceno"
        ,  "0737" : "Province of Macerata - area of Camerino"
        ,   "075" : "Province of Perugia"
        ,  "0765" : "Province of Rieti - area of Poggio Mirteto"
        ,  "0771" : "Province of Latina - areas of Formia and Fondi"
        ,  "0773" : "Province of Latina"
        ,  "0774" : "Province of Rome - area of Tivoli"
        ,  "0775" : "Province of Frosinone"
        ,  "0776" : "Province of Frosinone - area of Cassino"
        ,  "0783" : "Province of Oristano"
        ,  "0789" : "Province of Sassari - areas of Olbia and Costa Smeralda"
        ,   "079" : "Province of Sassari, including provincial capital and Alghero"
        ,   "080" : "City of Bari and surroundings"
        ,   "081" : "City of Naples and surroundings"
        ,  "0823" : "Province of Caserta"
        ,  "0824" : "Province of Benevento"
        ,  "0825" : "Province of Avellino"
        ,  "0832" : "Province of Lecce"
        ,   "085" : "Province of Pescara"
        ,  "0861" : "Province of Teramo"
        ,  "0862" : "Province of L'Aquila"
        ,  "0865" : "Province of Isernia"
        ,  "0874" : "Province of Campobasso"
        ,  "0881" : "Province of Foggia, including provincial capital"
        ,  "0882" : "Province of Foggia - areas of Apricena, San Giovanni Rotondo and Tremiti isles"
        ,  "0883" : "Province of Barletta-Andria-Trani"
        ,  "0884" : "Province of Foggia - areas of Rodi Garganico, Vieste and Manfredonia"
        ,   "089" : "Province of Salerno"
        ,   "090" : "Province of Messina"
        ,   "091" : "City of Palermo and surroundings"
        ,  "0921" : "Province of Palermo"
        ,  "0931" : "Province of Siracusa"
        ,  "0932" : "Province of Ragusa"
        ,  "0933" : "Province of Caltanissetta"
        ,  "0924" : "Province of Trapani"
        ,  "0922" : "Province of Agrigento"
        ,  "0925" : "Province of Agrigento"
        ,  "0934" : "Provinces of Caltanissetta and Enna"
        ,  "0941" : "Novara di Sicilia"
        ,  "0942" : "Province of Messina - area of Taormina"
        ,   "095" : "City of Catania and surroundings"
        ,  "0961" : "Province of Catanzaro"
        ,  "0962" : "Province of Crotone"
        ,  "0963" : "Province of Vibo Valentia"
        , "07965" : "Province of Reggio Calabria"
        ,  "0974" : "Province of Salerno"
        ,  "0975" : "Province of Potenza"
        ,   "099" : "Province of Taranto"
        ,  "0984" : "City of Cosenza - area of Cosenza"
        ,   "313" : "Mobile (Rete Ferroviaria Italiana)"
        ,   "320" : "Mobile (Wind Italy)"
        ,   "321" : "Mobile (Wind Italy)"
        ,   "322" : "Mobile (Wind Italy)"
        ,   "323" : "Mobile (Wind Italy)"
        ,   "324" : "Mobile (Wind Italy)"
        ,   "325" : "Mobile (Wind Italy)"
        ,   "326" : "Mobile (Wind Italy)"
        ,   "327" : "Mobile (Wind Italy)"
        ,   "328" : "Mobile (Wind Italy)"
        ,   "329" : "Mobile (Wind Italy)"
        ,   "330" : "Mobile (TIM)"
        ,   "331" : "Mobile (TIM)"
        ,   "332" : "Mobile (TIM)"
        ,   "333" : "Mobile (TIM)"
        ,   "334" : "Mobile (TIM)"
        ,   "335" : "Mobile (TIM)"
        ,   "336" : "Mobile (TIM)"
        ,   "337" : "Mobile (TIM)"
        ,   "338" : "Mobile (TIM)"
        ,   "339" : "Mobile (TIM)"
        ,   "340" : "Mobile (Vodafone Italy)"
        ,   "341" : "Mobile (Vodafone Italy)"
        ,   "342" : "Mobile (Vodafone Italy)"
        ,   "343" : "Mobile (Vodafone Italy)"
        ,   "344" : "Mobile (Vodafone Italy)"
        ,   "345" : "Mobile (Vodafone Italy)"
        ,   "346" : "Mobile (Vodafone Italy)"
        ,   "347" : "Mobile (Vodafone Italy)"
        ,   "348" : "Mobile (Vodafone Italy)"
        ,   "349" : "Mobile (Vodafone Italy)"
        ,   "350" : "Mobile"
        ,   "351" : "Mobile"
        ,   "352" : "Mobile"
        ,   "353" : "Mobile"
        ,   "354" : "Mobile"
        ,   "355" : "Mobile"
        ,   "356" : "Mobile"
        ,   "357" : "Mobile"
        ,   "358" : "Mobile"
        ,   "359" : "Mobile"
        ,   "360" : "Mobile (TIM)"
        ,   "361" : "Mobile (TIM)"
        ,   "362" : "Mobile (TIM)"
        ,   "363" : "Mobile (TIM)"
        ,   "364" : "Mobile (TIM)"
        ,   "365" : "Mobile (TIM)"
        ,   "366" : "Mobile (TIM)"
        ,   "367" : "Mobile (TIM)"
        ,   "368" : "Mobile (TIM)"
        ,   "369" : "Mobile (TIM)"
        ,   "370" : "Mobile"
        ,   "371" : "Mobile"
        ,   "372" : "Mobile"
        ,   "373" : "Mobile"
        ,   "374" : "Mobile"
        ,   "375" : "Mobile"
        ,   "376" : "Mobile"
        ,   "377" : "Mobile"
        ,   "378" : "Mobile"
        ,   "379" : "Mobile"
        ,   "380" : "Mobile (Wind Italy)"
        ,   "381" : "Mobile (Wind Italy)"
        ,   "382" : "Mobile (Wind Italy)"
        ,   "383" : "Mobile (Wind Italy)"
        ,   "384" : "Mobile (Wind Italy)"
        ,   "385" : "Mobile (Wind Italy)"
        ,   "386" : "Mobile (Wind Italy)"
        ,   "387" : "Mobile (Wind Italy)"
        ,   "388" : "Mobile (Wind Italy)"
        ,   "389" : "Mobile (Wind Italy)"
        ,   "390" : "Mobile (H3G Italy)"
        ,   "391" : "Mobile (H3G Italy)"
        ,   "392" : "Mobile (H3G Italy)"
        ,   "393" : "Mobile (H3G Italy)"
        ,   "394" : "Mobile (H3G Italy)"
        ,   "395" : "Mobile (H3G Italy)"
        ,   "396" : "Mobile (H3G Italy)"
        ,   "397" : "Mobile (H3G Italy)"
        ,   "398" : "Mobile (H3G Italy)"
        ,   "399" : "Mobile (H3G Italy)"
        }

    ndc_min_length     = 2

    ndc_types_normal   = {"geographic", "mobile"}

    ndc_usage_map = \
        {   "010" : "geographic"
        ,   "011" : "geographic"
        ,  "0122" : "geographic"
        ,  "0123" : "geographic"
        ,  "0124" : "geographic"
        ,  "0125" : "geographic"
        ,  "0131" : "geographic"
        ,  "0141" : "geographic"
        ,   "015" : "geographic"
        ,  "0161" : "geographic"
        ,  "0163" : "geographic"
        ,  "0165" : "geographic"
        ,  "0166" : "geographic"
        ,  "0171" : "geographic"
        ,  "0183" : "geographic"
        ,  "0185" : "geographic"
        ,  "0187" : "geographic"
        ,    "02" : "geographic"
        ,   "030" : "geographic"
        ,   "031" : "geographic"
        ,  "0321" : "geographic"
        ,  "0322" : "geographic"
        ,  "0324" : "geographic"
        ,  "0331" : "geographic"
        ,  "0332" : "geographic"
        ,  "0341" : "geographic"
        ,  "0342" : "geographic"
        ,  "0343" : "geographic"
        ,  "0344" : "geographic"
        ,  "0346" : "geographic"
        ,   "035" : "geographic"
        ,  "0362" : "geographic"
        ,  "0362" : "geographic"
        ,  "0363" : "geographic"
        ,  "0364" : "geographic"
        ,  "0365" : "geographic"
        ,  "0371" : "geographic"
        ,  "0372" : "geographic"
        ,  "0373" : "geographic"
        ,  "0375" : "geographic"
        ,  "0376" : "geographic"
        ,  "0382" : "geographic"
        ,   "039" : "geographic"
        ,   "040" : "geographic"
        ,   "041" : "geographic"
        ,  "0421" : "geographic"
        ,  "0422" : "geographic"
        ,  "0423" : "geographic"
        ,  "0424" : "geographic"
        ,  "0425" : "geographic"
        ,  "0426" : "geographic"
        ,  "0432" : "geographic"
        ,  "0444" : "geographic"
        ,  "0445" : "geographic"
        ,   "045" : "geographic"
        ,  "0461" : "geographic"
        ,  "0471" : "geographic"
        ,  "0481" : "geographic"
        ,   "049" : "geographic"
        ,   "050" : "geographic"
        ,   "051" : "geographic"
        ,  "0522" : "geographic"
        ,  "0521" : "geographic"
        ,  "0523" : "geographic"
        ,  "0532" : "geographic"
        ,  "0535" : "geographic"
        ,  "0536" : "geographic"
        ,  "0541" : "geographic"
        ,  "0543" : "geographic"
        ,  "0544" : "geographic"
        ,  "0545" : "geographic"
        ,  "0549" : "geographic"
        ,   "055" : "geographic"
        ,  "0565" : "geographic"
        ,  "0574" : "geographic"
        ,  "0575" : "geographic"
        ,  "0577" : "geographic"
        ,  "0583" : "geographic"
        ,  "0585" : "geographic"
        ,  "0586" : "geographic"
        ,   "059" : "geographic"
        ,    "06" : "geographic"
        ,   "070" : "geographic"
        ,   "071" : "geographic"
        ,  "0721" : "geographic"
        ,  "0731" : "geographic"
        ,  "0732" : "geographic"
        ,  "0733" : "geographic"
        ,  "0734" : "geographic"
        ,  "0735" : "geographic"
        ,  "0736" : "geographic"
        ,  "0737" : "geographic"
        ,   "075" : "geographic"
        ,  "0765" : "geographic"
        ,  "0771" : "geographic"
        ,  "0773" : "geographic"
        ,  "0774" : "geographic"
        ,  "0775" : "geographic"
        ,  "0776" : "geographic"
        ,  "0783" : "geographic"
        ,  "0789" : "geographic"
        ,   "079" : "geographic"
        ,   "080" : "geographic"
        ,   "081" : "geographic"
        ,  "0823" : "geographic"
        ,  "0824" : "geographic"
        ,  "0825" : "geographic"
        ,  "0832" : "geographic"
        ,   "085" : "geographic"
        ,  "0861" : "geographic"
        ,  "0862" : "geographic"
        ,  "0865" : "geographic"
        ,  "0874" : "geographic"
        ,  "0881" : "geographic"
        ,  "0882" : "geographic"
        ,  "0883" : "geographic"
        ,  "0884" : "geographic"
        ,   "089" : "geographic"
        ,   "090" : "geographic"
        ,   "091" : "geographic"
        ,  "0921" : "geographic"
        ,  "0931" : "geographic"
        ,  "0932" : "geographic"
        ,  "0933" : "geographic"
        ,  "0924" : "geographic"
        ,  "0922" : "geographic"
        ,  "0925" : "geographic"
        ,  "0934" : "geographic"
        ,  "0941" : "geographic"
        ,  "0942" : "geographic"
        ,   "095" : "geographic"
        ,  "0961" : "geographic"
        ,  "0962" : "geographic"
        ,  "0963" : "geographic"
        , "07965" : "geographic"
        ,  "0974" : "geographic"
        ,  "0975" : "geographic"
        ,   "099" : "geographic"
        ,  "0984" : "geographic"
        ,   "313" : "mobile"
        ,   "320" : "mobile"
        ,   "321" : "mobile"
        ,   "322" : "mobile"
        ,   "323" : "mobile"
        ,   "324" : "mobile"
        ,   "325" : "mobile"
        ,   "326" : "mobile"
        ,   "327" : "mobile"
        ,   "328" : "mobile"
        ,   "329" : "mobile"
        ,   "330" : "mobile"
        ,   "331" : "mobile"
        ,   "332" : "mobile"
        ,   "333" : "mobile"
        ,   "334" : "mobile"
        ,   "335" : "mobile"
        ,   "336" : "mobile"
        ,   "337" : "mobile"
        ,   "338" : "mobile"
        ,   "339" : "mobile"
        ,   "340" : "mobile"
        ,   "341" : "mobile"
        ,   "342" : "mobile"
        ,   "343" : "mobile"
        ,   "344" : "mobile"
        ,   "345" : "mobile"
        ,   "346" : "mobile"
        ,   "347" : "mobile"
        ,   "348" : "mobile"
        ,   "349" : "mobile"
        ,   "350" : "mobile"
        ,   "351" : "mobile"
        ,   "352" : "mobile"
        ,   "353" : "mobile"
        ,   "354" : "mobile"
        ,   "355" : "mobile"
        ,   "356" : "mobile"
        ,   "357" : "mobile"
        ,   "358" : "mobile"
        ,   "359" : "mobile"
        ,   "360" : "mobile"
        ,   "361" : "mobile"
        ,   "362" : "mobile"
        ,   "363" : "mobile"
        ,   "364" : "mobile"
        ,   "365" : "mobile"
        ,   "366" : "mobile"
        ,   "367" : "mobile"
        ,   "368" : "mobile"
        ,   "369" : "mobile"
        ,   "370" : "mobile"
        ,   "371" : "mobile"
        ,   "372" : "mobile"
        ,   "373" : "mobile"
        ,   "374" : "mobile"
        ,   "375" : "mobile"
        ,   "376" : "mobile"
        ,   "377" : "mobile"
        ,   "378" : "mobile"
        ,   "379" : "mobile"
        ,   "380" : "mobile"
        ,   "381" : "mobile"
        ,   "382" : "mobile"
        ,   "383" : "mobile"
        ,   "384" : "mobile"
        ,   "385" : "mobile"
        ,   "386" : "mobile"
        ,   "387" : "mobile"
        ,   "388" : "mobile"
        ,   "389" : "mobile"
        ,   "390" : "mobile"
        ,   "391" : "mobile"
        ,   "392" : "mobile"
        ,   "393" : "mobile"
        ,   "394" : "mobile"
        ,   "395" : "mobile"
        ,   "396" : "mobile"
        ,   "397" : "mobile"
        ,   "398" : "mobile"
        ,   "399" : "mobile"
        }

    def sn_max_length (self, ndc) :
        return 11 - len (ndc)
    # end def sn_max_length

    def sn_min_length (self, ndc) :
        return  9 - len (ndc)
    # end def sn_min_length

Country = Country__39 # end class

### __END__ GTW.OMP.PAP.E164._Country__39
