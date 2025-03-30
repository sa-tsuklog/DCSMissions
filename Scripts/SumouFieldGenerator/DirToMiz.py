'''
Created on 2021/01/04

@author: sa

python3 DirToMiz.py --template Test4

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="description sample")
    parser.add_argument('--template',type=str,default="TemplateMission")
    args = parser.parse_args()

    dt_now = datetime.datetime.now()
    os.makedirs(OUTPUT_DIR_NAME,exist_ok=True)
    outFilename = OUTPUT_DIR_NAME+"/{}_{:04}-{:02}-{:02}_{:02}{:02}{:02}.miz".format("TEST_",dt_now.year,dt_now.month,dt_now.day,dt_now.hour,dt_now.minute,dt_now.second)
    
    with zipfile.ZipFile(outFilename,"w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(args.template+"/mission",arcname="mission")
        zf.write(args.template+"/options", arcname="options")
        zf.write(args.template+"/theatre",arcname="theatre")
        zf.write(args.template+"/warehouses",arcname="warehouses")
        zf.write(args.template+"/l10n/DEFAULT/dictionary",arcname="l10n/DEFAULT/dictionary")
        zf.write(args.template+"/l10n/DEFAULT/mapResource",arcname="l10n/DEFAULT/mapResource")
        
        oggFiles = glob.glob(args.template+"/l10n/DEFAULT/*.ogg")
        for oggFile in oggFiles:
            soundFilename = os.path.basename(oggFile)
            zf.write(args.template+"/l10n/DEFAULT/"+soundFilename,arcname="l10n/DEFAULT/"+soundFilename)
        
        luaFiles = glob.glob(args.template+"/l10n/DEFAULT/*.lua")
        for luaFile in luaFiles:
            luaFilename = os.path.basename(luaFile)
            zf.write(args.template+"/l10n/DEFAULT/"+luaFilename,arcname="l10n/DEFAULT/"+luaFilename)
        
    
    
    #todo update maxDictId
    #todo update trig,func, condition, return
    print("----------------------")
    print("mission generated: ",outFilename)