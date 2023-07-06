#!/usr/bin/env python
######################################################
#
#    furniture_crafting.py
#
#  <description>
#
#  Usage: furniture_crafting.py <args>
#
######################################################

from __future__ import print_function

import sys
import argparse
import json
import os

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("-d", "--dir", help="help message", default="/home/techen/junk/git/ba-data/Excel")
    
    args = parser.parse_args()
    
    with open(os.path.join(args.dir, "CafeRankExcelTable.json"), "r") as f:
        mystuff = json.load(f)

    print("AP production:")
    for rank in mystuff['DataList']:
        print(f"base: {rank['ActionPointProductionCorrectionValue']}, coefficient: {rank['ActionPointProductionCoefficient']} total: {rank['ActionPointProductionCorrectionValue'] + (rank['ActionPointProductionCoefficient'] * rank ['ComfortMax'])}")
    print("AP max:")
    for rank in mystuff['DataList']:
        print(rank['ActionPointStorageMax'])
    print("Credit production coefficient:")
    for rank in mystuff['DataList']:
        print(rank['GoldProductionCorrectionValue'] + (rank['GoldProductionCoefficient'] * rank ['ComfortMax']))
    print("Credit max:")
    for rank in mystuff['DataList']:
        print(rank['GoldStorageMax'])
    print("Comfort max:")
    for rank in mystuff['DataList']:
        print(rank['ComfortMax'])
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

