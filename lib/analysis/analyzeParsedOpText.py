#!/usr/bin/env python3
import pprint
import os
import re
import sys
import json

### Globals
opts = {"updateOnly":True,"verbose":True}
if not opts['verbose'] :
    sys.stdout = open(os.devnull, 'w')

relPathToLibParseDir = '../../db/parse'
fileNameOpsJson = 'ops.json' 
fileNameOpsTypesJson = 'opsTypes.json' 
relPathToLibAnalysisDir = '../../db/analysis'
fileNameOpsValue = 'opsValues.json'
fileNameOpsVoid = 'opsVoid.json'
relPathToLibResolveDir = '../../db/Resolve'

tableUIDOps = {}
tableTypesUIDOps = {}
tableTypesValueOps = {}
tableTypesVoidOps = {}

# Utilities
def getParent(node):
    puid = node['parentUID']
    parent = tableUIDOps[puid]
    return parent

def getChilds(node):
    childUIDs = node['childUIDs']
    childs = []
    for cuid in childUIDs :
        childs.append(tableUIDOps[cuid]) 
    return childs

def getNode(uid):
    node = tableUIDOps[uid]
    return node

def getAbsPathFromRelPath(relPathArg):
    dirCurScript = os.path.dirname(__file__)
    dirtyAbsPathArg = os.path.join(dirCurScript, relPathArg) 
    absPathArg = os.path.abspath(dirtyAbsPathArg)
    return absPathArg

def importFromJson(path):
    with open(path, "r") as openfile:
        dict = json.load(openfile)
    return dict

def exportToJson(filePath,dict) :
    json_object = json.dumps(dict, indent=4)
    with open(filePath, "w+") as outfile :
        outfile.write(json_object)

def __exportValueTable() :
    dirLibAnalysis = getAbsPathFromRelPath(relPathToLibAnalysisDir)
    filePathOpsValueJson = os.path.join(dirLibAnalysis,fileNameOpsValue) 
    filePathOpsVoidJson = os.path.join(dirLibAnalysis,fileNameOpsVoid) 
    exportToJson(filePathOpsValueJson,tableTypesValueOps)
    exportToJson(filePathOpsVoidJson,tableTypesVoidOps)

### Methods
def __genValueTable (typeTable) :
    valueTable = {}
    voidTable = {}
    for type in typeTable :
        valueTable[type] = {}
        for uid in typeTable[type] : 
           node = getNode(uid)
           if node['value'] is not None :
               if node['value'].lower() not in valueTable[type] :
                   valueTable[type][node['value'].lower()] = {}
                   valueTable[type][node['value'].lower()]['nodes'] = []
               valueTable[type][node['value'].lower()]['nodes'].append(uid)
               valueTable[type][node['value'].lower()]['type'] = 'value' 
           elif node['data_line'] is not None:
               if node['data_line'].lower() not in valueTable[type] :
                   valueTable[type][node['data_line'].lower()] = {}
                   valueTable[type][node['data_line'].lower()]['nodes'] = []
               valueTable[type][node['data_line'].lower()]['nodes'].append(uid)
               valueTable[type][node['data_line'].lower()]['type'] = 'data_line' 
           else :
               if type not in voidTable :
                   voidTable[type]=[]
               voidTable[type].append(uid)
    return valueTable, voidTable

def __init():
   dirParseOps = getAbsPathFromRelPath(relPathToLibParseDir)
   filePathOpsJson = os.path.join(dirParseOps,fileNameOpsJson) 
   filePathOpsTypesJson = os.path.join(dirParseOps,fileNameOpsTypesJson) 
   tableUIDOps  = importFromJson(filePathOpsJson) 
   tableTypesUIDOps = importFromJson(filePathOpsTypesJson) 
   return tableUIDOps, tableTypesUIDOps


tableUIDOps, tableTypesUIDOps =  __init()
tableTypesValueOps, tableTypesVoidOps = __genValueTable(tableTypesUIDOps)
__exportValueTable()


    

