'''
Created on 2021/01/03

@author: sa
'''

from collections import OrderedDict
import os
import shutil
import zipfile
import LuaDictTool
import glob

DAY = 21
YEAR = 2016
MONTH = 6



INDENT_NUM = 4

THEATRE = [
        "Caucasus",
        "Nevada",
    ]

COUNTRY_DICT = {
        0: "Russia",
        1: "Ukraine",
        2: "USA",
        4: "UK",
        5: "France",
        6: "Germany",
        7: "USAF Aggressors",
        27: "China",
        46:"Sweden",
    }

def merge(dict1,dict2):
    for key,val in dict2.items():
        if(not key in dict1):
            dict1[key]= val
        else:
            if(isinstance(val,OrderedDict)):
                dict1[key] = merge(dict1[key],dict2[key])
            else:
                dict1[key] = val
    
    return dict1

class FileGenerator():
    def __init__(self,name):
        self.name = name
        self.dict = OrderedDict()
        
    def keyValToString(self,key):
        if(isinstance(key,str)):
            return "\""+key+"\""
        elif(isinstance(key,bool)):
            if(key):
                return "true"
            else:
                return "false"
        else:
            return str(key)
    
    def dumpElement(self,f,indent,element):
        for key,val in element.items():
            f.write(" "*(indent*INDENT_NUM))
            f.write("["+ self.keyValToString(key) + "] = ")
            if(isinstance(val,OrderedDict)):
                f.write("\n")
                f.write(" "*(indent*INDENT_NUM) +"{\n")
                self.dumpElement(f,indent+1,val)
                f.write(" "*(indent*INDENT_NUM))
                f.write("}, -- end of [" + self.keyValToString(key) + "]\n")
            else:
                f.write(self.keyValToString(val)+",\n")
    
    def getDict(self):
        return self.dict
    
    def dump(self):
        filename = "tmp/"+self.name
        LuaDictTool.dump(filename,self.dict,self.name)


class MissionGenerator(FileGenerator):
    def __init__(self,theatre):
        super(MissionGenerator,self).__init__("mission")
        self.dictKeys = OrderedDict()
        self.theatre = theatre
    
    def setDefaultParameters(self):
        self.dict["requiredModules"] = OrderedDict()
        self.dict["date"] = OrderedDict()
        self.dict["date"]["Day"] = DAY
        self.dict["date"]["Year"] = YEAR
        self.dict["date"]["Month"] = MONTH
        self.dict["trig"] = OrderedDict()
        self.dict["trig"]["actions"] = OrderedDict()
        self.dict["trig"]["events"] = OrderedDict()
        self.dict["trig"]["custom"] = OrderedDict()
        self.dict["trig"]["func"] = OrderedDict()
        self.dict["trig"]["flag"] = OrderedDict()
        self.dict["trig"]["conditions"] = OrderedDict()
        self.dict["trig"]["customStartup"] = OrderedDict()
        self.dict["trig"]["funcStartup"] = OrderedDict()
        self.dict["result"] = OrderedDict()
        self.dict["result"]["offline"] = OrderedDict()
        self.dict["result"]["offline"]["conditions"] = OrderedDict()
        self.dict["result"]["offline"]["actions"] = OrderedDict()
        self.dict["result"]["offline"]["func"] = OrderedDict()
        self.dict["result"]["total"] = 0
        self.dict["result"]["blue"] = OrderedDict()
        self.dict["result"]["blue"]["conditions"] = OrderedDict()
        self.dict["result"]["blue"]["actions"] = OrderedDict()
        self.dict["result"]["blue"]["func"] = OrderedDict()
        self.dict["result"]["red"] = OrderedDict()
        self.dict["result"]["red"]["conditions"] = OrderedDict()
        self.dict["result"]["red"]["actions"] = OrderedDict()
        self.dict["result"]["red"]["func"] = OrderedDict()
        self.dict["maxDictId"] = 5
        self.dict["pictureFileNameN"] = OrderedDict()
        self.dict["groundControl"] = OrderedDict()
        self.dict["groundControl"]["isPilotControlVehicles"] = False
        self.dict["groundControl"]["roles"] = OrderedDict()
        self.dict["groundControl"]["roles"]["artillery_commander"] = OrderedDict()
        self.dict["groundControl"]["roles"]["artillery_commander"]["neutrals"] = 0
        self.dict["groundControl"]["roles"]["artillery_commander"]["blue"] = 0
        self.dict["groundControl"]["roles"]["artillery_commander"]["red"] = 0
        self.dict["groundControl"]["roles"]["instructor"] = OrderedDict()
        self.dict["groundControl"]["roles"]["instructor"]["neutrals"] = 0
        self.dict["groundControl"]["roles"]["instructor"]["blue"] = 0
        self.dict["groundControl"]["roles"]["instructor"]["red"] = 0
        self.dict["groundControl"]["roles"]["observer"] = OrderedDict()
        self.dict["groundControl"]["roles"]["observer"]["neutrals"] = 0
        self.dict["groundControl"]["roles"]["observer"]["blue"] = 0
        self.dict["groundControl"]["roles"]["observer"]["red"] = 0
        self.dict["groundControl"]["roles"]["forward_observer"] = OrderedDict()
        self.dict["groundControl"]["roles"]["forward_observer"]["neutrals"] = 0
        self.dict["groundControl"]["roles"]["forward_observer"]["blue"] = 0
        self.dict["groundControl"]["roles"]["forward_observer"]["red"] = 0
        self.dict["goals"] = OrderedDict()
        self.dict["weather"] = OrderedDict()
        self.dict["weather"]["atmosphere_type"] = 0
        self.dict["weather"]["wind"] = OrderedDict()
        self.dict["weather"]["wind"]["at8000"] = OrderedDict()
        self.dict["weather"]["wind"]["at8000"]["speed"] = 0
        self.dict["weather"]["wind"]["at8000"]["dir"] = 0
        self.dict["weather"]["wind"]["at2000"] = OrderedDict()
        self.dict["weather"]["wind"]["at2000"]["speed"] = 0
        self.dict["weather"]["wind"]["at2000"]["dir"] = 0
        self.dict["weather"]["wind"]["atGround"] = OrderedDict()
        self.dict["weather"]["wind"]["atGround"]["speed"] = 0
        self.dict["weather"]["wind"]["atGround"]["dir"] = 0
        self.dict["weather"]["enable_fog"] = False
        self.dict["weather"]["enable_dust"] = False
        self.dict["weather"]["groundTurbulence"] = 0
        self.dict["weather"]["season"] = OrderedDict()
        self.dict["weather"]["season"]["temperature"] = 20
        self.dict["weather"]["type_weather"] = 0
        self.dict["weather"]["qnh"] = 760
        self.dict["weather"]["cyclones"] = OrderedDict()
        self.dict["weather"]["name"] = "Winter, clean sky"
        self.dict["weather"]["dust_density"] = 0
        self.dict["weather"]["fog"] = OrderedDict()
        self.dict["weather"]["fog"]["thickness"] = 0
        self.dict["weather"]["fog"]["visibility"]= 0
        self.dict["weather"]["visibility"] = OrderedDict()
        self.dict["weather"]["visibility"]["distance"] = 80000
        self.dict["weather"]["clouds"] = OrderedDict()
        self.dict["weather"]["clouds"]["thickness"] = 200
        self.dict["weather"]["clouds"]["density"] = 0
        self.dict["weather"]["clouds"]["base"] = 300
        self.dict["weather"]["clouds"]["iprecptns"] = 0
        self.dict["theatre"] = self.theatre
        self.dict["triggers"] = OrderedDict()
        self.dict["triggers"]["zones"] = OrderedDict()
        self.dict["map"] = OrderedDict()
        self.dict["map"]["centerY"] = 0
        self.dict["map"]["zoom"] = 100000
        self.dict["map"]["centerX"] = 0
        self.dict["coalitions"] = OrderedDict()
        self.dict["coalitions"]["neutrals"] = OrderedDict()
        self.dict["coalitions"]["neutrals"][1] = 70
        self.dict["coalitions"]["neutrals"][2] = 23
        self.dict["coalitions"]["neutrals"][3] = 65
        self.dict["coalitions"]["neutrals"][4] = 64
        self.dict["coalitions"]["neutrals"][5] = 25
        self.dict["coalitions"]["neutrals"][6] = 63
        self.dict["coalitions"]["neutrals"][7] = 76
        self.dict["coalitions"]["neutrals"][8] = 29
        self.dict["coalitions"]["neutrals"][9] = 62
        self.dict["coalitions"]["neutrals"][10] = 30
        self.dict["coalitions"]["neutrals"][11] = 31
        self.dict["coalitions"]["neutrals"][12] = 61
        self.dict["coalitions"]["neutrals"][13] = 32
        self.dict["coalitions"]["neutrals"][14] = 33
        self.dict["coalitions"]["neutrals"][15] = 60
        self.dict["coalitions"]["neutrals"][16] = 17
        self.dict["coalitions"]["neutrals"][17] = 35
        self.dict["coalitions"]["neutrals"][18] = 69
        self.dict["coalitions"]["neutrals"][19] = 36
        self.dict["coalitions"]["neutrals"][20] = 59
        self.dict["coalitions"]["neutrals"][21] = 71
        self.dict["coalitions"]["neutrals"][22] = 58
        self.dict["coalitions"]["neutrals"][23] = 57
        self.dict["coalitions"]["neutrals"][24] = 56
        self.dict["coalitions"]["neutrals"][25] = 55
        self.dict["coalitions"]["neutrals"][26] = 73
        self.dict["coalitions"]["neutrals"][27] = 39
        self.dict["coalitions"]["neutrals"][28] = 54
        self.dict["coalitions"]["neutrals"][29] = 72
        self.dict["coalitions"]["neutrals"][30] = 41
        self.dict["coalitions"]["neutrals"][31] = 42
        self.dict["coalitions"]["neutrals"][32] = 44
        self.dict["coalitions"]["neutrals"][33] = 75
        self.dict["coalitions"]["neutrals"][34] = 53
        self.dict["coalitions"]["neutrals"][35] = 22
        self.dict["coalitions"]["neutrals"][36] = 52
        self.dict["coalitions"]["neutrals"][37] = 66
        self.dict["coalitions"]["neutrals"][38] = 51
        self.dict["coalitions"]["neutrals"][39] = 74
        self.dict["coalitions"]["neutrals"][40] = 68
        self.dict["coalitions"]["neutrals"][41] = 50
        self.dict["coalitions"]["neutrals"][42] = 49
        self.dict["coalitions"]["neutrals"][43] = 48
        self.dict["coalitions"]["neutrals"][44] = 67
        self.dict["coalitions"]["neutrals"][45] = 77
        self.dict["coalitions"]["neutrals"][46] = 78
        self.dict["coalitions"]["neutrals"][47] = 79
        self.dict["coalitions"]["neutrals"][48] = 80
        self.dict["coalitions"]["neutrals"][49] = 81
        self.dict["coalitions"]["neutrals"][50] = 82
        self.dict["coalitions"]["neutrals"][51] = 83
        self.dict["coalitions"]["blue"] = OrderedDict()
        self.dict["coalitions"]["blue"][1] = 21
        self.dict["coalitions"]["blue"][2] = 11
        self.dict["coalitions"]["blue"][3] = 8
        self.dict["coalitions"]["blue"][4] = 28
        self.dict["coalitions"]["blue"][5] = 26
        self.dict["coalitions"]["blue"][6] = 13
        self.dict["coalitions"]["blue"][7] = 5
        self.dict["coalitions"]["blue"][8] = 16
        self.dict["coalitions"]["blue"][9] = 6
        self.dict["coalitions"]["blue"][10] = 15
        self.dict["coalitions"]["blue"][11] = 20
        self.dict["coalitions"]["blue"][12] = 12
        self.dict["coalitions"]["blue"][13] = 40
        self.dict["coalitions"]["blue"][14] = 45
        self.dict["coalitions"]["blue"][15] = 9
        self.dict["coalitions"]["blue"][16] = 46
        self.dict["coalitions"]["blue"][17] = 10
        self.dict["coalitions"]["blue"][18] = 3
        self.dict["coalitions"]["blue"][19] = 4
        self.dict["coalitions"]["blue"][20] = 1
        self.dict["coalitions"]["blue"][21] = 2
        self.dict["coalitions"]["red"] = OrderedDict()
        self.dict["coalitions"]["red"][1] = 18
        self.dict["coalitions"]["red"][2] = 24
        self.dict["coalitions"]["red"][3] = 27
        self.dict["coalitions"]["red"][4] = 34
        self.dict["coalitions"]["red"][5] = 37
        self.dict["coalitions"]["red"][6] = 38
        self.dict["coalitions"]["red"][7] = 0
        self.dict["coalitions"]["red"][8] = 43
        self.dict["coalitions"]["red"][9] = 19
        self.dict["coalitions"]["red"][10] = 47
        self.dict["coalitions"]["red"][11] = 7
        self.dict["descriptionText"] = "DictKey_descriptionText_1"
        self.dict["pictureFileNameB"] = OrderedDict()
        self.dict["pictureFileNameR"] = OrderedDict()
        self.dict["descriptionNeutralsTask"] = "DictKey_descriptionNeutralsTask_4"
        self.dict["descriptionBlueTask"] = "DictKey_descriptionBlueTask_3"
        self.dict["descriptionRedTask"] = "DictKey_descriptionRedTask_2"
        self.dict["coalition"] = OrderedDict()
        self.dict["coalition"]["neutrals"] = OrderedDict()
        self.dict["coalition"]["neutrals"]["bullseye"] = OrderedDict()
        self.dict["coalition"]["neutrals"]["bullseye"]["y"] = 0
        self.dict["coalition"]["neutrals"]["bullseye"]["x"] = 0
        self.dict["coalition"]["neutrals"]["nav_points"] = OrderedDict() 
        self.dict["coalition"]["neutrals"]["name"] = "neutrals"
        self.dict["coalition"]["neutrals"]["country"] = OrderedDict()  
        self.dict["coalition"]["blue"] = OrderedDict()
        self.dict["coalition"]["blue"]["bullseye"] = OrderedDict()
        self.dict["coalition"]["blue"]["bullseye"]["y"] = 0
        self.dict["coalition"]["blue"]["bullseye"]["x"] = 0
        self.dict["coalition"]["blue"]["nav_points"] = OrderedDict() 
        self.dict["coalition"]["blue"]["name"] = "blue"
        self.dict["coalition"]["blue"]["country"] = OrderedDict()
        self.dict["coalition"]["red"] = OrderedDict()
        self.dict["coalition"]["red"]["bullseye"] = OrderedDict()
        self.dict["coalition"]["red"]["bullseye"]["y"] = 0
        self.dict["coalition"]["red"]["bullseye"]["x"] = 0
        self.dict["coalition"]["red"]["nav_points"] = OrderedDict() 
        self.dict["coalition"]["red"]["name"] = "neutrals"
        self.dict["coalition"]["red"]["country"] = OrderedDict()
        self.dict["sortie"] = "DictKey_sortie_5"
        self.dict["version"] = 18
        self.dict["trigrules"] = OrderedDict()
        self.dict["currentKey"] = 38
        self.dict["start_time"] = 28800
        self.dict["forcedOptions"] = OrderedDict()
        self.dict["failures"] = OrderedDict()
        
        self.dictKeys["DictKey_descriptionText_1"] = ""
        self.dictKeys["DictKey_descriptionRedTask_2"] = "Shot down all enemies"
        self.dictKeys["DictKey_descriptionBlueTask_3"] = "Shot down all enemies"
        self.dictKeys["DictKey_descriptionNeutralsTask_4"] = ""
        self.dictKeys["DictKey_sortie_5"] = ""
        
    def addAircrafts(self):
        filenames = sorted(glob.glob("ClientAcList"))
        
        acDict = OrderedDict()
        acDict["coalition"] = OrderedDict()
        acDict["coalition"]["blue"] = OrderedDict()
        acDict["coalition"]["blue"]["country"] = OrderedDict()
        acDict["coalition"]["red"] = OrderedDict()
        acDict["coalition"]["red"]["country"] = OrderedDict()
        
        countryIdDict = OrderedDict()
        countryIdDict["blue"] = OrderedDict()
        countryIdDict["red"] = OrderedDict()
        
        countryCount = OrderedDict()
        countryCount["blue"] = 1
        countryCount["red"] = 1
        
        for filename in filenames:
            acDict = LuaDictTool.load(filename)
            coalition = acDict["coalition"]
            if(not acDict["countryId"] in countryIdDict[coalition]):
                countryIdDict[acDict["countryId"]] = countryCount[coalition]
                countryCount[coalition] += 1 
        
        
    def getDictKeys(self):
        return self.dictKeys
        
        
class OptionsGenerator(FileGenerator):
    def __init__(self):
        super(OptionsGenerator,self).__init__("options")
    
    def setDefaultParameters(self):
        self.dict["playerName"]=  "New callsign"
        self.dict["miscellaneous"] = OrderedDict()
        self.dict["miscellaneous"]["allow_server_screenshots"]=  True
        self.dict["miscellaneous"]["headmove"]=  False
        self.dict["miscellaneous"]["TrackIR_external_views"]=  True
        self.dict["miscellaneous"]["f5_nearest_ac"]=  True
        self.dict["miscellaneous"]["f11_free_camera"]=  True
        self.dict["miscellaneous"]["F2_view_effects"]=  1
        self.dict["miscellaneous"]["f10_awacs"]=  True
        self.dict["miscellaneous"]["Coordinate_Display"]=  "Lat Long"
        self.dict["miscellaneous"]["accidental_failures"]=  False
        self.dict["miscellaneous"]["autologin"]=  True
        self.dict["miscellaneous"]["force_feedback_enabled"]=  True
        self.dict["miscellaneous"]["collect_stat"]=  True
        self.dict["miscellaneous"]["chat_window_at_start"]=  True
        self.dict["miscellaneous"]["synchronize_controls"]=  False
        self.dict["miscellaneous"]["show_pilot_body"]=  False
        self.dict["difficulty"] = OrderedDict()
        self.dict["difficulty"]["geffect"]=  "realistic"
        self.dict["difficulty"]["padlock"]=  True
        self.dict["difficulty"]["cockpitStatusBarAllowed"]=  False
        self.dict["difficulty"]["wakeTurbulence"]=  False
        self.dict["difficulty"]["map"]=  True
        self.dict["difficulty"]["easyRadar"]=  False
        self.dict["difficulty"]["fuel"]=  False
        self.dict["difficulty"]["miniHUD"]=  False
        self.dict["difficulty"]["controlsIndicator"]=  True
        self.dict["difficulty"]["birds"]=  0
        self.dict["difficulty"]["optionsView"]=  "optview_all"
        self.dict["difficulty"]["permitCrash"]=  True
        self.dict["difficulty"]["immortal"]=  False
        self.dict["difficulty"]["easyCommunication"]=  True
        self.dict["difficulty"]["cockpitVisualRM"]=  False
        self.dict["difficulty"]["easyFlight"]=  False
        self.dict["difficulty"]["reports"]=  True
        self.dict["difficulty"]["hideStick"]=  False
        self.dict["difficulty"]["radio"]=  False
        self.dict["difficulty"]["userMarks"]=  True
        self.dict["difficulty"]["unrestrictedSATNAV"]=  False
        self.dict["difficulty"]["units"]=  "imperial"
        self.dict["difficulty"]["spectatorExternalViews"]=  True
        self.dict["difficulty"]["tips"]=  True
        self.dict["difficulty"]["userSnapView"]=  True
        self.dict["difficulty"]["RBDAI"]=  True
        self.dict["difficulty"]["externalViews"]=  True
        self.dict["difficulty"]["iconsTheme"]=  "nato"
        self.dict["difficulty"]["avionicsLanguage"]=  "native"
        self.dict["difficulty"]["weapons"]=  False
        self.dict["difficulty"]["setGlobal"]=  True
        self.dict["difficulty"]["labels"]=  True
        self.dict["VR"] = OrderedDict()
        self.dict["VR"]["enable"]=  True
        self.dict["VR"]["box_mouse_cursor"]=  False
        self.dict["VR"]["pixel_density"]=  1
        self.dict["VR"]["use_mouse"]=  True
        self.dict["VR"]["msaaMaskSize"]=  0.42
        self.dict["VR"]["prefer_built_in_audio"]=  True
        self.dict["VR"]["interaction_with_grip_only"]=  False
        self.dict["VR"]["bloom"]=  True
        self.dict["VR"]["custom_IPD_enable"]=  True
        self.dict["VR"]["custom_IPD"]=  "67.5"
        self.dict["VR"]["hand_controllers"]=  True
        self.dict["graphics"] = OrderedDict()
        self.dict["graphics"]["messagesFontScale"]=  1
        self.dict["graphics"]["rainDroplets"]=  True
        self.dict["graphics"]["preloadRadius"]=  150000
        self.dict["graphics"]["heatBlr"]=  1
        self.dict["graphics"]["anisotropy"]=  4
        self.dict["graphics"]["water"]=  2
        self.dict["graphics"]["motionBlur"]=  0
        self.dict["graphics"]["outputGamma"]=  2.2
        self.dict["graphics"]["treesVisibility"]=  6000
        self.dict["graphics"]["aspect"]=  2.6666666666667
        self.dict["graphics"]["textures"]=  2
        self.dict["graphics"]["shadows"]=  1
        self.dict["graphics"]["MSAA"]=  2
        self.dict["graphics"]["SSAA"]=  0
        self.dict["graphics"]["height"]=  2160
        self.dict["graphics"]["forestDistanceFactor"]=  0.5
        self.dict["graphics"]["cockpitGI"]=  1
        self.dict["graphics"]["terrainTextures"]=  "max"
        self.dict["graphics"]["multiMonitorSetup"]=  "lmfcd+camera+rmfcd"
        self.dict["graphics"]["shadowTree"]=  False
        self.dict["graphics"]["chimneySmokeDensity"]=  4
        self.dict["graphics"]["fullScreen"]=  False
        self.dict["graphics"]["DOF"]=  0
        self.dict["graphics"]["clouds"]=  1
        self.dict["graphics"]["flatTerrainShadows"]=  2
        self.dict["graphics"]["useDeferredShading"]=  1
        self.dict["graphics"]["width"]=  5760
        self.dict["graphics"]["SSLR"]=  0
        self.dict["graphics"]["effects"]=  3
        self.dict["graphics"]["SSAO"]=  0
        self.dict["graphics"]["lights"]=  2
        self.dict["graphics"]["sync"]=  False
        self.dict["graphics"]["LensEffects"]=  3
        self.dict["graphics"]["visibRange"]=  "Extreme"
        self.dict["graphics"]["clutterMaxDistance"]=  440
        self.dict["graphics"]["scaleGui"]=  1.5
        self.dict["graphics"]["civTraffic"]=  "high"
        self.dict["plugins"] = OrderedDict()
        self.dict["plugins"]["Su-25T"] = OrderedDict()
        self.dict["plugins"]["Su-25T"]["CPLocalList"]=  "default"
        self.dict["plugins"]["DCS-SRS"] = OrderedDict()
        self.dict["plugins"]["DCS-SRS"]["srsOverlayEnabled"]=  True
        self.dict["plugins"]["DCS-SRS"]["srsAutoLaunchEnabled"]=  True
        self.dict["plugins"]["DCS-SRS"]["srsOverlayCompactModeEnabled"]=  False
        self.dict["plugins"]["F/A-18C"] = OrderedDict()
        self.dict["plugins"]["F/A-18C"]["abDetent"]=  0
        self.dict["plugins"]["F/A-18C"]["canopyReflections"]=  0
        self.dict["plugins"]["F/A-18C"]["hmdEye"]=  1
        self.dict["plugins"]["F/A-18C"]["CPLocalList"]=  "default"
        self.dict["plugins"]["F/A-18C"]["F18RealisticTDC"]=  True
        self.dict["plugins"]["F/A-18C"]["mfdReflections"]=  0
        self.dict["plugins"]["Tacview"] = OrderedDict()
        self.dict["plugins"]["Tacview"]["tacviewDebugMode"]=  0
        self.dict["plugins"]["Tacview"]["tacviewRemoteControlPort"]=  "42675"
        self.dict["plugins"]["Tacview"]["tacviewFlightDataRecordingEnabled"]=  True
        self.dict["plugins"]["Tacview"]["tacviewRealTimeTelemetryPassword"]=  ""
        self.dict["plugins"]["Tacview"]["tacviewSinglePlayerFlights"]=  2
        self.dict["plugins"]["Tacview"]["tacviewTerrainExport"]=  0
        self.dict["plugins"]["Tacview"]["tacviewAutoDiscardFlights"]=  10
        self.dict["plugins"]["Tacview"]["tacviewRemoteControlPassword"]=  ""
        self.dict["plugins"]["Tacview"]["tacviewRealTimeTelemetryPort"]=  "42672"
        self.dict["plugins"]["Tacview"]["tacviewBookmarkShortcut"]=  0
        self.dict["plugins"]["Tacview"]["tacviewRemoteControlEnabled"]=  True
        self.dict["plugins"]["Tacview"]["tacviewMultiplayerFlightsAsHost"]=  2
        self.dict["plugins"]["Tacview"]["tacviewRealTimeTelemetryEnabled"]=  True
        self.dict["plugins"]["Tacview"]["tacviewMultiplayerFlightsAsClient"]=  2
        self.dict["plugins"]["Tacview"]["tacviewModuleEnabled"]=  True
        self.dict["plugins"]["AV8BNA"] = OrderedDict()
        self.dict["plugins"]["AV8BNA"]["CPLocalList"]=  "default"
        self.dict["plugins"]["AV8BNA"]["INS_Alignment"]=  0
        self.dict["plugins"]["AV8BNA"]["INS_GYROHasNAV"]=  False
        self.dict["plugins"]["AV8BNA"]["MPCD_EXPORT"]=  False
        self.dict["plugins"]["Bf-109K-4"] = OrderedDict()
        self.dict["plugins"]["Bf-109K-4"]["cameraOrigin"]=  0
        self.dict["plugins"]["Bf-109K-4"]["aileronTrim"]=  0
        self.dict["plugins"]["Bf-109K-4"]["assistance"]=  100
        self.dict["plugins"]["Bf-109K-4"]["CPLocalList"]=  "default"
        self.dict["plugins"]["Bf-109K-4"]["rudderTrim"]=  0
        self.dict["plugins"]["Bf-109K-4"]["autoRudder"]=  False
        self.dict["plugins"]["FW-190D9"] = OrderedDict()
        self.dict["plugins"]["FW-190D9"]["assistance"]=  100
        self.dict["plugins"]["FW-190D9"]["CPLocalList"]=  "default"
        self.dict["plugins"]["FW-190D9"]["autoRudder"]=  False
        self.dict["plugins"]["M-2000C"] = OrderedDict()
        self.dict["plugins"]["M-2000C"]["UNI_ALIGNED"]=  False
        self.dict["plugins"]["M-2000C"]["AOA_SHOWINHUD"]=  False
        self.dict["plugins"]["M-2000C"]["TDC_GatePPI"]=  5
        self.dict["plugins"]["M-2000C"]["TDC_PPI_is_Polar"]=  False
        self.dict["plugins"]["M-2000C"]["CPLocalList"]=  "default"
        self.dict["plugins"]["M-2000C"]["UNI_NODRIFT"]=  False
        self.dict["plugins"]["M-2000C"]["TDC_KBPrecission"]=  100
        self.dict["plugins"]["A-10C_2"] = OrderedDict()
        self.dict["plugins"]["A-10C_2"]["hmdEye"]=  1
        self.dict["plugins"]["A-10C_2"]["CPLocalList"]=  "aged"
        self.dict["plugins"]["A-10C_2"]["defaultGunMode"]=  0
        self.dict["plugins"]["Ka-50"] = OrderedDict()
        self.dict["plugins"]["Ka-50"]["Ka50TrimmingMethod"]=  0
        self.dict["plugins"]["Ka-50"]["CPLocalList"]=  "default"
        self.dict["plugins"]["Ka-50"]["Ka50RudderTrimmer"]=  False
        self.dict["plugins"]["Ka-50"]["helmetCircleDisplacement"]=  11
        self.dict["plugins"]["CaptoGlove"] = OrderedDict()
        self.dict["plugins"]["CaptoGlove"]["shoulderJointZ_Right"]=  23
        self.dict["plugins"]["CaptoGlove"]["armBending"]=  60
        self.dict["plugins"]["CaptoGlove"]["shoulderJointX_Right"]=  -15
        self.dict["plugins"]["CaptoGlove"]["mouseClickSrc"]=  0
        self.dict["plugins"]["CaptoGlove"]["shoulderJointZ_Left"]=  23
        self.dict["plugins"]["CaptoGlove"]["shoulderJointX_Left"]=  -15
        self.dict["plugins"]["CaptoGlove"]["set_debug"]=  False
        self.dict["plugins"]["CaptoGlove"]["pitchOffsetGlove_Left"]=  0
        self.dict["plugins"]["CaptoGlove"]["yawOffsetGlove_Left"]=  0
        self.dict["plugins"]["CaptoGlove"]["yawOffsetShoulder_Right"]=  0
        self.dict["plugins"]["CaptoGlove"]["useBending"]=  False
        self.dict["plugins"]["CaptoGlove"]["shoulderLength_Right"]=  40
        self.dict["plugins"]["CaptoGlove"]["pitchOffsetGlove_Right"]=  0
        self.dict["plugins"]["CaptoGlove"]["shoulderJointY_Left"]=  -23
        self.dict["plugins"]["CaptoGlove"]["forearmLength_Left"]=  30
        self.dict["plugins"]["CaptoGlove"]["shoulderLength_Left"]=  40
        self.dict["plugins"]["CaptoGlove"]["set_attach"]=  False
        self.dict["plugins"]["CaptoGlove"]["pitchOffsetShoulder_Right"]=  0
        self.dict["plugins"]["CaptoGlove"]["forearmLength_Right"]=  30
        self.dict["plugins"]["CaptoGlove"]["pitchOffsetShoulder_Left"]=  0
        self.dict["plugins"]["CaptoGlove"]["set_symmetrically"]=  False
        self.dict["plugins"]["CaptoGlove"]["yawOffsetShoulder_Left"]=  0
        self.dict["plugins"]["CaptoGlove"]["enable"]=  False
        self.dict["plugins"]["CaptoGlove"]["shoulderJointY_Right"]=  -23
        self.dict["plugins"]["CaptoGlove"]["yawOffsetGlove_Right"]=  0
        self.dict["plugins"]["TF-51D"] = OrderedDict()
        self.dict["plugins"]["TF-51D"]["assistance"]=  100
        self.dict["plugins"]["TF-51D"]["CPLocalList"]=  "default"
        self.dict["plugins"]["TF-51D"]["autoRudder"]=  False
        self.dict["plugins"]["A-10C"] = OrderedDict()
        self.dict["plugins"]["A-10C"]["CPLocalList"]=  "default"
        self.dict["plugins"]["SpitfireLFMkIX"] = OrderedDict()
        self.dict["plugins"]["SpitfireLFMkIX"]["assistance"]=  100
        self.dict["plugins"]["SpitfireLFMkIX"]["aileronTrim"]=  0
        self.dict["plugins"]["SpitfireLFMkIX"]["CPLocalList"]=  "default"
        self.dict["plugins"]["SpitfireLFMkIX"]["autoRudder"]=  False
        self.dict["plugins"]["F-86F"] = OrderedDict()
        self.dict["plugins"]["F-86F"]["landSeatAdjustF86"]=  True
        self.dict["plugins"]["F-86F"]["aiHelper"]=  False
        self.dict["plugins"]["F-86F"]["CPLocalList"]=  "default"
        self.dict["plugins"]["F-86F"]["NoseWheelSteeringSimpleBehaviourF86"]=  True
        self.dict["plugins"]["F-86F"]["gunCamera"]=  0
        self.dict["plugins"]["CA"] = OrderedDict()
        self.dict["plugins"]["CA"]["kompass_options"]=  1
        self.dict["plugins"]["CA"]["ground_target_info"]=  True
        self.dict["plugins"]["CA"]["ground_aim_helper"]=  True
        self.dict["plugins"]["CA"]["ground_platform_shake"]=  True
        self.dict["plugins"]["CA"]["ground_automatic"]=  True
        self.dict["plugins"]["FC3"] = OrderedDict()
        self.dict["plugins"]["FC3"]["CPLocalList_Su-25"]=  "default"
        self.dict["plugins"]["FC3"]["CPLocalList_Su-27"]=  "default"
        self.dict["plugins"]["FC3"]["CPLocalList_A-10A"]=  "default"
        self.dict["plugins"]["FC3"]["CPLocalList_Su-33"]=  "default"
        self.dict["plugins"]["FC3"]["CPLocalList_MiG-29S"]=  "default"
        self.dict["plugins"]["FC3"]["CPLocalList_MiG-29A"]=  "default"
        self.dict["plugins"]["FC3"]["CPLocalList_J-11A"]=  "default"
        self.dict["plugins"]["FC3"]["CPLocalList_MiG-29G"]=  "default"
        self.dict["plugins"]["FC3"]["CPLocalList_F-15C"]=  "default"
        self.dict["plugins"]["AJS37"] = OrderedDict()
        self.dict["plugins"]["AJS37"]["CPLocalList"]=  "default"
        self.dict["plugins"]["F-14"] = OrderedDict()
        self.dict["plugins"]["F-14"]["JESTER_HeadMenu"]=  True
        self.dict["plugins"]["F-14"]["FFB_TRIM"]=  False
        self.dict["plugins"]["F-14"]["JESTER_LandingCallouts"]=  True
        self.dict["plugins"]["F-14"]["AB_GATE"]=  False
        self.dict["plugins"]["F-14"]["JESTER_SwitchToPSTT"]=  True
        self.dict["plugins"]["F-14"]["TID_A2G"]=  False
        self.dict["plugins"]["F-14"]["WEAP_OFF_GUN"]=  False
        self.dict["plugins"]["F-14"]["WEAP_UP_SPPH"]=  False
        self.dict["plugins"]["F-14"]["JESTER_Camera"]=  True
        self.dict["plugins"]["F-14"]["RadioMenuPttOptions"]=  0
        self.dict["plugins"]["UH-1H"] = OrderedDict()
        self.dict["plugins"]["UH-1H"]["UHRudderTrimmer"]=  False
        self.dict["plugins"]["UH-1H"]["autoPilot"]=  True
        self.dict["plugins"]["UH-1H"]["UH1HCockpitShake"]=  50
        self.dict["plugins"]["UH-1H"]["CPLocalList"]=  "default"
        self.dict["plugins"]["UH-1H"]["weapTooltips"]=  True
        self.dict["plugins"]["UH-1H"]["UHTrimmingMethod"]=  0
        self.dict["plugins"]["F-16C"] = OrderedDict()
        self.dict["plugins"]["F-16C"]["abDetent"]=  0
        self.dict["plugins"]["F-16C"]["canopyReflections"]=  0
        self.dict["plugins"]["F-16C"]["hmdEye"]=  1
        self.dict["plugins"]["F-16C"]["CPLocalList"]=  "default"
        self.dict["plugins"]["F-16C"]["canopyTint"]=  1
        self.dict["plugins"]["F-16C"]["mfdReflections"]=  0
        self.dict["format"]=  1
        self.dict["sound"] = OrderedDict()
        self.dict["sound"]["main_output"]=  "{0.0.0.00000000}.{0e20bc54-f5d4-4b89-8848-a8469076827b}"
        self.dict["sound"]["FakeAfterburner"]=  False
        self.dict["sound"]["volume"]=  25
        self.dict["sound"]["headphones_on_external_views"]=  True
        self.dict["sound"]["subtitles"]=  True
        self.dict["sound"]["world"]=  35
        self.dict["sound"]["hear_in_helmet"]=  False
        self.dict["sound"]["radioSpeech"]=  True
        self.dict["sound"]["hp_output"]=  "{0.0.0.00000000}.{0e20bc54-f5d4-4b89-8848-a8469076827b}"
        self.dict["sound"]["cockpit"]=  100
        self.dict["sound"]["voice_chat_output"]=  "0:{0.0.0.00000000}.{305e0a85-05d5-4c5b-9d8d-89995596f9a9}"
        self.dict["sound"]["voice_chat"]=  False
        self.dict["sound"]["microphone_use"]=  2
        self.dict["sound"]["GBreathEffect"]=  True
        self.dict["sound"]["switches"]=  100
        self.dict["sound"]["play_audio_while_minimized"]=  False
        self.dict["sound"]["headphones"]=  100
        self.dict["sound"]["music"]=  0
        self.dict["sound"]["voice_chat_input"]=  "0:{0.0.1.00000000}.{0203fa2c-7930-4da8-819d-7bcbaad7406d}"
        self.dict["sound"]["gui"]=  100
        self.dict["views"] = OrderedDict()
        self.dict["views"]["cockpit"] = OrderedDict()
        self.dict["views"]["cockpit"]["mirrors"]=  False
        self.dict["views"]["cockpit"]["reflections"]=  False
        self.dict["views"]["cockpit"]["avionics"]=  4
        
class WarehousesGenerator(FileGenerator):
    def __init__(self,theatre):
        super(WarehousesGenerator,self).__init__("warehouses")
        self.theatre = theatre
        
    def setDefaultParameters(self,theatreInfo):
        self.dict["airports"] = OrderedDict()
        for airportKey in theatreInfo[self.theatre]["Airports"]:
            intKey = int(airportKey)
            
            self.dict["airports"][intKey] = OrderedDict()
            self.dict["airports"][intKey]
            self.dict["airports"][intKey]["gasoline"] = OrderedDict()
            self.dict["airports"][intKey]["gasoline"]["InitFuel"]=  100
            self.dict["airports"][intKey]["unlimitedMunitions"]=  True
            self.dict["airports"][intKey]["methanol_mixture"] = OrderedDict()
            self.dict["airports"][intKey]["methanol_mixture"]["InitFuel"]=  100
            self.dict["airports"][intKey]["OperatingLevel_Air"]=  10
            self.dict["airports"][intKey]["diesel"] = OrderedDict()
            self.dict["airports"][intKey]["diesel"]["InitFuel"]=  100
            self.dict["airports"][intKey]["speed"]=  16.666666
            self.dict["airports"][intKey]["size"]=  100
            self.dict["airports"][intKey]["periodicity"]=  30
            self.dict["airports"][intKey]["suppliers"] = OrderedDict()
            self.dict["airports"][intKey]["coalition"]=  "NEUTRAL"
            self.dict["airports"][intKey]["jet_fuel"] = OrderedDict()
            self.dict["airports"][intKey]["jet_fuel"]["InitFuel"]=  100
            self.dict["airports"][intKey]["OperatingLevel_Eqp"]=  10
            self.dict["airports"][intKey]["unlimitedFuel"]=  True
            self.dict["airports"][intKey]["aircrafts"] = OrderedDict()
            self.dict["airports"][intKey]["weapons"] = OrderedDict()
            self.dict["airports"][intKey]["OperatingLevel_Fuel"]=  10
            self.dict["airports"][intKey]["unlimitedAircrafts"]=  True
        
class TheatreGenerator():
    def __init__(self,theatre):
        self.theatre = theatre
    
    def dump(self):
        with open("tmp/theatre","w") as f:
            f.write(self.theatre)

class DictionaryGenerator(FileGenerator):
    def __init__(self):
        super(DictionaryGenerator,self).__init__("dictionary")
    
    def addDict(self,newDict):
        for key,value in newDict.items():
            self.dict[key]= value

class MapResourceGenerator(FileGenerator):
    def __init__(self):
        super(MapResourceGenerator,self).__init__("mapResource")


if __name__ == "__main__":
    theatre = THEATRE[0]
    
    dictPath = "tmp/l10n/DEFAULT"
    os.makedirs(dictPath,exist_ok=True)
    
    missionGen = MissionGenerator(theatre=theatre)
    missionGen.setDefaultParameters()
    missionGen.dump()
    
    optionsGen = OptionsGenerator()
    optionsGen.setDefaultParameters()
    optionsGen.dump()
    
    warehousesGen = WarehousesGenerator(theatre=theatre)
    warehousesGen.setDefaultParameters()
    warehousesGen.dump()
    
    theatreGen = TheatreGenerator(theatre)
    theatreGen.dump()
    
    dictionaryGen = DictionaryGenerator()
    dictionaryGen.addDict(missionGen.getDictKeys())
    dictionaryGen.dump()
    
    mapResourceGen = MapResourceGenerator()
    mapResourceGen.dump()
    
    
    
    
    shutil.move("tmp/dictionary",dictPath+"/dictionary")
    shutil.move("tmp/mapResource",dictPath+"/mapResource")
    
    with zipfile.ZipFile('mission.miz',"w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write("tmp/mission",arcname="mission")
        zf.write("tmp/options", arcname="options")
        zf.write("tmp/theatre",arcname="theatre")
        zf.write("tmp/warehouses",arcname="warehouses")
        zf.write("tmp/l10n/DEFAULT/dictionary",arcname="l10n/DEFAULT/dictionary")
        zf.write("tmp/l10n/DEFAULT/mapResource",arcname="l10n/DEFAULT/mapResource")
        
    shutil.move("mission.miz","C:/Users/sa/Saved Games/DCS.openbeta/Missions/mission.miz")

    
    
    #todo update maxDictId
    #todo update trig,func, condition, return
    
    print("mission generated")