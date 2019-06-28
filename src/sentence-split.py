#!/usr/bin/env python3

import re
import sys
import argparse
import configparser
import glob
import os

parser = argparse.ArgumentParser(description='sentence split')
parser.add_argument('--config', required=True, type=str, help='config file')
parser.add_argument('--do_lower_case', action='store_true', help='lowercase sentences')
args = parser.parse_args()

CURDIR = os.path.dirname(os.path.abspath(__file__))
CONFIGPATH = os.path.join(CURDIR, os.pardir, args.config)
config = configparser.ConfigParser()
config.read(CONFIGPATH)

TEXTDIR = config['DATA']['TEXTDIR']


def _get_text_file(text_dir=TEXTDIR):
    file_list = glob.glob(f'{text_dir}/*')
    files = ",".join(file_list)
    return files

def s_split():
    files = _get_text_file()
    for file in files.split(","):
        with open(file+".sent_splited","wt",encoding="utf8",errors="ignore") as o:
            with open(file,"rt",encoding="utf8",errors="ignore") as f:
                for p in f:
                    toks = p.split()
                    if len(toks) == 0:
                        o.write("")
                    for x in (range(len(toks)-1)):
                        ct = toks[x]
                        nt = toks[x+1]
                        if (re.search(r'[^\. ][^\. ]\.$',ct) and re.search(r'^[A-Z0-9]',nt)): # or (ct == "." and re.search(r'^[A-Z0-9]',nt)): # <- if text is already tokenized
                            if args.do_lower_case:
                                o.write(ct.lower()+"\n")
                            else:
                                o.write(ct+"\n")
                        else:
                            if args.do_lower_case:
                                o.write(ct.lower()+" ")
                            else:
                                o.write(ct+" ")
                    if toks:
                        if args.do_lower_case:
                            o.write(str(toks[-1]).lower())
                        else:
                            o.write(str(toks[-1]))
                    o.write("\n")

def main():
    s_split()

if __name__ == "__main__":
    main()
