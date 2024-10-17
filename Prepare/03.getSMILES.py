#!/usr/bin/python3.10
#
# script to obtain SMILES codes from PDBeChem databank by compound 3-letters code
#
# (C) Yuri V. Kravatsky, Yuri V. Milchevskiy
# email: milch@eimb.ru
#
# Dependencies:
#  1. python 3 (tested with python 3.10)
#  2. requests (tested with requests 2.22.0)
#
######################################################################################

from pprint import pprint
import sys
import requests
import json

#PDBeChecm URLS
#https://www.ebi.ac.uk/pdbe/api/pdb/compound/summary/:id
BASE_URL = "https://www.ebi.ac.uk/pdbe/"                  # the beginning of the URL for PDBe's API.
SEARCH_URL = BASE_URL + 'api/pdb/compound/summary/'       # the rest of the URL used for PDBe's search API.

def get_url(url):
    """
    Makes a request to a URL. Returns a JSON of the results
    :param str url:
    :return dict:
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("[No data retrieved - %s] %s" % (response.status_code, response.text))
    return {}

def get_pdbechem(pdbe_id):
    url = f"{SEARCH_URL}{pdbe_id}"
    data = get_url(url=url)
    listdict = (data[pdbe_id])[0]
    return listdict

out_list = []

FERR=open("aminoacids_smiles.err", "w")

with open('aminoacids_unique.txt', 'r') as INP:
    for line in INP:
        arr = line.split("\t")
        symb=arr[0].strip()
        name=arr[1].strip()
        if symb == "":
            continue
        results = get_pdbechem(symb)
        rname = results['name'].upper()
        if (rname != name):
            print ("Warning: code ", symb, "with name ", name, " doesn't coincide with results: ", rname, file=FERR)
        smilist=results['smiles']
        outstr = symb + '\t' + rname

        for i in range(len(smilist)):
            msmiles = smilist[i]
            currsmile = msmiles['name']
            outstr += '\t' + currsmile
        out_list.append(outstr)

with open("aminoacids_smiles.txt", "w") as fout:
    print ("Symbol", "\t", "Name", "\t", "Classical", "\t", "Isomeric", file=fout)
    for aminoac in out_list:
        print (aminoac, file=fout)
