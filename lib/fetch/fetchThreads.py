#!/usr/bin/env python3

import requests
import time
import os
from bs4 import BeautifulSoup
import re
import sys


opts = {"updateOnly":True,"verbose":True}
maxIter = 1000
urlOfCurPage = 'https://desuarchive.org/trash/search/text/%22Human%20Males%20On%20Female%20Anthros%20General%22/type/op/'
timeout = 1 #seconds
relPathToFile = '../../threads/html'
if not opts['verbose'] :
    sys.stdout = open(os.devnull, 'w')


def getContent (url, timeout) :
    time.sleep(timeout)
    session = requests.Session()
    r = session.get(url)
    return r

def getLastThreadNumFetchedPrev (dirThreadHtmls):
    listThreadNums = [fileName[:-5] for fileName in list(os.listdir(dirThreadHtmls))]
    lastThreadNumFetchedPrev = max(int(threadNum) for threadNum in listThreadNums)
    return str(lastThreadNumFetchedPrev)

def getUrlOfNextPage(soup): 
    urlOfNextPage = None
    liNextBtnDisabled = soup.find_all("li", {"class":re.compile("next disabled")})
    if not liNextBtnDisabled :
        liNextBtn = soup.find_all("li", {"class":re.compile("next")})
        aNextBtn = liNextBtn[0].find("a")
        urlOfNextPage = aNextBtn["href"]
    return urlOfNextPage

def getAbsPathRelToFile(relPathToFile):
    fileDir = os.path.dirname(__file__)
    absPathRelToFile = os.path.join(fileDir, relPathToFile) 
    return os.path.abspath(absPathRelToFile)



dirThreadHtmls = getAbsPathRelToFile(relPathToFile)
lastThreadNumFetchedPrev = getLastThreadNumFetchedPrev(dirThreadHtmls)
lastThreadNumFetchedPrevUpdated = False

print("Begining: fetchThreads.py")

for i in range(1, maxIter, 1) :
    print("starting page " + str(i))

    r = getContent(urlOfCurPage, timeout)
    soup = BeautifulSoup(r.content, 'html.parser')

    posts = soup.find_all("article", {"class" : re.compile("post doc_id_")})

    for post in posts :
        threadNumRaw = post.find("a", {"title" : "Reply to this post"})["data-post"]
        threadNum = str(threadNumRaw).strip()
        threadUrl = post.find("a", {"title" : "Reply to this post"})["href"]

        filePathThreadHtml  = os.path.join(dirThreadHtmls, threadNum+".html")
        if threadNum == lastThreadNumFetchedPrev :
            if not lastThreadNumFetchedPrevUpdated:
               lastThreadNumFetchedPrevUpdated = True 
               print("----updating thread " + str(lastThreadNumFetchedPrev))
               with open(filePathThreadHtml, 'w+') as f:
                   r = getContent(threadUrl,1)
                   f.write(r.text)
            else :
               break
        elif os.path.isfile(filePathThreadHtml) : 
            print("----skipping thread " + str(threadNum))
            break
        else :
           print("----adding thread " + str(threadNum))
           with open(filePathThreadHtml, 'w+') as f:
               r = getContent(threadUrl,1)
               f.write(r.text)
    else :
        urlOfCurPage = getUrlOfNextPage(soup)
        if urlOfCurPage is None :
            break
    break

print("Update Finished")
