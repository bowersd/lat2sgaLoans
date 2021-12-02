import needleman
import count_sylls
import subprocess
import hand_dates
#import hackydata
#subprocess.call(*args)
import re
import sys

#todo: incorporate manual override for dating
#todo: u-affection (a->u) p 138 Mccone, cf hock 2019?
#   when is this dated? lumping it with the other affection processes seems dicey, since our sources don't do this
# It is typically dated after raising but before lowering: */kalunas/ > ROUNDING: */kaulunas/ > LOWERING: */kaulonas/ > APOCOPE */kaulon/ > REDUCTION */kaul@n/: Attested as the name <Caulann>.
# Later: /au/>/u/ so <Culann>, which is also attested. I wouldn't say that a>u is one change. It is two changes: (1) dipthongization/rounding of a to au (and i to iu and e to eu if raising of e
# can't apply). (2) /a/ to /u/.


def read_in(filename):
    h = []
    with open(filename) as fileIn:
        for line in fileIn:
            h.append(line.strip().split(','))
    return h

def latin_orth_phon(*stringPairs):
    h = {}
    for pair in stringPairs:
        for i in range(len(pair[0])):
            if pair[0][i] not in h: h[pair[0][i]] = [pair[1][i]]
            elif pair[1][i] not in h[pair[0][i]]: h[pair[0][i]].append(h[pair[1][i]])
    return h

def strip_supra(latinPhon):
    return "".join(re.split("\.'/", latinPhon))

def length_mod(string):
    h = []
    change = {
            "ē":"e:",
            "ā":"a:",
            "ī":"i:",
            "ō":"o:",
            "ū":"u:",
            "ȳ":"i:",
            "é":"e:",
            "ú":"u:",
            "á":"a:",
            "ó":"o:",
            "í":"i:",
            }
    for x in string.lower():
        if x not in change:
            h.append(x)
        else:
            h.append(change[x])
    return "".join(h)

def clean_transcription(string):
    #print(string)
    #convert length marking to single characters
    #remove palatalization, suprasegmentals and "/"
    #NB: prefixes will mess up stress computation
    h = []
    i = len(string)-1
    while i > -1:
        if string[i] == ":":
            h.append(string[i-1].upper())
            i -= 2
            #if not re.match('[aeiouə]', string[i-1]): i -= 1
        elif re.match("[ˈ'./ʲ]", string[i]): 
            i -= 1
        elif string[i] == "ʃ": 
            h.append("s")
            i -= 1
        else:
            h.append(string[i])
            i -= 1
    i = 0
    j = 2
    while j < len(h):
        #print(h[i:j])
        if h[i:j][0] == h[i:j][1] and h[i] not in "aeiouAEIOUə":
            #print("HIT")
            h = h[:i]+[h[i].upper()]+h[j:]
        i += 1
        j += 1
    return "".join(reversed(h))

def check_envi(string, *regexen):
    h = []
    for r in regexen:
        h.append(r.search(string))
    return h

def check_appl(string, *regexen, **mappings):
    pass

triggers = [#what to look for in Latin
        re.compile('[Pp]'), #pk
        re.compile('((?<=[aeiouAEIOU])_*[tkbdgms])|f'), #lenition (f>s in, st>s removed due to post-lenition strata>strait) WHAT ABOUT LONG [f:]??
        re.compile('(((e|o)(?=_*[^AEIOUaeiou]?_*[iuIU]))|((i|u)(?=[^AEIOUaeiou]*[aoAO])))'), #affection ... just identifying all possible targets and letting process ID weed out the rest (non-initial syllables will be @ in Irish). ideally would also check morph class information on monosylables.
        #re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), #apocope
        re.compile('[aeiou]_*(?=[dgtk][^rlnm])'), #compensatory lengthening (shortening handled in procs_kludge() to avoid lookbehind limits)
        re.compile('(mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks)'), #syncope (phonotactics here, V deletion handled below) mp has different pre-history (we don't know when it vanished/what was the outcome), but part of natural class and made legal by syncope
        ]
processes = [ #slightly refined regexen to apply to latin, paired with dicts to check if the rule applied or not. these need to be alignment-proof (overlook _)
        ((re.compile('[Pp](?!_*t)'), {"p":"kxɣ", "P":"kxɣ"},1),(re.compile('[Pp]'), {"P":"pb","p":"pb"}, 0)),
        ((re.compile('((?<=[aeiouAEIOU])_*[t]|(s|k)(?![Tt]))|f'), { "t":"θð", "k":"xɣ",  "s":"h", "f":"s"},1), (re.compile('((?<=[aeiouAEIOU])_*(t|k|b|d|g|m|s(?![ptk])))'), {"t":"td", "k":"kg", "b":"b", "d":"d", "g":"g", "m":"m", "s":"s", },0)),
        ((re.compile('(((e|o)(?=_*[^AEIOUaeiou]?_*[iuIU]))|((i|u)(?=[^AEIOUaeiou]*[aoAO])))'),{"e":"i", "o":"u", "i":"e", "u":"o", },1),(re.compile('(((e|o)(?=_*[^AEIOUaeiou]?_*[iuIU]))|((i|u)(?=[^AEIOUaeiou]*[aoAO])))'), {"i":"i", "e":"e", "u":"u", "o":"o", },0)), #just dropping the string-initial requirement and relying on @ in Irish to rule out non-initial sylls
        #((re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), {"A":"aə", "E":"eə", "I":"iə", "O":"oə", "U":"uə"}),(re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), {"A":"AO", "E":"E", "I":"I", "O":"O", "U":"U"})), #apocope
        ((re.compile('[aeiou]_*(?=[dgtk][rlnm])'), {"a":"A", "e":"E", "i":"I", "o":"O", "u":"U"},1), (re.compile('[aeiou]_*(?=[dgtk][^rlnm])'), {"a":"a", "e":"e", "i":"i", "o":"o", "u":"u"},0)), #compensatory lengthening (shortening handled in procs_kludge() to avoid lookbehind limits) Is there data on failure to lengthen??
        ((re.compile('(mp|ŋk|n(t(?!$)))'),{"mp":"mb", "ŋk":"ŋg", "nt":"nd"},2),(re.compile('(mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks)'),{"mp":"mp", "ŋk":"ŋk", "nt":"nt", "ns":"ns", "nf":"nf","ks":"xsks"},3)), #syncope (phonotactics here, V deletion handled below)
        #((re.compile('(mp|ŋk|n(t(?!$)|f))|((?<!^e)ks)'),{"mp":"mb", "ŋk":"ŋg", "nt":"nd", "nf":"_v", "ks":"_s"},2),(re.compile('(mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks)'),{"mp":"mp", "ŋk":"ŋk", "nt":"nt", "ns":"ns", "nf":"nf","ks":"xsks"},3)), #syncope (phonotactics here, V deletion handled below)
        ]

def check_procs_nu(latin, irish, triggers, processes):
    values = []
    for i in range(len(triggers)):
        print(i)
        pvals = []
        if triggers[i].search(latin): 
            #print(i)
            for x in processes[i][0][0].finditer(latin):
                #print(latin, irish, x.span(), processes[i][0][0])
                if irish[x.start():x.end()] in processes[i][0][1][x.group()]:pvals.append((x.span(), processes[i][0][2]))
            for x in processes[i][1][0].finditer(latin):
                if irish[x.start():x.end()] in processes[i][1][1][x.group()]:pvals.append((x.span(), processes[i][1][2]))
        #else: pvals.append(("?", ""))
        #print(pvals)
        values.append([x[1] for x in sorted(pvals)])
    return values

def procs_kludge(latin, irish, values):
    #safe copy of values not created!
    if any([irish[x.start():x.end()] == "s_" for x in re.finditer("st", latin)]): values[2].append(1) #st>s happened in strata>srait (a post-lenition loan) and so diagnoses pre-affection (this is latest datable occurrence of st>s)
    if values[2] == [0] and latin[re.search('[aeiouAEIOU]', latin).start()] in 'eo' and irish[re.search('[aeiouAEIOU]', irish).start()+1] in 'xɣ': values[2] = [] #failure to raise across 'x' is not diagnostic of affection failure
    if latin[-1] in "Ii" and irish[-1] == "e": values[2].append(1) #detecting lowering of Latin /i/ by /-a.../. Are we sure that there wasn't a post-affection suffix -e that just replaced the Latin /i/ directly? -> may need a failure watch as in monosyllable_repair() EJFL: It seems more complicated to assume morphological replacement in all cases than that lowering affects medial i causing it to become -e; the phonology is totally regular.
    #DAB: the question isn't whether we assume morphological replacement in all cases, but whether a potential phonological criterion is truly criterial. We should not count something as showing a phonological process if it may be the result of morphology.
    if latin[-1] in "Ii" and irish[-1] in "Ii": 
        print("was failure due to envi not met or was loan too late?")
        print(latin)
        print(irish)
    sylls = count_sylls.count_syll(latin)
    #print(sylls)
    if len(sylls) == 1: values = monosyllable_repair(latin, irish, values)
    #if len(sylls) > 1 and latin[sylls[-1]] in "Uu" and irish[sylls[-1]] == "ə": values[2].append(1) #detecting lowering>reduction of /u/ in stem-final syllables
    #if len(sylls) > 1 and latin[sylls[-1]] in "Uu" and irish[sylls[-1]] in "Uu": 
    #    print("was failure due to envi not met or was loan too late?")
    #    print(latin)
    #    print(irish)
    if len(sylls) > 1: #detecting shortening of post-initial syllables (diagnoses pre/post-BEGINNING of compensatory lengthening), syncopation is not limited to weak positions, but it should be so limited!!
        longv = re.compile('[AEIOU]') 
        shortening = {"A":"aə_", "E":"eə_", "I":"iə_", "O":"oə_", "U":"uə_"} #outputs not over broad, because reduction didn't target word final open sylls IIRC
        for m in longv.finditer(latin[sylls[1]:sylls[-1]]):
            if irish[sylls[1]:sylls[-1]][m.start():m.end()] in shortening[m[0]]: values[-2].append(2)
            elif irish[sylls[1]:sylls[-1]][m.start():m.end()] == m[0] or (irish[sylls[1]:sylls[-1]][m.start():m.end()] == "O" and m[0]=="A"): values[-2].append(3)
    return values

def sync_check(irish, sylls, parity, values):
    #safe copy of values not created!
    #parity = count_sylls.alt_w_fin_degen(sylls)
    #also need to allow for an extra syll at end in irish, check if any non-weak sylls are deleted
    #print(parity)
    if all([irish[sylls[i]] == "_"  for i in range(len(sylls)) if not parity[i]]) and not all(parity) and not any([irish[sylls[i]] == "_"  for i in range(len(sylls)) if parity[i]]): values[-1].append(1)
    elif all([irish[sylls[i]] == "_"  for i in range(len(sylls)-1) if not parity[i]]) and all(parity[-2:]) and irish[sylls[-1]] == "_" and re.match("[aeiouə]", irish[sylls[-1]+1:]): values[-1].append(1)
    elif len(sylls)>2: values[-1].append(0)
    #else: values.append([])
    return values

def check_procs(latin, irish):
    #print(latin, irish)
    values = []
    triggers = [#what to look for in Latin
            re.compile('[Pp]'), #pk
            re.compile('((?<=[aeiouAEIOU])_*[tkbdgms])|f'), #lenition (f>s in, st>s removed due to post-lenition strata>strait) WHAT ABOUT LONG [f:]??
            re.compile('(((e|o)(?=_*[^AEIOUaeiou]?_*[iuIU]))|((i|u|U)(?=[^AEIOUaeiou]*[aoAO])))'), #affection ... just identifying all possible targets and letting process ID weed out the rest (non-initial syllables will be @ in Irish). ideally would also check morph class information on monosylables.
            re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), #apocope
            re.compile('[aeiou]_*(?=[dg][^aeiouAEIOU])'), #compensatory lengthening
            re.compile('(mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks)'), #syncope (phonotactics here, V deletion handled below) mp has different pre-history (we don't know when it vanished/what was the outcome), but part of natural class and made legal by syncope
            ]
    processes = [ #slightly refined regexen to apply to latin, paired with dicts to check if the rule applied or not. these need to be alignment-proof (overlook _)
            ((re.compile('[Pp](?!_*t)'), {"p":"kxɣ", "P":"kxɣ"}),(re.compile('[Pp]'), {"P":"pb","p":"pb"})),
            ((re.compile('((?<=[aeiouAEIOU])_*[t]|(s|k)(?![Tt]))|f'), { "t":"θð", "k":"xɣ",  "s":"h", "f":"s"}), (re.compile('((?<=[aeiouAEIOU])_*(t|k|b|d|g|m|s(?![ptk])))'), {"t":"td", "k":"kg", "b":"b", "d":"d", "g":"g", "m":"m", "s":"s", })),
            ((re.compile('(((e|o)(?=_*[^AEIOUaeiou]?_*[iuIU]))|((i|u|U)(?=[^AEIOUaeiou]*[aoAO])))'),{"e":"i", "o":"u", "i":"e", "u":"oə", "U":"ə"}),(re.compile('(((e|o)(?=_*[^AEIOUaeiou]?_*[iuIU]))|((i|u|U)(?=[^AEIOUaeiou]*[aoAO])))'), {"i":"i", "e":"e", "u":"u", "o":"o", "U":"u"})), #just dropping the string-initial requirement and relying on @ in Irish to rule out non-initial sylls
            ((re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), {"A":"aə", "E":"eə", "I":"iə", "O":"oə", "U":"uə"}),(re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), {"A":"AO", "E":"E", "I":"I", "O":"O", "U":"U"})), #apocope
            ((re.compile('[aeiou]_*(?=[dg][^aeiouAEIOU])'), {"a":"A", "e":"E", "i":"I", "o":"O", "u":"U"}), (re.compile('[aeiou]_*(?=[dg][^aeiouAEIOU])'), {"a":"a", "e":"e", "i":"i", "o":"o", "u":"u"})), #compensatory lengthening
            ((re.compile('(mp|ŋk|n(t(?!$)))|((?<!^e)ks)'),{"mp":"mb", "ŋk":"ŋg", "nt":"nd", "ks":"_s"}),(re.compile('(mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks)'),{"mp":"mp", "ŋk":"ŋk", "nt":"nt", "ns":"ns", "nf":"nf","ks":"xsks"})), #syncope (phonotactics here, V deletion handled below)
            ]
    for i in range(len(triggers)):
        #print(i)
        pvals = []
        if triggers[i].search(latin): 
            #print(i)
            for x in processes[i][0][0].finditer(latin):
                #print(latin, irish, x.span(), processes[i][0][0])
                if irish[x.start():x.end()] in processes[i][0][1][x.group()]:pvals.append((x.span(), 1))
            for x in processes[i][1][0].finditer(latin):
                if irish[x.start():x.end()] in processes[i][1][1][x.group()]:pvals.append((x.span(), 0))
        #else: pvals.append(("?", ""))
        #print(pvals)
        values.append([x[1] for x in sorted(pvals)])
    if any([irish[x.start():x.end()] == "s_" for x in re.finditer("st", latin)]): values[2].append(1) #st>s happened in strata>srait (a post-lenition loan) and so diagnoses pre-affection (this is latest datable occurrence of st>s)
    if values[2] == [0] and latin[re.search('[aeiouAEIOU]', latin).start()] in 'eo' and irish[re.search('[aeiouAEIOU]', irish).start()+1] in 'xɣ': values[2] = [] #failure to raise across 'x' is not diagnostic of affection failure
    if latin[-1] in "Ii" and irish[-1] == "e": values[2].append(1) #detecting lowering of Latin /i/ by /-a.../. Are we sure that there wasn't a post-affection suffix -e that just replaced the Latin /i/ directly? -> may need a failure watch as in monosyllable_repair() EJFL: It seems more complicated to assume morphological replacement in all cases than that lowering affects medial i causing it to become -e; the phonology is totally regular.
    if latin[-1] in "Ii" and irish[-1] in "Ii": 
        print("was failure due to envi not met or was loan too late?")
        print(latin)
        print(irish)
    sylls = count_sylls.count_syll(latin)
    #print(sylls)
    if len(sylls) > 1 and latin[sylls[-1]] in "Uu" and irish[sylls[-1]] == "ə": values[2].append(1) #detecting lowering>reduction of /u/ in stem-final syllables
    if len(sylls) > 1 and latin[sylls[-1]] in "Uu" and irish[sylls[-1]] in "Uu": 
        print("was failure due to envi not met or was loan too late?")
        print(latin)
        print(irish)
    if len(sylls) > 2: #detecting shortening of stem-internal syllables (diagnoses pre/post-compensatory lengthening), syncopation is not limited to weak positions, but it should be so limited!!
        longv = re.compile('[AEIOU]') 
        shortening = {"A":"aə_", "E":"eə_", "I":"iə_", "O":"oə_", "U":"uə_"}
        for m in longv.finditer(latin[sylls[1]:sylls[-1]]):
            if irish[sylls[1]:sylls[-1]][m.start():m.end()] in shortening[m[0]]: values[-2].append(1)
            elif irish[sylls[1]:sylls[-1]][m.start():m.end()] == shortening[m[0]] or (irish[sylls[1]:sylls[-1]][m.start():m.end()] == "O" and m[0]=="A"): values[-2].append(0)
    parity = count_sylls.alt_w_fin_degen(sylls)
    #also need to allow for an extra syll at end in irish, check if any non-weak sylls are deleted
    #print(parity)
    if len(sylls) == 1: values = monosyllable_repair(latin, irish, values)
    if all([irish[sylls[i]] == "_"  for i in range(len(sylls)) if not parity[i]]) and not all(parity) and not any([irish[sylls[i]] == "_"  for i in range(len(sylls)) if parity[i]]): values[-1].append(1)
    elif all([irish[sylls[i]] == "_"  for i in range(len(sylls)-1) if not parity[i]]) and all(parity[-2:]) and irish[sylls[-1]] == "_" and re.match("[aeiouə]", irish[sylls[-1]+1:]): values[-1].append(1)
    elif len(sylls)>2: values[-1].append(0)
    #else: values.append([])
    return values

def monosyllable_repair(latin, irish, vector):
    nu = [x for x in vector]
    if nu[3]: nu[3] = [] #fixing apocope
    #fixing harmony
    #we have no way of knowing whether failure to harmonize was due to lack of environment or being too late. would need actual morphological class information
    if ('e' in latin and 'i' in irish) or ('i' in latin and 'e' in irish) or ('o' in latin and 'u' in irish) or ('u' in latin and 'o' in irish): nu[2] = [1] 
    elif ('e' in latin and 'e' in irish) or ('i' in latin and 'i' in irish) or ('o' in latin and 'o' in irish) or ('u' in latin and 'u' in irish): 
        print("was failure due to envi not met or was loan too late?")
        print(latin)
        print(irish)
    return nu

def date(*proc_v):
    h = [0,7]
    i = 0
    kill = False
    while i != len(proc_v) and not kill: #find first applying process
        if any(proc_v[i]):
            h[1] = i+1
            kill = True
        i += 1
    i = len(proc_v)-1
    kill = False
    while i >= 0 and not kill: #find last non-applying process
        if any([not x for x in proc_v[i]]): 
            h[0] = i+1
            kill = True
        i -= 1
    return h

def date_nu(end, *proc_v):
    h = [0,end] #should be 6 now that apocope doesn't get a bin
    i = 0
    kill = False
    meta = False
    print(proc_v)
    while i != len(proc_v) and not kill: #find first applying process/ante-relegalization
        #if 1 in proc_v[i] and 2 in proc_v[i]:
        #    h[1] = i
        if 2 in proc_v[i]: #ante-relegalization
            h[1] = i
            kill = True
            meta = True
        elif 1 in proc_v[i]:
            h[1] = i+1
            kill = True
        i += 1
    i = len(proc_v)-1
    kill = False
    while i >= 0 and not kill: #find last non-applying process/post-relegalization
        if 0 in proc_v[i]: 
            h[0] = i+1
            kill = True
        if 3 in proc_v[i]: #post-relegalization
            h[0] = i
            kill = True
        i -= 1
    if meta and h[0] == h[1]: h[1] += 1 #true interstice belongs to next bin
    return h

if __name__ == "__main__":
    #input is csv where: 
    #   column[0] is phonological latin stem, 
    #   column[1] is phonological irish form, 
    #   column[2] is orthographic latin word (don't worry about replacing macrons)
    #   column[3] is orthographic irish word (don't worry about replacing acute accents)
    data = read_in(sys.argv[1]) 
    #data = read_in("irish_latin_loans.csv")
    #stems = read_in("orthStem_ipaWord_ipaStem.csv")
    #hand = hackydata.data2
    hand = {}
    for x in hand_dates.align_crashes: hand[x] = hand_dates.align_crashes[x] 
    for x in hand_dates.inconsistent: hand[x] = hand_dates.inconsistent[x]
    print(hand)
    check = hand_dates.retranscribed_or_autodate_modded
    undone = []
    match  = []
    unmatch  = []
    autoed = []
    #i = 1
    for d in data:
        #print(i)
        #i += 1
        print(d)
        print((d[0], d[1]))
        latin, irish = clean_transcription(d[0]), clean_transcription(d[1])
        if latin[-1] in "aeiouAEIOU" and not irish[-1] in "aeiouAEIOUə": latin = latin[:-1] #hack to enact british apocope/loss of stem vowel in addition to replacement of infl by zero suffixes
        latin, irish = needleman.align(latin, irish, 0.5, needleman.read_similarity_matrix('simMatrix.txt'))
        #if not date(*check_procs(latin, irish))[0] < date(*check_procs(latin, irish))[1]:
        #    with open('date_inconsistency_nu.txt', 'a') as file_out:
        #        file_out.write(latin+'\n')
        #        file_out.write(irish+'\n')
        #        file_out.write(" ".join(['['+','.join([str(y) for y in x])+']' if x else '[_]' for x in check_procs(latin, irish)])+'\n')
        #        file_out.write(" ".join([str(x) for x in date(*check_procs(latin, irish))])+'\n')
        #        file_out.write('\n')
        if   (d[0], d[1]) in check: info = (
                length_mod(d[2]), 
                length_mod(d[3]), 
                date_nu(6, *sync_check(irish, count_sylls.count_syll(latin), count_sylls.alt_w_fin_degen(count_sylls.count_syll(latin)), procs_kludge(latin, irish, check_procs_nu(latin, irish, triggers, processes)))),
                check[(d[0], d[1])][:2],
                sync_check(irish, count_sylls.count_syll(latin), count_sylls.alt_w_fin_degen(count_sylls.count_syll(latin)), procs_kludge(latin, irish, check_procs_nu(latin, irish, triggers, processes))), 
                latin, 
                irish)
        if   (d[0], d[1]) in check and info[2] == info[3] and info not in match: match.append(info)
        elif (d[0], d[1]) in check and info[2] != info[3] and info not in unmatch: unmatch.append(info)
        elif (d[0], d[1]) not in hand: autoed.append((
            latin, 
            irish, 
            sync_check(irish, count_sylls.count_syll(latin), count_sylls.alt_w_fin_degen(count_sylls.count_syll(latin)), procs_kludge(latin, irish, check_procs_nu(latin, irish, triggers, processes))), 
            date_nu(6, *sync_check(irish, count_sylls.count_syll(latin), count_sylls.alt_w_fin_degen(count_sylls.count_syll(latin)), procs_kludge(latin, irish, check_procs_nu(latin, irish, triggers, processes)))), 
            length_mod(d[2]), 
            length_mod(d[3]))) 
        #if (length_mod(d[2]), length_mod(d[3])) in check: info = (length_mod(d[2]), length_mod(d[3]), date(*check_procs(latin, irish)),check[(length_mod(d[2]), length_mod(d[3]))][:2],check_procs(latin, irish), latin, irish)
        #if (length_mod(d[2]), length_mod(d[3])) in check and info[2] == info[3] and info not in match: match.append(info)
        #elif (length_mod(d[2]), length_mod(d[3])) in check and info[2] != info[3] and info not in unmatch: unmatch.append(info)
        #elif (length_mod(d[2]), length_mod(d[3])) not in hand: autoed.append((latin, irish, check_procs(latin, irish), date(*check_procs(latin, irish)), length_mod(d[2]), length_mod(d[3]))) 
        #else: undone.append((length_mod(d[2]), length_mod(d[3]), date(*check_procs(latin, irish)), check_procs(latin, irish), latin, irish))

    #for s in stems:
    #    #print(s)
    #    for d in data:
    #        if s[0] == d[3] and s[1] == d[4]:
    #            latin, irish = needleman.align(clean_transcription(s[2]), clean_transcription(d[1]), 1, needleman.read_similarity_matrix('simMatrix.txt'))
    #            if (length_mod(d[2]), length_mod(d[0])) in hand:
    #                info = (length_mod(d[2]), length_mod(d[0]), d[4], d[1], date(*check_procs(latin, irish)),hand[(length_mod(d[2]), length_mod(d[0]))][:2],check_procs(latin, irish), latin, irish)
    #            if (length_mod(d[2]), length_mod(d[0])) in hand and date(*check_procs(latin, irish)) == hand[(length_mod(d[2]), length_mod(d[0]))][:2] and info not in match: 
    #                match.append(info)
    #                #match.append((length_mod(d[2]), length_mod(d[0]), d[4], d[1], date(*check_procs(latin, irish)),check_procs(latin, irish), latin, irish))
    #            elif (length_mod(d[2]), length_mod(d[0])) in hand and date(*check_procs(latin, irish)) != hand[(length_mod(d[2]), length_mod(d[0]))][:2] and info not in unmatch: 
    #                unmatch.append(info)
    #                #unmatch.append((length_mod(d[2]), length_mod(d[0]), d[4], d[1], date(*check_procs(latin, irish)),hand[(length_mod(d[2]), length_mod(d[0]))][:2],check_procs(latin, irish), latin, irish))
    #            #beware uncommenting this: will crash on key errors due to _ being included in target span
    #            #elif (length_mod(d[2]), length_mod(d[0]),  date(*check_procs(latin, irish), latin, irish)) not in undone: undone.append((length_mod(d[2]), length_mod(d[0]),  date(*check_procs(latin, irish)),latin, irish))
    #print(len(match), len(unmatch))
    print("####################")
    print("####################")
    print("####################")
    print("AUTOED")
    print("####################")
    print("####################")
    print("####################")
    with open("autodate_hand_free_check.csv", 'w') as file_out:
        for a in autoed:
            file_out.write(a[0]+'\n')
            file_out.write(";".join([str(x) for x in a[1:]])+'\n')
    print("####################")
    print("####################")
    print("####################")
    print("UNMATCHED")
    print("####################")
    print("####################")
    print("####################")
    print(len(match), len(unmatch))
    for x in unmatch: 
        print(x[0], x[1])
        print(x[-2], "latin aligned")
        print(x[-1], "irish aligned")
        print( x[4])
        print("auto:", x[2])
        print("hand:", x[3])
        print("\n")
   # print("####################")
   # print("####################")
   # print("####################")
   # print("MATCHED")
   # print("####################")
   # print("####################")
   # print("####################")
   # for x in match:
   #     print(x[0], x[1])
   #     print(x[-2], "latin aligned")
   #     print(x[-1], "irish aligned")
   #     print( x[4])
   #     print("date:", x[2])
   #     print("\n")
   # print("####################")
   # print("####################")
   # print("####################")
   # print("NO HAND HYPOTHESIS")
   # print("####################")
   # print("####################")
   # print("####################")
   # for x in undone:
   #     print(x[0], x[1])
   #     print(x[-2], "latin aligned")
   #     print(x[-1], "irish aligned")
   #     print(x[4])
                    
                #print(latin, irish)
                #print(date(*check_procs(latin, irish)), check_procs(latin, irish), d, irish)
                #h.append(date(*check_procs(s[2], d[1]), 
