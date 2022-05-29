
def blocks(*num_seqs):
    h = []
    edge = 0.0
    top = max([s[0] for s in num_seqs])
    right = sum([s[0] for s in num_seqs])
    boiler = ["\draw[xstep=40pt, ystep=50pt, opacity=0.1] (0pt,0pt) grid (560pt, 250pt);",
        "\\foreach \x / \label in {120pt/120, 240pt/240, 360pt/360, 480pt/480, 560pt/560}",
        "    {\draw (\x, -10pt) node {\huge \label} ;};",
        "\\foreach \y / \label in {50pt/50, 150pt/150, 250pt/250}",
        "   {\draw (-18pt, \y) node {\huge \label} ;};",
            ]
    for s in num_seqs:
        h.append("\draw({0}pt,0) rectangle ({1}pt, {2}pt);\n".format(edge, edge+s[0], s[0]))
        h.append("\draw[fill=black!100]({0}pt,0) rectangle ({1}pt, {2}pt);\n".format((edge+(s[0]/2)-(s[1]/2)), (edge+(s[0]/2)+(s[1]/2)), s[1]))
        for x in s[2:]: h.append("\draw({0}pt,{1}pt) circle (1pt);\n".format((edge+(s[0]/2)), x))
        edge += s[0]
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
