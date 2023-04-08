#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: make_json.py
# Author: #cf, 2016, revised 2023. 

"""
Script to prepare CollateX graph-viz output for visualisation with xdot.  
"""

# === Imports === 

import re
from os.path import join

# === Parameters === 

wdir = join("/", "home", "christof", "Github", "christofs", "beccaria", "collatex", "")

gvfile = join(wdir, "Beccaria_ch36_fr1766-fr1773-fr1782_t+n.gv")


# === Functions === 

def read_file(file):
    with open(file, "r") as infile: 
        text = infile.read()
        return text


def prepare_text(text): 
    # Simple replacements
    #text = re.sub(" # ","\n", text)

    # Additional linebreaks in long label text
    lines = []
    for line in re.split("\n", text): 
        if "->" not in line and "label" in line and len(re.split(" ", line)) > 8: 
            try: 
                n = 8
                line = re.split(" ", line)
                for i in range (n, len(line)+n, n+1 ):
                    line.insert ( i, "\n" )
                line = " ".join(line)
                lines.append(line)
            except:
                #print("empty line")
                lines.append(line) 
        else: 
            lines.append(line)
    text = "\n".join(lines)         
    return text

def save_gv(text, gvfile):
    filename = join(wdir, "Beccaria_ch36_fr1766-fr1773-fr1782_t+n-fixed.gv")
    with open(filename, "w") as outfile: 
        outfile.write(text)   


# === Main ===

def main():
    text = read_file(gvfile)
    text = prepare_text(text)
    save_gv(text, gvfile)
main()