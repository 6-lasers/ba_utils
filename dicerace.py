#!/usr/bin/env python3
######################################################
#
#    dicerace.py
#
#  <description>
#
#  Usage: dicerace.py <args>
#
######################################################

from __future__ import print_function

import sys
import argparse
import random

def dice_race(laps, rolls, starting_pos=0):
    if (laps and rolls) or (not laps and not rolls):
        print("pick just one pls")
        return False

    cur_pos = starting_pos

    # 18 squares per lap
    lap_length = 18

    eligma_ctr = 0
    eleph_ctr = 0
    credit_ctr = 0
    xp_ctr = 0
    stones_ctr = 0

    roll_ctr = 0
    lap_ctr = 0
    go_ahead_ctr = 0
    while not rolls or roll_ctr < rolls:
        # Assume standard die
        diceroll = random.randint(1,6)
        roll_ctr += 1
        cur_pos = cur_pos + diceroll
        # +3 on position 4
        # +1 on position 10
        # +2 on position 16
        if cur_pos == 4:
            cur_pos += 3
            go_ahead_ctr += 3
        elif cur_pos == 10:
            cur_pos += 1
            go_ahead_ctr += 1
        elif cur_pos == 16:
            cur_pos += 2
            go_ahead_ctr += 2

        # Rewards
        if cur_pos in [1,6,12]:
            eligma_ctr += 1
        elif cur_pos == 2:
            stones_ctr += 6
        elif cur_pos == 3:
            xp_ctr += 6
        elif cur_pos == 5:
            credit_ctr += 800000
        elif cur_pos == 7:
            credit_ctr += 500000
        elif cur_pos == 8:
            stones_ctr += 4
        elif cur_pos == 9:
            credit_ctr += 1200000
        elif cur_pos == 11:
            xp_ctr += 4
        elif cur_pos == 13:
            xp_ctr += 2
        elif cur_pos == 14:
            stones_ctr += 2
        elif cur_pos == 15:
            eleph_ctr += 3
        elif cur_pos == 17:
            eleph_ctr += 2
        elif cur_pos == 0:
            eleph_ctr += 1

        if cur_pos >= lap_length:
            lap_ctr += 1
            cur_pos -= lap_length
            if laps and lap_ctr >= laps:
                break

    print("--sim complete--")
    print(f"Rolls: {roll_ctr}")
    print(f"Laps: {lap_ctr}")
    print(f"# of go-ahead spaces: {go_ahead_ctr}\n")
    print(f"eligma: {eligma_ctr}")
    print(f"credits: {credit_ctr / 1000000}m (AP value {credit_ctr / 3095})")
    print(f"XP: {xp_ctr * 2000} (AP value {xp_ctr * 2000 / 141.075})")
    print(f"stones: {stones_ctr} (credit value: {stones_ctr * 32000}--AP value {stones_ctr * 32000 / 3095})")

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("--laps", type=int, help="help message")
    parser.add_argument("--rolls", type=int, help="help message")
    
    args = parser.parse_args()

    dice_race(args.laps, args.rolls)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

