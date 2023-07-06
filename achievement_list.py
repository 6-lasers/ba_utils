#!/usr/bin/env python
######################################################
#
#    achievement_list.py
#
#  <description>
#
#  Usage: achievement_list.py <args>
#
######################################################

from __future__ import print_function

import sys
import argparse
import os
import json

specific_clear_tags = ['ClearSpecificCampaignStageCount', 'ClearSpecificScenario', 'JoinSpecificRaidCount', 'ClearSpecificWeekDungeonCount', 'ClearSpecificChaserDungeonCount', 'ClearSpecificSchoolDungeonCount']

school_dungeon_id_to_name_mapping = {
    'SchoolA': "Trinity",
    'SchoolB': "Gehenna",
    'SchoolC': "Millenium"
}

def getScenariosFromFile(filename):
    scenario_list = []
    with open(filename, "r") as f:
        part = json.load(f)
        prev_scen = None
        for scenario in part['DataList']:
            if scenario['ScriptKr']:
                if not prev_scen or prev_scen['GroupId'] != scenario['GroupId']:
                    scenario_list.append(scenario)
                prev_scen = scenario
    return scenario_list

def main(argv=None):
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("-f", "--file", help="help message", default="/home/techen/junk/git/ba-data/Excel/MissionExcelTable.json")
    parser.add_argument("--ns", help="omit specific first clear achivements", action="store_true")
    
    args = parser.parse_args()
    
    with open(args.file, "r") as f:
        data = json.load(f)

    with open(os.path.join(os.path.dirname(args.file), "CampaignStageExcelTable.json"), "r") as f:
        campaign_stage = json.load(f)
    with open(os.path.join(os.path.dirname(args.file), "RaidStageExcelTable.json"), "r") as f:
        raid_list = json.load(f)
    with open(os.path.join(os.path.dirname(args.file), "GroundExcelTable.json"), "r") as f:
        ground_list = json.load(f)
    with open(os.path.join(os.path.dirname(args.file), "WeekDungeonExcelTable.json"), "r") as f:
        week_dungeon_list = json.load(f)
    with open(os.path.join(os.path.dirname(args.file), "SchoolDungeonStageExcelTable.json"), "r") as f:
        school_dungeon_list = json.load(f)
    with open(os.path.join(os.path.dirname(args.file), "AcademyLocationExcelTable.json"), "r") as f:
        academy_location = json.load(f)
    with open(os.path.join(os.path.dirname(args.file), "../GlobalExcel/Excel/LocalizeEtcExcelTable.json"), "r") as f:
        localize = json.load(f)
    scenario_list = []
    scenario_list += getScenariosFromFile(os.path.join(os.path.dirname(args.file), "../GlobalExcel/Excel/ScenarioScriptMain1ExcelTable.json"))
    scenario_list += getScenariosFromFile(os.path.join(os.path.dirname(args.file), "../GlobalExcel/Excel/ScenarioScriptMain2ExcelTable.json"))
    scenario_list += getScenariosFromFile(os.path.join(os.path.dirname(args.file), "ScenarioScriptMain2ExcelTable.json"))
    scenario_list += getScenariosFromFile(os.path.join(os.path.dirname(args.file), "ScenarioScriptMain3ExcelTable.json"))

    mission_dict = {}
    for mission in data['DataList']:
        if mission['Category'] == "Achievement" and not (args.ns and mission['CompleteConditionType'] in specific_clear_tags):
            achievement_type = mission['CompleteConditionType']
            if mission['CompleteConditionParameter']:
                # Safe to assume?
                parameter = mission['CompleteConditionParameter'][0]
                if mission['CompleteConditionType'] == 'ClearSpecificCampaignStageCount':
                    specific_stage = [stage for stage in campaign_stage['DataList'] if stage['Id'] == parameter][0]
                    condition_str = specific_stage['Name']
                elif mission['CompleteConditionType'] == 'ClearSpecificScenario':
                    specific_scenario = [scenario for scenario in scenario_list if scenario['GroupId'] == parameter][0]
                    condition_str = mission['Description'][-7:] + "--"
                    if 'TextEn' in specific_scenario:
                        condition_str += specific_scenario['TextEn']
                    else:
                        condition_str += specific_scenario['TextJp']
                elif mission['CompleteConditionType'] == 'JoinSpecificRaidCount':
                    specific_raid = [raid for raid in raid_list['DataList'] if raid['Id'] == parameter][0]
                    specific_ground = [ground for ground in ground_list['DataList'] if ground['Id'] == specific_raid['GroundId']][0]
                    condition_str = specific_raid['RaidBossGroup'] + "-" + specific_raid['Difficulty'] + "-" + specific_ground['StageTopography']
                elif mission['CompleteConditionType'] in ['ClearSpecificWeekDungeonCount', 'ClearSpecificChaserDungeonCount']:
                    specific_dungeon = [dungeon for dungeon in week_dungeon_list['DataList'] if dungeon['StageId'] == parameter][0]
                    if specific_dungeon['WeekDungeonType'] in ["ChaserA", "ChaserB", "ChaserC"]:
                        condition_str = "Bounty-" + specific_dungeon['StageTopography']                    
                    elif specific_dungeon['WeekDungeonType'] == "FindGift":
                        condition_str = "CreditCommission"
                    else:
                        condition_str = "BaseDefenseCommission"
                    condition_str += "-" + chr(ord('A') + specific_dungeon['Difficulty'] - 1)
                elif mission['CompleteConditionType'] == 'ClearSpecificSchoolDungeonCount':
                    specific_dungeon = [dungeon for dungeon in school_dungeon_list['DataList'] if dungeon['StageId'] == parameter][0]
                    condition_str = "Scrimmage-" + school_dungeon_id_to_name_mapping[specific_dungeon['DungeonType']]
                    condition_str += "-" + chr(ord('A') + specific_dungeon['Difficulty'] - 1)
                elif mission['CompleteConditionType'] == 'AcademyLocationAtSpecificRank':
                    specific_location = [location for location in academy_location['DataList'] if location['Id'] == parameter][0]
                    specific_localize = [item for item in localize['DataList'] if item['Key'] == specific_location['LocalizeEtcId']][0]
                    condition_str = specific_localize['NameEn']
                else:
                    condition_str = str(parameter)
                achievement_type += ": " + condition_str
            if achievement_type not in mission_dict:
                mission_dict[achievement_type] = []
            mission_dict[achievement_type].append(mission)

    for achievement_type in mission_dict:
        print(achievement_type)
        # Assuming already in order
        print(", ".join([str(mission['CompleteConditionCount']) for mission in mission_dict[achievement_type]]))
            

    return 0

if __name__ == "__main__":
    sys.exit(main())

