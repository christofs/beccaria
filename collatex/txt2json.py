#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: make_json.py
# Author: #cf, 2016, revised 2023. 

"""
Script to generate JSON from plain text files as needed for collation with CollateX. 
This script currently uses the following assumptions and/or parameters: 
- 3 text witnesses are available
- The tokenized input format is used
- A simple token normalization takes place 
"""

# === Imports === 

import re
from os.path import join

# === Parameters === 

wdir = join("/", "home", "christof", "Github", "christofs", "beccaria", "")

textids = ["fr1766", "fr1773", "fr1782"]

jsonfile = join(wdir, "collatex", "Beccaria_ch36_fr1766-fr1773-fr1782_t+n.json") 


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
        # Separate out punctuation
        text = re.sub(","," ,", text)
        text = re.sub("\'"," \' ", text)
        text = re.sub("\."," .", text)
        text = re.sub(":"," :", text)
        text = re.sub(";"," ;", text)
        # JSON protected characters
        text = re.sub("\n"," # ", text)
        text = re.sub("\"","\\\"", text)
        return text


def tokenize_text(text):
    tokens = re.split(" ", text)
    return tokens 


def normalize_tokens(tokens): 
    normalized = []
    for t in tokens: 
        # All lowercase
        n = t.lower()
        # Modernize orthography
        n = re.sub("&", "et", n)
        n = re.sub("adultere", "adultère", n)
        n = re.sub("affoiblir", "affaiblir", n)
        n = re.sub("aprés", "après", n)
        n = re.sub("ayent", "aient", n)
        n = re.sub("delit", "délit", n)
        n = re.sub("espece", "espèce", n)
        n = re.sub("feroit", "ferait", n)
        n = re.sub("gueres", "guère", n)
        n = re.sub("loix", "lois", n)
        n = re.sub("mème", "même", n)
        n = re.sub("plûpart", "plupart", n)
        n = re.sub("pouvoit", "pouvait", n)
        n = re.sub("regle", "règle", n)
        n = re.sub("récens", "récents", n)
        n = re.sub("seroit", "serait", n)
        n = re.sub("sauroit", "saurait", n)
        n = re.sub("tems", "temps", n)
        normalized.append(n)
    return normalized


def create_json(tokens, normalized):
    json_tokens = ""
    for i in range(0, len(tokens)): 
        jt = "\n{\"t\" : \""+ tokens[i] + " \", \"n\" : \"" + normalized[i] + " \"}, "
        if "\"\"" not in jt and "\" \"" not in jt:
            json_tokens = json_tokens + jt
    json_tokens = json_tokens[:-2]
    #print(json_tokens)
    return json_tokens



def build_collatex_json(json_tokens_all):
    collatex_json = "{\"witnesses\" : [ { \"id\" : \""+textids[0]+"\", \"tokens\" : [" + json_tokens_all[0] + "] }, { \"id\" : \""+textids[1]+"\", \"tokens\" : [" + json_tokens_all[1] + "] }, { \"id\" : \""+textids[2]+"\", \"tokens\" : [" + json_tokens_all[2]  + "] } ] }" 
    return collatex_json


def save_json(collatex_json, jsonfile):
    with open(jsonfile, "w") as outfile: 
        outfile.write(collatex_json)   


# === Main ===

def main():
    json_tokens_all = []
    for textid in textids: 
        file = join(wdir, "data", "selection", "Beccaria-ch36_"+textid+".txt")
        text = read_file(file)
        tokens = tokenize_text(text)
        print(textid, len(tokens), "tokens")
        normalized = normalize_tokens(tokens)
        json_tokens = create_json(tokens, normalized)
        json_tokens_all.append(json_tokens)
    collatex_json = build_collatex_json(json_tokens_all)
    save_json(collatex_json, jsonfile)

main()