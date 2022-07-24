
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
        ("'dra.ko:","/ˈdrawg/"):[1,7],#,dracō,drauc
        #("ˈha.ba.kuk","/ˈam.bə.kuk./"):[],#,Habacuc,Ambaucuc ... removed because hebrew
        #("i.du.'me:.","/ˈiə.ðuɱ.ðe/"):[],#,Idumaea,íadum\dae ... removed because hebrew
        ("'li.kwi.d","/ˈlʲex.ðəɣʲ.θʲe/"):[0,2],#,liquidus,lechd\aig\the
        ("'no.t","/ˈno.θəθ/"):[0,2],#,nothus,nothath
        ("ti.'mo.te.","/ˈtʲiəɱ.θe/"):[0,2],#,Timotheus,Tíamthe
        ("'tri.b","/ˈtʲrʲiwv/"):[0,3],#,tribus,triub #DAB: changed from 0,7 because i->u happened
        ("ka.'du:.k","/ˈkað.xəx/"):[0,2],#,cadūcus,cadch\ach
        ("pre.'di:.k","/ˈpʲrʲið.xəðʲ/"):[1,2], #,*predīcō,pridch\aid #DAB: misalignment put the k with <d> instead of [x]
}
inconsistent = {
        ("de:.bre.'ka:.ti.o:","/ˈdʲe.bʲrʲə.go:dʲ/"):[4,7], #,dēprecātiō,deiprecóit,McManus/Other #DAB not inconsistent, but there's a chance this syncopated to debrgo:d and then became debr@go:d
        ("me:.'tro.bo.l","/ˈme.drə.bəlʲ/"):[1,7], #,mētropolis,metrapoil,Ml. deiprecoit class
        ("a.kri.si.'o:.ne:","/ˈa.kʲrʲə.ʃən.de/"):[1,7], #,Acrisiōnē,acrision\dae,Sg. deiprecoit class
        #("ki.kla.si.a","/ˈkʲi.glə.ste/"):[3,7], #,Cyclasias,ciclas\tae,Sg. deiprecoit class > only kiklas was borrowed, the latter portion is an Irish suffix, so the borrowed portion would have been too short to syncopate, and this does not belong with deiprecoit
        ("ki.kla.si.a","/ˈkʲi.glə.ste/"):[3,7],#,Cyclasias,ciclas\tae #EJFL: Changed date from 2,6 to 3,6 (this was the consensus we reached). > due to failure to lower
        ("ko:n.'fes.si.o:","/ˈko.vəʃ/"):[0,5], #,cōnfessiō,cobais,"Ml.,MG" #nf>v is pre-syncope. post-syncope date was triggered by aggressive British apocope, so disregarding 
        ("mas.ku.'li:.n","/ˈma.sku.lʲən.de/"):[6,7], #,masculīnus,masculin\dae,Sg. #valuing lack of syncope over potential orthographic omission of length
        ("'no.ta:.ri","/ˈno.də.rʲe/"):[1,3], #,notārius,not/aire,Wb. #lack of syncope is due to (later) exceptionality of -aire
        ("fe:.ri.'a:.l","/ˈfʲe:.ro:lʲ/"):[4,7], #,fēriālis,féróil #DAB if the mapping were from the original Latin, [i] would be lost by syncope. But [a:]>[o:] shows it came through British Latin, where /i/ in hiatus became [j] (there was also British syncope), so Irish syncope actually had no vowel to target when this word came in.
        ("pa.le:s.'ti:.na","/ˈpa.lə.ʃtʲə.na/"):[6,7], #Palaestīna,Palastina  #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("fi.li.pi.a.'ne:n.s","/ˈfʲi.lʲə.pʲən.ste/"):[6,7], #philipianēnsis,Philipians\tae #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("fi.'le:.mo:n","/fʲi.lə.ɱo:nʲ/"):[6,7], #Philēmōn,Philomóin #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("po.si.'ti:.w","/ˈpo.sədʲ/"):[6,7], #positīuus,posit #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("su.ber.la:.'ti:.w","/ˈsu.ber.lədʲ/"):[6,7], #superlātīuus,superlait #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("so:s.te.ne:s","/sus.tə.nʲəs/"):[6,7], #Sōsthenēs,Susthenes #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("tes.ti.'mo:.ni.","/ˈtʲe.ʃtʲə.ɱʲənʲ/"):[6,7], #testimōnium,teistimin #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("we:.ro:.ˈne:n.s","/ˈfʲe.rə.nʲən.ste/"):[6,7], #uērōnēnsis,ueronens\tae #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("wes.pa.si.ˈa:.n","/ˈfʲe.spə.ʃiən/"):[6,7], #Uespasiānus,Uespisían #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
        ("mo.nis.'te:.ri.","/ˈmo.nʲə.ʃtʲərʲ/"):[6,7], #,*monistērium,moinistir #DAB literary loan. given inconsistent written length in Latin, we put more weight on the failure to syncopate than the apparent shortening
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
        ("tri.'bla:.ti.o:","/ˈtʲrʲe.vlədʲ/"):[1,3], #,*triblātiō,treblait #DAB syncope originally flagged as going wrong due to losses at end of word.
        ("si.'ki.li.","/ˈʃi.kʲəl.de/"):[6,7], #,Sicilia,Sicel\de #DAB i#>e# ignores that there is an Irish suffix here, so no reason for harmony
        ("pu.'gla:.ri.","/ˈpo:.lə.rʲe/"):[1,3], #,*puglāria,pól\ire #DAB entered early, but the suffix got productive and exceptional to syncope
        ("ma.ke.'do.ni.","/ˈma.kʲə.ðo:n.de/"):[6,7], #,Macedonia,Maccidón\dae #DAB i#>e# ignores that there is an Irish suffix here, so no reason for harmony
        ("pro.'me:.te.","/ˈpro.ɱə.θʲə.ðʲe/"):[6,7], #,Promētheus,promith\ide #DAB I can imagine th spelling t (no lenition, latin pronunciation) or T (no lenition, Greek pronunciation), but this word is post-syncope
        ("o.'ra:.ti.o:","/ˈor.θə/"):[0,2], #,*orātiō,ortha #DAB: autodate was getting tripped up on syncope results
        ("in.tel.'lek.t","/ˈinʲ.tʲluxt/"):[0,3], #,intellectus,intliucht #DAB: the loans spreadsheet has i->u occurring around affection, so that is given for the end point --- a pronunciation with /inʲ.dʲluxt/ is attested (seee Ml. 18c11) 
        ("me.ˈre.tri.k","/ˈmʲerʲ.dʲrʲəx/"):[1,6], #,meretricem,meirdrech #DAB the -x comes from a native suffix, so we follow the t-/->th and make it post-lenition
        ("pa.'tri.ki.","/ˈko.θrə.ɣʲe/"):[0,1], #,Patricius,Cothrige #the syncope problems are real, but this just has to be early early
        ("a.be.ke.'da:.ri.","/ˈabʲ.ɣʲə.dʲərʲ/"):[1,5],#,abecedārium,aipgitir
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
        #f->f
        ("'al.fa","/ˈal.fa/",):[0,7], #alpha,alfa
        ("fe.'bra:.ri.","/ˈfʲe.vre/",):[0,3], #*febrārius,Febrae
        ("fe:.mi.'ni:.n","/ˈfʲe.ɱʲən/",):[0,4], #fēminīnus,feimen 1
        ("fi.'lo.so.f","/ˈfʲel.suv/",):[0,3], #philosophus,felsub  ----> or 2,3 if the survival of medial f is indicative of post-lenition (otherwise f in this position would likely have disappeared)
        ("'fi.gu:.r","/ˈfʲi.ɣər/"):[0,4], #figūra,figor
        ("ˈfo:r.m","/ˈforʲmʲ/",):[0,7], #fōrma,foirm
        ("i.ˈfer.n","/ˈi.fʲərn/",):[0,7], #*ifernum,ifern ----> or 2,3 if the survival of medial f is indicative of post-lenition (otherwise f in this position would likely have disappeared)
        ("'sap.fir","/ˈsa.fʲər/",):[0,7], #sapphir,saphir
        }
##f->f ... if treatment of f is trigger for [1,X], undo it 
#alfa alfa [1, 7] CHANGE to 0,7
#febrAri fev__re [1, 3] CHANGE to 0,3
#fEminIn feɱ__ən [1, 4] CHANGE to 0,4
#filosof fel_suv [1, 3] CHANGE to 0,3
#figUr fiɣər [1, 4] CHANGE to 0,4
#fOrm form [1, 7] CHANGE to 0,7
#ifern ifərn [1, 7] CHANGE to 0,7
#sapfir sa_fər [1, 7] CHANGE to 0,7

##what about f>v? should it be treated as f>f?
#_skiful eskəvəl [0, 7]
#grIf grIv [0, 7]

#Unaffected by f-liberation
#Afrik__ afrəkðe [2, 7]
#abostrof abəstrəf [6, 7]
#kirkumfleks kirkunfləxs [6, 7]
#kOnfeSi ko_vəs_ [6, 7]
#kOnfiteor ku_vəd_ər [6, 7]
#elefant eləfAnt [6, 7]
#efrat__E efrədəðe [6, 7]
#fatAl fAdəl [2, 4]
#fEriAl fEr_Ol [4, 7]
#faetonti_a f_etəntəðe [6, 7]
#fIkul__ fIgulde [2, 7]
#firmAment fir__mənt [3, 4]
#infInIt infənəd [6, 7]
#lUkifer lukəfər [6, 7]
#oFerend of_rənd [0, 6]
#filipianEns__ filəp___ənste [6, 7]
#filEmOn filəɱOn [6, 7]
#fiRadi fir_ðe [3, 7]
#sakərfik sakərvək [2, 7]
#stefAn stefAn [4, 7]

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

#syncope does not trigger palatalization in these loans, and so can't be Irish syncope
#bigger_complen_syncope = {
#        ("tri:.n.'da:t","/ˈtʲrʲi:n.do:dʲ/"):[4,6], #,trīndātem,tríndóit #DAB just in case it wasn't British syncope
#        ("an.'da:.t","/ˈan.do:dʲ/"):[4,6], #,*andātem,andóit #DAB just in case it wasn't VL syncope from antitatem
#        }
