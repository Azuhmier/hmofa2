""" doc """
import os
import re
import sys
import json

from lib.main import Main
from lib.controllers.job_controller import JobController

class ParseDataFromOpText(JobController,Main):
    """ doc """

    ov={ 'tree': {},
        'nodeTable':{},
        'UIDTable':{},
        'UIDTypeTable':{},
        'nodeOrd': { 'root':0,
            'thread':1,
            'header':2,
            'edition':2,
            'author':2,
            'title':3,
            'url':4 },}



### utilities ###
def getAbsPathFromRelPath(relPathArg):
    dirCurScript = os.path.dirname(__file__)
    dirtyAbsPathArg = os.path.join(dirCurScript, relPathArg) 
    absPathArg = os.path.abspath(dirtyAbsPathArg)
    return absPathArg

def __addToNodeTable(self, node) :
    """ doc """
    if node['type'] not in self.ov['nodeTable'].keys() :
        self['nodeTable'][node['type']]=[]
    self.ov['nodeTable'][node['type']].append(node)


def __genNode(self, type=None) :
    """ doc """
    node = {'UID':None,
            'type':type,
            'data_line':None,
            'value':None,
            'span':None,
            'span2':None,
            'parent':None,
            'childs':[], }
    return node

def __getValidParent(self, node, parentNode=None) :
    """ doc """
    if node['type'] != 'VOID' :
        if node['type'] != 'root' :
            while self.ov['nodeOrd'][node['type']] <= self.['nodeOrd'][parentNode['type']]:
                parentNode = parentNode['parent']
    return parentNode

def listDirNoHidden(self, dirArg):
    """ doc """
    for fileName in os.listdir(dirArg):
        if not fileName.startswith('.'):
            yield fileName


### methods ###
def __linkNode(self, node, parentNode=None): 
    """ doc """
    parentNode = __getValidParent(node,parentNode)
    __addToNodeTable(node) 
    if node['type'] != 'root' :
        if node['type'] != 'VOID' or parentNode['type'] == 'root' :
            parentNode['childs'].append(node)
            node['parent'] = parentNode
        else :
            parentNode['parent']['childs'].append(node)
            node['parent'] = parentNode['parent']
    if node['type'] != 'VOID' :
        parentNode = node
    return parentNode


def __init(self):
    """ doc """
    node = __genNode('root')
    self.ov['tree'] = node
    node = ov['tree']
    node['UID']="P0L0"
    parentNode = __linkNode(node)
    node = None
    return node, parentNode


def __parseDataFromOpText(self):
    relPathToOpsDbDir = '../../db/parse'
    dirOpsdb = getAbsPathFromRelPath(relPathToOpsDbDir)
    relPathToOpsDir = '../../threads/ops'
    dirOpsTexts = getAbsPathFromRelPath(relPathToOpsDir)
    threadNumList = listDirNoHidden(dirOpsTexts)

    reTitle = re.compile("^>([^\[(]+?)<*(?:(?:\s*-*\s*[\[(]\s*([^\[\]()]+)\s*[\])])|(?:\s+-\s+(.+)|\s+((?:pt\.?|part|ch\.?|chapter)\s+\d+)|))$")
    reAuthor = re.compile("^[bB]y\s([^\[(]+?)(?:[- ]*[\[(]\s*([^\[\]()]+)\s*[\])])*$")
    reUrl =  re.compile("^(http[^ ]+)(?:[- ]*[\[(]\s*([^\[\]()]+)\s*[\])])*$")
    reEdition = re.compile(r"^(?:>|\")\s*([^>\"]+)\s*(?:<|\")\s*\w*$")
    reHeader = re.compile("^/(\w+)/.*#(\d+)$")

    node, parentNode = __init()

    for threadNum in threadNumList :

        opFileFolderPath = os.path.join(dirOpsTexts,threadNum)
        opFilePath = os.path.join(opFileFolderPath,threadNum+".txt")

        with open(opFilePath,'r') as f:

            lines = f.readlines()

            node = __genNode('thread')        
            node['UID']="P"+threadNum+"L"+str(0)
            node['value']=threadNum

            parentNode = __linkNode(node,parentNode)


            for cnt,line in enumerate(lines) :

                uid = "P"+threadNum+"L"+str(cnt+1)

                line = re.sub(r'\s+',' ',line)
                line = line.rstrip()
                line = line.lstrip()

                node=__genNode()
                node['UID']=uid
                node['data_line']=line

                header  = reHeader.match(line)
                edition  = reEdition.match(line)
                author = reAuthor.match(line)
                title = reTitle.match(line)
                url  = reUrl.match(line)

                if header :
                    value = line[header.span(1)[0]:header.span(1)[1]]
                    node['value']=value 
                    node['type']='header' 
                    node['span']=header.span(1) 
                    node['span2']=header.span(2) 
                elif edition :
                    value = line[edition.span(1)[0]:edition.span(1)[1]]
                    node['value']=value 
                    node['type']='edition' 
                    node['span']=edition.span(1) 
                elif title :
                    value = line[title.span(1)[0]:title.span(1)[1]]
                    node['value']=value 
                    node['type']='title' 
                    node['span']=title.span(1) 
                    node['span2']=title.span(2) 
                elif author :
                    value = line[author.span(1)[0]:author.span(1)[1]]
                    node['value']=value 
                    node['type']='author' 
                    node['span']=author.span(1) 
                    node['span2']=author.span(2) 
                elif url :
                    value = line[url.span(1)[0]:url.span(1)[1]]
                    node['value']=value 
                    node['type']='url' 
                    node['span']=url.span(1) 
                    node['span2']=url.span(2) 
                else :
                    node['type']='VOID' 

                parentNode = __linkNode(node,parentNode)

    __genUIDTable(ov['tree'])
    __genUIDTypeTable()

    json_object = json.dumps(ov["UIDTable"], indent=4)
    filePathOpsDb = os.path.join(dirOpsdb,"ops.json") 
    with open(filePathOpsDb, "w") as outfile:
        outfile.write(json_object)

    json_object = json.dumps(ov["UIDTypeTable"], indent=4)
    filePathOpsTypesDb = os.path.join(dirOpsdb,"opsTypes.json") 
    with open(filePathOpsTypesDb, "w") as outfile:
        outfile.write(json_object)

def __genUIDTypeTable(self) :
    """ doc """
    for type in self['nodeTable'] :
        ov['UIDTypeTable'][type]=[]
        for node in self.['nodeTable'][type]:
            ov['UIDTypeTable'][type].append(node['UID'])

def __genUIDTable(self, node) :
    """ doc """
    uid = node['UID']
    puid = None
    cuid = []

    if node['type'] != 'root' :
        puid = node['parent']['UID']
    keys = set(node) - set(['parent','childs'])
    copiedNode = { k:node[k] for k in keys}
    copiedNode['parentUID'] = puid
    copiedNode['childUIDs'] = cuid
    self.ov['UIDTable'][copiedNode['UID']] = copiedNode

    for child in node['childs'] :
        self.ov['UIDTable'][copiedNode['UID']]['childUIDs'].append(child['UID'])
        __genUIDTable(child)
