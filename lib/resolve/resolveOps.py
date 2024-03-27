#!/usr/bin/env python3
import pprint
import os
import re
import sys
import json

### Globals
ov = { 'h': {},
       'b': {},
       'p': { 'top': '../..',
              'bt_values':'db/buffers/t_values',
              'bvalues':'db/buffers/values.txt',
              'ht_uids':'db/parse/opsTypes.json',
              'huidStats':'db/analysis/uidStats.json',
              'ht_values':'db/analysis/opsValues.json',
              'huids':'db/parse/ops.json',
              'ht_valueStats':'db/analysis/uidStats.json',
              'ht_valueAliases':'db/resolve/t_valueAliases.json'},

       'c': { 't_lvls' : { 'root':0,
                           'thread':1,
                           'header':2,
                           'edition':2,
                           'author':2,
                           'title':3,
                           'url':4,
                           'VOID':4, },

              'h_import': [ 'uids',
                            't_uids',
                            't_values'],

              'b_import': [ 't_values',
                            'values', ],

              'h_export': [ 'uidStats',
                            't_valueStats',
                            't_valueAliases'],

              'b_export': [ 't_values',
                            'values'],

              't_valid_ptypes' : { 'root':['root'],
                                   'thread':['root'],
                                   'header':['thread'],
                                   'edition':['thread'],
                                   'author':['thread'],
                                   'title':['author'],
                                   'url':['title'],
                                   'VOID':[],} } }
                   
# Utilities
def getNode(uid):
    node = ov['h']['uids'][uid]
    return node

def getpuid(uid):
    node = getNode(uid)
    puid = node['parentUID']
    return puid

def getcuids(uid):
    node = getNode(uid)
    cuids = node['childUIDs']
    return cuids

def getFromNode(uid,key):
    node = getNode(uid)
    res = node[key]
    return res

def getlvl(uid):
    type = getFromNode(uid,'type')
    lvl = ov['c']['t_lvls'][type]
    return lvl

def valid_plvl(uid,puid):
    res = False
    lvl = getlvl(uid) 
    plvl = getlvl(puid)
    if (lvl - plvl) == 1 :
        res = True
    return res

def valid_ptype(uid,puid):
    res = False
    type = getFromNode(uid,'type')
    ptype = getFromNode(puid,'type')
    valid_ptypes = ov['c']['t_valid_ptypes'][type]
    if ptype in valid_ptypes:
        res = True
    return res

def getValueNode(value, type)  : 
    valueNode = ov['h']['t_values'][type][value]
    return valueNode

def getValue(uid):
    node = getNode(uid)
    type = node['type']
    value = None
    if node['value'] is not None:
        value = node['value']
    elif node['data_line'] is not None:
        value = node['data_line']
    return value,type 

def getAbsPath(relPath):
    scriptFilePath = os.path.dirname(__file__)
    top_dir = os.path.join(scriptFilePath, ov['p']['top']) 
    dirtyAbsPath = os.path.join(top_dir, relPath) 
    absPath = os.path.abspath(dirtyAbsPath)
    return absPath

def importFromJson(filePath):
    with open(filePath, "r") as openfile:
        jsonDict = json.load(openfile)
    return jsonDict

def exportToJson(filePath,jsonDict):
    json_object = json.dumps(jsonDict, indent=4)
    writeFile(filePath,json_object)

def writeFile(filePath,text):
    fileDir = os.path.dirname(filePath)
    if not os.path.isdir(fileDir):
        os.makedirs(fileDir)
    with open(filePath, "w+") as outfile :
        outfile.write(text)

def readFile(filePath):
    with open(filePath, "r") as outfile :
        lines = outfile.read().splitlines()
    return lines

### Hash Methods
def genht_valueAliases():
    hName = 't_valueAliases'
    uName = 'h'+hName
    relPath = ov['p'][uName]
    absPath = getAbsPath(relPath)
    ov['h']['t_valueAliases']={}
    for type in ov['h']['t_values'] :
        ov['h']['t_valueAliases'][type]={}

def genhuidStats():
    hName = 'uidStats'
    uName = 'h' + hName
    uidStats={}
    for uid in ov['h']['uids']:
        uidStats[uid]={'pdiff' : False, 'ptype': False}
        puid = getpuid(uid)
        if puid is not None :
            if valid_plvl(uid,puid) :
                uidStats[uid]['pdiff'] = True
            if valid_ptype(uid,puid) :
                uidStats[uid]['ptype'] = True
    ov['h'][hName] = uidStats 
    
def genht_valueStats():
    t_valueStats={}
    t_values = ov['h']['t_values']
    uidStats=ov['h']['uidStats']
    for type in t_values   :
        t_valueStats[type]={}
        for value in t_values[type] :
            t_valueStats[type][value]={'pvalue': False, 'parents': {}, }
            for uid in t_values[type][value]['nodes'] : 
                puid=getpuid(uid)
                pvalue, ptype = getValue(puid)
                if ptype not in t_valueStats[type][value]['parents'].keys():
                    t_valueStats[type][value]['parents'][ptype]={}
                if pvalue not in t_valueStats[type][value]['parents'][ptype].keys():
                    t_valueStats[type][value]['parents'][ptype][pvalue]={
                        'nodes':[]
                    }
                
                t_valueStats[type][value]['parents'][ptype][pvalue]['nodes'].append(uid)
            keys = t_valueStats[type][value]['parents'].keys()
            if len(keys) == 1:
                values = t_valueStats[type][value]['parents'][list(keys)[0]].keys()
                if len(values) == 1 :
                    t_valueStats[type][value]['pvalue'] = True
    ov['h']['t_valueStats']=t_valueStats

### Buffer Methods
def parsebt_values():
    bName = 't_values'
    uName = 'b'+bName
    relPath = ov['p'][uName]
    absPath = getAbsPath(relPath)
    ov['b'][bName] = {}
    for type in ov['h']['t_values']:
        ov['b'][bName][type] = []
        filePath = os.path.join(absPath,type+'.txt')
        if os.path.exists(filePath) :
            b = readFile(filePath)
            ov['b'][bName][type] = b

def parsebvalues():
    bName = 'values'
    uName = 'b'+bName
    relPath = ov['p'][uName]
    absPath = getAbsPath(relPath)
    ov['b'][bName] = []
    if os.path.exists(absPath) :
        b = readFile(absPath)
        ov['b'][bName] = b

def applybt_values():
    bName = 't_values'
    uName = 'b'+bName
    for type in ov['b'][bName] :
        for line in ov['b'][bName][type] :
            1;

def applybvalues():
    bName = 'values'
    uName = 'b'+bName
    for line in ov['b'][bName] :
        1;

def genbt_values():
    bName = 't_values'
    uName = 'b'+bName
    for type in ov['h'][bName] :
        lines = []
        values = list(ov['h']['t_values'][type].keys()) 
        values.sort()
        for value in values:
            lines.append(value)
        ov['b'][bName][type] = lines

def genbvalues():
    bName = 'values'
    uName = 'b'+bName
    for type in ov['h']['t_values'] :
        lineParts = []
        values = list(ov['h']['t_values'][type].keys()) 
        for value in values:
            lineParts.append([value,type])
        sorted_lineParts= sorted(lineParts, key=lambda x: x[0])
        lines = []
        for part in sorted_lineParts:
            line = (part[0] +" | "+ part[1])
            lines.append(line)
        ov['b'][bName] = lines


def writebt_values():
    bName = 't_values'
    uName = 'b'+bName
    relPath = ov['p'][uName]
    absPath = getAbsPath(relPath)
    for type in ov['b'][bName] :
        lines = ov['b'][bName][type]
        text = '\n'.join(lines)
        filepath = os.path.join(absPath,type+'.txt')
        writeFile(filepath,text)

def writebvalues():
    bName = 'values'
    uName = 'b'+bName
    relPath = ov['p'][uName]
    absPath = getAbsPath(relPath)
    lines = ov['b'][bName]
    text = '\n'.join(lines)
    writeFile(absPath,text)

### Methods
def __init():
    for hName in ov['c']['h_import'] :
        uName = 'h'+hName
        relPath = ov['p'][uName]
        absPath = getAbsPath(relPath)

        print("searching for "+absPath)
        if os.path.exists(absPath) :
            print(uName +" found!")
            h = importFromJson(absPath)
            ov['h'][hName] = h
        else :
            print(uName +" not found!")
            methodName = "gen"+uName
            if methodName in list(globals().keys()) :
                print("generating "+uName)
                globals()[methodName]()

    for bName in ov['c']['b_import']:

        uName = 'b'+bName
        methodName = "parse"+uName
        print("searching for method "+methodName)
        if methodName in list(globals().keys()) :

            print(methodName+" found!")
            globals()[methodName]()

def __genHashes() :
    for hName in ov['c']['h_export'] :
        methodName = "genh"+hName
        print("searching for method "+methodName)
        if methodName in list(globals().keys()) :
            print(methodName+" found!")
            globals()[methodName]()
            
def __applyBuffers() :
    for bName in ov['c']['b_export'] :
        methodName = "applyb"+bName
        if methodName in list(globals().keys()) :
            globals()[methodName]()

def __genBuffers() :
    for bName in ov['c']['b_export']:
        methodName = "genb"+bName
        if methodName in list(globals().keys()) :
            globals()[methodName]()


def __export():
    for hName in ov['c']['h_export']:
        uName = 'h'+hName
        relPath = ov['p'][uName]
        absPath = getAbsPath(relPath)
        exportToJson(absPath,ov['h'][hName])

    for bName in ov['c']['b_export']:
        methodName = "writeb"+bName
        if methodName in list(globals().keys()) :
            globals()[methodName]()
    


                


__init()
__genHashes()
__applyBuffers()
__genBuffers()
__export()

#thread(#ofpost,time)
#value number
#child share table
