import needleman
import count_sylls
import subprocess
import hackydata
#subprocess.call(*args)
import re
import sys

#todo: syncope clusters
#todo: g->G
#todo: ks>s
#todo: raising blocked by x
#todo: u-affection (a->u) p 138 Mccone, cf hock 2019?
#todo: f>f non-diagnostic
#todo: make sure to prevent voice neutralization in stops
#align the latin root with the irish word and pass the pair to check_procs()
#aligned = needleman.align(latin, irish, 1, needleman.read_similarity_matrix("simMatrix.txt")) #don't like calls to something outside of fun definition

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
    #prefixes will mess up stress computation
    #print(string)
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

def check_procs(latin, irish):
    values = []
    triggers = [#what to look for in Latin
            re.compile('[Pp]'), #pk
            re.compile('((?<=[aeiouAEIOU])_*[tkbdgms])|f|st'), #lenition
            ##re.compile('(?<=^[^aeiouAEIOU]{0,3})(((e|o)(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))'), #affection ... o->u can be detected in non-initial sylls. also need class information on monosyllabic roots (-> need root analysis here) maybe just flag monosyllables
            #re.compile('(?<=^[^aeiouAEIOU])_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))'), #affection ... o->u can be detected in non-initial sylls. also need class information on monosyllabic roots (-> need root analysis here) maybe just flag monosyllables
            re.compile('(((e|o)(?=_*[^AEIOUaeiou]?_*[iuIU]))|((i|u)(?=[^AEIOUaeiou]*[aoAO])))'), #affection ... just identifying all possible targets and letting process ID weed out the rest (non-initial syllables will be @ in Irish)
            #re.compile('('+
            #'_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #'(?<=^[^aeiouAEIOU])_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #'(?<=^[^aeiouAEIOU]{2})_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #'(?<=^[^aeiouAEIOU]{3})_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #    ')'), #affection ... o->u can be detected in non-initial sylls. also need class information on monosyllabic roots (-> need root analysis here) maybe just flag monosyllables
            re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), #apocope-apply to root!
            #re.compile('(([aeiou](?=[dg][^aeiouAEIOU]))|((?<=[aeiouAEIOU][^aeiouAEIOU]{0,3})[AEIOU](?=.*[AEIOUaeiou])))'), #compensatory lengthening
            #re.compile('(([aeiou]_*(?=[dg][^aeiouAEIOU]))|((?<=[aeiouAEIOU][^aeiouAEIOU])_*[AEIOU](?=.*[AEIOUaeiou])))'), #compensatory lengthening ... this doesn't truly capture non-initial sylls, just non-initial sylls not preceded by clusters
            re.compile('[aeiou]_*(?=[dg][^aeiouAEIOU])'), #compensatory lengthening
            ]
    processes = [ #slightly refined regexen to apply to latin, paired with dicts to check if the rule applied or not. these need to be alignment-proof (overlook _)
            ((re.compile('[Pp](?!_*t)'), {"p":"kxɣ", "P":"kxɣ"}),(re.compile('[Pp]'), {"P":"pb","p":"pb"})),
            ((re.compile('((?<=[aeiouAEIOU])_*[tgm]|(s|k)(?![Tt]))|f|st'), { "t":"θð", "k":"xɣ",  "m":"ɱ", "s":"h", "f":"s", "st":"s_"}), (re.compile('((?<=[aeiouAEIOU])_*(t|k|b|d|g|m|s(?![ptk])))|f'), {"t":"td", "k":"kg", "b":"b", "d":"d", "g":"g", "m":"m", "s":"s", })),
            ##((re.compile('(?<=^[^aeiouAEIOU]{0,3})(((e|o)(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))'),{"e":"i", "o":"u", "i":"e", "u":"o"}),(re.compile('(?<=^[^aeiouAEIOU]{0,3})(((e|o)(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))'), {"i":"i", "e":"e", "u":"u", "o":"o"})),
            #((re.compile('(?<=^[^aeiouAEIOU])(((e|o)(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))'),{"e":"i", "o":"u", "i":"e", "u":"o"}),(re.compile('(?<=^[^aeiouAEIOU])(((e|o)(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))'), {"i":"i", "e":"e", "u":"u", "o":"o"})),
            ((re.compile('(((e|o)(?=_*[^AEIOUaeioux]?_*[iuIU]))|((i|u)(?=[^AEIOUaeiou]*[aoAO])))'),{"e":"i", "o":"u", "i":"e", "u":"o"}),(re.compile('(((e|o)(?=_*[^AEIOUaeioux]?_*[iuIU]))|((i|u)(?=[^AEIOUaeiou]*[aoAO])))'), {"i":"i", "e":"e", "u":"u", "o":"o"})), #just dropping the string-initial requirement and relying on @ in Irish to rule out non-initial sylls
            #(
            #    (
            #        re.compile(
            #            '('+
            #            '_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #            '(?<=^[^aeiouAEIOU])_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #            '(?<=^[^aeiouAEIOU]{2})_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #            '(?<=^[^aeiouAEIOU]{3})_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+ ')'), 
            #        {"e":"i", "o":"u", "i":"e", "u":"o"}
            #        ),
            #    (
            #        re.compile(
            #            '('+ 
            #            '_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #            '(?<=^[^aeiouAEIOU])_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #            '(?<=^[^aeiouAEIOU]{2})_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #            '(?<=^[^aeiouAEIOU]{3})_*(((e|o)_*(?=[^AEIOUaeiou]?[iu]))|((i|u)(?=[^AEIOUaeiou]*[ao])))|'+
            #            ')'), 
            #        {"i":"i", "e":"e", "u":"u", "o":"o"}
            #        )
            #    ),
            ((re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), {"A":"aə", "E":"eə", "I":"iə", "O":"oə", "U":"uə"}),(re.compile('[AEIOU](?=[^aeiouAEIOU]*$)'), {"A":"AO", "E":"E", "I":"I", "O":"O", "U":"U"})), #apocope-apply to root!
            #((re.compile('(([aeiou](?=[dg][^aeiouAEIOU]))|((?<=[aeiouAEIOU][^aeiouAEIOU]{0,3})[AEIOU](?=.*[AEIOUaeiou])))'), {"a":"A", "e":"E", "i":"I", "o":"O", "u":"U", "A":"a@", "E":"e@", "I":"i@", "O":"o@", "U":"u@"}), (re.compile('(([aeiou](?=[dg][^aeiouAEIOU]))|((?<=[aeiouAEIOU][^aeiouAEIOU]{0,3})[AEIOU](?=.*[AEIOUaeiou])))'), {"a":"a@", "e":"e@", "i":"i@", "o":"o@", "u":"u@", "A":"A", "E":"E", "I":"I", "O":"O", "U":"U"})) #compensatory lengthening
            #((re.compile('(([aeiou]_*(?=[dg][^aeiouAEIOU]))|((?<=[aeiouAEIOU][^aeiouAEIOU])_*[AEIOU](?=.*[AEIOUaeiou])))'), {"a":"A", "e":"E", "i":"I", "o":"O", "u":"U", "A":"aə", "E":"eə", "I":"iə", "O":"oə", "U":"uə"}), (re.compile('(([aeiou]_*(?=[dg][^aeiouAEIOU]))|((?<=[aeiouAEIOU][^aeiouAEIOU])_*[AEIOU](?=.*[AEIOUaeiou])))'), {"a":"a", "e":"e", "i":"i", "o":"o", "u":"u", "A":"AO", "E":"E", "I":"I", "O":"O", "U":"U"})) #compensatory lengthening
            ((re.compile('[aeiou]_*(?=[dg][^aeiouAEIOU])'), {"a":"A", "e":"E", "i":"I", "o":"O", "u":"U"}), (re.compile('[aeiou]_*(?=[dg][^aeiouAEIOU])'), {"a":"a", "e":"e", "i":"i", "o":"o", "u":"u"})) #compensatory lengthening
            ]
    for i in range(len(triggers)):
        #print(i)
        pvals = []
        if triggers[i].search(latin): #may need to be lroot in some cases ... 
            #print(i)
            for x in processes[i][0][0].finditer(latin):
                #print(latin, irish, x.span(), processes[i][0][0])
                if irish[x.start():x.end()] in processes[i][0][1][x.group()]:pvals.append((x.span(), 1))
            for x in processes[i][1][0].finditer(latin):
                if irish[x.start():x.end()] in processes[i][1][1][x.group()]:pvals.append((x.span(), 0))
        #else: pvals.append(("?", ""))
        #print(pvals)
        values.append([x[1] for x in sorted(pvals)])
    sylls = count_sylls.count_syll(latin)
    #print(sylls)
    if len(sylls) > 2: #detecting shortening of stem-internal syllables (diagnoses pre/post-compensatory lengthening)
        longv = re.compile('[AEIOU]') 
        shortening = {"A":"aə_", "E":"eə_", "I":"iə_", "O":"oə_", "U":"uə_"}
        for m in longv.finditer(latin[sylls[1]:sylls[-1]]):
            if irish[sylls[1]:sylls[-1]][m.start():m.end()] in shortening[m[0]]: values[-1].append(1)
            elif irish[sylls[1]:sylls[-1]][m.start():m.end()] == shortening[m[0]] or (irish[sylls[1]:sylls[-1]][m.start():m.end()] == "O" and m[0]=="A"): values[-1].append(0)
    parity = count_sylls.alt_w_fin_degen(sylls)
    #also need to allow for an extra syll at end in irish, check if any non-weak sylls are deleted
    #print(parity)
    if len(sylls) == 1: values = monosyllable_repair(latin, irish, values)
    if all([irish[sylls[i]] == "_"  for i in range(len(sylls)) if not parity[i]]) and not all(parity) and not any([irish[sylls[i]] == "_"  for i in range(len(sylls)) if parity[i]]): values.append([1])
    elif all([irish[sylls[i]] == "_"  for i in range(len(sylls)-1) if not parity[i]]) and all(parity[-2:]) and irish[sylls[-1]] == "_" and re.match("[aeiouə]", irish[sylls[-1]+1:]): values.append([1])
    elif len(sylls)>2: values.append([0])
    else: values.append([])
    return values

def monosyllable_repair(latin, irish, vector):
    nu = [x for x in vector]
    if nu[3]: nu[3] = [] #fixing apocope
    #fixing harmony
    #we have no way of knowing whether failure to harmonize was due to lack of environment or being too late. would need actual morphological class information
    if ('e' in latin and 'i' in irish) or ('i' in latin and 'e' in irish) or ('o' in latin and 'u' in irish) or ('u' in latin and 'o' in irish): nu[2] = [1] 
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

if __name__ == "__main__":
    #input is csv where: 
    #   column[0] is phonological latin stem, 
    #   column[1] is phonological irish form, 
    #   column[2] is orthographic latin word (don't worry about replacing macrons)
    #   column[3] is orthographic irish word (don't worry about replacing acute accents)
    data = read_in(sys.argv[1]) 
    #data = read_in("irish_latin_loans.csv")
    #stems = read_in("orthStem_ipaWord_ipaStem.csv")
    hand = hackydata.data2
    undone = []
    match  = []
    unmatch  = []
    for d in data:
        latin, irish = clean_transcription(d[0]), clean_transcription(d[1])
        if latin[-1] in "aeiouAEIOU" and not irish[-1] in "aeiouAEIOUə": latin = latin[:-1] #working around british apocope/loss of stem vowel in addition to replacement of infl by zero suffixes
        latin, irish = needleman.align(latin, irish, 0.5, needleman.read_similarity_matrix('simMatrix.txt'))
        if (length_mod(d[2]), length_mod(d[3])) in hand: 
            info = (length_mod(d[2]), length_mod(d[3]), date(*check_procs(latin, irish)),hand[(length_mod(d[2]), length_mod(d[3]))][:2],check_procs(latin, irish), latin, irish)
        if (length_mod(d[2]), length_mod(d[3])) in hand and info[2] == info[3] and info not in match: match.append(info)
        elif (length_mod(d[2]), length_mod(d[3])) in hand and info[2] != info[3] and info not in unmatch: unmatch.append(info)
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
