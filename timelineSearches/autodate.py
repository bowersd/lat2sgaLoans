import needleman
import count_sylls
import subprocess
import hand_dates
#import latin_loans_prototype_dataset
#subprocess.call(*args)
import re
import sys


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
    #convert length marking to single characters
    #remove palatalization, suprasegmentals and "/"
    #NB: prefixes will mess up stress computation
    h = []
    i = len(string)-1
    while i > -1:
        if string[i] == ":":
            h.append(string[i-1].upper())
            i -= 2
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
        if h[i:j][0] == h[i:j][1] and h[i] not in "aeiouAEIOUə":
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
        re.compile('((?<=[aeiouAEIOU])_*[tkbdgm])'), #lenition (f>s in, st>s removed due to post-lenition strata>strait) WHAT ABOUT LONG [f:]??
        re.compile('(((e|o)(?=_*[^AEIOUaeiou]*_*[iuIU]))|((i|u)(?=[^AEIOUaeiou]*[aoAO])))'), #affection ... just identifying all possible targets and letting process ID weed out the rest (non-initial syllables will be @ in Irish). ideally would also check morph class information on monosylables.
        #re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), #apocope
        re.compile('((?<=[aeiouAEIOU])_*[dgtk][rlnm])|f'), #compensatory lengthening (shortening handled in procs_kludge() to avoid lookbehind limits)
        re.compile('(mp|ŋk|n(t|s|f))|((?<!^e)ks)'), #syncope (phonotactics here, V deletion handled below) mp has different pre-history (we don't know when it vanished/what was the outcome), but part of natural class and made legal by syncope
        ]
processes = [ #slightly refined regexen to apply to latin, paired with dicts to check if the rule applied or not. these need to be alignment-proof (overlook _)
        ((re.compile('[Pp](?!_*t)'), {"p":"kxɣ", "P":"kxɣ"},1),(re.compile('[Pp]'), {"P":"pb","p":"pb"}, 0)),
        ((re.compile('((?<=[aeiouAEIOU])_*[t]|(k)(?![Tt]))'), { "t":"θð", "k":"xɣ"},1), (re.compile('((?<=[aeiouAEIOU])_*(t|k|b|d|g|m))'), {"t":"td", "k":"kg", "b":"b", "d":"d", "g":"g", "m":"m", "f":"f"},0)),
        ((re.compile('(((e|o)(?=_*[^AEIOUaeiou]*_*[iuIU]))|((i|u)(?=[^AEIOUaeiou]*[aoAO])))'),{"e":"i", "o":"u", "i":"e", "u":"o", },1),(re.compile('(((e|o)(?=_*([bdgmnrlBDGMNRL]|(nd|mb|ml|mr|db|dr|gl|Dr|Gl))_*[iuIU]))|((i|u)(?=[^AEIOUaeiou]*[aoAO])))'), {"i":"i", "e":"e", "u":"u", "o":"o", },0)), #just dropping the string-initial requirement and relying on @ in Irish to rule out non-initial sylls ... allowing [k] as a permitter is a problem. if lenited it could block. it is only if unlenited that it permitted (apparently) --- EJFL: If you say so. I don't remember anything about this.
        #((re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), {"A":"aə", "E":"eə", "I":"iə", "O":"oə", "U":"uə"}),(re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), {"A":"AO", "E":"E", "I":"I", "O":"O", "U":"U"})), #apocope
        ((re.compile('((?<=[aeiouAEIOU])_*[dgtk][rlnm])|f'), {"dr":"_r", "dl":"_l", "dn":"_n", "dm":"_m","gr":"_r", "gl":"_l", "gn":"_n", "gm":"_m","tr":"_r", "tl":"_l", "tn":"_n", "tm":"_m","kr":"_r", "kl":"_l", "kn":"_n", "km":"_m", "f":"s"},1), (re.compile('(?<=[aeiouAEIOU])_*[dgtk][rlnm]'), {"dr":"drðr", "dl":"dlðl", "dn":"dnðn", "dm":"dmðm","gr":"grɣr", "gl":"glɣl", "gn":"gnɣn", "gm":"gmɣm","tr":"trθr", "tl":"tlθl", "tn":"tnθn", "tm":"tmθm","kr":"krxr", "kl":"klxl", "kn":"knxn", "km":"kmxm"},0)), #compensatory lengthening (shortening handled in procs_kludge() to avoid lookbehind limits) Is there data on failure to lengthen??

        ((re.compile('(mp|ŋk|nt|nf)'),{"mp":"mb", "ŋk":"ŋg", "nt":"nd", "nf":"_v"},2),(re.compile('(n(s|f))|((?<!^e)ks)'),{"ns":"ns", "nf":"nf","ks":"xsks"},3)), #syncope (phonotactics here, V deletion handled below)
        #((re.compile('(mp|ŋk|n(t(?!$)|f))|((?<!^e)ks)'),{"mp":"mb", "ŋk":"ŋg", "nt":"nd", "nf":"_v", "ks":"_s"},2),(re.compile('(mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks)'),{"mp":"mp", "ŋk":"ŋk", "nt":"nt", "ns":"ns", "nf":"nf","ks":"xsks"},3)), #syncope (phonotactics here, V deletion handled below)
        ]

def check_procs_nu(latin, irish, triggers, processes):
    values = []
    for i in range(len(triggers)):
        pvals = []
        if triggers[i].search(latin): 
            for x in processes[i][0][0].finditer(latin):
                if irish[x.start():x.end()] in processes[i][0][1][x.group()]:pvals.append((x.span(), processes[i][0][2]))
            for x in processes[i][1][0].finditer(latin):
                if irish[x.start():x.end()] in processes[i][1][1][x.group()]:pvals.append((x.span(), processes[i][1][2]))
        values.append([x[1] for x in sorted(pvals)])
    return values

def procs_kludge(latin, irish, values):
    values = values[:3]+[[]]+values[3:] #adding a gap between harmony and compensatory lengthening
    #if any([irish[x.start():x.end()] == "f" for x in re.finditer("f", latin)]): values[1].append(3) #lenition legalized f ... best to just treat lenition as a point, so use 0/1 coding (in processes)
    if any([irish[x.start():x.end()] == "s_" for x in re.finditer("st", latin)]): values[2].append(1) #st>s happened in strata>srait (a post-lenition loan) and so diagnoses pre-affection (this is latest datable occurrence of st>s)
    if values[2] == [0] and latin[re.search('[aeiouAEIOU]', latin).start()] in 'eo' and irish[re.search('[aeiouAEIOU]', irish).start()+1] in 'xɣ': values[2] = [] #failure to raise across 'x' is not diagnostic of affection failure
    if latin[-1] in "Ii" and irish[-1] == "e": values[2].append(1) #detecting lowering of Latin /i/ by /-a.../. Are we sure that there wasn't a post-affection suffix -e that just replaced the Latin /i/ directly? -> may need a failure watch as in monosyllable_repair() EJFL: It seems more complicated to assume morphological replacement in all cases than that lowering affects medial i causing it to become -e; the phonology is totally regular.
    #DAB: the question isn't whether we assume morphological replacement in all cases, but whether a potential phonological criterion is truly criterial. We should not count something as showing a phonological process if it may be the result of morphology. ---- EJFL: Yes, but I already excluded the possible cases where -e can be morphological. For example, felsube 'philosophy' could have been borrowed from Latin with i > e by harmony, but since -e is an suffix in Irish that creates abstract nouns, I excluded it since we have felsub from philosophus. To the best of my knowledge, all remaining cases of i > e cannot possibily be analyzed as containing a real meaningful Irish suffix.
    #if latin[-1] in "Ii" and irish[-1] in "Ii":  #isolating examples where there might have been harmony or application of a suffix. this was uncommented at the time that we ran the simulations for Bowers and Lash 2024, though the comments immediately above show that it was no longer a relevant check to run.
    #    print("was failure due to envi not met or was loan too late?")
    #    print(latin)
    #    print(irish)
    sylls = count_sylls.count_syll(latin)
    if len(sylls) == 1: values = monosyllable_repair(latin, irish, values)
    #if len(sylls) > 1 and latin[sylls[-1]] in "Uu" and irish[sylls[-1]] == "ə": values[2].append(1) #detecting lowering>reduction of /u/ in stem-final syllables #this did not end up yielding good data, and was commented out
    #if len(sylls) > 1 and latin[sylls[-1]] in "Uu" and irish[sylls[-1]] in "Uu": 
    #    print("was failure due to envi not met or was loan too late?")
    #    print(latin)
    #    print(irish)
    if len(sylls) > 1: #detecting shortening of post-initial syllables (diagnoses pre/post-BEGINNING of compensatory lengthening), syncopation is not limited to weak positions, but it should be so limited!!
        longv = re.compile('[AEIOU]') 
        shortening = {"A":"aə_", "E":"eə_", "I":"iə_", "O":"oə_", "U":"uə_"} #outputs not over broad, because reduction didn't target word final open sylls IIRC
        for m in longv.finditer(latin[sylls[1]:]):
            if irish[sylls[1]:][m.start():m.end()] in shortening[m[0]]: values[-2].append(2)
            elif irish[sylls[1]:][m.start():m.end()] == m[0] or (irish[sylls[1]:][m.start():m.end()] == "O" and m[0]=="A"): values[-2].append(3)
    return values

def sync_check(irish, sylls, parity, values):
    if all([irish[sylls[i]] == "_"  for i in range(len(sylls)) if not parity[i]]) and not all(parity) and not any([irish[sylls[i]] == "_"  for i in range(len(sylls)) if parity[i]]): values[-1].append(1)
    elif all([irish[sylls[i]] == "_"  for i in range(len(sylls)-1) if not parity[i]]) and all(parity[-2:]) and irish[sylls[-1]] == "_" and re.match("[aeiouə]", irish[sylls[-1]+1:]): values[-1].append(1)
    elif len(sylls)>2: values[-1].append(0)
    return values

def monosyllable_repair(latin, irish, vector):
    nu = [x for x in vector]
    #if nu[3]: nu[3] = [] #fixing apocope
    #looking for possible harmony in monosyllabic stems
    #we have no way of knowing whether failure to harmonize was due to lack of environment or being too late. would need actual morphological class information, see discussion in procs_kludge()
    if ('e' in latin and irish[latin.index('e')] == 'i') or ('i' in latin and irish[latin.index('i')] == 'e') or ('o' in latin and irish[latin.index('o')] == 'u') or ('u' in latin and irish[latin.index('u')] == 'o'): nu[2] = [1] 
    #elif ('e' in latin and irish[latin.index('e')] == 'e') or ('i' in latin and irish[latin.index('i')] == 'i') or ('o' in latin and irish[latin.index('o')] == 'o') or ('u' in latin and irish[latin.index('u')] == 'u'): #this check no longer needed to be performed, though, uncomment if you want to see these forms and judge for yourself
    #    print("was failure due to envi not met or was loan too late?")
    #    print(latin)
    #    print(irish)
    return nu

def date_nu(end, *proc_v):
    h = [0,end] #should be 7 since there's a space between harmony and compensatory lengthening
    i = 0
    kill = False
    meta = False
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
        elif 3 in proc_v[i]: #post-relegalization
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
    #hand = latin_loans_prototype_dataset.data2
    hand = {}
    for x in hand_dates.align_crashes: hand[x] = hand_dates.align_crashes[x] 
    for x in hand_dates.inconsistent: hand[x] = hand_dates.inconsistent[x]
    check = hand_dates.retranscribed_or_autodate_modded
    undone = []
    match  = []
    unmatch  = []
    autoed = []
    for d in data:
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
                date_nu(7, *sync_check(irish, count_sylls.count_syll(latin), count_sylls.alt_w_fin_degen(count_sylls.count_syll(latin)), procs_kludge(latin, irish, check_procs_nu(latin, irish, triggers, processes)))),
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
            date_nu(7, *sync_check(irish, count_sylls.count_syll(latin), count_sylls.alt_w_fin_degen(count_sylls.count_syll(latin)), procs_kludge(latin, irish, check_procs_nu(latin, irish, triggers, processes)))), 
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
