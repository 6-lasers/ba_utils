#!/usr/bin/env python
######################################################
#
#    cumulative_level.py
#
#  <description>
#
#  Usage: cumulative_level.py <args>
#
######################################################

from __future__ import print_function

import sys
import argparse
import json

from cumulative_level import xp_sum

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("-f", "--file", help="help message", default="/home/techen/junk/git/ba-data/Excel/CharacterWeaponLevelExcelTable.json")
    parser.add_argument("--sum", nargs=2, type=int, help="help message")
    
    args = parser.parse_args()
    
    #print args.arg
    #if args.name:
    #    print args.name
    with open(args.file, "r") as f:
        leveldata = json.load(f)
    
    if args.sum:
        xp_sum(leveldata, args.sum)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

