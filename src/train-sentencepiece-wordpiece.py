#!/usr/bin/env python3

import argparse
import configparser
import glob
import os
import sentencepiece as sp
import sys

parser = argparse.ArgumentParser(description='sentencepiece')
parser.add_argument('--config', required=True, type=str, help='config file')
args = parser.parse_args()

CURDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURDIR, os.pardir, 'bert'))
import tokenization 

CURDIR = os.path.dirname(os.path.abspath(__file__))
CONFIGPATH = os.path.join(CURDIR, os.pardir, args.config)
config = configparser.ConfigParser()
config.read(CONFIGPATH)

TEXTDIR = config['DATA']['TEXTDIR']
PREFIX = config['SENTENCEPIECE']['PREFIX']
VOCABSIZE = config['SENTENCEPIECE']['VOCABSIZE']
CTLSYMBOLS = config['SENTENCEPIECE']['CTLSYMBOLS']


def _get_text_file(text_dir=TEXTDIR):
    file_list = glob.glob(f'{text_dir}/*/*.sent_splited')
    files = ",".join(file_list)
    return files

def train(prefix=PREFIX, vocab_size=VOCABSIZE, ctl_symbols=CTLSYMBOLS):
    files = _get_text_file()
    print("files: {}".format(files))
    # pre-tokenization
    tokenizer = tokenization.BasicTokenizer(do_lower_case=True) #False?

    tokenak = []
    files_tokenized = ""  # comma separated files
    for fs in files.split(","):
        filename = fs + ".tokenized"
        with open(filename, 'w', encoding='utf-8') as fw:
            print("fs: {}".format(fs))
            with open(fs, 'r') as f:
                for line in f:
                    tokenak = tokenizer.tokenize(line)
                    fw.write(" ".join([str(x) for x in tokenak]))
                    fw.write('\n')
        files_tokenized += "," + filename

    # https://github.com/google/sentencepiece/blob/d4dd947fe71c4fa4ee24ad8297beee32887d8828/python/sentencepiece_python_module_example.ipynb
    # https://github.com/allenai/scibert/blob/5d72d0ec50e2d3ebe971122f8b282278c210eccd/scripts/cheatsheet.txt
    # spm.SentencePieceTrainer.Train('--input=combined.out --model_prefix=100B_9999_cased --vocab_size=31000 --character_coverage=0.9999 --model_type=bpe --input_sentence_size=100000000 --shuffle_input_sentence=true')
    command = f'--input={files_tokenized} --model_prefix={prefix} --vocab_size={vocab_size} --control_symbols={ctl_symbols} --character_coverage=1.0 --model_type=bpe --input_sentence_size=100000000 --shuffle_input_sentence=true --normalization_rule_name=identity'

    # --model_type=word
    #command = f'--input={files_tokenized} --model_prefix={prefix} --vocab_size={vocab_size} --control_symbols={ctl_symbols} --model_type=word --hard_vocab_limit=false'  # RuntimeError: Internal: /sentencepiece/src/trainer_interface.cc(498) [(trainer_spec_.vocab_size()) == (model_proto->pieces_size())]
    
    # 
    #command = f'--input={files_tokenized} --model_prefix={prefix} --vocab_size={vocab_size} --control_symbols={ctl_symbols} --hard_vocab_limit=false'  # RuntimeError: Internal: /sentencepiece/src/trainer_interface.cc(498) [(trainer_spec_.vocab_size()) == (model_proto->pieces_size())]
    sp.SentencePieceTrainer.Train(command)

    # remove tokens.txt

def main():
    train()

if __name__ == "__main__":
    main()
