'''
Created on 2021/01/04

@author: sa
'''
from collections import OrderedDict
import os
import shutil
import zipfile
import LuaDictTool
import glob
import json
import numpy as np
import datetime
from DcsMissionGeneration import TheatreGenerator
from DcsMissionGeneration import WarehousesGenerator
import sys
import argparse

RANDOM_HEADING = False

TIMEOFDAY_MIN = 7
TIMEOFDAY_MAX = 17

MIN_RANGE_FROM_EDGE = 150000
# CLIENT_PLANE_RANGE =  50000
# AI_PLANE_RANGE     = 100000
M_PER_NM = 1852

THEATRE = [
        "Caucasus",
        "Nevada",
        "PersianGulf",
        "Syria",
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


def relocate(missionDict,theatreInfo,theatre,mClientPlaneDistance,mAiPlaneDistance):
    bullseyeXMax = theatreInfo[theatre]["CombatArea"]["X"]["Max"] - MIN_RANGE_FROM_EDGE
    bullseyeXMin = theatreInfo[theatre]["CombatArea"]["X"]["Min"] + MIN_RANGE_FROM_EDGE
    bullseyeYMax = theatreInfo[theatre]["CombatArea"]["Y"]["Max"] - MIN_RANGE_FROM_EDGE
    bullseyeYMin = theatreInfo[theatre]["CombatArea"]["Y"]["Min"] + MIN_RANGE_FROM_EDGE
    
    rndX = np.random.rand()
    rndY = np.random.rand()
    bullseyeX = bullseyeXMax * rndX + bullseyeXMin * (1-rndX)
    bullseyeY = bullseyeYMax * rndY + bullseyeYMin * (1-rndY)
    
    #missionDict["coalition"]["neutrals"]["bullseye"]["x"] = bullseyeX
    #missionDict["coalition"]["neutrals"]["bullseye"]["y"] = bullseyeY
    missionDict["coalition"]["neutrals"]["bullseye"]["x"] = 0
    missionDict["coalition"]["neutrals"]["bullseye"]["y"] = 0
    
    missionDict["coalition"]["blue"]["bullseye"]["x"] = bullseyeX
    missionDict["coalition"]["blue"]["bullseye"]["y"] = bullseyeY
    
    missionDict["coalition"]["red"]["bullseye"]["x"] = bullseyeX
    missionDict["coalition"]["red"]["bullseye"]["y"] = bullseyeY
    
    missionDict["map"]["centerX"] = bullseyeX
    missionDict["map"]["centerY"] = bullseyeY
    
    #aiRangeScale = np.random.rand()*1.2 + 0.8 # x0.8 ~ 2.0
    aiRangeScale = 1
    
    radBlueDirection = np.random.rand() * np.pi * 2
    RAD_DIRECTION_DELTA = 0.001
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
                    
                    group["route"]["points"][1]["x"] = startPointX
                    group["route"]["points"][1]["y"] = startPointY
                    
                    group["route"]["points"][2]["x"] = bullseyeX
                    group["route"]["points"][2]["y"] = bullseyeY
                    
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
                    startPointX = bullseyeX + mAiPlaneDistance * aiRangeScale * np.cos(radDirection + RAD_DIRECTION_DELTA * aiCount[coalition] * 50);
                    startPointY = bullseyeY + mAiPlaneDistance * aiRangeScale * np.sin(radDirection + RAD_DIRECTION_DELTA * aiCount[coalition] * 50);
                     
                    group["route"]["points"][1]["x"] = startPointX
                    group["route"]["points"][1]["y"] = startPointY
                     
                    for unitNo in group["units"]:
                        group["units"][unitNo]["x"] = startPointX
                        group["units"][unitNo]["y"] = startPointY
                    
                    
                    aiCount[coalition] += 1
    
    return (bullseyeX,bullseyeY),radBlueDirection

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
    
    
def setDate(missionDict):
    dt_now = datetime.datetime.now()
    dt_now.year
    
    missionDict["date"]["Year"] = dt_now.year
    missionDict["date"]["Month"] = dt_now.month
    missionDict["date"]["Day"] = dt_now.day
    
    rnd = np.random.rand()
    missionDict["start_time"] = 3600 * int(TIMEOFDAY_MAX * rnd + TIMEOFDAY_MIN * (1-rnd))
    
    hour = missionDict["start_time"] // 3600
    min  = (missionDict["start_time"] // 60) % 60
    sec  = (missionDict["start_time"]) % 60
    
    print("Mission Time:{:04}/{:02}/{:02} {:02}-{:02}-{:02}".format(missionDict["date"]["Year"],missionDict["date"]["Month"],missionDict["date"]["Day"],hour,min,sec))

def setWeather(missionDict,weatherTemplates):
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
    cloudPreset = np.random.randint(0,30)
    if(cloudPreset < 27):
    	missionDict["weather"]["clouds"]["preset"] = "Preset"+str(cloudPreset+1)
    else:
    	missionDict["weather"]["clouds"]["preset"] = "RainyPreset"+str(cloudPreset-26)
    baseRnd = np.random.uniform()
    cloudBase = FEET_CLOUD_BASES[cloudPreset][0]*baseRnd + FEET_CLOUD_BASES[cloudPreset][1]*(1-baseRnd)
    missionDict["weather"]["clouds"]["base"] = (int)(cloudBase * 0.3048)
    print("Cloud Type:",CLOUD_NAMES[cloudPreset],"Base:",int(cloudBase)," [ft]")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="description sample")
    parser.add_argument('--theatre',default=None,help='Caucasus | Nevada | PersianGulf | Syria')
    parser.add_argument('--distance',type=int,default=45)
    parser.add_argument('--AWACSdistance',type=int,default=150)
    args = parser.parse_args()
    
    
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
    
    
    mClientPlaneDistance = M_PER_NM * args.distance/2
    mAiPlaneDistance = M_PER_NM * args.AWACSdistance/2
    
    
    dictPath = "tmp/l10n/DEFAULT"
    os.makedirs(dictPath,exist_ok=True)
    
    missionDict = LuaDictTool.load("TemplateMission/mission")
    optionsDict = LuaDictTool.load("TemplateMission/options")
    #warehousesDict = LuaDictTool.load("TemplateMission/warehouses")
    warehousesGen = WarehousesGenerator(theatre=theatre)
    warehousesGen.setDefaultParameters(theatreInfo=theatreInfo)
    dictionaryDict = LuaDictTool.load("TemplateMission/l10n/DEFAULT/dictionary")
    mapResourceDict = LuaDictTool.load("TemplateMission/l10n/DEFAULT/mapResource")
    theatreGen = TheatreGenerator(theatre=theatre)
    
    weatherTemplates = LuaDictTool.load("WeatherTemplates.txt")
    
    
    setDate(missionDict)
    setWeather(missionDict,weatherTemplates)
    
    
    missionDict["theatre"] = theatre
    bullseyePos,radBlueDirection = relocate(missionDict,theatreInfo,theatre,mClientPlaneDistance,mAiPlaneDistance)
    
    setWarehouseCoalition(bullseyePos, radBlueDirection, theatreInfo,theatre,warehousesGen.getDict())
    
    
    LuaDictTool.dump("tmp/mission", missionDict, "mission")
    LuaDictTool.dump("tmp/options", optionsDict, "options")
    #LuaDictTool.dump("tmp/warehouses", warehousesDict, "warehouses")
    warehousesGen.dump()
    LuaDictTool.dump("tmp/dictionary", dictionaryDict, "dictionary")
    LuaDictTool.dump("tmp/mapResource",mapResourceDict, "mapResource")
    theatreGen.dump()
    
    
    shutil.move("tmp/dictionary",dictPath+"/dictionary")
    shutil.move("tmp/mapResource",dictPath+"/mapResource")
    
    
    dt_now = datetime.datetime.now()
    outFilename = "GeneratedMission_{:04}-{:02}-{:02}_{:02}{:02}{:02}_{}.miz".format(dt_now.year,dt_now.month,dt_now.day,dt_now.hour,dt_now.minute,dt_now.second,theatre);
    
    with zipfile.ZipFile(outFilename,"w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write("tmp/mission",arcname="mission")
        zf.write("tmp/options", arcname="options")
        zf.write("tmp/theatre",arcname="theatre")
        zf.write("tmp/warehouses",arcname="warehouses")
        zf.write("tmp/l10n/DEFAULT/dictionary",arcname="l10n/DEFAULT/dictionary")
        zf.write("tmp/l10n/DEFAULT/mapResource",arcname="l10n/DEFAULT/mapResource")
        
        oggFiles = glob.glob("TemplateMission/l10n/DEFAULT/*.ogg")
        for oggFile in oggFiles:
            soundFilename = os.path.basename(oggFile)
            shutil.copyfile(oggFile,"tmp/l10n/DEFAULT/"+ soundFilename)
            zf.write("tmp/l10n/DEFAULT/"+soundFilename,arcname="l10n/DEFAULT/"+soundFilename)
        
        
    #shutil.move("mission.miz","C:/Users/sa/Saved Games/DCS.openbeta/Missions/mission.miz")

    
    
    #todo update maxDictId
    #todo update trig,func, condition, return
    print("----------------------")
    print("mission generated: ",outFilename)