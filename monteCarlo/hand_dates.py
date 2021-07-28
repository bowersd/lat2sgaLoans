
#remember: 1st digit is terminus ante quem, can enter no earlier
#          2nd digit is terminus post quem, can enter no later
#   digits reflect slice indices, not element indices
#       you can think of this in the usual phrasing, where counting starts from 0, the first digit is inclusive, and the second digit is exclusive
#       so, [0,2] represents the slice including the 0'th (first for humans) and stopping before the 2nd (third for humans) elements:
#           [E,F,G] -> [E,F]
#   for our purposes, there are 7 temporal bins
#       [[],[],[],[],[],[]]
#           bin 0: p->k
#           bin 1: lenition
#           bin 2: affection
#           bin 3: apocope
#           bin 4: compensatory lengthening
#           bin 5: syncope
#           bin 6: post-syncope
#       being dated [0,1] means it can only fall in bin 0: the word entered some time between the beginning of borrowing and before the end of p->k
#       being dated [0,2] means it can fall in bin 0 or 1: the word entered some time between the beginning of borrowing and before the end of lenition
#       being dated [1,2] means it can fall in bin 1: the word entered some time between the end of p->k and before the end of lenition
#           and so on
#   criteria:
#       if in doubt, consult check_procs() for regular expressions and ancillary statements (in  autodate.py)
#       todo: further enumeration 

align_crashes = {
        ("'dra.ko:","/ˈdrawg/"):[]#,dracō,drauc
        ("ˈha.ba.kuk","/ˈam.bə.kuk./"):[]#,Habacuc,Ambaucuc
        ("i.du.'me:.","/ˈiə.ðuɱ.ðe/"):[]#,Idumaea,íadum\dae
        ("'li.kwi.d","/ˈlʲex.ðəɣʲ.θʲe/"):[]#,liquidus,lechd\aig\the
        ("'no.t","/ˈno.θəθ/"):[]#,nothus,nothath
        ("ti.'mo.te.","/ˈtʲiəɱ.θe/"):[]#,Timotheus,Tíamthe
        ("'tri.b","/ˈtʲrʲiwv/"):[]#,tribus,triub
}
