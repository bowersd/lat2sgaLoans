import re

minimal_bare = [
        '(?<!m)[Pp](?!t)', #p->k pre
        '(?<!m)[Pp](?=t)', #p->k post
        '((?<=[aeiouAEIOU])(t|k(?!s))(?![rlmn]))', #lenition pre
        '((?<=[aeiouAEIOU])(b|([dgm](?![rlmn]))))', #lenition post
        '(^[^AEIOUaeiou]*[eoiu])', #radically slimmed harmony
        '(([^AEIOUaeiou]*[AEIOUaeiou].*[AEIOUaeiou]))', #polysyllabicity
        '([aeiouAEIOU][tkdg][rlmn])', #compensatory lengthening --fine tune lenition!
        '(st)', #st pre-affection
        '((?<!n)f)', #f up to comp len (that's a bit much!)
        '(mp|ŋk|nt|n(s(?!t)|f)|(?<!^e)ks(?!t))', #syncope phonotactics
        ]

full_suite_bare = [
        '(?<!m)[Pp](?!t)', #p->k pre
        '(?<!m)[Pp](?=t)', #p->k post
        '((?<=[aeiouAEIOU])(t|k(?!s))(?![rlmn]))', #lenition pre
        '((?<=[aeiouAEIOU])(b|([dgm](?![rlmn]))))', #lenition post
        '((^[^AEIOUaeiou]*[eoiu][^AEIOUaeiou]*$)|(^([^AEIOUaeiou]*(((e|o)[^AEIOUaeiou]?[iuIU])|((i|u)[^AEIOUaeiou]*[aoAO])))))', #mono/multisyllable affection -> non-low short vowel in initial syll (followed by V with opposite value of [HIGH])  ... this could be sensitive to type of consonant in the raising specification ... no, because there isn't a hard and fast blocking condition
        '(([^AEIOUaeiou]*[AEIOUaeiou].*[AEIOU]))', #shortening (long vowels in non-initial syllables)
        '([aeiouAEIOU][tkdg][rlmn])', #compensatory lengthening --fine tune lenition!
        '([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou]*[AEIOUaieou])|([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOU][^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou][AEIOUaeiou])', #syncope up to 6 syllables... phonotactics version has only long vowels in second syll by mistake. need to fix that and re-run multiverse
        '(st)', #st pre-affection
        '((?<!n)f)', #f up to comp len (that's a bit much!)
        '(mp|ŋk|nt|n(s(?!t)|f)|(?<!^e)ks(?!t))', #syncope phonotactics
        ]

minimal = [
        re.compile('(?<!m)[Pp](?!t)'), #p->k pre
        re.compile('(?<!m)[Pp](?=t)'), #p->k post
        re.compile('((?<=[aeiouAEIOU])(t|k(?!s))(?![rlmn]))'), #lenition pre
        re.compile('((?<=[aeiouAEIOU])(b|([dgm](?![rlmn]))))'), #lenition post
        re.compile('(^[^AEIOUaeiou]*[eoiu])'), #radically slimmed harmony
        re.compile('([AEIOU])'), #radically slimmed shortening (long vowels anywhere)
        re.compile('([aeiouAEIOU][tkdg][rlmn])'), #compensatory lengthening --fine tune lenition!
        re.compile('([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou]*[AEIOUaieou])|([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOU][^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou][AEIOUaeiou])'), #syncope up to 6 syllables... phonotactics version has only long vowels in second syll by mistake. need to fix that and re-run multiverse
        re.compile('st'), #st pre-affection
        re.compile('(?<!n)f'), #f up to comp len (that's a bit much!)
        re.compile('(mp|ŋk|nt|n(s(?!t)|f)|(?<!^e)ks(?!t))'), #syncope phonotactics
        ]

middle = [
        re.compile('(?<!m)[Pp](?!t)'), #p->k pre
        re.compile('(?<!m)[Pp](?=t)'), #p->k post
        re.compile('((?<=[aeiouAEIOU])(t|k(?!s))(?![rlmn]))'), #lenition pre
        re.compile('((?<=[aeiouAEIOU])(b|([dgm](?![rlmn]))))'), #lenition post
        re.compile('((^[^AEIOUaeiou]*[eoiu][^AEIOUaeiou]*$)|(^([^AEIOUaeiou]*(((e|o)[^AEIOUaeiou]?[iuIU])|((i|u)[^AEIOUaeiou]*[aoAO])))))'), #mono/multisyllable affection -> non-low short vowel in initial syll (followed by V with opposite value of [HIGH])  ... this could be sensitive to type of consonant in the raising specification ... no, because there isn't a hard and fast blocking condition
        re.compile('(([^AEIOUaeiou]*[AEIOUaeiou].*[AEIOU]))'), #shortening (long vowels in non-initial syllables)
        re.compile('([aeiouAEIOU][tkdg][rlmn])'), #compensatory lengthening --fine tune lenition!
        re.compile('([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou]*[AEIOUaieou])|([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOU][^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou][AEIOUaeiou])'), #syncope up to 6 syllables... phonotactics version has only long vowels in second syll by mistake. need to fix that and re-run multiverse
        re.compile('st'), #st pre-affection
        re.compile('(?<!n)f'), #f up to comp len (that's a bit much!)
        re.compile('(mp|ŋk|nt|n(s(?!t)|f)|(?<!^e)ks(?!t))'), #syncope phonotactics
        ]

maximal = [
        re.compile('(?<!m)[Pp](?!t)'), #p->k pre
        re.compile('(?<!m)[Pp](?=t)'), #p->k post
        re.compile('((?<=[aeiouAEIOU])(t|k(?!s)))'), #lenition pre
        re.compile('((?<=[aeiouAEIOU])([bdgm]))'), #lenition post
        re.compile('((^[^AEIOUaeiou]*[eoiu][^AEIOUaeiou]*$)|(^([^AEIOUaeiou]*(((e|o)[^AEIOUaeiou]?[iuIU])|((i|u)[^AEIOUaeiou]*[aoAO])))))'), #mono/multisyllable affection -> non-low short vowel in initial syll (followed by V with opposite value of [HIGH])  ... this could be sensitive to type of consonant in the raising specification ... no, because there isn't a hard and fast blocking condition
        re.compile('(([^AEIOUaeiou]*[AEIOUaeiou].*[AEIOU]))'), #shortening (long vowels in non-initial syllables)
        re.compile('([aeiouAEIOU][tkdg][rlmn])'), #compensatory lengthening --fine tune lenition!
        re.compile('([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou]*[AEIOUaieou])|([^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOU][^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[aeiou][^AEIOUaeiou][AEIOUaeiou])'), #syncope up to 6 syllables... phonotactics version has only long vowels in second syll by mistake. need to fix that and re-run multiverse
        re.compile('st'), #st pre-affection
        re.compile('f'), #f up to comp len (that's a bit much!)
        re.compile('(mp|ŋk|nt|n(s|f)|(?<!^e)ks)'), #syncope phonotactics
        ]

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

