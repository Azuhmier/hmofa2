#!/usr/bin/env python3

import requests
import time
import os
from bs4 import BeautifulSoup
import re

def get_content (url, timeout) :
    time.sleep(timeout)
    session = requests.Session()
    r = session.get(url)
    return r

def getLastThreadNoArchivedPrev (contents_dir):
    threadNoList = list(os.listdir(contents_dir))
    lastThreadNoArchivedPrev = max(int(thread_no) for thread_no in threadNoList)
    return lastThreadNoArchivedPrev

def getUrlOfNextPage(soup): 
    urlOfNextPage = None
    liNextBtnDisabled = soup.find_all("li", {"class" : re.compile("next disabled")})
    if not liNextBtnDisabled :
        liNextBtn = soup.find_all("li", {"class" : re.compile("next")})
        aNextBtn = liNextBtn[0].find("a")
        urlOfNextPage = aNextBtn["href"]
    return urlOfNextPage

def getAbsPathRelToFile(relPathToFile):
    file_dir = os.path.dirname(__file__)
    absPathRelToFile = os.path.join(file_dir, relPathToFile) 
    return absPathRelToFile

relPathToFile   = '../../../content/ops'
contents_dir    = getAbsPathRelToFile(relPathToFile)
lastThreadNoArchivedPrev    = str(getLastThreadNoArchivedPrev(contents_dir))
urlOfCurPage    = 'https://desuarchive.org/trash/search/text/%22Human%20Males%20On%20Female%20Anthros%20General%22/type/op/'
max_iter        = 1000
timeout         = 1 #seconds
lastThreadNoArchivedPrevIsUpdated = False

print("Begining update")

for i in range(1, max_iter, 1) :
    print("++starting page" + str(i))
    r = get_content(urlOfCurPage, timeout)
    soup = BeautifulSoup(r.content, 'html.parser')

    posts = soup.find_all("article", {"class" : re.compile("post doc_id_")})
    for post in posts :
        thread_no_raw = post.find("a", {"title" : "Reply to this post"})["data-post"]
        thread_no = str(thread_no_raw).strip()
        thread_url = post.find("a", {"title" : "Reply to this post"})["href"]

        content_path  = os.path.join(contents_dir, thread_no)
        if thread_no == lastThreadNoArchivedPrev :
            if not lastThreadNoArchivedPrevIsUpdated:
               lastThreadNoArchivedPrevIsUpdated = True 
               print("++++updating thread " + str(lastThreadNoArchivedPrev))
               with open(content_path, 'w+') as f:
                   r = get_content(thread_url,1)
                   f.write(r.text)
            else :
               break
        elif os.path.isfile(content_path) : 
            break
        else :
           print("++++adding thread " + str(lastThreadNoArchivedPrev))
           with open(content_path, 'w+') as f:
               r = get_content(thread_url,1)
               f.write(r.text)

    if lastThreadNoArchivedPrevIsUpdated:
        break
    urlOfCurPage = getUrlOfNextPage(soup)
    if urlOfCurPage is None :
        break
print("Update Finished")
