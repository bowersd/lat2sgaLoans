import math

def blocks(*num_seqs):
    h = []
    edge = 0.0
    top = max([s[0] for s in num_seqs])
    right = sum([s[0] for s in num_seqs])
    boiler = ["\draw[xstep=40pt, ystep=50pt, opacity=0.1] (0pt,0pt) grid (560pt, 250pt);\n",
        "\\foreach \x / \label in {120pt/120, 240pt/240, 360pt/360, 480pt/480, 560pt/560}\n",
        "    {\draw (\x, -10pt) node {\huge \label} ;};\n",
        "\\foreach \y / \label in {50pt/50, 150pt/150, 250pt/250}\n",
        "   {\draw (-18pt, \y) node {\huge \label} ;};\n",
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
        for x in s[2:]: h.append("\draw({0}pt,{1}pt) circle (1pt);\n".format((edge+(num_seqs[i][0]/2)), x))
        boiler.append("\draw ({0}, -36pt) node {\huge {1}};".format(edge+(s[0]/2), names[i]))
        edge += num_seqs[i][0]
    return boiler + h


def logblocks(*num_seqs):
    h = []
    edge = 0.0
    top = max([math.log(s[0])/math.log(2) for s in num_seqs])
    right = sum([s[0] for s in num_seqs])
    boiler = ["\draw[xstep=0, ystep=1cm, opacity=0.1] (0pt,0pt) grid ({0}cm, 8cm);".format(right),
        "\\foreach \y / \label in {50pt/50, 150pt/150, 250pt/250}",
        "   {\draw (-18pt, \y) node {\huge \label} ;};",
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
        for x in s[2:]: h.append("\draw({0}pt,{1}pt) circle (1pt);\n".format((edge+(num_seqs[i][0]/2)), x))
        boiler.append("\draw ({0}, -36pt) node {\huge {1}};".format(edge+(s[0]/2), names[i]))
        edge += num_seqs[i][0]
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
    for x in blocks((86.9,18), (80.6, 3), (78.9, 10), (61.5, 2), (50.8, 0), (52.9, 0), (120.4, 72)): print(x)
