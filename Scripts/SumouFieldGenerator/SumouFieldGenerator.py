'''
Created on 2021/01/04

@author: sa

TODO: 引数省略のためのPresetを作る
TODO: ミッション内日付をSprint/Summer/Autum/Winterぐらいで指定できるようにする
TODO: ミッション内時刻をday/night/時刻ぐらいで指定できるようにする

SATAC用プリセットコマンド：
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud clear --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport all
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud all --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport all
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud clear --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Tbilishi,Sukhumi
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud cloudy --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Tbilishi,Sukhumi
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud clear --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Batumi,Sochi
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud cloudy --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Batumi,Sochi
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud clear --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Kobuleti,Sukhumi
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud cloudy --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Kobuleti,Sukhumi
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud clear --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Sochi,Mozdok
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud cloudy --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Sochi,Mozdok
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud clear --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Maykop,Anapa
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud cloudy --wind 0.0 --distance 80 --AWACSdistance 140 --date all --airport Maykop,Anapa
python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR --template SatacMissionBase_v1.4.6 --cloud clear --wind 0.0 --distance 60 --AWACSdistance 140 --date all --airport Nalchik,Senaki


Guns用プリセットコマンド
python3 SumouFieldGenerator.py --theatre Ca --fileprefix WVR --template Guns_WVRMissionBase_v1.2 --cloud clear --wind 0.0 --distance 15 --AWACSdistance 140 --date all --airport all
python3 SumouFieldGenerator.py --theatre Ca --fileprefix WVR --template Guns_WVRMissionBase_v1.2 --cloud all --wind 0.0 --distance 15 --AWACSdistance 140 --date all --airport all

WW2 Guns用プリセットコマンド
python3 SumouFieldGenerator.py --theatre Ca --fileprefix WW2 --template Guns_WW2_MissionBase_v1.0 --cloud clear --wind 0.0 --distance 15 --AWACSdistance 140 --date all --airport all

'''

from collections import OrderedDict
import os
import shutil
import zipfile
import LuaDictTool2
import glob
import json
import numpy as np
import datetime
from DcsMissionGeneration import TheatreGenerator
from DcsMissionGeneration import WarehousesGenerator
import sys
import argparse
import random
from enum import IntEnum,auto
import copy

OUTPUT_DIR_NAME = "GeneratedMissions"

RANDOM_HEADING = False

TIMEOFDAY_MIN = 12
TIMEOFDAY_MAX = 16

FOG_PROBABILITY = 0.1
DUST_PROBABILITY = 0.02

MIN_RANGE_FROM_EDGE = 150000
# CLIENT_PLANE_RANGE =  50000
# AI_PLANE_RANGE     = 100000
M_PER_NM = 1852

THEATRE = [
        "Caucasus",
        "Nevada",
        "PersianGulf",
        "Syria",
        "MarianaIslands"
    ]

PRESET = [
    "SATAL",
    "SATAC"
]

FEET_CLOUD_BASES = [
	(2756,13780),	#Light Scattered 1
	(4134,8268),	#Light Scattered 2
	(2756,8268),	#High Scattered 1
	(4134,8268),	 #High Scattered 2
	(4134,15157),	#Scattered 1
	(4134,13780),	#Scattered 2
	(5512,16535),	#Scattered 3
	(12402,17913),	#High Scattered 3
	(5512,12402),	#Scattered 4
	(4134,13780),	#Scattered 5
	(8268,17913),	#Scattered 6
	(5512,11024),	#Scattered 7
	(5512,11024),	#Broken 1
	(5512,11024),	#Broken 2
	(2756,16535),	#Broken 3
	(4134,13780),	#Broken 4
	(0,8268),	#Broken 5
	(0,12402),	#Broken 6
	(0,9646),	#Broken 7
	(0,12402),	#Broken 8
	(4134,13780),	#Overcast 1
	(1378,13780),	#Overcast 2
	(2756,11024),	#Overcast 3
	(1378,8268),	#Overcast 4
	(1378,11024),	#Overcast 5
	(1378,9646),	#Overcast 6
	(1378,8268),	#Overcast 7
	(1378,9646),	#Overcast And Rain 1
	(2756,8268),	#Overcast And Rain 2
	(2756,8268),	#Overcast And Rain 3
]

CLOUD_NAMES = [
	"Light Scattered 1",
	"Light Scattered 2",
	"High Scattered 1",
	"High Scattered 2",
	"Scattered 1",
	"Scattered 2",
	"Scattered 3",
	"High Scattered 3",
	"Scattered 4",
	"Scattered 5",
	"Scattered 6",
	"Scattered 7",
	"Broken 1",
	"Broken 2",
	"Broken 3",
	"Broken 4",
	"Broken 5",
	"Broken 6",
	"Broken 7",
	"Broken 8",
	"Overcast 1",
	"Overcast 2",
	"Overcast 3",
	"Overcast 4",
	"Overcast 5",
	"Overcast 6",
	"Overcast 7",
	"Overcast And Rain 1",
	"Overcast And Rain 2",
	"Overcast And Rain 3",
]

DAYS_IN_MONTH = [
    31, #dummy
    31, #1
    28, #2
    31, #3
    30, #4
    31, #5
    30, #6
    31, #7
    31, #8
    30, #9
    31, #10
    30, #11
    31, #12
]

RED_LIVERY_DICT = {
    "F-14B":"vf-74 adversary",
    "F-15C":"65th Aggressor SQN (WA) SUPER_Flanker",
    "F-15ESE":"IDF 69th Hammers Scheme B",
    "F-16C_50":"64th Aggressor 'Ghost'",
    "FA-18C_hornet":"fictional russia air force",
    "J-11A":"usn aggressor vfc-13 'ferris' (fictional)",
    "Su-27":"Mirgorod AFB (Digital camo)",
    "Su-33":"t-10k-5 test paint scheme",
    "E-3A":"nato",
    "A-50":"RF Air Force"
}

STN_START = 200
STN_INCREMENT = 10
RED_STN_OFFSET = 1000


class CLOUD_TYPES(IntEnum):
    CLEAR = auto()
    CLOUDY = auto()
    RAINY = auto()
    ALL = auto()

def relocate(missionDict,theatreInfo,theatre,mClientPlaneDistance,mAiPlaneDistance,bullseyePos=None,radBlueDirection=None):
    if(bullseyePos is None):
        bullseyeXMax = theatreInfo[theatre]["CombatArea"]["X"]["Max"] - MIN_RANGE_FROM_EDGE
        bullseyeXMin = theatreInfo[theatre]["CombatArea"]["X"]["Min"] + MIN_RANGE_FROM_EDGE
        bullseyeYMax = theatreInfo[theatre]["CombatArea"]["Y"]["Max"] - MIN_RANGE_FROM_EDGE
        bullseyeYMin = theatreInfo[theatre]["CombatArea"]["Y"]["Min"] + MIN_RANGE_FROM_EDGE
        
        rndX = np.random.rand()
        rndY = np.random.rand()
        bullseyeX = bullseyeXMax * rndX + bullseyeXMin * (1-rndX)
        bullseyeY = bullseyeYMax * rndY + bullseyeYMin * (1-rndY)
    else:
        bullseyeX = bullseyePos[0]
        bullseyeY = bullseyePos[1]
    
    missionDict["coalition"]["neutrals"]["bullseye"]["x"] = bullseyeX
    missionDict["coalition"]["neutrals"]["bullseye"]["y"] = bullseyeY
    # missionDict["coalition"]["neutrals"]["bullseye"]["x"] = 0
    # missionDict["coalition"]["neutrals"]["bullseye"]["y"] = 0
    
    missionDict["coalition"]["blue"]["bullseye"]["x"] = bullseyeX
    missionDict["coalition"]["blue"]["bullseye"]["y"] = bullseyeY
    
    missionDict["coalition"]["red"]["bullseye"]["x"] = bullseyeX
    missionDict["coalition"]["red"]["bullseye"]["y"] = bullseyeY
    
    missionDict["map"]["centerX"] = bullseyeX
    missionDict["map"]["centerY"] = bullseyeY
    
    #aiRangeScale = np.random.rand()*1.2 + 0.8 # x0.8 ~ 2.0
    aiRangeScale = 1
    
    if(radBlueDirection is None):
        radBlueDirection = np.random.rand() * np.pi * 2

    RAD_DIRECTION_DELTA = 0.001
    NM_AI_RANGE_DELTA = 5.0
    NM_AI_TRACK = 40
    clientCount = OrderedDict()
    clientCount["blue"] = 0
    clientCount["red"] = 0
    clientCount["neutrals"] = 0
    
    aiCount = OrderedDict()
    aiCount["blue"] = 0
    aiCount["red"] = 0
    aiCount["neutrals"] = 0
    
    for coalition in missionDict["coalition"]:
        for countryNo in missionDict["coalition"][coalition]["country"]:
            for groupNo in missionDict["coalition"][coalition]["country"][countryNo]["plane"]["group"]:
                group = missionDict["coalition"][coalition]["country"][countryNo]["plane"]["group"][groupNo]
                
                if(coalition == "blue"):
                    radDirection = radBlueDirection
                else:
                    radDirection = radBlueDirection + np.pi
                
                if(group["units"][1]["skill"] == "Client"):                    
                    startPointX = bullseyeX + mClientPlaneDistance * np.cos(radDirection + RAD_DIRECTION_DELTA*clientCount[coalition])
                    startPointY = bullseyeY + mClientPlaneDistance * np.sin(radDirection + RAD_DIRECTION_DELTA*clientCount[coalition])
                    
                    #print(group["name"],": ",len(group["route"]["points"]))

                    if(len(group["route"]["points"]) <= 3):
                        if(1 in group["route"]["points"]):
                            group["route"]["points"][1]["x"] = startPointX
                            group["route"]["points"][1]["y"] = startPointY
                        
                        if(2 in group["route"]["points"]):
                            group["route"]["points"][2]["x"] = bullseyeX
                            group["route"]["points"][2]["y"] = bullseyeY

                        if(3 in group["route"]["points"]):
                            group["route"]["points"][3]["x"] = bullseyeX + (bullseyeX - startPointX)
                            group["route"]["points"][3]["y"] = bullseyeY + (bullseyeY - startPointY)
                    else:
                        group["route"]["points"][1]["x"] = startPointX
                        group["route"]["points"][1]["y"] = startPointY
                        
                        numWp = len(group["route"]["points"])

                        for i in range(2, numWp - 1):
                            weight = 0.05 * i
                            group["route"]["points"][i]["x"] = (1-weight)*startPointX + weight * bullseyeX
                            group["route"]["points"][i]["y"] = (1-weight)*startPointY + weight * bullseyeY

                        group["route"]["points"][numWp-1]["x"] = bullseyeX
                        group["route"]["points"][numWp-1]["y"] = bullseyeY

                        group["route"]["points"][numWp]["x"] = bullseyeX + 0.95*(bullseyeX - startPointX)
                        group["route"]["points"][numWp]["y"] = bullseyeY + 0.95*(bullseyeY - startPointY)

                    for unitNo in group["units"]:
                        group["units"][unitNo]["x"] = startPointX
                        group["units"][unitNo]["y"] = startPointY
                        if(RANDOM_HEADING):
                            group["units"][unitNo]["heading"] = 2*(np.random.rand()-0.5)*np.pi
                            group["units"][unitNo]["psi"] = 2*(np.random.rand()-0.5)*np.pi
                        else:
                            psi = -radDirection+np.pi
                            if(psi < -np.pi):
                                psi += 2*np.pi
                            if(psi > np.pi):
                                psi -= 2*np.pi
                            
                            group["units"][unitNo]["heading"] = 0
                            group["units"][unitNo]["psi"] = psi
                            
                    clientCount[coalition] += 1
                else:
                    #print(group["name"],": ",len(group["route"]["points"]))
                    if(len(group["route"]["points"]) == 1):
                        startPointX = bullseyeX + mAiPlaneDistance * aiRangeScale * np.cos(radDirection + RAD_DIRECTION_DELTA * aiCount[coalition] * 50)
                        startPointY = bullseyeY + mAiPlaneDistance * aiRangeScale * np.sin(radDirection + RAD_DIRECTION_DELTA * aiCount[coalition] * 50)
                        
                        group["route"]["points"][1]["x"] = startPointX
                        group["route"]["points"][1]["y"] = startPointY
                    else:
                        basePointX = bullseyeX + (mAiPlaneDistance + NM_AI_RANGE_DELTA * M_PER_NM * aiCount[coalition]) * aiRangeScale * np.cos(radDirection)
                        basePointY = bullseyeY + (mAiPlaneDistance + NM_AI_RANGE_DELTA * M_PER_NM * aiCount[coalition]) * aiRangeScale * np.sin(radDirection);

                        startPointX = basePointX + NM_AI_TRACK/2 * M_PER_NM * np.cos(radDirection+np.pi/2)
                        startPointY = basePointY + NM_AI_TRACK/2 * M_PER_NM * np.sin(radDirection+np.pi/2)

                        endPointX = basePointX + NM_AI_TRACK/2 * M_PER_NM * np.cos(radDirection-np.pi/2)
                        endPointY = basePointY + NM_AI_TRACK/2 * M_PER_NM * np.sin(radDirection-np.pi/2)
                        
                        if(aiCount[coalition] % 2 == 1):
                            startPointX,endPointX = endPointX,startPointX
                            startPointY,endPointY = endPointY,startPointY


                        numWp = len(group["route"]["points"])
                        for i in range(0,numWp-2):
                            weight = 0.05 * i
                            group["route"]["points"][i+1]["x"] = (1-weight) * basePointX + weight * startPointX
                            group["route"]["points"][i+1]["y"] = (1-weight) * basePointY + weight * startPointY

                        group["route"]["points"][numWp-1]["x"] = startPointX
                        group["route"]["points"][numWp-1]["y"] = startPointY

                        group["route"]["points"][numWp]["x"] = endPointX
                        group["route"]["points"][numWp]["y"] = endPointY

                    


                    for unitNo in group["units"]:
                            group["units"][unitNo]["x"] = startPointX
                            group["units"][unitNo]["y"] = startPointY
                    
                    aiCount[coalition] += 1
    
    return (bullseyeX,bullseyeY),radBlueDirection

def sanitizeStn(missionDict):
    ##################################
    # Sanitize STN
    ##################################
    global STN_START
    for countryNo in missionDict["coalition"]["blue"]["country"]:
        for groupNo in missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"]:
            groupHaveStn = False
            for unitId in missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"][groupNo]["units"]:
                if("AddPropAircraft" in missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"][groupNo]["units"][unitId] 
                and "STN_L16" in missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"][groupNo]["units"][unitId]["AddPropAircraft"]):
                    missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"][groupNo]["units"][unitId]["AddPropAircraft"]["STN_L16"] = "{:05}".format(STN_START + unitId)
                    groupHaveStn = True

            if(groupHaveStn):
                STN_START = STN_START + STN_INCREMENT

def copyBlueToRed(missionDict):
    ##################################
    # Create unitId conversion dict
    ##################################
    unitIdConversionDict = OrderedDict()
    for countryNo in missionDict["coalition"]["blue"]["country"]:
        for groupNo in missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"]:
            for unitId in missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"][groupNo]["units"]:
                unitIdConversionDict[missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"][groupNo]["units"][unitId]["unitId"]] = -1

    newUnitId = 1
    for missionUnitId in unitIdConversionDict:
        if(unitIdConversionDict[missionUnitId] < 0):
            while(newUnitId in unitIdConversionDict):
                newUnitId += 1
            unitIdConversionDict[missionUnitId] = newUnitId
            newUnitId += 1

    ##################################
    # clear red groups
    ##################################
    missionDict["coalition"]["red"]["country"] = OrderedDict()
    missionDict["coalition"]["red"]["country"][1] = OrderedDict()
    missionDict["coalition"]["red"]["country"][1]["id"] = 81
    missionDict["coalition"]["red"]["country"][1]["name"] = "CJTF Red"
    missionDict["coalition"]["red"]["country"][1]["plane"] = OrderedDict()
    missionDict["coalition"]["red"]["country"][1]["plane"]["group"] = OrderedDict()

    newGroupCount = 1

    ##################################
    # Copy Blue to Red
    ##################################

    for countryNo in missionDict["coalition"]["blue"]["country"]:
        for groupNo in missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"]:
            group = copy.deepcopy(missionDict["coalition"]["blue"]["country"][countryNo]["plane"]["group"][groupNo])
            for unitId in group["units"]:
                if(group["units"][unitId]["type"] in RED_LIVERY_DICT):
                    group["units"][unitId]["livery_id"] = RED_LIVERY_DICT[group["units"][unitId]["type"]]
                else:
                    print("!!Warning: {} does not exist in LIVERY DICT. Livery kept unchanged.".format(group["units"][unitId]["type"]))
                group["units"][unitId]["name"] = group["units"][unitId]["name"].replace("BLUE","RED")
                group["units"][unitId]["name"] = group["units"][unitId]["name"].replace("Blue","Red")
                group["units"][unitId]["name"] = group["units"][unitId]["name"].replace("blue","red")

                group["units"][unitId]["unitId"] = unitIdConversionDict[group["units"][unitId]["unitId"]]

                if("AddPropAircraft" in group["units"][unitId] and "STN_L16" in group["units"][unitId]["AddPropAircraft"]):
                    group["units"][unitId]["AddPropAircraft"]["STN_L16"] = "{:05}".format(int(group["units"][unitId]["AddPropAircraft"]["STN_L16"])+RED_STN_OFFSET)


                if("datalinks" in group["units"][unitId] and "Link16" in group["units"][unitId]["datalinks"] and "network" in group["units"][unitId]["datalinks"]["Link16"] and "teamMembers" in group["units"][unitId]["datalinks"]["Link16"]["network"]):
                    for teamMemberId in group["units"][unitId]["datalinks"]["Link16"]["network"]["teamMembers"]:
                        group["units"][unitId]["datalinks"]["Link16"]["network"]["teamMembers"][teamMemberId]["missionUnitId"] = unitIdConversionDict[group["units"][unitId]["datalinks"]["Link16"]["network"]["teamMembers"][teamMemberId]["missionUnitId"]]

                    for donorId in group["units"][unitId]["datalinks"]["Link16"]["network"]["donors"]:
                        group["units"][unitId]["datalinks"]["Link16"]["network"]["donors"][donorId]["missionUnitId"] = unitIdConversionDict[group["units"][unitId]["datalinks"]["Link16"]["network"]["donors"][donorId]["missionUnitId"]]
                    

            group["name"] = group["name"].replace("BLUE","RED")
            group["name"] = group["name"].replace("Blue","Red")
            group["name"] = group["name"].replace("red","red")

            missionDict["coalition"]["red"]["country"][1]["plane"]["group"][newGroupCount] = group
            newGroupCount += 1

def addStnToName(mittionDict):
    for coalition in ["blue","red"]:
        for countryNo in missionDict["coalition"][coalition]["country"]:
            for groupNo in missionDict["coalition"][coalition]["country"][countryNo]["plane"]["group"]:
                groupHaveStn = False
                stn = ""
                group = missionDict["coalition"][coalition]["country"][countryNo]["plane"]["group"][groupNo]
                for unitId in group["units"]:
                    if("AddPropAircraft" in group["units"][unitId] and "STN_L16" in group["units"][unitId]["AddPropAircraft"]):
                        groupHaveStn = True
                        stn = group["units"][unitId]["AddPropAircraft"]["STN_L16"]
                        break

                if(groupHaveStn):
                    group["name"] = group["name"] + ", STN=" +stn


def setWarehouseCoalition(bullseyePos,radBlueDirection,theatreInfo,theatre,warehouseDict):
    for key,value in theatreInfo[theatre]["Airports"].items():
        radAirportDirection =  np.arctan2(value["Y"]-bullseyePos[1],value["X"]-bullseyePos[0])
        directionDiff = radAirportDirection - radBlueDirection
        if(directionDiff < -np.pi):
            directionDiff += np.pi*2
        if(directionDiff > np.pi):
            directionDiff -= np.pi*2
        
        if(directionDiff < np.pi/2 and directionDiff > -np.pi/2):
            warehouseDict["airports"][int(key)]["coalition"] = "BLUE"
        else:
            warehouseDict["airports"][int(key)]["coalition"] = "RED"
    
    
def setDate(missionDict,date):
    dt_now = datetime.datetime.now()
        
    if(date == "all"):
        month = np.random.randint(1,12)
        day = np.random.randint(1,DAYS_IN_MONTH[month])
        missionDict["date"]["Year"] = dt_now.year
        missionDict["date"]["Month"] = month
        missionDict["date"]["Day"] = day
    elif(date == "spring"):
        month = np.random.randint(3,5)
        day = np.random.randint(1,DAYS_IN_MONTH[month])
        missionDict["date"]["Year"] = dt_now.year
        missionDict["date"]["Month"] = month
        missionDict["date"]["Day"] = day
    elif(date == "summer"):
        month = np.random.randint(6,8)
        day = np.random.randint(1,DAYS_IN_MONTH[month])
        missionDict["date"]["Year"] = dt_now.year
        missionDict["date"]["Month"] = month
        missionDict["date"]["Day"] = day
    elif(date == "autumn"):
        month = np.random.randint(9,11)
        day = np.random.randint(1,DAYS_IN_MONTH[month])
        missionDict["date"]["Year"] = dt_now.year
        missionDict["date"]["Month"] = month
        missionDict["date"]["Day"] = day
    elif(date == "winter"):
        month = np.random.randint(0,3)
        if(month == 0):
            month=12
        day = np.random.randint(1,DAYS_IN_MONTH[month])
        missionDict["date"]["Year"] = dt_now.year
        missionDict["date"]["Month"] = month
        missionDict["date"]["Day"] = day
    else:   #today
        missionDict["date"]["Year"] = dt_now.year
        missionDict["date"]["Month"] = dt_now.month
        missionDict["date"]["Day"] = dt_now.day
    
    rnd = np.random.rand()
    missionDict["start_time"] = 3600 * int(TIMEOFDAY_MAX * rnd + TIMEOFDAY_MIN * (1-rnd))
    
    hour = missionDict["start_time"] // 3600
    min  = (missionDict["start_time"] // 60) % 60
    sec  = (missionDict["start_time"]) % 60
    
    print("Mission Time:{:04}/{:02}/{:02} {:02}-{:02}-{:02}".format(missionDict["date"]["Year"],missionDict["date"]["Month"],missionDict["date"]["Day"],hour,min,sec))

def setWeather(missionDict,weatherTemplates,cloudType=CLOUD_TYPES.ALL):
    probabilityTotal = 0
    cumulativeProbability = OrderedDict()
    
    for key,val in weatherTemplates["Probability"]["Winter"].items():
        probabilityTotal += val
        cumulativeProbability[key] = probabilityTotal
    
    rnd = np.random.rand() * probabilityTotal
    
    for key,val in cumulativeProbability.items():
        if(rnd < val):
            selectedWeather = key
            break
            
    
#     print(rnd,",",key)
#     print(cumulativeProbability)
#     print(weatherTemplates["weathers"].keys())
    #print("Selected weather:",selectedWeather)
    #missionDict["weather"] = weatherTemplates["weathers"][selectedWeather]

    if(cloudType == CLOUD_TYPES.ALL):
        cloudPreset = np.random.randint(0,50)
    elif(cloudType == CLOUD_TYPES.CLEAR):
        cloudPreset = np.random.randint(30,50)
    elif(cloudType == CLOUD_TYPES.CLOUDY):
        cloudPreset = np.random.randint(0,27)
    elif(cloudType == CLOUD_TYPES.RAINY):
        cloudPreset = np.random.randint(27,30)



    if(cloudPreset < 27):
    	missionDict["weather"]["clouds"]["preset"] = "Preset"+str(cloudPreset+1)
    elif(cloudPreset < 30):
    	missionDict["weather"]["clouds"]["preset"] = "RainyPreset"+str(cloudPreset-26)
    else:
    	pass #(no clouds)
    if(cloudPreset < 30):
	    baseRnd = np.random.uniform()
	    cloudBase = FEET_CLOUD_BASES[cloudPreset][0]*baseRnd + FEET_CLOUD_BASES[cloudPreset][1]*(1-baseRnd)
	    missionDict["weather"]["clouds"]["base"] = (int)(cloudBase * 0.3048)
	    print("Cloud Type:",CLOUD_NAMES[cloudPreset],"Base:",int(cloudBase)," [ft]")
    else:
    	print("Cloud Type: No cloud")

def setWind(missionDict,maxWindspeed=50):
    maxTurbulence = maxWindspeed

    WINDSPEED_CONST = maxWindspeed/4
    TURBULENCE_CONST = maxTurbulence/4

    windDirAtGround = np.random.rand()*360
    windDirAt2000   = windDirAtGround + np.random.normal()*60
    windDirAt8000   = windDirAt2000   + np.random.normal()*60

    if(windDirAtGround < 0):
        windDirAtGround += 360
    elif(windDirAtGround > 360):
        windDirAtGround -= 360

    if(windDirAt2000 < 0):
        windDirAt2000 += 360
    elif(windDirAt2000 > 360):
        windDirAt2000 -= 360

    if(windDirAt8000 < 0):
        windDirAt8000 += 360
    elif(windDirAt8000 > 360):
        windDirAt8000 -= 360

    windspeedBase = np.random.exponential()
    windspeedAtGround = WINDSPEED_CONST * (windspeedBase + np.random.normal()/3 - 0.3)
    windspeedAt2000   = WINDSPEED_CONST * (windspeedBase + np.random.normal()/3 - 0.3)
    windspeedAt8000   = WINDSPEED_CONST * (windspeedBase + np.random.normal()/3 - 0.3)
    groundTurbulence  = TURBULENCE_CONST * (windspeedBase + np.random.normal()/3 - 0.3)


    if(windspeedAtGround < 0):
        windspeedAtGround = 0
    #elif(windspeedAtGround > maxWindspeed):
    #	windspeedAtGround = maxWindspeed

    if(windspeedAt2000 < 0):
        windspeedAt2000 = 0
    #elif(windspeedAt2000 > maxWindspeed):
    #	windspeedAt2000 = maxWindspeed

    if(windspeedAt8000 < 0):
        windspeedAt8000 = 0
    #elif(windspeedAt8000 > maxWindspeed):
    #	windspeedAt8000 = maxWindspeed

    if(groundTurbulence < 0):
        groundTurbulence = 0
    #elif(groundTurbulence > maxTurbulence):
    #	groungTurbulence = maxTurbulence


    print("-------------------")
    print("speed at ground:",windspeedAtGround)
    print("speed at 2000:",windspeedAt2000)
    print("speed at 8000:",windspeedAt8000)
    print("turbulence:",groundTurbulence)
    print("dir at ground:",windDirAtGround)
    print("dir at 2000:",windDirAt2000)
    print("dir at 8000:",windDirAt8000)
    print("-------------------")


    missionDict["weather"]["wind"]["atGround"]["speed"] = windspeedAtGround
    missionDict["weather"]["wind"]["atGround"]["dir"] = windDirAtGround

    missionDict["weather"]["wind"]["at2000"]["speed"] = windspeedAt2000
    missionDict["weather"]["wind"]["at2000"]["dir"] = windDirAt2000

    missionDict["weather"]["wind"]["at8000"]["speed"] = windspeedAt8000
    missionDict["weather"]["wind"]["at8000"]["dir"] = windDirAt8000

    missionDict["weather"]["groundTurbulence"] = groundTurbulence
	

def setFogAndDust(missionDict):
	FOG_VISIBILITY_MAX = 6000
	FOG_THICKNESS_MAX = 1000
	DUST_DENSITY_MAX = 3000
	
	FOG_VISIBILITY_CONST = FOG_VISIBILITY_MAX/2
	FOG_THICKNESS_CONST = FOG_THICKNESS_MAX/2
	DUST_DENSITY_CONST = DUST_DENSITY_MAX/2
	
	fogRnd = np.random.rand()
	dustRnd = np.random.rand()
	
	if(fogRnd < FOG_PROBABILITY):
		fogVisibility = FOG_VISIBILITY_MAX - FOG_VISIBILITY_CONST * np.random.exponential()
		fogThickness = FOG_THICKNESS_CONST * np.random.exponential()
		
		if(fogVisibility < 0):
			fogVisibility = 0
		elif(fogVisibility > FOG_VISIBILITY_MAX):
			fogVisibility = FOG_VISIBILITY_MAX
		
		
		if(fogThickness < 0):
			fogThickness = 0
		elif(fogThickness > FOG_THICKNESS_MAX):
			fogThickness = FOG_THICKNESS_MAX
		
		missionDict["weather"]["enable_fog"] = True
		missionDict["weather"]["fog"]["thickness"] = fogThickness
		missionDict["weather"]["fog"]["visibility"] = fogVisibility
		
		#print("Fog thickness = ",fogThickness)
		#print("Fog visibility = ",fogVisibility)
		
	if(dustRnd < DUST_PROBABILITY):
		dustDensity = DUST_DENSITY_CONST * np.random.exponential()
		
		if(dustDensity < 0):
			dustDensity = 0
		elif(dustDensity > DUST_DENSITY_MAX):
			dustDensity = DUST_DENSITY_MAX
		
		missionDict["weather"]["enable_dust"] = True
		missionDict["weather"]["dust_density"] = dustDensity
		
		#print("Dust", dustDensity)
		

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="description sample")
    parser.add_argument('--theatre',default=None,help='Caucasus | Nevada | PersianGulf | Syria')
    parser.add_argument('--distance',type=int,default=45)
    parser.add_argument('--AWACSdistance',type=int,default=120)
    parser.add_argument('--airports',type=str,default=None, help='Kobuleti,Gudauta... | all')
    parser.add_argument('--cloud',type=str,default="all",help='clear|cloudy|rainy|all')
    parser.add_argument('--wind',type=float,default=50.0,help='Max Windspeed[m/s] in float')
    parser.add_argument('--template',type=str,default="TemplateMission")
    parser.add_argument('--fileprefix',type=str,default="GeneratedMission")
    parser.add_argument('--date',type=str,default='today',help='today|spring|summer|autumn|winter|all')

    args = parser.parse_args()

    ##############################################
    # Theatreのパース
    ##############################################
    if(not args.theatre is None):
        theatreCandidates = args.theatre.split(",")
        theatreIndex = np.random.randint(0,len(theatreCandidates))
         
        theatre = THEATRE[0]
        for tmpTheatre in THEATRE:
            if(tmpTheatre.lower().replace(" ","").startswith(theatreCandidates[theatreIndex].lower().replace(" ",""))):
                theatre = tmpTheatre
         
    else:
        theatre = THEATRE[np.random.randint(0,len(THEATRE))]
    
    print("Theatre:",theatre)
    
    with open("TheatreInfo.json") as f:
        theatreInfo = json.load(f)
    
    ##############################################
    # Airportのパース, Bullseye位置の設定
    ##############################################
    airportCandidates = []
    if(not args.airports is None):
        airportNames = args.airports.split(",")

        for airportName in airportNames:
            if(airportName=="all"):
                for key,val in theatreInfo[theatre]["Airports"].items():
                    airportCandidates.append(key)
            else:
                for key,val in theatreInfo[theatre]["Airports"].items():
                    if(val["name"].lower().replace(" ","").startswith(airportName.lower().replace(" ",""))):
                        airportCandidates.append(key)

    if(len(airportCandidates) == 0):
        bullseyePos = None
        radBlueDirection = None
        airportPostfix = ""
    elif(len(airportCandidates) == 1):
        bullseyePos = theatreInfo[theatre]["Airports"][airportCandidates[0]]["X"],theatreInfo[theatre]["Airports"][airportCandidates[0]]["Y"]
        radBlueDirection = None
        airportPostfix = "_"+theatreInfo[theatre]["Airports"][airportCandidates[0]]["name"]
    else:
        airport1,airport2 = random.sample(airportCandidates,2)
        pos1 = (theatreInfo[theatre]["Airports"][airport1]["X"] , theatreInfo[theatre]["Airports"][airport1]["Y"])
        pos2 = (theatreInfo[theatre]["Airports"][airport2]["X"] , theatreInfo[theatre]["Airports"][airport2]["Y"])
        bullseyePos = (pos1[0]+pos2[0])/2,(pos1[1]+pos2[1])/2
        radBlueDirection = np.arctan2(pos1[1]-pos2[1],pos1[0]-pos2[0])
        airportPostfix = "_"+theatreInfo[theatre]["Airports"][airport1]["name"]+"_"+theatreInfo[theatre]["Airports"][airport2]["name"]
    
    ##############################################
    # 距離のパース
    ##############################################
    mClientPlaneDistance = M_PER_NM * args.distance/2
    mAiPlaneDistance = M_PER_NM * args.AWACSdistance/2
    

    ##############################################
    # 雲のパース
    ##############################################
    cloudType = CLOUD_TYPES.ALL
    if("all".startswith(args.cloud.lower().replace(" ",""))):
        cloudType = CLOUD_TYPES.ALL
    elif("clear").startswith(args.cloud.lower().replace(" ","")):
        cloudType = CLOUD_TYPES.CLEAR
    elif("cloudy".startswith(args.cloud.lower().replace(" ",""))):
        cloudType = CLOUD_TYPES.CLOUDY
    elif("rainy".startswith(args.cloud.lower().replace(" ",""))):
        cloudType = CLOUD_TYPES.RAINY
    print(cloudType)
    
    dictPath = "tmp/l10n/DEFAULT"
    os.makedirs(dictPath,exist_ok=True)
    
    try:
        missionDict = LuaDictTool2.load(args.template+"/mission")
        optionsDict = LuaDictTool2.load(args.template+"/options")
        #warehousesDict = LuaDictTool.load("TemplateMission/warehouses")
        warehousesGen = WarehousesGenerator(theatre=theatre)
        warehousesGen.setDefaultParameters(theatreInfo=theatreInfo)
        dictionaryDict = LuaDictTool2.load(args.template+"/l10n/DEFAULT/dictionary")
        mapResourceDict = LuaDictTool2.load(args.template+"/l10n/DEFAULT/mapResource")
        theatreGen = TheatreGenerator(theatre=theatre)
        
        weatherTemplates = LuaDictTool2.load("WeatherTemplates.txt")
    except FileNotFoundError as e:
        print(e)
        sys.exit(0)
    

    setDate(missionDict,args.date)
    setWeather(missionDict,weatherTemplates,cloudType)
    setFogAndDust(missionDict)
    setWind(missionDict,args.wind)
    
    missionDict["theatre"] = theatre
    sanitizeStn(missionDict)
    copyBlueToRed(missionDict)
    addStnToName(missionDict)
    bullseyePos,radBlueDirection = relocate(missionDict,theatreInfo,theatre,mClientPlaneDistance,mAiPlaneDistance,bullseyePos,radBlueDirection)
    
    setWarehouseCoalition(bullseyePos, radBlueDirection, theatreInfo,theatre,warehousesGen.getDict())
    
    
    LuaDictTool2.dump("tmp/mission", missionDict, "mission")
    LuaDictTool2.dump("tmp/options", optionsDict, "options")
    #LuaDictTool.dump("tmp/warehouses", warehousesDict, "warehouses")
    warehousesGen.dump()
    LuaDictTool2.dump("tmp/dictionary", dictionaryDict, "dictionary")
    LuaDictTool2.dump("tmp/mapResource",mapResourceDict, "mapResource")
    theatreGen.dump()
    
    
    shutil.move("tmp/dictionary",dictPath+"/dictionary")
    shutil.move("tmp/mapResource",dictPath+"/mapResource")
    
    
    dt_now = datetime.datetime.now()
    os.makedirs(OUTPUT_DIR_NAME,exist_ok=True)
    outFilename = OUTPUT_DIR_NAME+"/{}_{:04}-{:02}-{:02}_{:02}{:02}{:02}_{}{}.miz".format(args.fileprefix,dt_now.year,dt_now.month,dt_now.day,dt_now.hour,dt_now.minute,dt_now.second,theatre,airportPostfix)
    
    with zipfile.ZipFile(outFilename,"w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write("tmp/mission",arcname="mission")
        zf.write("tmp/options", arcname="options")
        zf.write("tmp/theatre",arcname="theatre")
        zf.write("tmp/warehouses",arcname="warehouses")
        zf.write("tmp/l10n/DEFAULT/dictionary",arcname="l10n/DEFAULT/dictionary")
        zf.write("tmp/l10n/DEFAULT/mapResource",arcname="l10n/DEFAULT/mapResource")
        
        oggFiles = glob.glob(args.template+"/l10n/DEFAULT/*.ogg")
        for oggFile in oggFiles:
            soundFilename = os.path.basename(oggFile)
            shutil.copyfile(oggFile,"tmp/l10n/DEFAULT/"+ soundFilename)
            zf.write("tmp/l10n/DEFAULT/"+soundFilename,arcname="l10n/DEFAULT/"+soundFilename)
        
        luaFiles = glob.glob(args.template+"/l10n/DEFAULT/*.lua")
        for luaFile in luaFiles:
            luaFilename = os.path.basename(luaFile)
            shutil.copyfile(luaFile,"tmp/l10n/DEFAULT/"+ luaFilename)
            zf.write("tmp/l10n/DEFAULT/"+luaFilename,arcname="l10n/DEFAULT/"+luaFilename)
        
    
    
    #todo update maxDictId
    #todo update trig,func, condition, return
    print("----------------------")
    print("mission generated: ",outFilename)