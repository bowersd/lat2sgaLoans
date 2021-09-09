import sys
import autodate
import needleman

def count(stop, *dates):
    h = []
    for i in range(stop): #starts
        for j in range(1, stop-i): #diffs
            cnt = 0
            for d in dates:
                if d[0] == i and d[1]-d[0] == j: 
                    cnt += 1
            h.append((i, j, cnt))
    return h

def divvy(bins, *spans):
    nu = [x for x in bins]
    for s in spans:
        for i in range(s[0], s[0]+s[1]): nu[i] += s[2]/s[1]
    return nu

if __name__ == "__main__":
    raw = autodate.read_in(sys.argv[1])
    dates = []
    #i = 1
    for r in raw:
        #print(i)
        #i += 1
        latin, irish = autodate.clean_transcription(r[0]), autodate.clean_transcription(r[1])
        if latin[-1] in "aeiouAEIOU" and not irish[-1] in "aeiouAEIOUə": latin = latin[:-1] #hack to enact british apocope/loss of stem vowel in addition to replacement of infl by zero suffixes
        latin_a, irish_a = needleman.align(latin, irish, 0.5, needleman.read_similarity_matrix('simMatrix.txt'))
        if (not any([0 in x and 1 in x for x in autodate.check_procs(latin_a, irish_a)])) and autodate.date(*autodate.check_procs(latin_a, irish_a))[0] < autodate.date(*autodate.check_procs(latin_a, irish_a))[1]: 
            dates.append(autodate.date(*autodate.check_procs(latin_a, irish_a)))
    print(divvy([0 for i in range(7)], *count(8, *dates)))
    c = count(8, *dates)
    for i in range(7):
        for t in c:
            if t[0] == i and t[1] == 1: print(i, t[2])

