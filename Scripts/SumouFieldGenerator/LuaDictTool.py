'''
Created on 2021/01/04

@author: sa
'''

import re
import json
from _collections import OrderedDict

RE_SUBSTITUTE = "( )*\[([^\[\]]+)\] *= *((.+)(\n.*)*),"
RE_NEWCATEGORY = "( )*\[([^\[\]]+)\] *= *$"
RE_ENDCATEGORY = "( )*}, -- end of \[(.+)\]"
RE_STRING = "\"((.*)(\n.*)*)\"$"
RE_TRUE   = "true$"
RE_FALSE  = "false$"
RE_INT = "-?[0-9]+$"
RE_FLOAT = "-?[0-9]+\.[0-9]*$"

SPACES_PER_INDENT = 4

def parseValue(val):
    match = re.match(RE_STRING,val)
    if(match):
        return match.group(1)
    
    match = re.match(RE_TRUE,val)
    if(match):
        return True
    
    match = re.match(RE_FALSE,val)
    if(match):
        return False
    
    match = re.match(RE_INT,val)
    if(match):
        return int(val)
    
    match = re.match(RE_FLOAT,val)
    if(match):
        return float(val)
    
    print("unknown type:",val)

def load(filename):
    dictStack = []
    currentDict = OrderedDict()
    
    with open(filename) as f:
        lines = f.readlines()
        
        multilineBuf = ""
        
        for line in lines:
            line = multilineBuf + line
            
            if(line[-2] == "\\"):
                multilineBuf = line[0:-2] + "\\\n"
                continue
            else:
                multilineBuf = ""
            
            match1 = re.match(RE_SUBSTITUTE,line)
            match2 = re.match(RE_NEWCATEGORY,line)
            match3 = re.match(RE_ENDCATEGORY,line)
            if(match1):
                variable = parseValue(match1.group(2))
                value = parseValue(match1.group(3))
                # print("add property ",variable," = ",value)
                currentDict[variable] = value
                
            elif(match2):
                # print("new category:" + match2.group(2))
                category = parseValue(match2.group(2))
                currentDict[category] = OrderedDict()
                dictStack.append(currentDict)
                currentDict = currentDict[category]
                
            elif(match3):
                # print("endcategory:" + match3.group(2))
                currentDict = dictStack.pop(len(dictStack)-1)
                
#            else:
#                print("unexpected line:", line)
        
    return currentDict

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
    
    
    