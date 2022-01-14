from autodate import *
import sys
import needleman
import count_sylls
import hand_dates
import re

names = ["", "p→k", "lenition", "harmony", "shortening", "compensatory lengthening", "syncope", "MS"]

if __name__ == "__main__":
    #input is csv where: 
    #   column[0] is phonological latin stem, 
    #   column[1] is phonological irish form, 
    #   column[2] is orthographic latin word (don't worry about replacing macrons)
    #   column[3] is orthographic irish word (don't worry about replacing acute accents)
    data = read_in(sys.argv[1]) 
    hand = {}
    for x in hand_dates.align_crashes: hand[x] = hand_dates.align_crashes[x] 
    for x in hand_dates.inconsistent: hand[x] = hand_dates.inconsistent[x]
    h = {(i, j):0 for i in range(8) for j in range(8)}
    problems = []
    for d in data:
        latin, irish = clean_transcription(d[0]), clean_transcription(d[1])
        if latin[-1] in "aeiouAEIOU" and not irish[-1] in "aeiouAEIOUə": latin = latin[:-1] #hack to enact british apocope/loss of stem vowel in addition to replacement of infl by zero suffixes
        latin, irish = needleman.align(latin, irish, 0.5, needleman.read_similarity_matrix('simMatrix.txt'))
        if (d[0], d[1]) in hand : h[tuple(hand[(d[0], d[1])])] += 1
        else: 
            points = date_nu(7, *sync_check(irish, count_sylls.count_syll(latin), count_sylls.alt_w_fin_degen(count_sylls.count_syll(latin)), procs_kludge(latin, irish, check_procs_nu(latin, irish, triggers, processes))))
            h[tuple(points)] += 1
            if points[0] >= points[1]: problems.append((d[0], d[1], points))
            if points == [5, 6]: print("FIVE SIXER", d[0], d[1])
            if points == [3, 4]: print("THREE FOURER", d[0], d[1])
    for x in h:
        #if x[1]-x[0]==1: print(x, h[x])
        if x[0]<x[1]: print(x, h[x])
        elif h[x]: print(x, h[x], "SOMETHING IS WRONG")
    #for p in problems: print(p)
    mn = [0 for i in range(8)]
    tot = sum([h[x] for x in h])
    eq = [0 for i in range(8)]
    for x in h:
        for j in range(x[1]-x[0]):
            eq[x[0]+j] += h[x]/(x[1]-x[0])
    holder = [
            ("period", "name", "minimum", "maximum", "naive"),
            ("0","", "0", "0", "0"),
            ]
    prev = 0
    for i in range(8):
        mx = 0
        for x in h:
            if x[1] == i: mn[i] += h[x]
            if x[0] > i: mx += h[x]
        #print(i, sum(mn[:i+1]), tot-prev, sum(eq[:i]))
        if i > 0: holder.append((str(i), names[i], str(sum(mn[:i+1])), str(tot-prev), str(sum(eq[:i]))))
        prev = mx
    with open("core_data.csv", 'w') as file_out:
        for x in holder: 
            print(x)
            file_out.write(",".join(x)+'\n')
