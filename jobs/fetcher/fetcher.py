#tos
import time
import sys
import pickle
import requests
import yaml
import json
import copy
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidCookieDomainException
from selenium.common.exceptions import ElementNotInteractableException

class triggered(Exception):
    pass
ov = {
    "dc" : {},
    "s" : None,
    "wd" : None,
    "res" :[],
}

with open("/home/azuhmier/hmofa/test/domains.yml","r",encoding='utf-8') as infile:
    ov["dc"] = yaml.safe_load(infile) 

"""
archive
    jobs
        job
            *get
            *get_special
            *get_value
            *do
            wfls
                wlf
                    action
                        requests
                            post
                            get
                            download
                        selinium
                            post
                            get
                            download
                            click
                        parse

---------
action
element
get
wfl
special
---------
_VARS

ov
    s
    d_config
    j
        GET
        VARS 
        SPECIAL
            cookie
        config
        a
            r
            sp
ov
j
a
[j]
[]
{
    a[k].r[k]
    a[k].sp[k]
    j.GET[k]
    j.VARS[k]
    j.special[k]
    
    
}


"""

def init_session(**kwargs) :
    ov["s"] = requests.Session()



def get_domain_config(j) :
    url = j["VARS"]["url"]
    o = urlparse(url)

    if o.netloc in ov["dc"] :
        j["config"] = ov["dc"][o.netloc]
        return 1

    pos = o.netloc.index('.')
    k = o.netloc[pos:]
    j["VARS"]["domain_key"] = k

    if k in ov["dc"] :
        j["config"] = ov["dc"][k]
        return 1
    sys.exit("ERROR")


def get_wfl(j) :
    if not j["current_workflow"] :
        for wfl_name, wfl in j["config"]["workflows"] :
            if wfl["default"] :
                return wfl_name,wfl
    else :
        wfl_name = j["current_workflow"]
        wfl = j["config"]["workflows"]["wfl_name"]
        return wfl_name, wfl
    sys.exit(f"ERROR: No Default workflow for domain {j['VARS']['domain']}")



def do_action_requests_post(j) :
    a = j["a"][-1]

    # payload
    for k,v in a["payload"].items() :
        a["payload"][k]=get_value(j,v)

    a["r"] = j["s"].post(
        a["url"],
        headers=a["headers"],
        data=a["payload"],
        cookies=a["cookies"]
    )



def do_action_requests_get(j) :
    a = j["a"][-1]
    a["r"] = j["s"].get(
        a["url"],
        headers=a["headers"],
        cookies=a["cookies"]
    )



def do_action_requests(j) :
    a = j["a"][-1]

    # headers
    for k,v in a["header"].items() :
        a["header"][k] = get_value(j,v)

    #url
    for i in a["url"]:
        a["url"] = a["url"] + get_value(j,i)

    #cookie
    cookie={}
    if 'cookie' in a["headers"]:
        a["cookies"] = a["headers"].pop('Cookie')

    # get
    if a["type"] == 'get' :
        if not do_action_requests_get(j):
            return 0

    #post
    elif a["type"] == 'post' :
        if not do_action_requests_get(j) :
            return 0



def do_parse(j) :
    a = j["actions"][-1]
    # parse
    if "sp" not in j :
        j["sp"] = []
    if a["parse"] :
        j["sp"].append(bs(j["r"][-1].content,'html.parser'))

    #get
    if "get" in a :
        for g in a["get"] :
            if not get(j,g): 
                return 0



def do_action(j) :
    a = j["a"][-1]

    if a["method"] == "requests" : 
        if not do_action_requests(j) :
            return 0

    if a["parse"] :
        if not do_parse(j) :
            return 0




def do_wfl(j) :
    try :
        #default worflow
        wfl_name, wfl = get_wfl(j)
        wfl = copy.deepcopy(wfl) 
        wfl["name"] = wfl_name

        for action_name in wfl["do"] :
            action = copy.deepcopy(j["config"]["actions"][action_name])
            action["name"] = action_name
            j["a"].append(action) 
            if not do_action(j["a"][-1]) :
                return 0
            ry()


    except triggered:
        return 0

    j["running"] = False

    

def do(j, dothese) :
    for dothis in dothese : 
        this = dothis[0]
        if this == 'wfl' :
            wfl = dothis[1]
            j["current_wfl"] = wfl



def trigger(j, type=None, **kwargs) :
    trgs = j["config"]["triggers"]
    for trg in trgs:
        if trg["type"] == type :
            for k,v in trg["criteria"].items():
                if kwargs[k] != v[k] :
                    break
            else :
                continue
            do(j,trg["do"])
            j["triggered"] = True
            raise triggered()



def get_special(j,v) :
    retu = None
    if v == '_cookies_' :
        retu = ov["s"].cookies.get_dict(domain=j["VARS"]["domain_key"])
    else: 
        name = v[1:-1]
        for a in j["a"] :
            if a["name"] == name :
                d = json.loads(a["r"].text)
                retu = d
    return retu



def get(j,vvg) :
    get = None

    if vvg in j["GET"] :
        get = j["GET"][vvg]
    elif vvg in j["config"]["get"]
        get = j["config"]["get"][vvg][0]
        k = get[0]

        if isinstance(k,list) :
            d=get_value(j,k)
            try:
                get = d[get[1]]
            except KeyError:
                trigger(j,type=get, val=vvg)

            j["GET"][k[0]] = get
        else :
            ele = j["config"]["elements"][k]

            attr=get[1]

            tag = ele[0]
            clss = ele[1]
            val = ele[2]

            res = j["sp"][0].find_all(tag,{clss:val})

            get = res[0][attr]
            j["GET"][vvg] = get
    if not get :
        trigger(j,type=get, val=vvg)
    return get

def get_value(j,v) :
    retu = v
    if isinstance(v,list) :
        if len(v) == 1 :
            vv = v[0]
            if vv.isupper() :
                retu = get(j,vv)
            elif vv[0] == '_' :
                if vv[-1] == '_':
                    retu = get_special(j,vv)
                else :
                    retu = j["VARS"][vv[1:]]
    elif isinstance(v,dict):
        pass
    else :
        retu=str(retu)
    return retu


                


                        
                    








urls = [
    "https://spacedimsum.itch.io/bread",
    "https://frulepllc.itch.io/tricky-guardians-2",
    "https://tetchyy.itch.io/hop-fire",
    "https://codanon.itch.io/coda-demo",
    #"https://oliver-hart.itch.io/a-red-winter",
    #"https://eloisanon.itch.io/all-the-birds-seem-to-sing-for-you",
]

init_session()

jj = []
for url in urls :
    time.sleep(3)

    get_domain_config(j,url)
    o = urlparse(url)
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'

    j={
        "GET":{},
        "VARS":{
            "domain" : o.netloc,
            "url" : o.geturl(),
            "ua": ua,
        },
        "VALS": {},
        "triggered": None,
        "actions":[],
        "o": o,
        "running": True,
        "current_wfl" : None,
    }

    while do_wfl(j) :
        if not j["running"] :
            break   
    jj.append(j)
