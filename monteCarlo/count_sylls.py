import sys

def count_syll(word):
    cnt = []
    i = 0
    while i != len(word):
        if word[i] in "aA":
            cnt.append(i)
            if i < len(word)-1:
                if word[i+1] in "eu": i += 1
        elif word[i] in "oO": 
            cnt.append(i)
            if i < len(word)-1:
                if word[i+1] == "e": i += 1
        elif word[i] in "eE": 
            cnt.append(i)
            if i < len(word)-1:
                if word[i+1] in "ui": i += 1
        elif word[i] in "uU":
            if i > 0:
                if word[i-1] != "q": 
                    cnt.append(i)
            else: cnt.append(i)
        elif word[i] in "iI":
            if i == 0 and word[i+1] not in "aeiouAEIOU": cnt.append(i) #initial glides
            elif i<len(word)-1:
                if  i == 1 and not (word[i-1] in "aeiou:AEIOU" and word[i+1] in "aeiouAEIOU"): cnt.append(i) #hiatus glides
                elif i > 1 and word[i-2:i] != "qu" and not (word[i-1] in "aeiou:AEIOU" and word[i+1] in "aeiouAEIOU"): cnt.append(i)
            else: cnt.append(i)
        i += 1
    return cnt

def alt_w_fin_degen(cnt):
    parity = True
    h = []
    for c in cnt:
        h.append(parity)
        parity = not parity
    h[-1] = True
    return h

def find_long(word, cnt):
    #diphthongs not managed. I assume they were long?
    h = []
    for i in cnt:
        h.append(False)
        if i < len(word)-1:
            if word[i+1] == ":": h[-1] = True
    return h

def read_in(filename):
    h = []
    with open(filename) as file_in:
        for l in file_in:
            h.append(l.strip("\n"))
    return h

def write_out(filename, *vector):
    with open(filename, 'w') as file_out:
        for x in vector:
            file_out.write(str(x)+"\n")

if __name__ == "__main__":
    data = read_in(sys.argv[1])
    h = []
    m = []
    #getting the possibly preservable long vowels (v-finality not managed)
    for d in data:
        c = count_syll(d)
        if len(c) == 3 and find_long(d, c)[2] and not find_long(d,c)[1] : h.append(d)
        elif len(c) == 3 : m.append(d)
        #if len(c) == 4 and find_long(d, c)[2] and not find_long(d,c)[1]: h.append(d)
        #elif len(c) == 5 and (not (find_long(d, c)[1] == True and find_long(d, c)[3] == True)) and any(find_long(d, c)[1:4]): h.append(d)
        #elif len(c) == 6 and (not (find_long(d, c)[1] == True and find_long(d, c)[3] == True)) and any(find_long(d, c)[1:5]): h.append(d)
        #elif len(c) > 3: m.append(d)
    write_out("albright_latin_nouns_stems_viable_semi_late_syncopaters.txt", *h)
    write_out("albright_latin_nouns_stems_nonviable_semi_late_syncopaters.txt", *m)
    print(len(h))
    print(len(m))
    print(len(h)/(len(m)+len(h)))
    #getting the raw syll counts
    #for d in data: h.append(len(count_syll(d)))
    #write_out("albright_latin_nouns_stems_syllcount.txt", *h)
