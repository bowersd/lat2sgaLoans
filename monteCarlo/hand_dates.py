
#remember: 1st digit is terminus ante quem, can enter no earlier
#          2nd digit is terminus post quem, can enter no later
#   digits reflect slice indices, not element indices
#       you can think of this in the usual phrasing, where counting starts from 0, the first digit is inclusive, and the second digit is exclusive
#       so, [0,2] represents the slice including the 0'th (first for humans) and stopping before the 2nd (third for humans) elements:
#           [E,F,G] -> [E,F]
#   for our purposes, there are 6 temporal bins
#       [[pk],[len],[harm],[complen],[sync],[postsync]]
#           bin 0: p->k
#           bin 1: lenition
#           bin 2: affection
#           bin 3: compensatory lengthening
#           bin 4: syncope
#           bin 5: post-syncope
#       being dated [0,1] means it can only fall in bin 0: the word entered some time between the beginning of borrowing and before the end of p->k
#       being dated [0,2] means it can fall in bin 0 or 1: the word entered some time between the beginning of borrowing and before the end of lenition
#       being dated [1,2] means it can fall in bin 1: the word entered some time between the end of p->k and before the end of lenition
#           and so on
#   criteria:
#       if in doubt, consult check_procs() for regular expressions and ancillary statements (in  autodate.py)
#       todo: further enumeration 

align_crashes = {
        ("'dra.ko:","/ˈdrawg/"):[],#,dracō,drauc
        ("ˈha.ba.kuk","/ˈam.bə.kuk./"):[],#,Habacuc,Ambaucuc
        ("i.du.'me:.","/ˈiə.ðuɱ.ðe/"):[],#,Idumaea,íadum\dae
        ("'li.kwi.d","/ˈlʲex.ðəɣʲ.θʲe/"):[],#,liquidus,lechd\aig\the
        ("'no.t","/ˈno.θəθ/"):[],#,nothus,nothath
        ("ti.'mo.te.","/ˈtʲiəɱ.θe/"):[],#,Timotheus,Tíamthe
        ("'tri.b","/ˈtʲrʲiwv/"):[],#,tribus,triub
        ("ka.'du:.k","/ˈkað.xəx/"):[0,2],#,cadūcus,cadch\ach
}
inconsistent = {
        "a.be.ke.'da:.ri.","/ˈabʲ.ɣʲə.dʲərʲ/":[2,4],#,abecedārium,aipgitir
        ("a.kri.si.'o:.ne:","/ˈa.kʲrʲə.ʃən.de/"):[5,6],#,Acrisiōnē,acrision\dae
        ("aj.'ne:","/ˈaj.nʲe:.ðe"):[5,6],#,Aenēās,aenee\dae since there isn't anything different phonologically, one of these aeneas's should be removed
        ("aj.'ne:.a:s","/ˈaj.nʲe:.a:s/"):[5,6],#,Aenēās,Aeneas
        ("'e:.o.le:n.s","/ˈew.lʲe:ns.te/"):[4,6],#,aeolēnsis,eolens\tae
        ("al.le.'lu:.j","/ˈalʲ.lʲe/"):[0,3],#,allelūia,aille
        ("ar.gu:.'men.t","/ˈar.gə.mʲənʲtʲ/"):[5,6],#,argūmentum,argumeint
        ("awk.ˈsi.li.","/ˈu:.sə.lʲe/"):[5,6],#,auxilius,úsaile
        ("ak.'sil.l","/ˈox.səl/"):[4,6],#,axilla,ochsal
        ("be.re:.'e:n.s","/ˈbʲe.rʲən.ste/"):[4,6],#,beroeēnsis,berens\dae
        ("bis.'sek.st","/ˈbʲi.ʃəxs/"):[4,6],#,bissextus,bissex
        ("ka.bil.'la:.ti.o:","/ˈka.blədʲ/"):[0,4],#,capillātiō,caplait
        ("kar.'buŋ.ku.l","/ˈkar.buŋ.kəlʲ/"):[5,6],#,carbunculus,carbuncail
        ("ka.te:.'ku:.me.n","/ˈkaθ.xəɱʲ.nʲəð/'"):[0,2],#,catēchūmenus,cathchoimn\id
        ("'ken.tr","/ˈkʲinʲ.tʲərʲ/"):[4,6],#,centrum,cinteir
        ("kir.kum.'flek.s","/ˈkʲir.kunʲ.fʲlʲəxs/"):[5,6],#,circumflexus,circunflex
        ("kom.'mu:.ni.o:","/ˈko.mən/"):[3,4],#,commūniō,comman
        ("kom.pa.ra:.'ti:.w","/ˈkom.pə.rədʲ/"):[5,6],#,comparātīuus,comparait
        ("ko:ns.tan.ti:.'no.bo.l","/ˈkon.stənʲ.tʲi:.nə.bəl/"):[5,6],#,Cōnstantīnopolis,Constantinopol
        ("ko:n.'sum.m","/ˈkos.ɱəðʲ/"):[0,5],#,cōnsummō,cosm\aid
        ("ki.kla.si.a","/ˈkʲi.glə.ste/"):[2,6],#,Cyclasias,ciclas\tae
        ("der.'be:n.s","/ˈdʲer.bən.ste/"):[4,6],#,derbēnsis,derbens\dae
        ("dew.te.ro.'no.mi.","/ˈdʲew.tər.nəmʲ/"):[5,6],#,deuteronomium,deutornim
        ("dik.'ta:.to:r","/ˈdik.tə.do:rʲ/"):[5,6],#,dictātōr,dicta\tóir
        }
#where is emilianus, anton?

retranscribed_or_autodate_modded = {
        ("e:t.'jo.bi.","/ˈe.tʲəbʲ/"):[2,6],#,Aethiobia,Ethioip
        ("a.lek.'san.der","/a.lək.sən.dər/"):[5,6],#,Alexander,Alaxander
        ("a.ˈna.ni.","/ˈan.ne/"):[0,3],#,Ananiās,Annae
        ("an.te.be:.'nul.ti.m","/an.tʲe.bʲe:.nʲulʲtʲ/"):[5,6],#,antepaenultima,antepeneuilt
        ("ar.'ti.ku.l","/ˈarʲ.tʲə.gəl/"):[5,6],#,articulus,articol DUMP u>@
        ("'a.to.m","/ˈa.dəɱ/"):[2,6],#,atomus,atom
        ("ba.'tis.m","/ˈba.θʲəs/"):[0,2],#,*batisma,baithes DUMP s>h!!
        ("ko.'lum.b","/ˈko.ləm/"):[3,6],#,columba,colum
        ("'ko:n.sul","/ˈkon.səl/"):[5,6],#,cōnsul,consal DUMP u>@
        ("dam.'na:.ti.o:","/ˈda.mənʲ/"):[2,6],#,damnātiō,dammain
        }
