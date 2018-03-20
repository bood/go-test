#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import subprocess
import yaml
import argparse
import sys
import platform

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


PASS_STATUS = "%s[PASS]%s" % (bcolors.OKGREEN, bcolors.ENDC)
FAIL_STATUS = "%s[FAIL]%s" % (bcolors.FAIL, bcolors.ENDC)


MULTI_RUN_GROUPS = ("ladder")
DEFAULT_MULTI_RUNS = 10


group_score = {}
group_total = {}


def my_print(message):
    print(message.encode('utf-8'), end="")
    sys.stdout.flush()


def print_status(moves, is_pass):
    message = ' '.join(moves) if isinstance(moves, list) else str(moves)
    print("%s %s" % (PASS_STATUS if is_pass else FAIL_STATUS, message.encode('utf-8')))
    sys.stdout.flush()


def print_multi_status(results):
    pass_num = sum(x for x in results)
    color = bcolors.WARNING
    if pass_num == len(results):
        color = bcolors.OKGREEN
    elif pass_num == 0:
        color = bcolors.FAIL
    print("%s[%s/%s PASSES]%s" % (color, pass_num, len(results), bcolors.ENDC))
    sys.stdout.flush()


def debug(message):
    if args.debug:
        print("DEBUG: %s" % message, end='')
        sys.stdout.flush()


def find(values, value):
    try:
        return values.index(value)
    except ValueError:
        return -1


def update_score(test, result):
    group = test['group']
    group_total[group] = group_total.get(group, 0) + 1
    group_score[group] = group_score.get(group, 0) + (1 if result else 0)


def mock_single_test(test):
    result = False
    update_score(test, result)
    return ("TEST", result)


def do_single_test(test):
    if test.get('number'):
        if sysform =="Windows":
            gtp = "loadsgf .\sgf\%s %s\n" % (test['sgf'], test['number'])
        else:
            gtp = "loadsgf ./sgf/%s %s\n" % (test['sgf'], test['number'])
    else:
        if sysform =="Windows":
            gtp = "loadsgf .\sgf\%s\n" % test['sgf']
        else:
            gtp = "loadsgf ./sgf/%s\n" % test['sgf']
    gtp += "time_settings 0 100 0\n"  # Ensure playouts are not limited on slow machines
    gtp += "genmove %s" % test['move']
    listgtp = gtp.split('\n')
    gtp = "(echo " + " & echo ".join(listgtp) + ")"
    lines = subprocess.check_output("%s | %s" % (gtp, command), stderr=subprocess.STDOUT, shell=True, encoding='utf8').split("\n")
    #   E1 ->     792 (V: 37.43%) (N: 31.68%) PV: E1 H5 F6 G6 F7 E13 D11 D10 E10 E9 F9 E11
    lines = [line for line in lines if re.match('^\s+[A-Z][0-9]+ +->|^[0-9]+\s+visits', line)]
    debug("\n%s\n" % ("\n".join(lines)))
    line = lines[0]

    match = re.search('\(V: +(\d+\.\d+)%\).+PV: +(.+)', line)
    win_rate = float(match.group(1))
    moves = match.group(2).split(' ')
    next_move = moves[0]

    if test.get('yes_move'):
        yes_moves = [m.upper() for m in test['yes_move']]
        result = next_move in yes_moves
    elif test.get('no_move'):
        no_moves = [m.upper() for m in test['no_move']]
        result = next_move not in no_moves
    elif test.get('max_win_rate'):
        result = win_rate <= float(test['max_win_rate'])
    else:
        raise Exception("Neither yes_move, no_move or win_rate found")

    update_score(test, result)
    return (line, result)

sysform = platform.system() #detect operating system
print (("%s OS") % sysform)

parser = argparse.ArgumentParser(description='Scenario testing tool for Go')
parser.add_argument('--debug', action='store_true', help='Debug messages')
parser.add_argument('--command', help='Override the test command in config.yml')
parser.add_argument('--case', action='append',
                    help='Only run specify cases')
parser.add_argument('--group', action='append',
                    help='Only run cases of specify groups')

args = parser.parse_args()

with open("config.yml", 'r') as stream:
    config = yaml.load(stream)

if args.command:
    command = args.command
else:
    command = config['command']
tests = config['tests']

my_print("Command: %s\n" % command)

for test in tests:
    name = test['name']
    group = test['group']
    sgf = test['sgf']
    if args.case and name not in args.case:
        continue
    if args.group and group not in args.group:
        continue
    my_print("%s - %s (%s)\n" % (name, group, sgf))

    results = []
    for i in range(0, DEFAULT_MULTI_RUNS):
        my_print("%s " % i)
        (line, result) = do_single_test(test)
        results.append(result)
    my_print("\n")
    print_multi_status(results)

for group in group_score:
    color = bcolors.WARNING
    if group_score[group] == 0:
        color = bcolors.FAIL
    elif group_score[group] == group_total[group]:
        color = bcolors.OKGREEN
    my_print("%s: %s[%s/%s PASSES]%s\n" % (group, color, group_score[group], group_total[group], bcolors.ENDC))
