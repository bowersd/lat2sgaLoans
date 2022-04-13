
def blocks(*num_seqs):
    h = []
    edge = 0.0
    for s in num_seqs:
        h.append("\draw[fill=black!50]({0}pt,0) rectangle ({1}pt, {2}pt);\n".format(edge, edge+s[0], s[0]))
        h.append("\draw[fill=black!100]({0}pt,0) rectangle ({1}pt, {2}pt);\n".format((edge+(s[0]/2)-(s[1]/2)), (edge+(s[0]/2)+(s[1]/2)), s[1]))
        for x in s[2:]: h.append("\draw[fill=black!100,opacity=0.5]({0}pt,{1}pt) circle (5pt);\n".format((edge+(s[0]/2)), x))
        edge += s[0]
    return h

def tikz(file_out, *lines):
    with open(file_out, 'w') as fout:
        fout.write("\documentclass{standalone}"+"\n")
        fout.write("\\usepackage{tikz}"+"\n")
        fout.write("\begin{document}"+"\n")
        fout.write("\\begin{tikzpicture}"+"\n")
        for l in lines:
            fout.write(l)
        fout.write("\\end{tikzpicture}"+"\n")
        fout.write("\\end{document}"+"\n")

if __name__ == "__main__":
    for x in blocks((86.9,18), (80.6, 3), (78.9, 10), (61.5, 2), (50.8, 0), (52.9, 0), (120.4, 72)): print(x)
