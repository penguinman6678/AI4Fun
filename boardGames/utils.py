import sys, os, re
import json
import os.path

def print_as_log(astr):
    print("LOG_MESSAGE\t%s" % (str(astr)))

def write_json_to_file(json_st, filename=None):
    outputname = "./game_output.log"

    if filename != None:
        outputname = filename
    output_rule_to_append_or_create = 'w'
    if os.path.isfile(outputname):
        output_rule_to_append_or_create = 'a'
    with open(outputname, output_rule_to_append_or_create) as fd:
        json.dump(json_st, fd )
        fd.write("\n")

def read_a_game(filename):
    move_sequences_json = None
    with open(filename, 'r') as fd:
        move_sequences_json = json.load(fd)
    return move_sequences_json

