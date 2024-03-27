#!/usr/bin/env python3
import pprint
import os
import re
import sys
import json

### Globals
relPathToLibParseDir = '../../db/parse'
fileNameOpsJson = 'ops.json' 
fileNameOpsTypesJson = 'opsTypes.json' 
relPathToLibAnalysisDir = '../../db/analysis'
fileNameOpsValue = 'opsValues.json'
fileNameOpsVoid = 'opsVoid.json'
relPathToLibResolveDir = '../../db/resolve'

tableUIDOps = {}
tableTypesUIDOps = {}
tableTypesValueOps = {}
tableTypesVoidOps = {}

# Utilities
def insertStr(idx, substring, string) :
    newString = string[:idx] + substring + string[idx:]
    return newString

def insertMultStr(args, string) :
    listChars = list(string)
    for i, arg in enumerate(args) :
        idx = arg[0]+i
        substring = arg[1]
        listChars.insert(idx, substring)
    return ''.join(listChars)



def getNode(uid):
    node = tableUIDOps[uid]
    return node

def getChilds(uid):
    node = getNode(uid)
    childUIDs = node['childUIDs']
    return childUIDs

def getParent(uid):
    node = getNode(uid)
    puid = node['parentUID']
    return puid

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

### Methods
def __init():
    dirParseOps = getAbsPathFromRelPath(relPathToLibParseDir)
    filePathOpsJson = os.path.join(dirParseOps,fileNameOpsJson) 
    filePathOpsTypesJson = os.path.join(dirParseOps,fileNameOpsTypesJson) 
    tableUIDOps  = importFromJson(filePathOpsJson) 
    tableTypesUIDOps = importFromJson(filePathOpsTypesJson) 

    dirAnalysisOps = getAbsPathFromRelPath(relPathToLibAnalysisDir)
    filePathOpsValue = os.path.join(dirAnalysisOps,fileNameOpsValue) 
    filePathOpsVoid = os.path.join(dirAnalysisOps,fileNameOpsVoid) 
    tableTypesValueOps  = importFromJson(filePathOpsValue) 
    tableTypesVoidOps = importFromJson(filePathOpsValue) 
    return tableUIDOps, tableTypesUIDOps, tableTypesValueOps, tableTypesVoidOps


def summarizeValueTable(valueTable, valueType=None) :
    types = None
    if valueType is not None :
        types = [valueType]
    else :
        types = list(valueTable.keys())
    for type in types :
        print(type)
        values = list(valueTable[type].keys())
        values.sort()
        for value in values:
            cnt = str(len(valueTable[type][value]['nodes'])) + ")"
            print(f"    ({cnt:<5}{value}")

def printNode2(UID,lvl=0) :
    node = getNode(UID)
    tab = "----"*lvl
    if node['type'] == 'root' :
        print(node['type']+" "+tab+'root')
    elif node['type'] == 'VOID' :
        print(node['type']+"   "+tab+node['data_line'])
    elif node['type'] == 'thread':
        print(node['type']+" "+tab+node['value'])
    elif node['type'] == 'author':
        print(node['type']+" "+tab+node['value'])
    elif node['type'] == 'edition':
        print(node['type']+""+tab+node['value'])
    elif node['type'] == 'header':
        print(node['type']+" "+tab+node['value'])
    elif node['type'] == 'title':
        print(node['type']+"  "+tab+node['value'])
    elif node['type'] == 'url':
        print(node['type']+"    "+tab+node['value'])
    childs = getChilds(UID)
    for child in childs :
        printNode2(child,lvl+1)


def printNode(uid,lvl=0) :

    node = getNode(uid)
    args = None

    if node['type'] == 'root' :
        print('%%%%%%%% ROOT %%%%%%%%%%')

    elif node['type'] == 'VOID' :
        print(node['data_line'])

    elif node['type'] == 'thread':
        print("-------##"+node['value'])

    elif node['type'] == 'author':

        if node['span2'][0] == -1:
            args = [[0,'<A>'], 
                    [0,'<d>{'], 
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [len(node['data_line']),'</A>'], ]

        else :
            args = [[0,'<A>'], 
                    [0,'<d>{'], 
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [node['span2'][0],'<a>{'],
                    [node['span2'][1],'}</a>'],
                    [len(node['data_line']),'</A>'], ]

    elif node['type'] == 'edition':
        args = [[0,'<E>'], 
                [0,'<d>{'], 
                [node['span'][0],'}</d>'],
                [node['span'][0],'<v>{'],
                [node['span'][1],'}</v>'],
                [len(node['data_line']),'</E>'], ]

    elif node['type'] == 'header':
        args = [[0,'<H>'], 
                [node['span2'][0],'<a>{'],
                [node['span2'][1],'}</a>'],
                [node['span'][0],'<v>{'],
                [node['span'][1],'}</v>'],
                [len(node['data_line']),'</H>'], ]

    elif node['type'] == 'title':

        if node['span2'][0] == -1:
            args = [[0,'<T>'], 
                    [0,'<d>{'], 
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [len(node['data_line']),'</T>'], ]

        else :
            args = [[0,'<T>'], 
                    [0,'<d>{'], 
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [node['span2'][0],'<a>{'],
                    [node['span2'][1],'}</a>'],
                    [len(node['data_line']),'</T>'], ]


    elif node['type'] == 'url':

        if node['span2'][0] == -1:
            args = [[0,'<U>'], 
                    [0,'<d>{'], 
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [len(node['data_line']),'</U>'], ]

        else :
            args = [[0,'<U>'], 
                    [0,'<d>{'], 
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [node['span2'][0],'<a>{'],
                    [node['span2'][1],'}</a>'],
                    [len(node['data_line']),'</U>'], ]

    
    if args is not None :
        line = insertMultStr(args, node['data_line'])
        print(line)

    childs = getChilds(uid)
    for child in childs :
        printNode(child,lvl+1)
  


tableUIDOps, tableTypesUIDOps, tableTypesValueOps, tableTypesVoidOps = __init()
printNode('P0L0')
printNode2('P0L0')
summarizeValueTable(tableTypesValueOps)
#def printrVtable(show=None):
#    summary = {}
#    for type in rVtable:
#        summary[type] = {'invalid':0,'valid':0,'total':0}
#        for value in rVtable[type]:
#            summary[type]['total'] = summary[type]['total'] + 1
#            lines = []
#            bool_pvalue = rVtable[type][value]['pvalue']
#            if show is not None and show != bool_pvalue : 
#                continue
#            lines.append(type+"("+str(bool_pvalue)+")----"+value)
#            for ptype in rVtable[type][value]['parents']:
#                for pvalue in rVtable[type][value]['parents'][ptype]:
#                    lines.append("    "+ptype+"----"+str(pvalue))
#                    for uid in rVtable[type][value]['parents'][ptype][pvalue]['nodes']:
#                        bool_pdiff = rtable[uid]['pdiff']
#                        bool_ptype = rtable[uid]['ptype']
#                        if show is not None and show != bool_ptype : 
#                            break
#                        if show is not None and show != bool_pdiff : 
#                            break
#                        lines.append("        ----"+uid+" D:"+str(bool_pdiff)+" T:"+str(bool_ptype))
#            if len(lines) > 1 :
#                summary[type]['valid'] = summary[type]['valid'] + 1
#                for line in lines :
#                    print(line)
#
#    print("summary")
#    print("----------")
#    for type in summary :
#        data = [str(summary[type]['invalid']),
#                str(summary[type]['valid']),
#                str(summary[type]['total']),]
#        print("    "+type+": " +str(int(data[2]) - int(data[1])) +", "+data[1]+", "+data[2]) 
