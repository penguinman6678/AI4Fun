import sys, os, re
import json

def print_as_log(astr):
    print("LOG_MESSAGE\t%s" % (str(astr)))

def write_json_to_file(json_st, filename=None):
    outputname = "./game_output.log"
    if filename != None:
        outputname = filename
    with open(outputname, 'w') as fd:
        json.dump(json_st, fd )

def read_a_game(filename):
    move_sequences_json = None
    with open(filename, 'r') as fd:
        move_sequences_json = json.load(fd)
    return move_sequences_json

