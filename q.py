import os.path
import random
import sys

import yaml
from yaml import CLoader as Loader

KEYNAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def randomize(paper):
    random.shuffle(paper)
    for q in paper:
        if "options" in q:
            perm = list(range(len(q["options"])))
            random.shuffle(perm)
            q["perm"] = perm

paper = list(yaml.load_all(open(sys.argv[1], "r"), Loader=Loader))

def preamble(outfile):
    outfile.write(
        r"""
    \documentclass[twocolumn,10pt,addpoints]{exam}
    \usepackage[margin=0.5cm]{geometry}
    \usepackage{listings}
    \usepackage{fontspec}
    \usepackage{comment}
    \usepackage{savetrees}
    \usepackage{float}
    \floatplacement{figure}{H}
    \usepackage{caption,subcaption}

    \renewcommand{\arraystretch}{1.6}
    \usepackage{setspace}

    \begin{document}
    """
    )

def postamble(outfile):
    outfile.write(r"""\end{document}""")

def writeout(paper, key):
    outfile = open(f"{os.path.splitext(sys.argv[1])[0]}{key}.tex", "w")
    preamble(outfile)
    keybox = f"\\framebox{{\\huge\\sc {key}}}"
    pointbox = r"\framebox{\huge \sc \numpoints\ points}"
    outfile.write(f"\\hbox{{{keybox} {pointbox}}}")
    outfile.write(
    r"""
    \begin{tabular}{ll}
    Full Name&\underline{\phantom{xxxxxxxxxxxxxxx}}\\
    Section \& Subsection &\underline{\phantom{xxxxxxxxxxxxxxx}}\\
    Roll \#&\underline{\phantom{xxxxxxxxxxxxxxx}}
    \end{tabular}

    \lstset{language=Python,basicstyle=\ttfamily}
    """
    )
    outfile.write(r"\begin{questions}")
    for q in paper:
        outfile.write(f"\\question[{q['marks']}] {q['description']}\n")
        if "options" in q:
            outfile.write(r"\begin{oneparchoices}")
            for o in q["perm"]:
                outfile.write(f"\\choice {q['options'][o]}")
            outfile.write(r"\end{oneparchoices}")
    outfile.write(r"\end{questions}")
    postamble(outfile)

keyfile = open("keyfile.txt", "w")

def write_key(paper, k):
    keyfile.write(f"{k}:")
    for i, q in enumerate(paper):
        if "options" in q:
            keyfile.write(f" ({i+1}) {KEYNAMES[q['perm'].index(0)]}")
    keyfile.write("\n")

nkeys = 14
seed  = 0XABCDEF
if len(sys.argv) >= 3:
    seed = int(sys.argv[2])
if len(sys.argv) >= 4:
    nkeys = int(sys.argv[3])
random.seed(seed)
for k in KEYNAMES[:nkeys]:
    randomize(paper)
    writeout(paper, k)
    write_key(paper, k)

keyfile.close()
