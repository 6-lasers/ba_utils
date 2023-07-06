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

# Property 115000c, T1 colorful, 0, 690000 T2/T3 colorful?
# 14375 T1, 86250 T2/T3

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("-d", "--dir", help="help message", default="/home/techen/junk/git/ba-data/Excel")
    
    args = parser.parse_args()
    
    with open(os.path.join(args.dir, "LocalizeEtcExcelTable.json"), "r") as f:
        pass

    furniture_group_keys = []
    with open(os.path.join(args.dir, "GachaCraftNodeExcelTable.json"), "r") as f:
        mydata = json.load(f)
        for item in mydata['DataList']:
            if item['Icon'] == "UIs/01_Common/19_CraftDuration/CraftNode_Furniture":
                furniture_group_keys
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

