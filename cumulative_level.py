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

def xp_sum(leveldata, bounds):
    total = 0
    max_idx = len(leveldata['DataList']) + 1
    if bounds[0] > bounds[1] or bounds[1] < 1 or bounds[0] > max_idx or bounds[1] > max_idx:
        print("bad sum bounds", max_idx)
    else:
        for level in range(bounds[0] - 1, bounds[1] - 1):
            total += leveldata['DataList'][level]['Exp']
    print("Total XP:", total)

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("-f", "--file", help="help message", default="/home/techen/junk/git/ba-data/Excel/AccountLevelExcelTable.json")
    parser.add_argument("--sum", nargs=2, type=int, help="help message")
    parser.add_argument("--list", action="store_true", help="help message")
    
    args = parser.parse_args()
    
    #print args.arg
    #if args.name:
    #    print args.name
    with open(args.file, "r") as f:
        leveldata = json.load(f)
    
    if args.sum:
        xp_sum(leveldata, args.sum)
    if args.list:
        for level in range(len(leveldata['DataList'])):
            print(f"{leveldata['DataList'][level]['Exp']}")
            #print(f"{level + 1} {leveldata['DataList'][level]['Exp']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

