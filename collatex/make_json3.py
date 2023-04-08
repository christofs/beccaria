#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: make_json.py
# Author: #cf, 2016, revised 2023. 

"""
Script to generate JSON from plain text files as needed for collation with CollateX. 
"""

# === Imports === 

import re
from os.path import join

# === Parameters === 

wdir = join("/", "home", "christof", "Github", "christofs", "beccaria", "data", "selection", "")

textid1 = "fr1766"
textid2 = "fr1773"
textid3 = "fr1782"


# === Functions === 

def read_file(file):
    with open(file, "r") as infile: 
        text = infile.read()
        # Cleaning up the text
        text = re.sub("#\d+","", text)
        text = re.sub("\t"," ", text)
        text = re.sub("\’","'", text)
        text = re.sub("\n\n","\n", text)
        text = re.sub("\n"," ", text)
        # JSON protected characters
        text = re.sub("\n"," # ", text)
        text = re.sub("\"","\\\"", text)
        return text

def merge_to_json(text1, text2, text3):
    json = "{\"witnesses\" : [ { \"id\" : \""+textid1+"\", \"content\" : \"" + text1 + "\" }, { \"id\" : \""+textid2+"\", \"content\" : \"" + text2 + "\" }, { \"id\" : \""+textid3+"\", \"content\" : \"" + text3 + "\" } ] }" 
    return json


def save_json(json, jsonfile):
    with open(jsonfile, "w") as outfile: 
        outfile.write(json)   


# === Main ===

def main():
    file1 = join(wdir, "Beccaria-ch36_"+textid1+".txt")
    text1 = read_file(file1)
    file2 = join(wdir, "Beccaria-ch36_"+textid2+".txt")
    text2 = read_file(file2)
    file3 = join(wdir, "Beccaria-ch36_"+textid3+".txt")
    text3 = read_file(file3)
    json = merge_to_json(text1, text2, text3)
    jsonfile = join(wdir, "..", "..", "collatex", "Beccaria_ch36_fr1766-fr1773-fr1782.json")
    save_json(json, jsonfile)

main()