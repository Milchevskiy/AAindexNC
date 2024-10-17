#!/usr/bin/python3.10
#
# script to scan already downloaded PDB databank to find unique
# non-canoical amino acids
#
# (C) Yuri V. Kravatsky, Yuri V. Milchevskiy
# email: milch@eimb.ru
#
# Dependencies:
#  1. python 3 (tested with python 3.10)
#  2. ProDy (tested with ProDy 2.4.1 installed by pip)
#
######################################################################################

import fnmatch
import os
from prody import *

modr_array = []

# directory where the top of PDB is downloaded
path="/home/milch/PDB"
for root, dirs, files in os.walk(path):
    for extension in ('*.pdb', '*.pdb.gz', '*.PDB', '*.PDB.gz', '*.ent.gz', '*.ent'):
        for filename in fnmatch.filter(files, extension):
            fpath = root.strip() +'/'+ filename.strip()
            polys = parsePDBHeader(fpath, 'polymers')
            for prot in polys:
# According to ProDy manual class Polymer is a data structure for storing information 
# on polymer components (protein or nucleic) of PDB structures.
# A Polymer instance includes the following attribute:
# modified 	is a Python list of modified residues (MODRES)
# when modified residues are present, each will be represented as: 
#(resname, chid, resnum, icode, stdname, comment)
              if prot.modified:
                   elems = len(prot.modified)
                   for i in range(elems):
                       symb = prot.modified[i][0]
                       name = prot.modified[i][4]
                       nameup = name.upper()
# "MODIFIED RESIDUE" name should be removed, it's definitely not non-canonical amino acid
                       if nameup == "MODIFIED RESIDUE":
                            continue
                       modr = symb.strip() + '\t' + name.strip()
                       modr_array.append(modr)

# Removing duplicates by first changing to a set and then back to a list
list_unique = list(set(modr_array))

with open("aminoacids_unique.txt", "w") as fout:
    for aminoac in list_unique:
        print (aminoac, file=fout)
