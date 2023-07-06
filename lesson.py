#!/usr/bin/env python
######################################################
#
#    lesson.py
#
#  <description>
#
#  Usage: lesson.py <args>
#
######################################################

from __future__ import print_function

import sys
import argparse

import json
import os

def localize_lookup(data, localize_id):
    return next((x['NameEn'] for x in data['DataList'] if x['Key'] == localize_id), None)

def get_drop_table(localize, item_data, area):
    drop_table = {}
    for idx,item_id in enumerate(area['ExtraRewardParcelId']):
        item_localize_id = next((x['LocalizeEtcId'] for x in item_data['DataList'] if x['Id'] == item_id), None)
        item_name = localize_lookup(localize, item_localize_id)
        if item_name not in drop_table:
            drop_table[item_name] = 0
        drop_table[item_name] += (area['ExtraRewardProb'][idx] * area['ExtraRewardAmount'][idx])
    return drop_table

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("-f", "--file", help="help message", default="/home/techen/junk/git/ba-data/Excel/AcademyRewardExcelTable.json")
    parser.add_argument("-r", "--rank_filter", help="help message", default="max")
    parser.add_argument("--no-filter", help="help message", action="store_true")
    
    args = parser.parse_args()
    
    #print args.arg
    #if args.name:
    #    print args.name
    with open(args.file, "r") as f:
        data = json.load(f)
    
    with open(os.path.join(os.path.dirname(args.file), "LocalizeEtcExcelTable.json"), "r") as f:
        localize = json.load(f)
    with open(os.path.join(os.path.dirname(args.file), "ItemExcelTable.json"), "r") as f:
        item_data = json.load(f)
    with open(os.path.join(os.path.dirname(args.file), "AcademyZoneExcelTable.json"), "r") as f:
        zone_data = json.load(f)
    with open(os.path.join(os.path.dirname(args.file), "EventContentZoneExcelTable.json"), "r") as f:
        event_zone_data = json.load(f)
    
    translation_table = {
        '샬레 업무관': "Schale Office",
        '샬레 레지던스': "Schale Residence",
        '게헨나 학원': "Gehenna Academy",
        '아비도스 학원': "Abydos Academy",
        '밀레니엄 학원': "Millennium Academy",
        '트리니티 학원': "Trinity Academy",
        '붉은겨울 학원': "Red Winter Academy"
    }
    event_translation_table = {
        '227호 온천장': "Hot Springs Resort No. 227",
        '체육제 스타디움': "Sports Festival Stadium"
    }

    output = {}
    for item in data['DataList']:
        is_event = False
        local_zone_data = zone_data

        if item['Location'] in translation_table:
            location = translation_table[item['Location']]

            if args.rank_filter == "max":
                rank_list = [12]
            elif args.rank_filter == "all":
                rank_list = [1,4,7,10,11,12]
            else:
                rank_list = [int(val) for val in args.rank_filter.split(",")]
        else:
            location = event_translation_table[item['Location']]
            is_event = True
            local_zone_data = event_zone_data

            if args.rank_filter == "max":
                rank_list = [8]
            elif args.rank_filter == "all":
                rank_list = range(1,9)
            else:
                rank_list = [int(val) for val in args.rank_filter.split(",")]

        if location not in output:
            output[location] = {}
        if item['ScheduleGroupId'] not in output[location]:
            zone_item = next((x for x in local_zone_data['DataList'] if x['LocalizeEtcId'] == item['LocalizeEtcId']), None)

            if is_event:
                zone_unlock_rank = (zone_item['EventPointForLocationRank'] // 500)
                if zone_unlock_rank == 0:
                    zone_unlock_rank = 8
            else:
                zone_unlock_rank = zone_item['LocationRankForUnlock']

            output[location][item['ScheduleGroupId']] = {
                'name': localize_lookup(localize, item['LocalizeEtcId']),
                'zone_unlock_rank': zone_unlock_rank,
                'members': []
            }
        if item['LocationRank'] in rank_list:
            if not args.no_filter and item['LocationRank'] < output[location][item['ScheduleGroupId']]['zone_unlock_rank'] and output[location][item['ScheduleGroupId']]['members']:
                output[location][item['ScheduleGroupId']]['members'].pop()
                
            output[location][item['ScheduleGroupId']]['members'].append(item)
    
    for location,data in output.items():
        print(f"{location}:")
        for area_id,area_data in data.items():
            print(f"    id: {area_id} name: {area_data['name']}")
            print(f"    unlock level: {area_data['zone_unlock_rank']}")
            for member in area_data['members']:
                drop_table = get_drop_table(localize, item_data, member)
                print(f"    rank: {member['LocationRank']}")
                print(f"        Bond points: {member['FavorExp']} ({member['ExtraFavorExpProb'] / 100}% chance to double)")
                print(f"        Shard drop chance: {member['SecretStoneProb'] / 100}%")
                for item in drop_table:
                    print(f"        {item} drop chance: {drop_table[item] / 100}%")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

