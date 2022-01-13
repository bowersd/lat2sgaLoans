
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
        ("pa.le:s.'ti:.na","/ˈpa.lə.ʃtʲə.na/"):[6,7], #Palaestīna,Palastina  #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("fi.li.pi.a.'ne:n.s","/ˈfʲi.lʲə.pʲən.ste/"):[6,7], #philipianēnsis,Philipians\tae #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("fi.'le:.mo:n","/fʲi.lə.ɱo:nʲ/"):[6,7], #Philēmōn,Philomóin #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("po.si.'ti:.w","/ˈpo.ʃədʲ/"):[6,7], #positīuus,posit #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("su.ber.la:.'ti:.w","/ˈsu.ber.lədʲ/"):[6,7], #superlātīuus,superlait #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("so:s.te.ne:s","/sus.tə.nʲəs/"):[6,7], #Sōsthenēs,Susthenes #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("tes.ti.'mo:.ni.","/ˈtʲe.ʃtʲə.ɱʲənʲ/"):[6,7], #testimōnium,teistimin #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("we:.ro:.ˈne:n.s","/ˈfʲe.rə.nʲən.ste/"):[6,7], #uērōnēnsis,ueronens\tae #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("wes.pa.si.ˈa:.n","/ˈfʲe.spə.ʃiən/"):[6,7], #Uespasiānus,Uespisían #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("mo.nas.'te:.ri.","/ˈmo.nʲə.ʃtʲərʲ/"):[6,7], #,monastērium,moinistir #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("ho.ra.ti.'a:.n","/ˈo.rə.tʲən.de/"):[6,7], #horatiānus,oratian\dae #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("op.ta:.'ti:.w","/ˈob.tədʲ/"):[6,7], #,optātīuus,optait #DAB post-syncope/literary loan
        ("in.fi:.'ni:.t","/ˈinʲ.fʲə.nʲədʲ/"):[6,7], #,infīnītum,infinit #DAB post-syncope/literary loan
        ("e.'fra.te:.","/ˈe.frə.dʲə.ðʲe/"):[6,7], #,Ephrataeus,Eufrat\ide #DAB post-syncope/literary loan
        ("wes.per.'ti:.n","/ˈe.spər.tə/"):[1,4], #,(hōra) uespertīna,esparta #DAB after syncope schwa was likely inserted before the liquid
        ("e.mi.li.'a:.n","/ˈe.mʲəlʲe:nde/"):[6,7], #,aemil-iān-us,emil\én\dae #DAB pretty clear failure to shorten
        ("eks.kom.mu:.ni.'ka:.ti.o:","/ˈesk.ɱən/"):[0,4], #,excommūnicātiō,escmon #DAB: automatic methods thrown off by aggressive truncation. What survived into Irish clearly underwent shortening and syncope
        ("kwiŋ.kwa:.'ge:s.m","/ˈkʲeŋ.kʲə.ɣʲəs/"):[0,3], #,*quinquāgēsma,cingciges #DAB not clear why syncope failed here, but most of the evidence points to a pre-harmony loan
        ("a.ris.'to.te.le:s","/ˈa.rʲə.stə.təlʲ/"):[6,7], #,Aristotelēs,Aristotil #DAB literary loan
        ("fir.ˈra.di.","/ˈfʲir.ðe/"):[3,7],#,Phirradios,phir\de #DAB i#>e# ignores that there is an Irish suffix here, so no reason for harmony
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

post_lenition_fs_theory = {
        ("ˈfik.t","/ˈʃext/"):[1,4], #,fictus,secht
        ("'fa.b","/ˈʃevʲ/"):[1,4], #,faba,seib
        ("fe.'nes.tr","/ˈʃe.nʲə.ʃtʲər/"):[1,4], #,fenestra,seinester
        ("'fe:.ri.","/ˈʃe:.rʲe/"):[1,4], #,fēria,séire
        ("'fer.ku.l","/ˈʃer.kəl/"):[1,4], #,ferculum,sercol
        ("'fi:.bu.l","/ˈʃi:.vəl/"):[1,4], #,fībula,síbal
        ("fle:k.t","/ˈʃlʲe:x.təðʲ/"):[1,4], #,flēctō,slécht\aid
        ("'flo:.k","/ˈslo:x/"):[1,4], #,*flōcus,slóch
        ("ˈfur.n","/ˈsorn/"):[1,4], #,furnus,sorn
        ("'fre:.n","/ˈʃrʲiən/"):[1,4], #,frēnum,srían
        ("fra.'gil.l","/ˈsro.ɣʲəl/"):[1,4], #,*fragillum,sroigel
        ("'fu:s.t","/ˈsu:st/"):[1,4], #,fūstis,súst
        }

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
