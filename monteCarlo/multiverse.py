##todo: the best 15 probability log isn't working right (0 stays at top)...
import sys
import math
import random #too many combinations to calculate exactly. original used itertools.product()
import operator
from functools import reduce
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

def assess_prob(sum_bins, prop_bins, prior_rates):
    p = 1
    for j in range(len(sum_bins)):
        binomial_results = []
        for k in range(len(prop_bins[j])): binomial_results.append(binomial(prop_bins[j][k], sum_bins[j], prior_rates[k]))
        #print("processes {0}".format(prop_bins[j]))
        #print("sum_bins:{0}".format(j))
        #print(product(*binomial_results))
        p *= product(*binomial_results)
    return p

def top_rank(candidate, tops):
    j = len(tops)-1
    while p>tops[j]: 
        if p<tops[j-1] or j == 0: return j
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
    time_containers = [[[x.count(j)] for j in range(slot_cnt)] for x in offspring]
    proc_containers = [[[0 for j in range(len(procs[0]))] for k in range(slot_cnt)] for x in offspring]
    for i in range(len(offspring)):
        for j in range(len(offspring[i])): proc_containers[i][j][offspring[i][j]] = list(map(operator.add, procs[j], proc_containers[i][j][offspring[i][j]]))
    return (time_containers, proc_containers)


def genetic_search(rates, slot_cnt, procs, *dates) 
    ##initialization
    verses = [d[0] for d in dates] #date samples, initialized to earliest possible entry for all words
    top_probs = [0 for i in range(15)] #probabilities of verses
    time_bins = [] #how many words in each time slot by verse
    distributions = [] #how many words in each time slot match phonotactics of interest
    changeable = [j  for j in range(len(dates)) if dates[j][1]-dates[j][0] > 1]
    rnd = 1
    while rnd < 20: #mutations and recombinations compete head-to-head, instead of mutations spreading off recombinations
        nu_verses       = [x for x in verses       ]
        nu_top_probs    = [x for x in top_probs    ]
        nu_time_bins    = [x for x in time_bins    ]
        nu_distributions= [x for x in distributions]
        nu_gen = recombine(1000, [x for x in verses])
        nu_gen_vit_stats = recombine_aux(procs, slot_cnt, *nu_gen)
        for i in range(len(nu_gen)):
            p = assess_prob(nu_gen_vit_stats[i][0], nu_gen_vit_stats[i][1], rates)
            if any([p>x for x in nu_top_probs]): #update pool
                loc = top_rank(p, nu_top_probs)
                #print("{0} overturns {1} (i:{2}, rnd:{3})".format(p, tops[loc], loc, i))
                nu_top_probs =      nu_top_probs[:loc]+[p]+nu_top_probs[loc:-1]
                nu_time_bins =      nu_time_bins[:loc]+[nu_gen_vit_stats[i][0]]+nu_time_bins[loc:-1]
                nu_verses =         nu_verses[:loc]+[s]+nu_verses[loc:-1]
                nu_distributions =  nu_distributions[:loc]+[nu_gen_vit_stats[i][1]]+nu_distributions[loc:-1]
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
                p = assess_prob(cnts, bin_procs, rates) #assess
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

def random_search(rates, slot_cnt, procs, *dates) 
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
                p = assess_prob(cnts, bin_procs, rates) #assess
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

phonotactics = [#what to look for in Latin
        re.compile('((?<!m)(P|p))|((?<!n)f)'), #missing phonemes what about [f:]? contextual carve-outs to allow cluster detection
        re.compile('((?<=[aeiouAEIOU])([tkbdgm]|s(?!t|k)))'), #lenition 
        re.compile('^[^AEIOUaeiou]*[eoiu]'), #affection -> non-low short vowel in initial syll
        re.compile('^[^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOUAEIOU][^AEIOUaeiou]*$)'), #disyllables (apocope-adjacent)
        re.compile('[^AEIOUaeiou]*[AEIOUaieou][^AEIOUaeiou]*[AEIOUAEIOU][^AEIOUaeiou]*[AEIOUaieou])'), #trisyllables or greater (syncope, also complen-adjacent)
        re.compile('[AEIOU]'), #long vowels (apocope/shortening/complen-adjacent)
        re.compile('[aeiou](?=[dg][^aeiouAEIOU])'), #compensatory lengthening -> somewhat correlated with lenition, affection
        re.compile('(st|mp|ŋk|n(t(?!$)|s|f))|((?<!^e)ks)'), #syncope+st phonotactics. 
        ]

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
