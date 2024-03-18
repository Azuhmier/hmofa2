#!/usr/bin/env python3
import os
import re
import sys

opts = {"updateOnly":True,"verbose":True}
if not opts['verbose'] :
    sys.stdout = open(os.devnull, 'w')

reTitle = re.compile("^>([^\[(]+?)<*(?:(?:\s*-*\s*[\[(]\s*([^\[\]()]+)\s*[\])])|(?:\s+-\s+(.+)|\s+((?:pt\.?|part|ch\.?|chapter)\s+\d+)|))$")
reAuthor = re.compile("^[bB]y\s([^\[(]+?)(?:[- ]*[\[(]\s*([^\[\]()]+)\s*[\])])*$")
reUrl =  re.compile("^(http[^ ]+)(?:[- ]*[\[(]\s*([^\[\]()]+)\s*[\])])*$")
reEdition = re.compile(r"^(?:>|\")\s*([^>\"]+)\s*(?:<|\")\s*edition$")
reHeader = re.compile("^/(\w+)/.*#(\d+)$")

relPathToOpsDir = '../../threads/ops'

parentNode = {'value':None,
              'type':'root',
              'childs':[],
              'UID':("p"+str(0)+"l"+str(0))}

nodeOrd = {'root':0,
           'thread':1,
           'header':2,
           'edition':2,
           'author':2,
           'title':3,
           'url':4 }

nodeTable  = {'author':[],
              'thread':[],
              'edition':[],
              'header':[],
              'url':[],
              'title':[],
              'VOID':[],
              'root':[] }

nodeTable['root'].append(parentNode)

node = None

def listDirNoHidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def getAbsPathRelToFile(relDirThreadHtmls):
    fileDir = os.path.dirname(__file__)
    absPathRelToFile = os.path.join(fileDir, relDirThreadHtmls) 
    return os.path.abspath(absPathRelToFile)
  
def insertStr(pos, string, line) :
    newString = line[:pos] + string + line[pos:]
    return newString

def insertMultStr(args, s) :
    ca = list(s)
    for i, arg in enumerate(args) :
        ca.insert(arg[0]+i, arg[1])
    return ''.join(ca)

def genValueTable () :
    valueTable = {}    
    for type in nodeTable :
        valueTable[type] = {}
        for node in nodeTable[type] : 
           if node['value'] is not None :
               if node['value'].lower() not in valueTable[type] :
                   valueTable[type][node['value'].lower()] = {}
                   valueTable[type][node['value'].lower()]['nodes'] = []
                   valueTable[type][node['value'].lower()]['nodes'].append(node)
               else :
                   valueTable[type][node['value'].lower()]['nodes'].append(node)
           else :
               if node['type'] != 'root':
                   if node['data_line'].lower() not in valueTable[type] :
                       valueTable[type][node['data_line'].lower()] = {}
                       valueTable[type][node['data_line'].lower()]['nodes'] = []
                       valueTable[type][node['data_line'].lower()]['nodes'].append(node)
                   else :
                       valueTable[type][node['data_line'].lower()]['nodes'].append(node)
    return valueTable

def getValidParent(node,parentNode) :
    if node['type'] != 'VOID' :
        while nodeOrd[node['type']] <= nodeOrd[parentNode['type']]:
            parentNode = parentNode['parent']
    return parentNode

def summarizeValueTable() :
    for type in valueTable :
        print(type)
        values = list(valueTable[type].keys())
        values.sort()
        for value in values:
            cnt = str(len(valueTable[type][value]['nodes'])) + ")"
            print(f"    ({cnt:<5}{value}")

def genVoidNode(line,UID) :
    node = { 'value':None,
             'data_line':line,
             'UID':UID,
             'type':'VOID',
             'childs':[] }
    return node

def printNode(node,lvl=0) :

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

    for child in node['childs'] :
        printNode(child,lvl+1)
    

dirOpsTexts = getAbsPathRelToFile(relPathToOpsDir)
threadNumList = listDirNoHidden(dirOpsTexts)

i = 0

for threadNum in threadNumList :
    #if i == 1: 
    #    break
    #i=1+i

    opFileFolderPath = os.path.join(dirOpsTexts,threadNum)
    opFilePath = os.path.join(opFileFolderPath,threadNum+".txt")

    with open(opFilePath,'r') as f:

        lines = f.readlines()

        node = {'value':threadNum,
                'type':'thread',
                'childs':[],
                'UID':("p"+threadNum+"l"+str(0))};

        parentNode = getValidParent(node,parentNode)
        nodeTable['thread'].append(node)
        parentNode['childs'].append(node)
        node['parent'] = parentNode
        parentNode = node


        for cnt,line in enumerate(lines) :

            UID = "p"+threadNum+"l"+str(cnt+1)

            line = re.sub(r'\s+',' ',line)
            line = line.rstrip()
            line = line.lstrip()

            header  = reHeader.match(line)
            edition  = reEdition.match(line)
            author = reAuthor.match(line)
            title = reTitle.match(line)
            url  = reUrl.match(line)

            if header :
                value = line[header.span(1)[0]:header.span(1)[1]]
                node = { 'value':value,
                         'data_line':line,
                         'UID':UID,
                         'type':'header',
                         'childs':[], 
                         'span2': header.span(1),
                         'span': header.span(2)}
            elif edition :
                value = line[edition.span(1)[0]:edition.span(1)[1]]
                node = { 'value':value,
                         'data_line':line,
                         'UID':UID,
                         'type':'edition',
                         'childs':[], 
                         'span': edition.span(1)}
            elif title :
                node = { 'value':line[title.span(1)[0]:title.span(1)[1]],
                         'data_line':line,
                         'UID':UID,
                         'type':'title',
                         'span': title.span(1),
                         'span2': title.span(2),
                         'childs':[], }
            elif author :
                value = line[author.span(1)[0]:author.span(1)[1]]
                node = { 'value':value,
                         'data_line':line,
                         'UID':UID,
                         'type':'author',
                         'childs':[], 
                         'span2': author.span(2),
                         'span': author.span(1)}
                nodeTable['author'].append(node)
            elif url :
                node = { 'value':line[url.span(1)[0]:url.span(1)[1]],
                         'data_line':line,
                         'UID':UID,
                         'type':'url',
                         'childs':[], 
                         'span2': url.span(2),
                         'span': url.span(1)}

            else :
                node = genVoidNode(line,UID)






            parentNode = getValidParent(node,parentNode)
            #if node['type'] == 'title' :
            #    if parentNode['type'] != 'author' :
            #        node = genVoidNode(line,UID)
            #        parentNode = getValidParent(node,parentNode)
            nodeTable[node['type']].append(node)
            parentNode['childs'].append(node)
            node['parent'] = parentNode

            if node['type'] != 'VOID' :
                parentNode = node


#printNode(nodeTable['root'][0])
valueTable = genValueTable()
summarizeValueTable()
