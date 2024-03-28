#!/usr/bin/env python3
import os
import logging
import sys
import time
import datetime
from bs4 import BeautifulSoup

opts = {"updateOnly":True,"verbose":True}
if not opts['verbose'] :
    sys.stdout = open(os.devnull, 'w')
relDirThreadHtmls   = '../../threads/html'
relDirOpTexts   = '../../threads/ops'

def getThreadNums(dirThreadHtmls):
    for fileNameThreadHtml in os.listdir(dirThreadHtmls):
        if not fileNameThreadHtml.startswith('.'):
            threadNum = fileNameThreadHtml[:-5]
            yield threadNum

def getMetaText (article) :
    metaText=''
    meta = article.find_all("div", class_="pull-right")[0].text
    listMetaValues = meta[1:-1].split(' / ')
    listMetaKeys = ['posts ','images','ip    ']
    listMeta = ['    '.join(z) for z in zip(listMetaKeys, listMetaValues)]
    metaText = metaText + '\n'.join(listMeta)
    dateTimeOfThreadCreation = article.find_all("span", class_="time_wrap")[0].text
    formatString = " %a %d %b %Y %H:%M:%S "
    timeStampOfThreadCreation = time.mktime(datetime.datetime.strptime(dateTimeOfThreadCreation, formatString).timetuple())
    metaText = metaText + '\ntime      '+str(timeStampOfThreadCreation)
    return metaText

def getOpText(article):
    div = article.find_all("div", class_="text")[0]
    for elem in div.find_all(["a", "span", "div", "br"]):
        if elem.name == 'br':
            elem.replace_with("\n")
        else :
            elem.replace_with(elem.text)
    opText = div.get_text()
    return opText

def getAbsPathRelToFile(relDirThreadHtmls):
    fileDir = os.path.dirname(__file__)
    absPathRelToFile = os.path.join(fileDir, relDirThreadHtmls) 
    return os.path.abspath(absPathRelToFile)
  

dirThreadHtmls = getAbsPathRelToFile(relDirThreadHtmls)
dirOpTextFolders = getAbsPathRelToFile(relDirOpTexts)
listThreadNums = getThreadNums(dirThreadHtmls)

print("Parsing OPs from Thread Htmls")

i = 0
for threadNum in listThreadNums :
    #if i == 2:
    #    break

    pathOpTextFolder = os.path.join(dirOpTextFolders,threadNum)
    filePathOpText = os.path.join(pathOpTextFolder,threadNum+".txt")
    filePathOpMetaText = os.path.join(pathOpTextFolder,"meta"+threadNum+".txt")
    filePathThreadHtml  = os.path.join(dirThreadHtmls, threadNum+".html")

    if os.path.exists(pathOpTextFolder) : 
        if os.path.isfile(filePathOpText) :
            if os.stat(filePathOpText).st_size != 0 :
                if os.path.isfile(filePathOpMetaText) :
                    print("[already parsed]--skipping " + threadNum)
                    continue

    elif os.stat(filePathThreadHtml).st_size == 0 :
        print("--[empty html]skipping " + threadNum)
        continue

    i = i + 1
    print("--Parsing OP from "+filePathThreadHtml)

    soup = BeautifulSoup(open(filePathThreadHtml), 'html.parser')
    article = soup.body.find_all("article", id=threadNum)[0]
    opText = getOpText(article)
    metaText = getMetaText(article)
    

    if not os.path.exists(pathOpTextFolder):
        os.mkdir(pathOpTextFolder)
    with open(filePathOpText, 'w+') as f:
        f.write(opText)
    with open(filePathOpMetaText, 'w+') as fMeta:
        fMeta.write(metaText)

print("Finished")

