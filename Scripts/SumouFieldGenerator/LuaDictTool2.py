import re
import json
from _collections import OrderedDict
from enum import IntEnum,auto

RE_TOPLEVEL = "^[ \t]*([A-Za-z0-9_]+)"
RE_DICT_START = "^[ \t]*{"
RE_DICT_END = "^[ \t]*},?"
RE_PROPERTY_NAME = "^[ \t]*\[\"(.+)\"\]"
RE_PROPERTY_NUM = "^[ \t]*\[([0-9]+)\]"
RE_SUBSTITUTE = "^[ \t]*="
RE_VAL_TRUE = "^[ \t]*true,?"
RE_VAL_FALSE = "^[ \t]*false,?"
RE_VAL_INT = "^[ \t]*(-?[0-9]+),?"
RE_VAL_FLOAT = "^[ \t]*(-?[0-9]*\.[0-9]+),?"
RE_VAL_STRING = "^[ \t]*\"(.*)\",?"
RE_COMMENT = "^[ \t]--.+"

SPACES_PER_INDENT = 4

class TOKEN_TYPE(IntEnum):
    DICT_START = auto()
    DICT_END = auto()
    PROPERTY_NAME = auto()
    PROPERTY_NUM = auto()
    SUBSTITUTE = auto()
    VAL_TRUE = auto()
    VAL_FALSE = auto()
    VAL_INT = auto()
    VAL_FLOAT = auto()
    VAL_STRING = auto()
    COMMENT = auto()
    INVALID = auto()

class STATE(IntEnum):
    IDLE = auto()
    PROPERTY = auto()
    SUBSTITUTE = auto()


def parseLine(line):
    if(match := re.match(RE_DICT_START,line)):
        tokenType = TOKEN_TYPE.DICT_START
        value = None
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_DICT_END,line)):
        tokenType = TOKEN_TYPE.DICT_END
        value = None
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_PROPERTY_NAME,line)):
        tokenType = TOKEN_TYPE.PROPERTY_NAME
        value = str(match.group(1))
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_PROPERTY_NUM,line)):
        tokenType = TOKEN_TYPE.PROPERTY_NUM
        value = int(match.group(1))
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_SUBSTITUTE,line)):
        tokenType = TOKEN_TYPE.SUBSTITUTE
        value = None
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_VAL_TRUE,line)):
        tokenType = TOKEN_TYPE.VAL_TRUE
        value = True
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_VAL_FALSE,line)):
        tokenType = TOKEN_TYPE.VAL_FALSE
        value = False
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_VAL_FLOAT,line)):
        tokenType = TOKEN_TYPE.VAL_FLOAT
        value = float(match.group(1))
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_VAL_INT,line)):
        tokenType = TOKEN_TYPE.VAL_INT
        value = int(match.group(1))
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_VAL_STRING,line)):
        tokenType = TOKEN_TYPE.VAL_STRING
        value = str(match.group(1))
        remainingLine = line[match.span()[1]:]
    elif(match := re.match(RE_COMMENT,line)):
        tokenType = TOKEN_TYPE.COMMENT
        value = None
        remainingLine = ""
    else:
        tokenType= TOKEN_TYPE.INVALID
        value = None
        remainingLine = line
    
    return tokenType,value,remainingLine



def load(filename):
    dictStack = []
    currentDict = OrderedDict()
    
    with open(filename) as f:
        lines = f.readlines()
        state = STATE.SUBSTITUTE    #1line 目を "mission = "等と仮定してスタート
        propertyKey = re.match(RE_TOPLEVEL,lines[0]).group(1)
        dictDepth = 0

        for i in range(1,len(lines)):
            line = lines[i]

            while(True):
                tokenType,value,remainingLine = parseLine(line)


                if(tokenType == TOKEN_TYPE.INVALID or tokenType == TOKEN_TYPE.COMMENT):
                    if(tokenType == TOKEN_TYPE.INVALID and len(line) > 2):  #"\n"は除く
                        print("in ",filename," line ",i+1,"INVALID LINE: ",line)
                    break

                if(state == STATE.IDLE):
                    if(tokenType == TOKEN_TYPE.PROPERTY_NAME or tokenType == TOKEN_TYPE.PROPERTY_NUM):
                        propertyKey = value
                        state = STATE.PROPERTY
                    elif(tokenType == TOKEN_TYPE.DICT_END):
                        currentDict = dictStack.pop(len(dictStack)-1)
                        state = STATE.IDLE
                        dictDepth-=1
                        # print("\tDict end, depth = ",dictDepth)
                    else:
                        print("in ",filename," line",line+1,": AT STATE.IDLE, Invalid token ",tokenType," (",line,")")
                elif(state == STATE.PROPERTY):
                    if(tokenType == TOKEN_TYPE.SUBSTITUTE):
                        state = STATE.SUBSTITUTE
                    else:
                        print("in ",filename," line",line+1,": AT STATE.PROPERTY, Invalid token ",tokenType," (",line,")")
                elif(state == STATE.SUBSTITUTE):
                    if(tokenType == TOKEN_TYPE.VAL_TRUE or tokenType == TOKEN_TYPE.VAL_FALSE or 
                        tokenType == TOKEN_TYPE.VAL_INT or tokenType == TOKEN_TYPE.VAL_FLOAT or tokenType == TOKEN_TYPE.VAL_STRING):
                        currentDict[propertyKey] = value
                        state = STATE.IDLE
                    elif(tokenType == TOKEN_TYPE.DICT_START):
                        newDict = OrderedDict()
                        currentDict[propertyKey] = newDict
                        dictStack.append(currentDict)
                        currentDict = newDict
                        state = STATE.IDLE
                        dictDepth+=1
                        # print("\t",propertyKey," = New Dict, depth = ",dictDepth)
                    else:
                        print("in ",filename," line",line+1,": AT STATE.SUBSTITUTE, Invalid token ",tokenType," (",line,")")

                line = remainingLine

    
    if(dictDepth != 0):
        print("---------parse warning at ",filename,"--------------")
        print("Dict depth not equal to Zero.")
        print("Parse might have failed.")

    topKey = list(currentDict.keys())[0]
    return currentDict[topKey]
        
def keyValToString(key):
        if(isinstance(key,str)):
            return "\""+key+"\""
        elif(isinstance(key,bool)):
            if(key):
                return "true"
            else:
                return "false"
        else:
            return str(key)
    
def dumpElement(f,indent,element):
    for key,val in element.items():
        f.write(" "*(indent*SPACES_PER_INDENT))
        f.write("["+ keyValToString(key) + "] = ")
        if(isinstance(val,OrderedDict)):
            f.write("\n")
            f.write(" "*(indent*SPACES_PER_INDENT) +"{\n")
            dumpElement(f,indent+1,val)
            f.write(" "*(indent*SPACES_PER_INDENT))
            f.write("}, -- end of [" + keyValToString(key) + "]\n")
        else:
            f.write(keyValToString(val)+",\n")

def dump(filename,luaDict,rootname):
    with open(filename,"w",newline="\n") as f:
        f.write(rootname + " = \n")
        f.write("{\n")
        dumpElement(f,1, luaDict)
        f.write("} -- end of " + rootname+"\n")
    


if __name__ == "__main__":
#     # load("SatacMissionBase_v1.4.1/mission")
    print(load("sample_dict.txt"))
#     # load("templateMission/mission")
#     print(load("SatacMissionBase_v1.4.1/mission"))