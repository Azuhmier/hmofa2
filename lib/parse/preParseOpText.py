#!/usr/bin/env python3
import os
import re

nodeOrd = {'root':0,'thread':1,'author':2,'title':3,'url':4}
parentNode = {'value':None, 'type':'root', 'childs':[],'UID':("p"+str(0)+"l"+str(0))}
nodeTable  = { 'author':[], 'thread':[], 'url':[], 'title':[], 'VOID':[], 'root':[]}
nodeTable['root'].append(parentNode)
node = None

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def getAbsPathRelToFile(relPathToFile):
    file_dir = os.path.dirname(__file__)
    absPathRelToFile = os.path.join(file_dir, relPathToFile) 
    return absPathRelToFile
  
def insertStr(pos, string, line) :
    new_string = line[:pos] + string + line[pos:]
    return new_string

def insertMultStr(args, s) :
    ca = list(s)
    for i, arg in enumerate(args) :
        ca.insert(arg[0]+i, arg[1])
    return ''.join(ca)


def getValidParent(node,parentNode) :
    if node['type'] != 'VOID' :
        while nodeOrd[node['type']] <= nodeOrd[parentNode['type']]:
            parentNode = parentNode['parent']
    return parentNode

def printNode(node,lvl=0) :

    if node['type'] == 'root' :
        #print('root')
        1;

    elif node['type'] == 'thread':
        print("-------##"+node['value'])

    elif node['type'] == 'author':
        if node['span2'][0] == -1:
            args = [
                       [0,'<A>'], 
                       [0,'<d>{'], 
                       [node['span'][0],'}</d>'],
                       [node['span'][0],'<v>{'],
                       [node['span'][1],'}</v>'],
                       [len(node['data_line']),'</A>'],
                   ]
        else :
            args = [
                       [0,'<A>'], 
                       [0,'<d>{'], 
                       [node['span'][0],'}</d>'],
                       [node['span'][0],'<v>{'],
                       [node['span'][1],'}</v>'],
                       [node['span2'][0],'<a>{'],
                       [node['span2'][1],'}</a>'],
                       [len(node['data_line']),'</A>'],
                   ]
        line = insertMultStr(args, node['data_line'])
        print(line)

    elif node['type'] == 'title':
        if node['span2'][0] == -1:
            args = [
                       [0,'<T>'], 
                       [0,'<d>{'], 
                       [node['span'][0],'}</d>'],
                       [node['span'][0],'<v>{'],
                       [node['span'][1],'}</v>'],
                       [len(node['data_line']),'</T>'],
                   ]
        else :
            args = [
                       [0,'<T>'], 
                       [0,'<d>{'], 
                       [node['span'][0],'}</d>'],
                       [node['span'][0],'<v>{'],
                       [node['span'][1],'}</v>'],
                       [node['span2'][0],'<a>{'],
                       [node['span2'][1],'}</a>'],
                       [len(node['data_line']),'</T>'],
                   ]
        line = insertMultStr(args, node['data_line'])
        print(line)

    elif node['type'] == 'url':
        if node['span2'][0] == -1:
            args = [
                       [0,'<U>'], 
                       [0,'<d>{'], 
                       [node['span'][0],'}</d>'],
                       [node['span'][0],'<v>{'],
                       [node['span'][1],'}</v>'],
                       [len(node['data_line']),'</U>'],
                   ]
        else :
            args = [
                       [0,'<U>'], 
                       [0,'<d>{'], 
                       [node['span'][0],'}</d>'],
                       [node['span'][0],'<v>{'],
                       [node['span'][1],'}</v>'],
                       [node['span2'][0],'<a>{'],
                       [node['span2'][1],'}</a>'],
                       [len(node['data_line']),'</U>'],
                   ]
        line = insertMultStr(args, node['data_line'])
        print(line)

    elif node['type'] == 'VOID' :
        1;
        print(node['data_line'])

    for child in node['childs'] :
        printNode(child,lvl+1)
    
re_title = re.compile("^>([^\[(]+?)<*(?:(?:\s*-*\s*[\[(]\s*([^\[\]()]+)\s*[\])])|(?:\s+-\s+(.+)|\s+((?:pt\.?|part|ch\.?|chapter)\s+\d+)|))$")
re_author =  re.compile("^[bB]y\s([^\[(]+?)(?:[- ]*[\[(]\s*([^\[\]()]+)\s*[\])])*$")
re_url =  re.compile("^(http[^ ]+)(?:[- ]*[\[(]\s*([^\[\]()]+)\s*[\])])*$")

relPathToOpsDir = '../../../threads/ops'
ops_dir = getAbsPathRelToFile(relPathToOpsDir)
threadNumList = listdir_nohidden(ops_dir)
i = 1

for thread_num in threadNumList :
    #if i > 500: 
    #    break
    #i=1+i

    opFileFolderPath = os.path.join(ops_dir,thread_num)
    opFilePath = os.path.join(opFileFolderPath,thread_num+".txt")

    with open(opFilePath,'r') as f:
        lines = f.readlines()
        node = {'value':thread_num, 'type':'thread', 'childs':[],'UID':("p"+thread_num+"l"+str(0))};
        parentNode = getValidParent(node,parentNode)
        nodeTable['thread'].append(node)
        parentNode['childs'].append(node)
        node['parent'] = parentNode
        parentNode = node


        for cnt,line in enumerate(lines) :
            UID = "p"+thread_num+"l"+str(cnt+1)

            line = re.sub(r'\s+',' ',line)
            line = line.rstrip()
            line = line.lstrip()
            line = line.translate(str.maketrans({"}": r"\}",
                                                 "{": r"\{",
                                                 "\\": r"\\"}))

            author = re_author.match(line)
            title = re_title.match(line)
            url  = re_url.match(line)

            if author :
                value = line[author.span(1)[0]:author.span(1)[1]]
                node = { 'value':value,
                         'data_line':line,
                         'UID':UID,
                         'type':'author',
                         'childs':[], 
                         'span2': author.span(2),
                         'span': author.span(1)}
                nodeTable['author'].append(node)

            elif title :
                node = { 'value':line[title.span(1)[0]:title.span(1)[1]],
                         'data_line':line,
                         'UID':UID,
                         'type':'title',
                         'span': title.span(1),
                         'span2': title.span(2),
                         'childs':[], }

                nodeTable['title'].append(node)

            elif url :
                node = { 'value':line[url.span(1)[0]:url.span(1)[1]],
                         'data_line':line,
                         'UID':UID,
                         'type':'url',
                         'childs':[], 
                         'span2': url.span(2),
                         'span': url.span(1)}
                nodeTable['url'].append(node)

            else :
                node = { 'value':None,
                         'data_line':line,
                         'UID':UID,
                         'type':'VOID',
                         'childs':[] }
                nodeTable['VOID'].append(node)

            parentNode = getValidParent(node,parentNode)
            parentNode['childs'].append(node)
            node['parent'] = parentNode
            if node['type'] != 'VOID' :
                parentNode = node

    printNode(nodeTable['root'][0])
    

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
    return valueTable

valueTable = genValueTable()
#for type in valueTable :
#    print(type)
#    values = list(valueTable[type].keys())
#    values.sort()
#    for value in values:
#        cnt = str(len(valueTable[type][value]['nodes'])) + ")"
#        print(f"    ({cnt:<5}{value}")
