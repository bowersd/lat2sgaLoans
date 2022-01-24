##todo: the best 15 probability log isn't working right (0 stays at top)...
import sys
import math
import random #too many combinations to calculate exactly. original used itertools.product()
import operator
from functools import reduce
import re
from scipy.stats import chi2
import autodate
import needleman
import hand_dates
import count_sylls
#from hackydata import *

#[x, y...] #FORMS
#[(start, stop), (start, stop)...] #eligible DATES
#[(p1, p2, p3, p4, p5, p6, p7), ...] #eligible PROCesseS:pk, lenition, shortening, harmony, apocope?, lengthening?, syncope, NC, Ks
#(pct1, pct2, pct3 ... pct7) #q: proportion of corpus that can undergo processes ... may need a couple for Latin, loans corpora 

def span(start, stop):
    n = start
    while n != stop:
        yield n
        n += 1

def kullbackleibler(p,q): return sum([p[i]*math.log2(p[i]/q[i]) for i in range(len(p))])

def binomial(n, N, p): return (math.factorial(N)/(math.factorial(n)*math.factorial(N-n)))*(p**n)*((1-p)**(N-n))#successes, trials, probability of success

def product(*args): return reduce(operator.mul, [a for a in args], 1)

def mean(*ns): return sum(ns)/len(ns)

def stdev(*ns): return math.sqrt(mean(*[(ns[x]-mean(*ns)**2) for x in ns])) #not performing bessel's correction (decrease denom by 1) since we have a complete sample

def hamming(v1, v2):
    c = 0
    for i in range(len(v1)):
        if v1[i] != v2[i]: c += 1
    return c

def readin(filename):
    h = []
    with open(filename) as file_in:
        for l in file_in:
            h.append(",".split(l.strip()))
    return h

def tally_procs(regexen, *forms):
    procs = [[0 for i in range(len(regexen))] for j in range(len(forms))]
    for i in range(len(forms)):
        for j in range(len(regexen)):
            if regexen[j].search(forms[i]): 
                procs[i][j] = 1
    return procs

def naive(top, *date_ranges):
    h = [0 for i in range(top)]
    for d in date_ranges:
        for i in range(d[1]-d[0]): h[d[0]+i] += 1/(d[1]-d[0])
    return h

def chi_squared_pdf(observed, expected):
    #exact (not cumulative as in standard chi2 test) probability that observed was drawn from expected
    #commented line below uses iid expected distribution and laplace smoothing, could use the naive distribution
    #p *= chi2.pdf(sum([(((x+1)-((sum(sum_bins)+len(sum_bins))/len(sum_bins)))**2)/((sum(sum_bins)+len(sum_bins))/len(sum_bins)) for x in sum_bins]), len(sum_bins)-1)
    chsq = 0
    for i in range(len(observed)): chsq += ((observed[i]-expected[i])**2)/expected[i]
    return chi2.pdf(chsq, len(observed)-1)

def assess_phonotactic_prob(sum_bins, prop_bins, prior_rates):
    p = 1
    for j in range(len(sum_bins)):
        binomial_results = []
        for k in range(len(prop_bins[j])): 
            binomial_results.append(binomial(prop_bins[j][k], sum_bins[j], prior_rates[k]))
        #print("processes {0}".format(prop_bins[j]))
        #print("sum_bins:{0}".format(j))
        #print(product(*binomial_results))
        p *= product(*binomial_results)
        #p *= (sum_bins[j]+1)/(sum(sum_bins)+len(sum_bins))
    return p

def top_rank(candidate, tops):
    j = len(tops)-1
    while candidate>tops[j]: 
        if candidate<=tops[j-1] or j == 0: return j
        j -= 1

def recombine(num_offspring, cands):
    h = []
    while cands:
        x = cands.pop()
        for y in cands:
            for i in range(num_offspring):
                nu = []
                for j in range(len(x)):
                    if x[j] != y[j] and random.randrange(0,2) == 0: nu.append(y[j])
                    else: nu.append(x[j])
                h.append(nu)
    return h

def recombine_aux(procs, slot_cnt, *offspring):
    time_containers = [[x.count(j) for j in range(slot_cnt)] for x in offspring]
    proc_containers = [[[0 for j in range(len(procs[0]))] for k in range(slot_cnt)] for x in offspring]
    for i in range(len(offspring)):
        for j in range(len(offspring[i])): proc_containers[i][offspring[i][j]] = list(map(operator.add, procs[j], proc_containers[i][offspring[i][j]]))
    return (time_containers, proc_containers)


def genetic_search(rates, slot_cnt, procs, nallocation, *dates):
    ##initialization
    verses = [[d[0] for d in dates]] #date samples, initialized to earliest possible entry for all words
    top_probs = [-20 for i in range(100)] #probabilities of verses
    time_bins = [] #how many words in each time slot by verse
    distributions = [] #how many words in each time slot match phonotactics of interest
    changeable = [j  for j in range(len(dates)) if dates[j][1]-dates[j][0] > 1]
    rnd = 1
    lst_update = 1
    lst_mutate = 1
    mutated = True
    mut_rt = 0.05
    while rnd < 121: 
        #print(rnd)
    #while rnd < 121 and (sum(top_probs) == 0 or any([x != y for x in top_probs for y in top_probs])): #pool can be split but unchangeable, so this is not a good convergence detection
        nu_gen = recombine(20, [x for x in verses])
        nu_gen_vit_stats = recombine_aux(procs, slot_cnt, *nu_gen)
        for i in range(len(nu_gen)):
            p = assess_phonotactic_prob(nu_gen_vit_stats[0][i], nu_gen_vit_stats[1][i], rates)
            #p *= chi_squared_pdf(nu_gen_vit_stats[0][i], nallocation)
            #p = assess_phonotactic_prob(nu_gen_vit_stats[0][i], nu_gen_vit_stats[1][i], rates)-(kullbackleibler([(x+1)/(sum(nu_gen[i])+7) for x in nu_gen[i]], [1/len(nu_gen[i]) for x in nu_gen[i]]))
            if any([p>x for x in top_probs]) and nu_gen[i] not in verses: #update pool
                loc = top_rank(p, top_probs)
                #if len(verses)<100: print("RECOMBIN  overturns {1} (p:{0}, rnd:{2})".format(p, loc, rnd))
                #if len(verses)>=100: print("RECOMBIN  overturns {1} (p:{0}, rnd:{2}, ham:{3})".format(p, loc, rnd, hamming(nu_gen[i], verses[loc])))
                lst_update = rnd
                #print("RECOMBIN  overturns {1} (p:{0}, rnd:{2})".format(p, loc, rnd))
                top_probs =      top_probs[:loc]+[p]+top_probs[loc:-1]
                time_bins =      time_bins[:loc]+[nu_gen_vit_stats[0][i]]+time_bins[loc:-1]
                verses =         verses[:loc]+[nu_gen[i]]+verses[loc:-1]
                distributions =  distributions[:loc]+[nu_gen_vit_stats[1][i]]+distributions[loc:-1]
        nu_verses       = [x for x in verses       ]
        nu_top_probs    = [x for x in top_probs    ]
        nu_time_bins    = [x for x in time_bins    ]
        nu_distributions= [x for x in distributions]
        if not mutated and mut_rt > 0.0: mut_rt -= 0.001
        mutated = False
        for v in verses:
            for i in range(1000):
                cnts = [0 for j in range(slot_cnt)] #0 for however many time slots there are
                s = [] #tracking individual slot placements
                bin_procs = [[0 for j in range(len(procs[0]))] for k in range(len(cnts))] #how many instances of proc are in each bin (for prob calc)
                #change = random.sample(changeable, len(changeable))
                if rnd == 1: change = random.sample(changeable, len(changeable))
                if rnd > 1: change = random.sample(changeable, round(len(changeable)*mut_rt))
                #change = random.sample(changeable, len(changeable)//rnd)
                for j in range(len(dates)):  #sample
                    k = v[j]
                    if j in change: k = random.randrange(dates[j][0], dates[j][1])
                    cnts[k] += 1
                    s.append(k)
                    bin_procs[k] = list(map(operator.add, procs[j], bin_procs[k]))
                p = assess_phonotactic_prob(cnts, bin_procs, rates)
                #p *= chi_squared_pdf(cnts, nallocation)
                #p = assess_phonotactic_prob(cnts, bin_procs, rates)-(kullbackleibler([(x+1)/(sum(cnts)+7) for x in cnts], [1/len(cnts) for x in cnts])) #assess
                if any([p>x for x in nu_top_probs]) and s not in nu_verses: #update pool
                    mutated = True
                    loc = top_rank(p, nu_top_probs)
                    #if len(verses)<100: print("MUTATION  overturns {1} (p:{0}, rnd:{2})".format(p, loc, rnd))
                    #if len(verses)>=100: print("MUTATION  overturns {1} (p:{0}, rnd:{2}, ham:{3})".format(p, loc, rnd, hamming(s, verses[loc])))
                    lst_update = rnd
                    lst_mutate = rnd
                    #print("MUTATION  overturns {1} (p:{0}, rnd:{2})".format(p, loc, rnd))
                    nu_top_probs =      nu_top_probs[:loc]+[p]+nu_top_probs[loc:-1]
                    nu_time_bins =      nu_time_bins[:loc]+[cnts]+nu_time_bins[loc:-1]
                    nu_verses =         nu_verses[:loc]+[s]+nu_verses[loc:-1]
                    nu_distributions =  nu_distributions[:loc]+[bin_procs]+nu_distributions[loc:-1]
        verses       = [x for x in nu_verses       ]
        top_probs    = [x for x in nu_top_probs    ]
        time_bins    = [x for x in nu_time_bins    ]
        distributions= [x for x in nu_distributions]
        rnd += 1
    print("last updated: ", lst_update, "last mutated: ", lst_mutate)
    return (verses, top_probs, time_bins, distributions)

def random_search(rates, slot_cnt, procs, *dates):
    ##initialization
    verses = [d[0] for d in dates] #date samples, initialized to earliest possible entry for all words
    top_probs = [0 for i in range(15)] #probabilities of verses
    time_bins = [] #how many words in each time slot by verse
    distributions = [] #how many words in each time slot match phonotactics of interest
    changeable = [j  for j in range(len(dates)) if dates[j][1]-dates[j][0] > 1]
    rnd = 1
    while rnd < 20:
        nu_verses       = [x for x in verses       ]
        nu_top_probs    = [x for x in top_probs    ]
        nu_time_bins    = [x for x in time_bins    ]
        nu_distributions= [x for x in distributions]
        for v in verses:
            for i in range(10000):
                cnts = [0 for j in range(slot_cnt)] #0 for however many time slots there are
                s = [] #tracking individual slot placements
                bin_procs = [[0 for j in range(len(procs[0]))] for k in range(len(cnts))] #how many instances of proc are in each bin (for prob calc)
                change = random.sample(changeable, len(changeable)//cnt)
                for j in range(len(dates)):  #sample
                    k = v[j]
                    if j in change: random.randrange(dates[j][0], dates[j][1])
                    cnts[k] += 1
                    s.append(k)
                    bin_procs[k] = list(map(operator.add, procs[j], bin_procs[k]))
                p = assess_phonotactic_prob(cnts, bin_procs, rates) #assess
                if any([p>x for x in nu_top_probs]): #update pool
                    loc = top_rank(p, nu_top_probs)
                    #print("{0} overturns {1} (i:{2}, rnd:{3})".format(p, tops[loc], loc, i))
                    nu_top_probs =      nu_top_probs[:loc]+[p]+nu_top_probs[loc:-1]
                    nu_time_bins =      nu_time_bins[:loc]+[cnts]+nu_time_bins[loc:-1]
                    nu_verses =         nu_verses[:loc]+[s]+nu_verses[loc:-1]
                    nu_distributions =  nu_distributions[:loc]+[bin_procs]+nu_distributions[loc:-1]
        verses       = [x for x in nu_verses       ]
        top_probs    = [x for x in nu_top_probs    ]
        time_bins    = [x for x in nu_time_bins    ]
        distributions= [x for x in nu_distributions]
        rnd += 1
    return (verses, top_probs, time_bins, distributions)

#{these really live in latin/phonotactic_survey, duplicated here temporarily
phonotactics = [#what to look for in Latin
        re.compile('((?<!m)[Pp])|((?<!n)[Ff])'), #missing phonemes what about [f:]? contextual carve-outs to allow cluster detection
        re.compile('((?<=[aeiouAEIOU])(([tkdg](?![rlmn]))|[bm]))'), #lenition excluding compensatory lengthening
        #re.compile('^[^AEIOUaeiou]*[eoiu][^AEIOUaeiou]*$'), #monosyllable affection -> non-low short vowel 
        re.compile('((^[^AEIOUaeiou]*[eoiu][^AEIOUaeiou]*$)|(^[^AEIOUaeiou]*(((e|o)[^AEIOUaeiou]?[iuIU])|((i|u)[^AEIOUaeiou]*[aoAO]))))'), #mono/multisyllable affection -> non-low short vowel in initial syll (followed by V with opposite value of [HIGH]) (weakly? correlated with trisyllables) ... this could be sensitive to type of consonant in the raising specification ... no, because there isn't a hard and fast blocking condition
        #re.compile('^[^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOUAEIOU][^AEIOUaeiou]*$'), #disyllables (not correlated with anything in Irish)
        re.compile('[^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOUAEIOU][^AEIOUaeiou]*[AEIOUaieou]'), #trisyllables or greater (syncope-adjacent)
        re.compile('(([^AEIOUaeiou]*[AEIOUaeiou].*[AEIOU])|([aeiouAEIOU][tkdg][rlmn]))'), #long vowels in non-initial syllables OR lengthening clusters (shortening/complen-adjacent, a bit correlated with trisyllables due to length overlap)
        #re.compile('[AEIOU]'), #long vowels (shortening/complen-adjacent)
        #re.compile('[aeiouAEIOU][tkdg][rlmn]'), #compensatory lengthening ... moved to the shortening/complen test (long vowels in non-initial syllables
        re.compile('(st|mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks)'), #syncope+st phonotactics... st phonotactics are different temporally though...
        ]

hacked_prior = [0.2711864406779661, 0.5747303543913713, 0.1997945557267591, 0.1561376476630714, 0.37493579866461224, 0.17565485362095531]
#hacked_prior = [0.2567991631799163, 0.6244769874476988, 0.44142259414225943, 0.08002092050209204, 0.14905857740585773, 0.48169456066945604, 0.017259414225941423, 0.17468619246861924]
#}

if __name__ == "__main__":
    raw = autodate.read_in(sys.argv[1])
    dates = []
    procs = []
    words = []
    hand = {}
    for x in hand_dates.align_crashes: hand[x] = hand_dates.align_crashes[x] 
    for x in hand_dates.inconsistent: hand[x] = hand_dates.inconsistent[x]
    #for x in hand_dates.post_lenition_fs_theory: hand[x] = hand_dates.post_lenition_fs_theory[x]
    #i = 1
    for r in raw:
        #print(i)
        #i += 1
        latin, irish = autodate.clean_transcription(r[0]), autodate.clean_transcription(r[1])
        if latin[-1] in "aeiouAEIOU" and not irish[-1] in "aeiouAEIOUə": latin = latin[:-1] #hack to enact british apocope/loss of stem vowel in addition to replacement of infl by zero suffixes
        procs.extend(tally_procs(phonotactics, latin))
        if (r[0], r[1]) in hand : 
            dates.append(hand[(r[0], r[1])])
            words.append((latin, irish))
        else:
            latin_a, irish_a = needleman.align(latin, irish, 0.5, needleman.read_similarity_matrix('simMatrix.txt'))
            dates.append(autodate.date_nu(7, *autodate.sync_check(irish_a, count_sylls.count_syll(latin_a), count_sylls.alt_w_fin_degen(count_sylls.count_syll(latin_a)), autodate.procs_kludge(latin_a, irish_a, autodate.check_procs_nu(latin_a, irish_a, autodate.triggers, autodate.processes)))))
            words.append((latin, irish))
        #if (not any([0 in x and 1 in x for x in autodate.check_procs(latin_a, irish_a)])) and autodate.date(*autodate.check_procs(latin_a, irish_a))[0] < autodate.date(*autodate.check_procs(latin_a, irish_a))[1]: 
        #    dates.append(autodate.date(*autodate.check_procs(latin_a, irish_a)))
            #    words.append((latin, irish))
    meta_means = []
    naive_allocation = naive(7, *dates)
    for ind in range(5):
        print(ind)
        x = genetic_search(hacked_prior, 7, procs, naive_allocation, *dates)
        #names = ["","p→k", "lenition", "harmony", "shortening", "compensatory lengthening", "syncope", "MS"]
        means = [0 for y in x[2][0]]
        for i in range(len(x[2][0])):
            means[i] = mean(*[y[i] for y in x[2]])
        meta_means.append(means)
        with open("model_predictions_{}.csv".format(str(ind)), 'w') as file_out:
            file_out.write("period,model\n")
            for i in range(len(means)+1): file_out.write(",".join((str(i), str(sum(means[:i]))))+'\n')
        with open("model_summary_{}".format(str(ind)), 'w') as file_out:
            file_out.write("mean p (top 15): "+str(mean(*[x[1][i] for i in range(15)]))+'\n')
            file_out.write("mean p (all):    "+str(mean(*[x[1][i] for i in range(len(x[0]))]))+'\n')
            file_out.write("mean bin size: "+str(means)+"\n")
        for i in range(15):
            with open("model_{}_".format(str(ind))+str(i), 'w') as file_out:
                file_out.write("p: "+str(x[1][i])+'\n')
                file_out.write("\n")
                file_out.write("hamming distances from:\n")
                for j in range(15):
                    file_out.write(str(j)+": "+str(hamming(x[0][i], x[0][j]))+"\n")
                file_out.write("\n")
                file_out.write("time slots have these many members:\n")
                file_out.write(str(x[2][i])+"\n")
                for j in range(len(x[2][i])):
                    file_out.write("In time slot "+str(j)+" ("+str(x[2][i][j])+"):\n")
                    for k in range(len(x[0][i])):
                        if x[0][i][k] == j: 
                            file_out.write(words[k][0]+"\n")
                            file_out.write(words[k][1]+"\n")
                            file_out.write("\n")
    with open("model_aggregate.csv", 'w') as file_out:
        file_out.write("period,model\n")
        for i in range(len(means)+1): file_out.write(",".join((str(i), str(sum([meta_means[j][:i] for j in range(len(meta_means))]/len(meta_means)))))+'\n')
    #hack_prior("albright_latin_nouns_stems_reorthed.txt")

##trial simulations
#if __name__ == "__main__":
#    procs = [[0 for i in range(len(process_list))] for j in range(len(forms))]
#    for i in range(len(forms)):
#        for j in range(len(process_list)):
#            if process_list[j].search(forms[i]): 
#                procs[i][j] = 1
#
#    ##initialization with prior distributions
#    time_bins = []
#    verses = []
#    distributions = []
#    distances = [0 for i in range(15)]
#    for i in range(10000):
#        cnts = [0,0,0,0,0,0,0] #0 for however many time slots there are
#        s = []
#        bin_procs = [[0 for j in range(len(procs[0]))] for k in range(len(cnts))]
#        for j in range(len(data)): 
#            k = random.randrange(data[j][0], data[j][1])
#            cnts[k] += 1
#            s.append(k)
#            bin_procs[k] = list(map(operator.add, procs[j], bin_procs[k]))
#        #d = 0
#        #for j in range(len(cnts)):
#        #    for k in range(len(procs[0])):
#        #        d += distance(q[k], bin_procs[j][k], cnts[j])
#        #if any([d<x for x in distances]):
#        #    j = 14
#        #    while d<distances[j] and j != 0: 
#        #        j -= 1
#        #        if d>distances[j] or j == 0: 
#        #            distances = distances[:j]+[d]+distances[j:-1]
#        #            time_bins = time_bins[:j]+[cnts]+time_bins[j:-1]
#        #            verses = verses[:j]+[s]+verses[j:-1]
#        #            distributions = distributions[:j]+[bin_procs]+distributions[j:-1]
#        p = 1
#        for j in range(len(cnts)):
#            binomial_results = []
#            for k in range(len(bin_procs[j])):
#                b = binomial(bin_procs[j][k], cnts[j], q[k])
#                binomial_results.append(b)
#            #print("processes {0}".format(bin_procs[j]))
#            #print("cnts:{0}".format(j))
#            #print(product(*binomial_results))
#            p *= product(*binomial_results)
#            #p *= product(*[binomial(bin_procs[j][k], cnts[j], q[k]) for k in range(len(bin_procs[j]))])
#        if any([p>x for x in distances]): #rename distances to probs
#            j = 14
#            while p>distances[j]: 
#                if p<distances[j-1] or j == 0: 
#                    #print("{0} overturns {1} (i:{2}, rnd:{3})".format(p, distances[j], j, i))
#                    distances = distances[:j]+[p]+distances[j:-1]
#                    time_bins = time_bins[:j]+[cnts]+time_bins[j:-1]
#                    verses = verses[:j]+[s]+verses[j:-1]
#                    distributions = distributions[:j]+[bin_procs]+distributions[j:-1]
#                j -= 1
#
#    ##further runs to try to get closer to priors
#    cnt = 2
#    while cnt < 20:
#        nuverses = [x for x in verses]
#        nudistances = [x for x in distances]
#        nutime_bins = [x for x in time_bins]
#        nudistributions = [x for x in distributions]
#        for v in nuverses:
#            for i in range(10000):
#                change = random.sample(range(len(v)), len(v)//cnt)
#                cnts = [0,0,0,0,0,0,0] #0 for however many time slots there are
#                s = []
#                bin_procs = [[0 for j in range(len(procs[0]))] for k in range(len(cnts))]
#                for j in range(len(v)):
#                    k = v[j]
#                    if j not in change: k = random.randrange(data[j][0], data[j][1])
#                    cnts[k] += 1
#                    s.append(k)
#                    bin_procs[k] = list(map(operator.add, procs[j], bin_procs[k]))
#                #d = 0
#                #for j in range(len(cnts)):
#                #    for k in range(len(procs[0])):
#                #        d += distance(q[k], bin_procs[j][k], cnts[j])
#                #if any([d<x for x in distances]):
#                #    j = 14
#                #    while d<distances[j] and j != 0: 
#                #        j -= 1
#                #        if d>distances[j] or j == 0: 
#                #            distances = distances[:j]+[d]+distances[j:-1]
#                #            time_bins = time_bins[:j]+[cnts]+time_bins[j:-1]
#                #            verses = verses[:j]+[s]+verses[j:-1]
#                #            distributions = distributions[:j]+[bin_procs]+distributions[j:-1]
#                p = 1
#                for j in range(len(cnts)):
#                    p *= product(*[binomial(bin_procs[j][k], cnts[j], q[k]) for k in range(len(bin_procs[j]))])
#                if any([p>x for x in distances]): #rename distances to probs
#                    j = 14
#                    while p>distances[j]: 
#                        if p<distances[j-1] or j==0: 
#                            #print("{0} overturns {1} (i:{2}, rnd:{3})".format(p, distances[j], j, cnt))
#                            distances = distances[:j]+[p]+distances[j:-1]
#                            time_bins = time_bins[:j]+[cnts]+time_bins[j:-1]
#                            verses = verses[:j]+[s]+verses[j:-1]
#                            distributions = distributions[:j]+[bin_procs]+distributions[j:-1]
#                        j -= 1
#        cnt += 1
#
#    for i in range(len(time_bins)): 
#        for j in range(len(time_bins[i])):
#            print(time_bins[i][j], product(*[binomial(distributions[i][j][k], time_bins[i][j], q[k]) for k in range(len(distributions[i][j]))]))
#        print("\n")
#    means = [0 for x in time_bins[0]]
#    for i in range(len(time_bins[0])):
#        means[i] = mean(*[x[i] for x in time_bins])
#    print(means)
#    #for x in distances: print(x)
#
#    ##sampling
#    h = []
#    verses = []
#    for i in range(10000):
#        cnts = [0,0,0,0,0,0,0] #0 for however many time slots there are
#        s = []
#        for x in data: 
#            j = random.randrange(x[0], x[1])
#            cnts[j] += 1
#            s.append(j)
#        h.append(cnts)
#        verses.append(s)
#
#    means = [0 for x in h[0]]
#    for i in range(len(h[0])):
#        means[i] = mean(*[x[i] for x in h])
#    print(means)
#
#    ##attempted complete enumeration :P
#    #h = []
#    #cnt = 0
#    #for v in it.product(*[span(d[0], d[1]) for d in data]):
#    #    cnt += 1
#    #    cnts = [0,0,0,0,0,0,0] #0 for however many time slots there are
#    #    for x in v:
#    #        cnts[x] += 1 
#    #    #h.append(cnts)
#    #    print(cnts)
#
##    data = readin(sys.argv[1])
##    forms = [x[0] for x in data] #make longer if say, latin and UR are included, adjust indices below
##    dates = [(x[1], x[2]) for x in data]
##    procs = [tuple(x[3:]) for x in data]
##    q = readin(sys.argv[2]) #prior/overall process eligibility->single line file
##    h = []
##    #sample the multiverse, collect count of words, process composition for each bin in a 'verse ... can't iterate because, there's 10^75 combinations...
##    for i in range(int(sys.argv[2])):
##        cnts = [0,0,0,0,0,0] #0 for however many time slots there are
##        hits = [[0 for j in range(len(procs[0]))] for k in range(len(cnts))]
##        divs = []
##        for j in range(len(dates)): #might be useful for debugging to use forms (animations using different orderings?) but otherwise irrelevant
##            t = random.randrange(dates[j][0], dates[j][1])
##            cnts[t] += 1 
##            for k in range(len(procs[j])): hits[t][k] += procs[j][k]
##        for j in range(len(cnts)):
##            divs.append(kullbackleibler([x/cnts[j] if cnts[j] != 0 else 0 for x in hits[j]], q)*(cnts[j]/sum(cnts))) #weight divergences by size of time slot
##        h.append((cnts, hits, divs, mean(*divs), stdev(*divs))) #sanity check, all means should be the same (after weighting), but stdevs not
#        
