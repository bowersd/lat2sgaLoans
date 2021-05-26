import re

process_list = [
        re.compile('p'),
        re.compile('f'),
        re.compile('[mn][ptcfs]'), #weaken this, bc less reliable. how many early forms violate? relevant for evaluating start date
        re.compile('x|([cg]s)'), #weaken this, bc less reliable
        re.compile('[aeiouy](:)?(p|t|k|b|d|g|s(?!ptk)|m)'),
        re.compile('^(([^aeiouy]*[aeiouy])|i[aeiou]).+:'), #fully comorbid with syncope...manage i=j...manage digraphs/diphthongs...manage qu
        re.compile('^((([^aeiouy]*[eo][^aeiouy]?[iuy])|([^aeiouy]*[iuy][^aeiouy]*[ao]))|(([^aeiouy]*[eo][^aeiouy]$)|[^aeiouy]*[iu][^aeiouy]*$))'), #monosyllables. mostly comorbid with syncope...manage i=j
        re.compile('[^:][dg][^aeiouy]'),
        re.compile('[aeiouy].*[aeiouy]'),#...manage digraphs/diphthongs...manage qu
        ]

q = [393, 153, 269, 73, 1164, 574, 208, 74, 1302] #p, f, NC, Ks, lenition, shortening, harmony, lengthening, syncope (disyllables and greater (y's excluded)), many words not parsed
q = [x/1978 for x in q]
data = [
        [0,1], #pk
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1], #fs enter before lenition -> enter between 400 and 425
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,1],
        [0,2], #undergo lenition in 450 -> enter between 400 and 450
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2], #undergoes affection
        [0,2], #undergoes affection
        [0,2], #undergoes affection
        [0,2],
        [1,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [1,2],
        [1,2],
        [1,2],
        [1,2],
        [1,2],
        [1,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [0,2],
        [2,3], #undergo harmony in INITIAL SYLLABLE-> enter between 400 and 475
        [2,3],
        [2,3],
        [2,3],
        [2,3], 
        [0,3],
        [2,3], #if we think we know the medial syll harmonized, then the end point is pre-harmony (shortening=60?)
        [0,3],
        [0,3],
        [2,3], #why post lenition??
        [2,3],
        [2,6],#post-lenition
        [2,5],#post-lenition pre lengthening
        [2,5],
        [2,7],#w/ VL-syncope of stressed (but lab_C) i: post-lenition. else: post-harmony but palatalization problems
        [2,4],
        [2,7],
        [2,5],
        [2,7],
        [2,7],
        [2,4],
        [2,7],
        [2,6],
        [2,7],
        [2,5],
        [2,5], #shortening might be pre-irish
        [2,7],
        [2,7],
        [2,7],
        [2,7],
        [2,7],
        [2,4], #shortening due to writing??
        [2,7],
        [2,4], #why post lenition??
        [2,7],
        [2,7], #thought to be quite late (why??)
        [2,4],
        [3,7], #post harmony loans
        [3,4],
        [3,7],
        [3,6],
        [3,7],
        [3,4],
        [3,7],
        [0,6], #{listed as leniting, but needs discussion or may be anytime loans
        [0,7],
        [0,7],
        [0,7],#palatalization
        [0,6], #f: can't be pre-lenition and become f by mere phonology 
        [0,3],#certainly pre-harmony}
        [0,7],#{no datable phonology but listed as leniting-> enter between 400 and 550
        [0,6],#(odd, nt-/>nd, but syncopates). is degemination sufficient for lenition? post-lenition would presumably also degeminate. Macneill
        [0,7],
        [0,7],
        [0,6],
        [0,7],
        [0,7], #well, we do get u-coloring, which indicates it was around sometime when affection was happening
        [0,7], 
        [0,7], #}
        [0,6], #{affection in non-initial syllable  (and not listed under lenition) -> could be any time
        [2,5], #post-lenition pre lengthening
        [0,5], #listed as post-lenition, but I only see evidence for pre-lengthening
        [2,6], #post-lenition
        [2,7],
        [2,6],
        [2,6],
        [0,7],
        [2,4], #if second syll affection is reliable, then early shortening (=60?). else: pre-apocope
        [2,4],#if second syll affection is reliable, then early shortening (=60?). else: pre-apocope
        [0,3],#if second syll affection is reliable, then early shortening (=60?). else: pre-affection
        [0,6],
        [2,6],
        [2,4],
        [0,7],#}
        [4,7], #listed as post-lenition, but should be post apocope
        [0,7],
        [0,4], 
        [0,4], 
        [0,7], #strongly considering making this undergo affection across [rt] (150->75)
        [0,7],
        [0,7],
        [1,4],
        [1,7], #a->o??
        [4,7], #{listed as post-lengthening, but could be post-apocope
        [4,7],
        [4,7],
        [4,7],
        [4,6],#}
        [6,7], #{post-syncope loans. auxilius in particular has some flags on it
        [6,7],
        [6,7],
        [6,7],
        [6,7],
        [6,7],
        [6,7],#}
        ]

forms =[
        "apostolus",       
        "pa:scha",         
        "pallium",         
        "panna",           
        "patricius",       
        "pellicia",        
        "pi:pio-",         
        "piper",           
        "pict-",           
        "planta",          
        "plecta",          
        "plu:ma",          
        "presbyter",       
        "pugnus",          
        "pulta",           
        "purpura",         
        "purpureus",       
        "puteus",          
        "fictus",          
        "floccus",         
        "fre:num",         
        "faba",            
        "fu:stis",         
        "fe:ria",          
        "fenestra",        
        "fi:bula",         
        "flecto",          
        "flagellum",       
        "furnus",          
        "crotalum",        
        "abba:tem",        
        "dominicus",       
        "gradus",          
        "creterra",        
        "ado:ra:re",       
        "habe:na",         
        "baculum",         
        "baptisma",        
        "brassica",        
        "brittones",       
        "dia:conus",       
        "dicta:re",        
        "dominicus",       
        "vesperti:na",     
        "vi:num",          
        "genea:logia",     
        "i:do:lum",        
        "calicem",         
        "cancella",        
        "castellum",       
        "camellus",        
        "cathedra",        
        "cervi:cal",       
        "cippus",          
        "cista",           
        "cle:ricus",       
        "christiAnus",     
        "crocus",          
        "crotalia",        
        "crucem",          
        "exhibernum",      
        "figu:ra",         
        "februa:rius",     
        "crux",            
        "culcita",         
        "cucullus",        
        "quadra:ge:sima",  
        "la:ikus",         
        "labo:rem",        
        "leo:",            
        "levia:than",      
        "li:tus",          
        "librum",          
        "lo:ri:ca",        
        "macula",          
        "monachus",        
        "medicus",         
        "mendi:cus",       
        "mi:ra:bilis",     
        "modius",          
        "mone:ta",         
        "morta:litas",     
        "oleum",           
        "o:ra:tio:",       
        "ocreae",          
        "axilla",          
        "parabola",        
        "paroecia",        
        "pecca:tum",       
        "praedica:re",     
        "proba:re",        
        "pugilla:ria",     
        "re:gula",         
        "ro:ma",           
        "rubrum",          
        "sagitta",         
        "sacellus",        
        "saturni",         
        "sexta:rius",      
        "secundi:nus",     
        "septima:na",      
        "si:tula",         
        "signum",          
        "synodus",         
        "stra:tu:ra",      
        "stuppa",          
        "tabella",         
        "tra:cta:re",      
        "tribu:nus",       
        "tridua:na",       
        "tunica",          
        "ungere",          
        "va:gi:na",        
        "vi:cus",          
        "vitulus",         
        "i:talia",         
        "innocuus",        
        "philosophus",     
        "philosophia",     
        "scri:pulus",      
        "cingula",         
        "coqui:na",        
        "cultrum",         
        "moniste:rium",    
        "scriptu:ra",      
        "tri:bula:tio:",   
        "apostolus",       
        "occa:sio",        
        "o:ra:culum",      
        "episcopus",       
        "ecle:sia",        
        "episcopus",       
        "fata:le",         
        "graeca",          
        "infernum",        
        "latro:nem",       
        "macula",          
        "meretri:cem",     
        "nota",            
        "nota:rius",       
        "na:ta:licia",     
        "patricius",       
        "pa:cem",          
        "rosa",            
        "sacerdo:s",       
        "psallendum",      
        "seca:le",         
        "sco:pa",          
        "scriptu:ra",      
        "stra:ta",         
        "thesis",          
        "cande:la",        
        "benedictio:",     
        "ido:neus",        
        "quaestio:",       
        "crepusculum",     
        "litania",         
        "mensu:ra",        
        "historia",        
        "ante tertiam",    
        "gallus",          
        "confessio:",      
        "numerus",         
        "offerendum",      
        "moli:na",         
        "organum",         
        "intellectus",     
        "angelus",         
        "longa",           
        "de:na:rius",      
        "mu:rus",          
        "virtus",          
        "arma",            
        "barica",          
        "ie:iu:nium",      
        "elee:mosina",      
        "ostia:rius",      
        "basilica",        
        "ca:seus",         
        "capitulum",       
        "camisia",         
        "culi:na",         
        "lati:na",         
        "ma:tuti:na",      
        "coctu:ra",        
        "martyrium",       
        "memoria",         
        "paradi:sus",      
        "uncia",           
        "antita:tem",      
        "cle:rus",         
        "coro:na",         
        "psalte:rium",     
        "cortis",          
        "maledictio:",     
        "ho:ra",           
        "perso:na",        
        "prandium",        
        "ima:go:",         
        "alta:re",         
        "o:ra:tio:",       
        "tri:nita:tem",    
        "candela:rius",    
        "auxilius",        
        "consul",          
        "tympanum",        
        "carbunculus",     
        "purgato:rium",    
        "epistula",        
        "firma:mentum",    
        ]

#           pk end      lenition    harmony     apocope                     lengthening     syncope   (sub-divide to pre Wb/Ml/Sg)
#0          1           2           3           4                           5               6         7
#   pk
#   fs          fs
#   lenition    lenition
#   harmony     harmony     harmony
#   shorten     shorten     shorten     shorten     shorten non-root final
#   syncope     syncope     syncope     syncope     syncope                     syncope
#this is more accurate than the lists above
data2 = {
        ("apostolus",       "axal"):[0,1,0,0,0,0,0,0], #pk
        ("pa:scha",         "ca:sc"):[0,1,0,0,0,0,0,0],
        ("pallium",         "caille"):[0,1,0,0,0,0,0,0],
        ("panna",           "cann"):[0,1,0,0,0,0,0,0],
        ("patricius",       "cothrige"):[0,1,0,0,0,0,0,0], ##problem derivation
        ("pellicia",        "cuilche"):[0,1,0,0,0,0,0,0],
        ("pi:pio-",         "ci:chanach"):[0,1,0,0,0,0,0,0], ##problem derivation
        ("piper",           "scibar"):[0,1,0,0,0,0,0,0], ##problem derivation
        ("pict-",           "cicht"):[0,1,0,0,0,0,0,0],
        ("planta",          "cland"):[0,1,0,0,0,0,0,0],
        ("plecta",          "clecht"):[0,1,0,0,0,0,0,0],
        ("plu:ma",          "clu:m"):[0,1,0,0,0,0,0,0],
        ("presbyter",       "cruimther"):[0,1,0,0,0,0,0,0],
        ("pugnus",          "cu:an"):[0,1,0,0,0,0,0,0],
        ("pulta",           "colt"):[0,1,0,0,0,0,0,0],
        ("purpura",         "corcur"):[0,1,0,0,0,0,0,0], ##problem derivation
        ("purpureus",       "corcra"):[0,1,0,0,0,0,0,0], ##problem derivation
        ("puteus",          "cuithe"):[0,1,0,0,0,0,0,0],
        ("fictus",          "secht"):[0,2,0,0,0,0,0,0], #fs enter before lenition -> enter between 400 and 425 (McManus has entering after lenition and before kw->k (post-affection!!)) these should be 0,2 no?
        ("floccus",         "slo:ch"):[0,2,0,0,0,0,0,0],
        ("fre:num",         "sri:an"):[0,2,0,0,0,0,0,0],
        ("faba",            "seib"):[0,2,0,0,0,0,0,0], ##problem derivation
        ("fu:stis",         "su:st"):[0,2,0,0,0,0,0,0],
        ("fe:ria",          "se:ire"):[0,2,0,0,0,0,0,0],
        ("fenestra",        "senester"):[0,2,0,0,0,0,0,0], ##problem derivation
        ("fi:bula",         "si:bal"):[0,2,0,0,0,0,0,0],
        ("flecto",          "sle:chtaid"):[0,2,0,0,0,0,0,0],
        ("flagellum",       "sroigell"):[0,2,0,0,0,0,0,0],
        ("furnus",          "sorn"):[0,2,0,0,0,0,0,0],
        ("crotalum",        "crothal"):[0,2,0,0,0,0,0,0], #undergo lenition in 450 -> enter between 400 and 450
        ("abba:tem",        "abbaith"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (a:->e)
        ("dominicus",       "domnach"):[0,2,0,0,0,0,0,0],
        ("gradus",          "gra:d"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (initial v lengthening, due to VL?)
        ("creterra",        "creithir"):[0,2,0,0,0,0,0,0],
        ("ado:ra:re",       "adraid"):[0,2,0,0,0,0,0,0],
        ("habe:na",         "abann"):[0,2,0,0,0,0,0,0],
        ("baculum",         "bachall"):[0,2,0,0,0,0,0,0],
        ("baptisma",        "baithes"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (sm->s:)
        ("brassica",        "braisech"):[0,2,0,0,0,0,0,0],
        ("brittones",       "bretain"):[0,2,0,0,0,0,0,0], #undergoes affection
        ("dia:conus",       "dechon"):[0,2,0,0,0,0,0,0], #undergoes affection
        ("dicta:re",        "dechtaid"):[0,2,0,0,0,0,0,0], #undergoes affection
        ("dominicus",       "domnach"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (i->e to avoid dovnixah -> duvnixah? though I thought raising didn't apply over clusters)
        ("vesperti:na",     "espartan"):[1,2,0,0,0,0,0,0],
        ("vi:num",          "fi:n"):[0,2,0,0,0,0,0,0],
        ("genea:logia",     "genelach"):[0,2,0,0,0,0,0,0], ##problem derivation
        ("i:do:lum",        "i:dol"):[0,2,0,0,0,0,0,0],
        ("calicem",         "cailech"):[0,2,0,0,0,0,0,0],
        ("cancella",        "caingel"):[0,2,0,0,0,0,0,0],
        ("castellum",       "caisel"):[0,2,0,0,0,0,0,0],
        ("camellus",        "camall"):[0,2,0,0,0,0,0,0],
        ("cathedra",        "cathai:r"):[0,2,0,0,0,0,0,0], ##problem derivation
        ("cervi:cal",       "cerchaill"):[0,2,0,0,0,0,0,0], ##problem derivation
        ("cista",           "ces"):[0,2,0,0,0,0,0,0],
        ("cle:ricus",       "cle:irech"):[0,2,0,0,0,0,0,0],
        ("christiAnus",     "cre:sen"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (initial v lengthening and lowering, due to VL?)
        ("crocus",          "cro:ch"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (initial v lengthening, due to VL?)
        ("crotalia",        "crothla"):[0,2,0,0,0,0,0,0],
        ("crucem",          "croch"):[0,2,0,0,0,0,0,0],
        ("exhibernum",      "esarn"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (hi deletion, b->B to get ksB->ks(v|w)->xs(v|w)->s(v|w)->s)
        ("figu:ra",         "figor"):[0,2,0,0,0,0,0,0],
        ("februa:rius",     "febra"):[0,2,0,0,0,0,0,0],
        ("crux",            "cros"):[0,2,0,0,0,0,0,0],
        ("culcita",         "colcaid"):[0,2,0,0,0,0,0,0], ##problem derivation
        ("cucullus",        "cochall"):[0,2,0,0,0,0,0,0], ##problem derivation
        ("quadra:ge:sima",  "corgus"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (sm->s:)
        ("la:ikus",         "la:ech"):[0,2,0,0,0,0,0,0],
        ("labo:rem",        "lubair"):[0,2,0,0,0,0,0,0], ##u by "backing" /a/ when followed by /u/ (derived from british)
        ("levia:than",      "lebeda:n"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (w->b-...->v this feels like the exhibernum change)
        ("li:tus",          "li:th"):[0,2,0,0,0,0,0,0],
        ("librum",          "lebor"):[0,2,0,0,0,0,0,0],
        ("lo:ri:ca",        "lu:irech"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (o:->u: (affection doesn't happen to long vowels!)
        ("macula",          "machaill"):[0,2,0,0,0,0,0,0],
        ("monachus",        "manach"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (o->a (common variants after labials))
        ("medicus",         "midach"):[0,2,0,0,0,0,0,0], ##problem derivation
        ("mendi:cus",       "mindech"):[0,2,0,0,0,0,0,0],
        ("mi:ra:bilis",     "mi:rbail"):[0,2,0,0,0,0,0,0],
        ("modius",          "muide"):[0,2,0,0,0,0,0,0],
        ("mone:ta",         "monad"):[0,2,0,0,0,0,0,0],
        ("morta:litas",     "mortlaith"):[0,2,0,0,0,0,0,0],
        ("oleum",           "olae"):[0,2,0,0,0,0,0,0],
        ("o:ra:tio:",       "ortha"):[0,2,0,0,0,0,0,0],
        ("ocreae",          "ochra"):[0,2,0,0,0,0,0,0],
        ("axilla",          "oxal"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (a->o)
        ("parabola",        "parbail"):[1,2,0,0,0,0,0,0],
        ("paroecia",        "pairche"):[1,2,0,0,0,0,0,0],
        ("pecca:tum",       "peccath"):[1,2,0,0,0,0,0,0],
        ("praedica:re",     "pridchid"):[1,2,0,0,0,0,0,0],
        ("proba:re",        "promad"):[1,2,0,0,0,0,0,0], #there is also paramail instead of par(a?)bail. evidently rarely you might swap out a <b>=v with an <m>=\~m 
        ("pugilla:ria",     "po:lire"):[1,2,0,0,0,0,0,0],  ##problem derivation (within scope) ##idiosyncratic changes applied (ll-> l (Latin vgvll -> v:l ... can get vg->v: if there is no vl, but then can't lenite l, so lenited by magic wand)
        ("re:gula",         "ri:agol"):[0,2,0,0,0,0,0,0], #i: by "breaking"
        ("ro:ma",           "rUam"):[0,2,0,0,0,0,0,0], #u: by "breaking"
        ("rubrum",          "robur"):[0,2,0,0,0,0,0,0],
        ("sagitta",         "saiget"):[0,2,0,0,0,0,0,0],
        ("sacellus",        "sachall"):[0,2,0,0,0,0,0,0],
        ("saturni",         "satharn"):[0,2,0,0,0,0,0,0],
        ("sexta:rius",      "sesra"):[0,2,0,0,0,0,0,0],
        ("secundi:nus",     "sechnall"):[0,2,0,0,0,0,0,0],
        ("septima:na",      "sechtmon"):[0,2,0,0,0,0,0,0],
        ("si:tula",         "si:thal"):[0,2,0,0,0,0,0,0],
        ("signum",          "se:n"):[0,2,0,0,0,0,0,0],
        ("synodus",         "senad"):[0,2,0,0,0,0,0,0],
        ("stra:tu:ra",      "srathar"):[0,2,0,0,0,0,0,0],
        ("tabella",         "ta:ball"):[0,2,0,0,0,0,0,0], ##idiosyncratic changes applied (initial v lengthening, due to VL?)
        ("tra:cta:re",      "tra:chtaid"):[0,2,0,0,0,0,0,0],
        ("tribu:nus",       "trebunn"):[0,2,0,0,0,0,0,0],
        ("tridua:na",       "tredan"):[0,2,0,0,0,0,0,0],
        ("tunica",          "tuinech"):[0,2,0,0,0,0,0,0],
        ("va:gi:na",        "faigen"):[0,2,0,0,0,0,0,0],
        ("vi:cus",          "fi:ch"):[0,2,0,0,0,0,0,0],
        ("vitulus",         "fi:thal"):[0,2,0,0,0,0,0,0],
        ("i:talia",         "eta:il"):[2,3,0,0,0,0,0,0], #undergo harmony in INITIAL SYLLABLE-> enter between 400 and 475
        ("innocuus",        "ennac"):[2,3,0,0,0,0,0,0],
        ("philosophus",     "felsub"):[2,3,0,0,0,0,0,0],
        ("philosophia",     "felsube"):[2,3,0,0,0,0,0,0],
        ("scri:pulus",      "screpul"):[2,3,0,0,0,0,0,0], 
        ("cingula",         "cengal"):[0,3,0,0,0,0,0,0],
        ("coqui:na",        "cucann"):[2,3,0,0,0,0,0,0], ##if we think we know the medial syll harmonized, then the end point is pre-harmony (shortening=60?)
        ("cultrum",         "coltar"):[0,3,0,0,0,0,0,0],
        ("moniste:rium",    "muinter"):[0,3,0,0,0,0,0,0],
        ("scriptu:ra",      "screptar"):[2,3,0,0,0,0,0,0], ##why post lenition?? not p->f->(s?)?
        ("tri:bula:tio:",   "treblait"):[2,3,0,0,0,0,0,0], ##problem derivation ##idiosyncratic changes applied (B->v of a kind with exhibernum, leviathan? also potential VL shortening)
        ("apostolus",       "apstal"):[2,6,0,0,0,0,0,0],#post-lenition
        ("occa:sio",        "accuis"):[2,5,0,0,0,0,0,0],#post-lenition pre lengthening ##idiosyncratic changes applied (degemination despite post-lenition)
        ("o:ra:culum",      "aracol"):[2,5,0,0,0,0,0,0], ##idiosyncratic changes applied (o->a)
        ("episcopus",       "epscop"):[2,7,0,0,0,0,0,0],##w/ VL-syncope of stressed i (did happen in lab_C): post-lenition. else: post-harmony but palatalization problems
        ("ecle:sia",        "eclais"):[2,4,0,0,0,0,0,0],
        ("episcopus",       "eskop"):[2,7,0,0,0,0,0,0],
        ("fata:le",         "fa:tal"):[2,5,0,0,0,0,0,0], ##idiosyncratic changes applied (initial v lengthening)
        ("graeca",          "gre:c"):[2,7,0,0,0,0,0,0],
        ("infernum",        "ifern"):[2,7,0,0,0,0,0,0], ##idiosyncratic changes applied (nf->f)
        ("latro:nem",       "latrann"):[2,4,0,0,0,0,0,0],
        ("macula",          "mocol"):[2,7,0,0,0,0,0,0],
        ("meretri:cem",     "meirtrech"):[2,6,0,0,0,0,0,0],
        ("nota",            "not"):[2,7,0,0,0,0,0,0], 
        ("nota:rius",       "notire"):[2,5,0,0,0,0,0,0],##problem derivation (within scope)
        ("na:ta:licia",     "notlaic"):[2,5,0,0,0,0,0,0], ##shortening might be pre-irish
        ("patricius",       "pa:traic"):[2,7,0,0,0,0,0,0], ##idiosyncratic changes applied (initial v lengthening, due to VL?)
        ("pa:cem",          "po:c"):[2,7,0,0,0,0,0,0],
        ("rosa",            "ro:s"):[2,7,0,0,0,0,0,0],
        ("sacerdo:s",       "sacart"):[2,7,0,0,0,0,0,0],
        ("psallendum",      "salland"):[2,7,0,0,0,0,0,0],
        ("seca:le",         "secal"):[2,4,0,0,0,0,0,0], ##shortening due to writing??
        ("sco:pa",          "scu:ap"):[2,7,0,0,0,0,0,0],
        ("scriptu:ra",      "scriptuir"):[2,4,0,0,0,0,0,0], ##why post lenition?? not p->f->(s?)?
        ("stra:ta",         "sra:it"):[2,7,0,0,0,0,0,0],
        ("thesis",          "te:is"):[2,7,0,0,0,0,0,0], ##thought to be quite late (why??)
        ("cande:la",        "caindel"):[2,4,0,0,0,0,0,0],
        ("benedictio:",     "bendacht"):[3,7,0,0,0,0,0,0], #post harmony loans ##problem derivation
        ("ido:neus",        "idan"):[3,4,0,0,0,0,0,0], ##idiosyncratic changes applied (shortening, not problematic)
        ("quaestio:",       "ceist"):[3,7,0,0,0,0,0,0],
        ("crepusculum",     "crapscuil"):[3,6,0,0,0,0,0,0],
        ("litania",         "lita:n"):[3,7,0,0,0,0,0,0],
        ("mensu:ra",        "messar"):[3,4,0,0,0,0,0,0], ##idiosyncratic changes applied (shortening (u:->u) not problematic because borrowed during shortening period)
        ("historia",        "stoir"):[3,7,0,0,0,0,0,0],
        ("x", "y"):[0,7,0,0,0,0,0,0],
        ("x", "y"):[0,7,0,0,0,0,0,0],
        ("x", "y"):[0,7,0,0,0,0,0,0],
        ("x", "y"):[0,7,0,0,0,0,0,0],
        ("ante tertiam",    "anteirt"):[0,6,0,0,0,0,0,0], ##{listed as leniting, but needs discussion (may be anytime loans) ##idiosyncratic changes applied (haplology?)->no, syncope and delenition
        ("gallus",          "gall"):[0,7,0,0,0,0,0,0], #we don't know if it underwent lenition because written with ll, and Thurneysen contradicts our analysis of consonantal sonorant lenition
        ("confessio:",      "cobais"):[2,7,0,0,0,0,0,0], #it can't be pre-lenition, because f should be s!
        ("numerus",         "nuimir"):[0,7,0,0,0,0,0,0],#no obstruents to lenite. palatalization
        ("offerendum",      "oifrend"):[0,6,0,0,0,0,0,0], #f: this can't be pre-lenition and become f by mere phonology: ff->ssw->sw->s
        ("moli:na",         "muilenn"):[0,3,0,0,0,0,0,0],# no obstruents to lenite, certainly pre-harmony
        ("organum",         "orga:n"):[0,7,0,0,0,0,0,0],#no obstruents to lenite ... no datable phonology but listed as leniting-> enter between 400 and 550
        ("intellectus",     "intliucht"):[0,6,0,0,0,0,0,0],#no obstruents to lenite (odd, nt-/>nd, but syncopates). is degemination sufficient for lenition? post-lenition would presumably also degeminate. Macneill
        ("angelus",         "aingel"):[0,7,0,0,0,0,0,0], #no obstruents to lenite
        ("longa",           "long"):[0,7,0,0,0,0,0,0], #no obstruents to lenite
        ("de:na:rius",      "di:rna"):[0,6,0,0,0,0,0,0],  #no obstruents to lenite ##problem derivation
        ("mu:rus",          "mu:r"):[0,7,0,0,0,0,0,0], #no obstruents to lenite
        ("virtus",          "fiurt"):[0,7,0,0,0,0,0,0], #no obstruents to lenite #well, we do get u-coloring, which indicates it was around sometime when affection was happening
        ("arma",            "arm"):[0,7,0,0,0,0,0,0],#no obstruents to lenite  
        ("stuppa",          "sopp"):[1,2,0,0,0,0,0,0], #no loans with p are written with lenition right? so how would we know this was lenited? certainly affected
        ("cippus",          "cepp"):[1,2,0,0,0,0,0,0],#no loans with p are written with lenition right? so how would we know this was lenited? certainly affected
        ("ungere",          "ongaid"):[0,2,0,0,0,0,0,0], #no obstruents to lenite
        ("barica",          "ba:rc"):[0,7,0,0,0,0,0,0], #} #no obstruents to lenite ##idiosyncratic changes applied (initial v lengthening)
        ("ie:iu:nium",      "ai:ne"):[0,6,0,0,0,0,0,0], #{affection in non-initial syllable  (and not listed under lenition) -> could be any time
        ("leo:",            "leo"):[0,2,0,0,0,0,0,0], #thought to be pre-lenition because of lost /w/ (was it there really?), but does not undergo affection. an early loan provided by Carney
        ("elee:mosina",      "almsan"):[2,5,0,0,0,0,0,0], #post-lenition pre lengthening
        ("ostia:rius",      "aistire"):[0,5,0,0,0,0,0,0], #listed as post-lenition, but I only see evidence for pre-lengthening (st doesn't necessarily lenite)  ##idiosyncratic changes applied (o->a)
        ("basilica",        "baislec"):[2,6,0,0,0,0,0,0], #post-lenition
        ("ca:seus",         "ca:ise"):[2,7,0,0,0,0,0,0],
        ("capitulum",       "caiptel"):[2,6,0,0,0,0,0,0],
        ("camisia",         "caimmse"):[2,6,0,0,0,0,0,0],
        ("culi:na",         "*cuilenn"):[0,7,0,0,0,0,0,0], #can we get an existing form?
        ("lati:na",         "laiten"):[2,4,0,0,0,0,0,0], #if second syll affection is reliable, then early shortening (=60?). else: pre-apocope
        ("ma:tuti:na",      "matan"):[2,4,0,0,0,0,0,0],#if second syll affection is reliable, then early shortening (=60?). else: pre-apocope ##problem derivation
        ("coctu:ra",        "cuchtar"):[0,3,0,0,0,0,0,0],#if second syll affection is reliable, then early shortening (=60?). else: pre-affection
        ("martyrium",       "martrae"):[0,6,0,0,0,0,0,0], ##problem derivation
        ("memoria",         "memmra"):[2,6,0,0,0,0,0,0],
        ("paradi:sus",      "pardus"):[2,4,0,0,0,0,0,0], #must be pre-apocope
        ("uncia",           "ungae"):[0,7,0,0,0,0,0,0],#}
        ("antita:tem",      "ando:it"):[4,7,0,0,0,0,0,0], #listed as post-lenition, but should be post apocope ##idiosyncratic changes applied (*NC repair despite post-lenition, not problematic)
        ("cle:rus",         "cle:r"):[0,7,0,0,0,0,0,0], #also cli:ar ... how would it raise? (and then break)
        ("coro:na",         "corann"):[0,4,0,0,0,0,0,0], 
        ("psalte:rium",     "saltair"):[0,4,0,0,0,0,0,0], 
        ("cortis",          "cuirt"):[0,7,0,0,0,0,0,0], #strongly considering making this undergo affection across [rt] (150->75) ##idiosyncratic changes applied (o->u)
        ("maledictio:",     "maldacht"):[0,7,0,0,0,0,0,0],
        ("ho:ra",           "u:ar"):[0,7,0,0,0,0,0,0],
        ("perso:na",        "persan"):[1,4,0,0,0,0,0,0],
        ("prandium",        "proind"):[1,7,0,0,0,0,0,0], #a->o??
        ("ima:go:",         "i:ma:ig"):[4,7,0,0,0,0,0,0], #{listed as post-lengthening, but could be post-apocope ##idiosyncratic changes applied (initial v lengthening, due to VL?)
        ("alta:re",         "alto:ir"):[4,7,0,0,0,0,0,0],
        ("o:ra:tio:",       "oro:it"):[4,7,0,0,0,0,0,0],
        ("tri:nita:tem",    "trindo:it"):[4,7,0,0,0,0,0,0],
        ("candela:rius",    "caindleo:ir"):[4,6,0,0,0,0,0,0],#}
        ("auxilius",        "u:saile"):[6,7,0,0,0,0,0,0], #{post-syncope loans. auxilius in particular has some flags on it
        ("consul",          "consal"):[6,7,0,0,0,0,0,0],
        ("tympanum",        "timpa:n"):[6,7,0,0,0,0,0,0],
        ("carbunculus",     "carbuncail"):[6,7,0,0,0,0,0,0],
        ("purgato:rium",    "purgato:ir"):[6,7,0,0,0,0,0,0],
        ("epistula",        "epistil"):[6,7,0,0,0,0,0,0],
        ("firma:mentum",    "firmimint"):[6,7,0,0,0,0,0,0],#}
        }

if __name__ == "__main__":
    for i in range(len(forms)):
        for x in data2:
            if forms[i] == x[0] and data[i] != data2[x][:2]: print(forms[i], data[i], x, data2[x])

