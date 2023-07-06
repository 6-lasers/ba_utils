#!/usr/bin/env python
######################################################
#
#    draw.py
#
#  <description>
#
#  Usage: draw.py <args>
#
######################################################

from __future__ import print_function

import sys
import argparse
import os
import json

type_decode = {
    1 : "Credits",
    10000 : "Aru shards",
    23 : "Eligma"
    16012 : "NY Junko shards",
}

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("event", help="help message")
    parser.add_argument("-d", "--dir", help="help message", default="/home/techen/junk/git/ba-data/Excel")
    
    args = parser.parse_args()
    
    if args.event == "68":
        eventId = 809
    elif args.event == "gourmet":
        eventId = 820
    else:
        print("Invalid event type")
        sys.exit(1)

    with open(os.path.join(args.dir, "EventContentFortuneGachaShopExcelTable.json"), "r") as f:
        mydata = json.load(f)
        cards = [card for card in mydata['DataList'] if card['EventContentId'] == eventId]

    card_grades = {}
    for card in cards:
        if card['Grade'] not in card_grades:
            card_grades[card['Grade']] = card
        else:
            grade = card_grades[card['Grade']]
            if card['RewardParcelId'] == grade['RewardParcelId'] and card['RewardParcelAmount'] == grade['RewardParcelAmount']:
                grade['Prob'] += card['Prob']
            else:
                mod_grade = card['Grade'] + 0.5
                if mod_grade not in card_grades:
                    card_grades[mod_grade] = card
                else:
                    card_grades[mod_grade]['Prob'] += card['Prob']
    for grade in sorted(card_grades.keys()):
        grade_data = card_grades[grade]
        print(f"{grade_data['Prob'] / 10000:.2%}")
        for i,itype in enumerate(grade_data['RewardParcelId']):
            print(f"{type_decode[itype]}: {grade_data['RewardParcelAmount'][i]}")

    return 0

if __name__ == "__main__":
    sys.exit(main())

