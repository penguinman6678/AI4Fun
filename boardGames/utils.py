import sys, os, re
import json
import os.path
import numpy as np

log_output_dir = "./log_outs"
def print_as_log(astr):
    #print("LOG_MESSAGE\t%s" % (str(astr)))
    pass

def write_json_to_file(json_st, filename_prefix=None, filename_postfix = None):

    #import time
    #time_stamp_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

    #import inspect
    #arg_names = inspect.getargspec(write_json_to_file).args
    outputname = "game_output"
    if filename_prefix != None:
        outputname = filename_prefix + "_" + outputname
    outputname = log_output_dir + "/{0}_{1}.log".format(outputname, filename_postfix)
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

def read_games(filename):
    list_of_dicts = []
    with open(filename, 'r') as fd:
        for each_line in fd:
            list_of_dicts.append(json.loads(each_line))
    return list_of_dicts


def print_three_arrays_helper(an_arry, d, flag_for_x=False):
    output_str = "[ " + " ".join([("%4.2f" % item) for item in list(np.round(an_arry, decimals=d))]) + " ]"
    if flag_for_x:
        output_str = output_str.replace("2.00", "O").replace("0.00", "-").replace("1.00", "X")
    return output_str

def print_three_arrays(arr1, arr2, arr3):
    fmt = "{a1:s}\t{a2:s}\t{a3:s}"
    fromhere = 0
    upto = 3
    d = 2
    s1 = print_three_arrays_helper(arr1[fromhere:upto], d)
    for i in range(1, 4):
        upto = i * 3

        print(fmt.format(a1=print_three_arrays_helper(arr1[fromhere:upto], d, True),
                         a2=print_three_arrays_helper(arr2[fromhere:upto], d),
                         a3=print_three_arrays_helper(arr3[fromhere:upto], d)
                         )
             )

        fromhere = upto
