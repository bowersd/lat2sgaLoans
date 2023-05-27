import re
import regexen as rxn

processes = [#what to look for in Latin
        re.compile('[Pp]'), #pk
        re.compile('((?<=[aeiouAEIOU])[tkdgbm])'), #lenition 
        re.compile('((^[^AEIOUaeiou]*[eoiu][^AEIOUaeiou]*$)|(^[^AEIOUaeiou]*(((e|o)[^AEIOUaeiou]?[iuIU])|((i|u)[^AEIOUaeiou]*[aoAO]))))'), #mono/multisyllable affection -> non-low short vowel in initial syll (followed by V with opposite value of [HIGH])  ... this could be sensitive to type of consonant in the raising specification ... no, because there isn't a hard and fast blocking condition
        re.compile('(([^AEIOUaeiou]*[AEIOUaeiou].*[AEIOU]))'), #shortening (long vowels in non-initial syllables)
        re.compile('([aeiouAEIOU][tkdg][rlmn])'), #compensatory lengthening
        re.compile('([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou]*[AEIOUaieou])|([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOU][^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou][AEIOUaeiou])'), #syncope up to 6 syllables... phonotactics version has only long vowels in second syll by mistake. need to fix that and re-run multiverse
        ]
phonotactics = [#what to look for in Latin
        re.compile('((?<!m)[Pp])'), #p, contextual carve-out to allow cluster detection
        re.compile('((?<=[aeiouAEIOU])(([tkdg](?![rlmn]))|[bm]))'), #lenition excluding compensatory lengthening 
        re.compile('((?<!n)[Ff])'), #f, contextual carve-out to allow cluster detection
        #re.compile('^[^AEIOUaeiou]*[eoiu][^AEIOUaeiou]*$'), #monosyllable affection -> non-low short vowel 
        re.compile('((st)|(^[^AEIOUaeiou]*[eoiu][^AEIOUaeiou]*$)|(^[^AEIOUaeiou]*(((e|o)[^AEIOUaeiou]?[iuIU])|((i|u)[^AEIOUaeiou]*[aoAO]))))'), #st and mono/multisyllable affection -> non-low short vowel in initial syll (followed by V with opposite value of [HIGH]) (weakly? correlated with trisyllables) ... this could be sensitive to type of consonant in the raising specification ... no, because there isn't a hard and fast blocking condition
        #re.compile('^[^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOUAEIOU][^AEIOUaeiou]*$'), #disyllables (not correlated with anything in Irish)
        re.compile('[^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOUAEIOU][^AEIOUaeiou]*[AEIOUaieou]'), #trisyllables or greater (syncope-adjacent)
        re.compile('(([^AEIOUaeiou]*[AEIOUaeiou].*[AEIOU])|([aeiouAEIOU][tkdg][rlmn]))'), #long vowels in non-initial syllables OR lengthening clusters (shortening/complen-adjacent, a bit correlated with trisyllables due to length overlap)
        #re.compile('[AEIOU]'), #long vowels (shortening/complen-adjacent)
        #re.compile('[aeiouAEIOU][tkdg][rlmn]'), #compensatory lengthening ... moved to the shortening/complen test (long vowels in non-initial syllables) before move this was like 4.5%, but it only boosted the bigger regex by about 2% ... highly correlated!
        re.compile('(mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks)'), #syncope+st phonotactics... st phonotactics are different temporally though...
        ]

phonotactics_interstitial = [#make sure the function for calculating interstitial probabilities is set up to handle list of 2 member tuples
        ("", re.compile('[Pp](?![tT])')), #-, before end of pk
        (re.compile('[Pp](?![tT])'), re.compile('([aeiouAEIOU](t|(k(?![Tt]))))')), #after end of pk, before end of lenition
        (re.compile('([aeiouAEIOU](d|g|b|m|t|(k(?![Tt]))))'), re.compile('(^[^AEIOUaeiou]*(((e|o)[^AEIOUaeiou]?[iuIU])|((i|u)[^AEIOUaeiou]*[aoAO])))')), #after end of lenition, before end of harmony. multisyllable only (include monosyllable too?)
        (re.compile('(^[^AEIOUaeiou]*(((e|o)[^AEIOUaeiou]?[iuIU])|((i|u)[^AEIOUaeiou]*[aoAO])))'), re.compile('[AEIOUaeiou].*[AEIOU]')), #after end of affection (limited to initial sylls, need to restrict to just the raising contexts where there could not have been blocking), before end of shortening/beginning of compensatory lengthening
        (re.compile('([aeiouAEIOU].*[AEIOU])'), re.compile('(([aeiouAEIOU][tkdg][rlmn])|(mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks))')), #after end of shortening/beginning of comp len, before end of comp len/beginning of syncope (juxtapositions)
        (re.compile('(([aeiouAEIOU][tkdg][rlmn])|(mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks))'), re.compile('([^AEIOUaeiou]*[AEIOUaieou]){3}')), #after end of comp len/beginning of syncope juxtapositions, before end of syncope (trisyllables or greater)
        ]

def calc_interstit_prior(procs, *data):
    h = []
    for p in procs:
        c = 0
        for d in data:
            if p.search(d): c += 1
        h.append(c/len(data))
    return h

def calc_prior(procs, *data):
    h = []
    for p in procs:
        c = 0
        for d in data:
            if p.search(d): c += 1
        h.append(c/len(data))
    return h

def hack_prior(filename):
    data = []
    with open(filename, 'r') as file_in:
        for l in file_in:
            if l and "UNKNOWN" not in l:
                data.append(l.strip())
    #x = calc_prior(rxn.full_suite, *data)
    #for i in range(len(rxn.full_suite)): print(x[i], rxn.full_suite[i])
    print(calc_prior(rxn.minimal, *data))

def overlap(bare_regexes, data):
    while bare_regexes:
        x = bare_regexes.pop()
        px = sum([1 if re.search(x, d) else 0 for d in data])/len(data)
        print(x)
        print(px)
        for y in bare_regexes:
            py = sum([1 if re.search(y, d) else 0 for d in data])/len(data)
            pxy = sum([1 if re.search("|".join([y, x]), d) else 0 for d in data])/len(data)
            intersection = -(pxy-py-px)
            expected = py*px
            print('\t', y)
            print('\t', py, pxy, intersection, expected)
            print('\t', intersection>expected, intersection<expected)
            

hacked_prior = [0.17822290703646637, 0.011299435028248588, 0.3682588597842835, 0.2824858757062147, 0.46070878274268107, 0.7447354904982023, 0.04519774011299435, 0.06266050333846944, 0.08371854134566, 0.15305598356445815] #minimal overlap
#hacked_prior = [0.17822290703646637, 0.011299435028248588, 0.3682588597842835, 0.2824858757062147, 0.1997945557267591, 0.3533641499743195, 0.04519774011299435, 0.3194658448895737, 0.06266050333846944, 0.08371854134566, 0.15305598356445815] #full suite
#hacked_prior = [0.18746789933230612, 0.5747303543913713, 0.08885464817668208, 0.25218284540318436, 0.1561376476630714, 0.37493579866461224, 0.12378017462763226]
#hacked_prior = [0.18746789933230612, 0.6122239342578326, 0.25218284540318436, 0.1561376476630714, 0.37493579866461224, 0.12378017462763226]
#hacked_prior = [0.2711864406779661, 0.5747303543913713, 0.1997945557267591, 0.1561376476630714, 0.37493579866461224, 0.17565485362095531]
#hacked_prior = [0.2567991631799163, 0.6244769874476988, 0.44142259414225943, 0.08002092050209204, 0.14905857740585773, 0.48169456066945604, 0.017259414225941423, 0.17468619246861924]

if __name__  == "__main__":
    #hack_prior("stemmed_latin_nouns_phon.txt")
    data = []
    with open("stemmed_latin_nouns_phon.txt") as file_in:
        for l in file_in:
            if l and "UNKNOWN" not in l:
                data.append(l.strip())
    overlap(rxn.minimal_bare, data)
    print('\n')
    overlap(rxn.full_suite_bare, data)


