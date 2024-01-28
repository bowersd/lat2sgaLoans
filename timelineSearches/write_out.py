import math

def blocks(*num_seqs):
    h = []
    edge = 0.0
    top = max([s[0] for s in num_seqs])
    right = sum([s[0] for s in num_seqs])
    boiler = ["\draw[xstep=40pt, ystep=50pt, opacity=0.1] (0pt,0pt) grid (560pt, 250pt);\n",
        r"\foreach \x / \label in {120pt/120, 240pt/240, 360pt/360, 480pt/480, 560pt/560}\n",
        r"    {\draw (\x, -10pt) node {\huge \label} ;};\n",
        r"\foreach \y / \label in {50pt/50, 150pt/150, 250pt/250}\n",
        r"   {\draw (-18pt, \y) node {\huge \label} ;};\n",
            ]
    names = ["[p]$\\to$[k]",
            "Len.",
            "Harm.",
            "Shorten.",
            "Lengthen",
            "Syncope",
            "Post-Syncope",
            ]
    for i in range(len(num_seqs)):
        h.append("\draw({0}pt,0) rectangle ({1}pt, {2}pt);\n".format(edge, edge+num_seqs[i][0], num_seqs[i][0]))
        h.append("\draw[fill=black!100]({0}pt,0) rectangle ({1}pt, {2}pt);\n".format((edge+(num_seqs[i][0]/2)-(num_seqs[i][1]/2)), (edge+(num_seqs[i][0]/2)+(num_seqs[i][1]/2)), num_seqs[i][1]))
        for x in num_seqs[i][2:]: h.append("\draw({0}pt,{1}pt) circle (1pt);\n".format((edge+(num_seqs[i][0]/2)), x))
        boiler.append("\draw ({0}, -36pt) node {{\huge {1}}};".format(edge+(num_seqs[i][0]/2), names[i]))
        edge += num_seqs[i][0]
    return boiler + h

def upto1(x): 
    if x < 1: return 1
    return x

def logBlocks(*num_seqs):
    h = []
    edge = 0.0
    top = max([math.log(upto1(s[0]), 2) for s in num_seqs])
    right = sum([math.log(upto1(s[0]), 2) for s in num_seqs])
    boiler = ["\draw[xstep=0, ystep=1cm, opacity=0.1] (0,0) grid ({0}cm, 8cm);\n".format(right),
        "\\foreach \y / \label in {1cm/2, 2cm/4, 3cm/8, 4cm/16, 5cm/32, 6cm/64, 7cm/128, 8cm/256}\n",
        "    {\draw (-18pt, \y) node {\huge \label} ;};\n"
            ]
    names = ["[p]$\\to$[k]",
            "Lenition",
            "Harmony",
            "Short.",
            "Length",
            "Syncope",
            "Post-Syncope",
            ]
    for i in range(len(num_seqs)):
        h.append("\draw({0}cm,0) rectangle ({1}cm, {2}cm);\n".format(edge, edge+math.log(upto1(num_seqs[i][0]),2), math.log(upto1(num_seqs[i][0]),2)))
        h.append("\draw[fill=black!100]({0}cm,0) rectangle ({1}cm, {2}cm);\n".format((edge+(math.log(upto1(num_seqs[i][0]), 2)/2)-(math.log(upto1(num_seqs[i][1]), 2)/2)), (edge+(math.log(upto1(num_seqs[i][0]), 2)/2)+(math.log(upto1(num_seqs[i][1]), 2)/2)), math.log(upto1(num_seqs[i][1]), 2)))
        for x in num_seqs[i][2:]: h.append("\draw({0}cm,{1}cm) circle (0.1cm);\n".format((edge+(math.log(upto1(num_seqs[i][0]), 2)/2)), math.log(upto1(x), 2)))
        boiler.append("\draw ({0}, -36pt) node {{\huge {1}}};\n".format(edge+(math.log(upto1(num_seqs[i][0]), 2)/2), names[i]))
        edge += math.log(upto1(num_seqs[i][0]), 2)
    return boiler + h

def tikz(file_out, *lines):
    with open(file_out, 'w') as fout:
        fout.write("\documentclass{standalone}"+"\n")
        fout.write("\\usepackage{tikz}"+"\n")
        fout.write("\\usepackage{times}"+"\n")
        fout.write("\\usepackage{graphicx}"+"\n")
        fout.write("\\begin{document}"+"\n")
        fout.write("\\begin{tikzpicture}"+"\n")
        for l in lines:
            fout.write(l)
        fout.write("\\end{tikzpicture}"+"\n")
        fout.write("\\end{document}"+"\n")

if __name__ == "__main__":
    tikz('testfig.tex', *logBlocks(*((86.9,18), (80.6, 3), (78.9, 10), (61.5, 2), (50.8, 0), (52.9, 0), (120.4, 72))))
