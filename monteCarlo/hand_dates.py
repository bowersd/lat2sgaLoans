
#remember: 1st digit is terminus ante quem, can enter no earlier
#          2nd digit is terminus post quem, can enter no later
#   digits reflect slice indices, not element indices
#       you can think of this in the usual phrasing, where counting starts from 0, the first digit is inclusive, and the second digit is exclusive
#       so, [0,2] represents the slice including the 0'th (first for humans) and stopping before the 2nd (third for humans) elements:
#           [E,F,G] -> [E,F]
#   for our purposes, there are 7 temporal bins
#       [[pk],[len],[harm],[complen],[sync],[postsync]]
#           bin 0: p->k
#           bin 1: lenition
#           bin 2: affection
#           bin 3: post-affection-pre-compensatory lengthening (shortening period)
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
        ("'dra.ko:","/ˈdrawg/"):[2,7],#,dracō,drauc
        #("ˈha.ba.kuk","/ˈam.bə.kuk./"):[],#,Habacuc,Ambaucuc ... removed because hebrew
        #("i.du.'me:.","/ˈiə.ðuɱ.ðe/"):[],#,Idumaea,íadum\dae ... removed because hebrew
        ("'li.kwi.d","/ˈlʲex.ðəɣʲ.θʲe/"):[0,2],#,liquidus,lechd\aig\the
        ("'no.t","/ˈno.θəθ/"):[0,2],#,nothus,nothath
        ("ti.'mo.te.","/ˈtʲiəɱ.θe/"):[0,2],#,Timotheus,Tíamthe
        ("'tri.b","/ˈtʲrʲiwv/"):[0,3],#,tribus,triub #DAB: changed from 0,7 because i->u happened
        ("ka.'du:.k","/ˈkað.xəx/"):[0,2],#,cadūcus,cadch\ach
}
inconsistent = {
        ("law.'ren.ti.","/ˈlaw.rʲən.tə.ðʲe"):[0,7], #,Laurentium,laurent\ide #DAB this is probably post-syncope/literary, but restriction to root makes it too short for syncope, and even if syncope did apply, stranded sonorant epenthesis could have undone it
        ("tri.'bla:.ti.o:","/ˈtʲrʲe.vlədʲ/"):[0,3], #,*triblātiō,treblait #DAB syncope originally flagged as going wrong due to losses at end of word.
        ("si.'ki.li.","/ˈʃi.kʲəl.de/"):[6,7], #,Sicilia,Sicel\de #DAB i#>e# ignores that there is an Irish suffix here, so no reason for harmony
        ("pu.'gla:.ri.","/ˈpo:.lə.rʲe/"):[1,3], #,*puglāria,pól\ire #DAB entered early, but the suffix got productive and exceptional to syncope
        ("ma.ke.'do.ni.","/ˈma.kʲə.ðo:n.de/"):[6,7], #,Macedonia,Maccidón\dae #DAB i#>e# ignores that there is an Irish suffix here, so no reason for harmony
        ("pro.'me:.te.","/ˈpro.ɱə.θʲə.ðʲe/"):[6,7], #,Promētheus,promith\ide #DAB I can imagine th spelling t (no lenition, latin pronunciation) or T (no lenition, Greek pronunciation), but this word is post-syncope
        ("o.'ra:.ti.o:","/ˈor.θə/"):[0,2], #,*orātiō,ortha #DAB: autodate was getting tripped up on syncope results
        ("in.tel.'lek.t","/ˈinʲ.tʲluxt/"):[0,3], #,intellectus,intliucht #DAB: the loans spreadsheet has i->u occurring around affection, so that is given for the end point
        ("me.ˈre.tri.k","/ˈmʲerʲ.dʲrʲəx/"):[2,6], #,meretricem,meirdrech #DAB the -x comes from a native suffix, so we follow the t-/->th and make it post-lenition
        ("pa.'tri.ki.","/ˈko.θrə.ɣʲe/"):[0,1], #,Patricius,Cothrige #the syncope problems are real, but this just has to be early early
        ("a.be.ke.'da:.ri.","/ˈabʲ.ɣʲə.dʲərʲ/"):[2,5],#,abecedārium,aipgitir
        ("a.kri.si.'o:.ne:","/ˈa.kʲrʲə.ʃən.de/"):[6,7],#,Acrisiōnē,acrision\dae
        ("aj.'ne:","/ˈaj.nʲe:.ðe"):[6,7],#,Aenēās,aenee\dae since there isn't anything different phonologically, one of these aeneas's should be removed
        ("aj.'ne:.a:s","/ˈaj.nʲe:.a:s/"):[6,7],#,Aenēās,Aeneas
        ("'e:.o.le:n.s","/ˈew.lʲe:ns.te/"):[5,7],#,aeolēnsis,eolens\tae
        ("al.le.'lu:.j","/ˈalʲ.lʲe/"):[0,4],#,allelūia,aille
        ("ar.gu:.'men.t","/ˈar.gə.mʲənʲtʲ/"):[6,7],#,argūmentum,argumeint
        ("awk.ˈsi.li.","/ˈu:.sə.lʲe/"):[6,7],#,auxilius,úsaile
        ("ak.'sil.l","/ˈox.səl/"):[5,7],#,axilla,ochsal
        ("be.re:.'e:n.s","/ˈbʲe.rʲən.ste/"):[5,7],#,beroeēnsis,berens\dae
        ("bis.'sek.st","/ˈbʲi.ʃəxs/"):[5,7],#,bissextus,bissex
        ("ka.bil.'la:.ti.o:","/ˈka.blədʲ/"):[0,5],#,capillātiō,caplait
        ("kar.'buŋ.ku.l","/ˈkar.buŋ.kəlʲ/"):[6,7],#,carbunculus,carbuncail
        ("ka.te:.'ku:.me.n","/ˈkaθ.xəɱʲ.nʲəð/'"):[0,2],#,catēchūmenus,cathchoimn\id
        ("'ken.tr","/ˈkʲenʲ.tʲərʲ/"):[5,7],#,centrum,cinteir
        ("kir.kum.'flek.s","/ˈkʲir.kunʲ.fʲlʲəxs/"):[6,7],#,circumflexus,circunflex
        ("kom.'mu:.ni.o:","/ˈko.mən/"):[3,5],#,commūniō,comman
        ("kom.pa.ra:.'ti:.w","/ˈkom.pə.rədʲ/"):[6,7],#,comparātīuus,comparait
        ("ko:ns.tan.ti:.'no.bo.l","/ˈkon.stənʲ.tʲi:.nə.bəl/"):[6,7],#,Cōnstantīnopolis,Constantinopol
        ("ko:n.'sum.m","/ˈkos.ɱəðʲ/"):[0,6],#,cōnsummō,cosm\aid
        ("ki.kla.si.a","/ˈkʲi.glə.ste/"):[3,7],#,Cyclasias,ciclas\tae #EJFL: Changed date from 2,6 to 3,6 (this was the consensus we reached).
        ("der.'be:n.s","/ˈdʲer.bən.ste/"):[5,7],#,derbēnsis,derbens\dae
        ("dew.te.ro.'no.mi.","/ˈdʲew.tər.nəmʲ/"):[6,7],#,deuteronomium,deutornim
        ("dik.'ta:.to:r","/ˈdik.tə.do:rʲ/"):[6,7],#,dictātōr,dicta\tóir
        }
#where is emilianus, anton?

retranscribed_or_autodate_modded = {
        ("pal.la.ˈki:.n","/ˈpal.nəg.ðe/"):[6,7], #,pallacīnus,palnac\de #DAB ex x ... but orth c indicates [g]
        ("'lak.s,","/ˈlaks/"):[5,7], #,laxus,lax #DAB ex x
        ("'sim.ma.k,","/ˈʃi.mək/"):[3,7], #,Symmachus,Simmach #DAB former Irish x
        ("i.na.k","/ˈi.nək.ðe/"):[3,7], #,Inachus,inach\dae #DAB formerly had x in Irish
        ("ek.ˈsor.kis.t","/ˈek.sər.kə.stəðʲ/"):[6,7], #,exorcistus,exarcist\id #DAB: formerly had x in Irish
        ("eks.'kep.t","/ˈek.skəp.təðʲ/'"):[6,7], #,exceptus,except\aid #DAB: formerly had x in Irish
        ("e:t.'jo.bi.","/ˈe.tʲəbʲ/"):[2,7],#,Aethiobia,Ethioip   #EJFL: Should be "et.'jo.bi.", "/ˈe.tʲəbʲ/"
        ("a.lek.'san.der","/a.lək.sən.dər/"):[6,7],#,Alexander,Alaxander
        #("a.ˈna.ni.","/ˈan.ne/"):[0,3],#,Ananiās,Annae removed bc Hebrew
        ("an.te.be:.'nul.ti.m","/an.tʲe.bʲe:.nʲulʲtʲ/"):[6,7],#,antepaenultima,antepeneuilt #EJFL: Should be "an.te.be.'nul.ti.m","/an.tʲe.bʲe.nʲulʲtʲ/"
        ("ar.'ti.ku.l","/ˈarʲ.tʲə.gəl/"):[6,7],#,articulus,articol DUMP u>@
        ("'a.to.m","/ˈa.dəɱ/"):[2,7],#,atomus,atom
        ("ba.'tis.m","/ˈba.θʲəs/"):[0,2],#,*batisma,baithes DUMP s>h!!
        ("ko.'lum.b","/ˈko.ləm/"):[3,7],#,columba,colum
        ("'ko:n.sul","/ˈkon.səl/"):[6,7],#,cōnsul,consal DUMP u>@
        ("dam.n","/ˈda.mənʲ/"):[2,7],#,damnum,dammain #EJFL: Latin should be "dam.n", damnnum
        }
