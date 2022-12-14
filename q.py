import os.path
import random
import sys

import yaml
from yaml import CLoader as Loader

random.seed(15122022)


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

    \renewcommand{\arraystretch}{1.6}
    \usepackage{setspace}

    \begin{document}
    """
    )


def postamble(outfile):
    outfile.write(
        r"""
    \end{document}
    """
    )


def writeout(paper, key):
    outfile = open(f"{os.path.splitext(sys.argv[1])[0]}{key}.tex", "w")
    preamble(outfile)
    outfile.write(f"\\framebox{{\\huge\\bf {key}}}\\\\")
    outfile.write(r"\framebox{\numpoints\ points.}")
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


def write_key(paper):
    for q in paper:
        if "options" in q:
            keyfile.write(f"{'ABCDEFGH'[q['perm'].index(0)]}")


for k in "ABCDEFGHIJKLMN"[:2]:
    randomize(paper)
    writeout(paper, k)
    keyfile.write(f"{k}: ")
    write_key(paper)
    keyfile.write("\n")

keyfile.close()
