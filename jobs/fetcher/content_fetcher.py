#!/usr/bin/env python3
"""_summary_

Returns:
    _type_: _description_
"""
#429, a03
#403, fanfiction
#500, sofurry
import logging
import os
from pathlib import Path
import json
import time
import sys
import csv
from urllib.parse import urlparse
import copy
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import yaml
from bs4 import BeautifulSoup

bp = {

    "archive_config" : {
        "name" : None,
        "skip_login" : []
    },
    "urlpath_config" : {
        "skip" : "",
    },


    "archive_meta" : { 
        "last_fetched" : None,
        "first_fetched" : None,
        "domains" : 0,
        "fail" : 0,
        "fetches" : 0,
        "size" : 0,
        "codes" : {},
        "statuses" : {},
        "urls" : 0,
    },
    "archive_lists" : {
        "domains" : [],
        "statuses" : {},
        "codes" : {},
        "current_job" : [],
        "urls" : [],
        "fetch_times" : [],
        "fail" : [],
    },

    "urlpath_meta" : {
        "job_status" : None,
        "last_code" : None,
        "last_status" : None,
        "first_fetched" : None,
        "last_fetched" : None,
        "fetches" : 0,
        "size" : 0,
        "scheme"  : "https://"
    },
    "urlpath_lists" : {
        "history": [
            {
                "name" : None,
                "size" : None,
                "code" : None,
                "status" : None,
            }
        ],
    },



    "fetch_meta" : {
        "header" : None,
        "time_end" : None,
        "method" : None,
        "login" : None,
        "url" : None,
        "resuhtant_url": None,
        "cookies" : None,
        "session" : None,

        "scheme" : None,
        "code" : None,
        "time_start" : None,

        "size" : None,
    },

}
ov = {
    "BP": bp,
    "PATHS" : {
        "PATH_TO_PWDS": '/home/azuhmier/.pwds',
        "PATH_TO_URLS": "/home/azuhmier/hmofa/hmofa/.ohm/output/paged_lists/objs/plain/url.txt",
        "ARCHIVE_DIRECTORY": "/home/azuhmier/hmofa/test",
    }
}

verbose = None
if len(sys.argv) > 1 :
    verbose = sys.argv[1]

v_lvl = None
if not verbose or verbose == 0:
    v_lvl = logging.NOTSET
elif verbose == 1:
    v_lvl = logging.info
elif verbose == 2:
    v_lvl = logging.debug

logger = logging.getLogger(__name__)
logfile = os.path.join( ov["PATHS"]["ARCHIVE_DIRECTORY"], "ohmfa_fetch.log")
with open(logfile, 'w'):
    pass
#logging.basicConfig(filename=logfile, level=v_lvl, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename=logfile, level=v_lvl, format='%(levelname)s - %(message)s')



def gen_diff(new_dict={}, old_dict={}) :
    diff = {}
    r_align = 0
    for k in old_dict :
        if len(k) > r_align :
            r_align = len(k)
        if k in new_dict :
            if isinstance(old_dict[k], list) :
                diff[k] = [
                    '-' + str(list(set(new_dict[k]) - set(old_dict[k]))),
                    '+' + str(list(set(old_dict[k]) - set(new_dict[k]))),
                ]
            elif old_dict[k] != new_dict[k]:
                diff[k] = [old_dict[k], new_dict[k]]
        else :
            diff[k] = [old_dict[k], None]

    for k in new_dict :
        if len(k) > r_align :
            r_align = len(k)
        if k not in old_dict :
            diff[k] = [None,new_dict[k]]

    diff_strings = []
    format_str = ">" + str(r_align)
    for k, v in diff.items() :
        string = f"{k:{format_str}}: {v[0]} || {v[1]}"
        diff_strings.append(string)


    str_output = '\n'.join(diff_strings)


    return diff, str_output



def get_latest_strtime_dir(p) :
    """returns the strtime directory with the newest time

    Moduhes: Path from pathlib

    Args:
        directory (_str_): _description_

    Returns:
        _str_: self explainatory
    """
    retu = None
    strtimes = []
    for p_item in p.iterdir() :
        if p_item.name not in ["config.yml", "meta.json", "lists.json"]:
            strtimes.append(p_item.name)

    latest =  max(strtimes)
    retu = Path(os.path.join(p.absolute(),latest))
    return retu



def get_urlpath_from_dir(urlpath_dir):
    """_summary_

    Args:
        urlpath_dir (_type_): _description_

    Returns:
        _type_: _description_
    """
    retu = urlpath_dir.replace('__','/',1)
    retu = retu.replace('_','/')
    return retu



def strip_scheme(url):
    """_summary_

    Args:
        url (_type_): _description_

    Returns:
        _type_: _description_
    """
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)     



def get_fileobj(name, parent_directory=None, bp_in=None, clear=False, no_exist="error") :
    """_summary_

    Args:
        name (_type_): _description_
        parent_directory (_type_, optional): _description_. Defaults to None.
        bp_in (_type_, optional): _description_. Defaults to None.
        clear (bool, optional): _description_. Defaults to False.
        no_exist (str, optional): _description_. Defaults to "error".

    Returns:
        _type_: _description_
    """
    # check args
    if no_exist not in ["error", "make", "continue"] :
        sys.exit("ERROR: 'Invalid value for parameter 'no_exist' - '" + no_exist + "' ")
    elif no_exist == "make" and not bp_in :
        sys.exit("ERROR")
    elif bp_in and not isinstance(bp_in,dict) :
        sys.exit("ERROR")

    # create file_object.
    path = os.path.join(parent_directory, name) if parent_directory else name
    p = Path(path)

    # clone boilerplate if not None
    bp_copy = copy.deepcopy(bp_in) if bp_in else bp_in

    # initialize file data variable
    file_data = None

    # If it exist, get data.
    if p.is_file() :
        with p.open(mode='r', encoding="utf-8") as infile:
            if p.suffix == ".json":
                file_data=json.load(infile)
            elif p.suffix == ".yml":
                file_data = yaml.safe_load(infile)
            else :
                file_data = infile

    # Else If 'make' was specified, make it.
    elif no_exist == "make":
        with p.open(mode='w+', encoding="utf-8") as outfile:
            if p.suffix == ".json":
                json.dump(bp_copy,outfile)
            elif p.suffix == ".yml":
                yaml.dump(bp_copy,outfile)
            else :
                p.write_text(bp_copy, encoding="utf-8")

    # Else throw an error.
    elif no_exist == "error" :
        sys.exit("ERROR: File does not exist '" + str(p.absolute()) + "'")

    # clone file data if it's a dict
    data = copy.deepcopy(file_data) if isinstance(file_data, dict) else file_data
    
    # if clear is True, set data to boiler plate else conform data to it.
    data = bp_copy if clear else conform_to_bp(data, bp_copy) 

    return p, data, file_data



def conform_to_bp(data,bp_in) :
    """_summary_

    Args:
        data (_type_): _description_
        bp_in (_type_): _description_

    Returns:
        _type_: _description_
    """
    if bp_in:
        bp_copy = copy.deepcopy(bp_in)
        if data :
            for k in bp_copy :
                if k in data :
                    bp_copy[k] = data[k]
        data = bp_copy
    return data



def iter_dir(name, parent_directory=None, no_exist = "error", givedir=False) :
    """_summary_

    Args:
        name (_type_): _description_
        parent_directory (_type_, optional): _description_. Defauhts to None.
        make (bool, optional): _description_. Defauhts to False.

    Returns:
        _type_: _description_
    """

    if no_exist not in ["error", "make", "continue"] :
        sys.exit("ERROR: 'Invalid value for parameter 'no_exist' - '" + no_exist + "' ")
    retu = []

    path=name
    if parent_directory :
        path = os.path.join(parent_directory, name)
    p = Path(path)

    if not p.is_dir() and no_exist == "make":
        p.mkdir()
        retu.append(p)
    elif not p.is_dir() and no_exist == 'error' :
        sys.exit("ERROR: Directory does not exists '" + str(p.absolute()) +"'")
    elif not givedir :
        #IS EMPTY?
        for p_item in p.iterdir():

            retu.append(p_item)
    else :
        retu.append(p)

    return retu



##########################################
# IMPORTS
##########################################

def import_urls (path_to_urls) :
    """ Imports urls from a given file path and returns them
        as a list. 
    
    Required: pathlib.

    Args:
        path (_str_): Absolute path of of a json or a newline
        delmited file of urls. Only json files where there exists
        "root[Objs][urls]" are supported.

    Returns:
        _list_: urls stored as strings
    """
    # Initialized return value as an empty list
    retu = []

    # Get file extension to dertermine if valid
    file_ext = Path(path_to_urls).suffix

    # Supported file extensions
    if file_ext in [".txt", ".json"] :

        with open(path_to_urls, encoding="utf-8") as infile:

            # txt file
            if file_ext == ".txt":
                for line in infile:
                    retu.append(line)

            # json file
            if file_ext == ".json":
                json_dict = json.load(infile)

                if "objs" in json_dict :

                    if "url" in json_dict["objs"] :

                        for obj in json_dict["objs"]["url"] :
                            retu.append(obj["val"])
                    else :
                        sys.exit("ERROR: json dict key(s) 'objs' does not exists at '" + path_to_urls + "'")

                else :
                    sys.exit("ERROR: json dict key(s) 'objs.url' does not exists at '" + path_to_urls + "'")

    # Non supported file extension
    else :
        sys.exit("ERROR: '" + file_ext + "' is not a valid file extension at '" + path_to_urls + "'")

    return retu



def import_pwds (path_to_pwds, delim) :
    """ Imports passwords from a give file. It's assumed that the file is
    delimited to create key-value pairs: The website the credentials belong to
    and the keys 'usr' and 'pwd' for username and password respectivly and the.

    Required: csv

    Args:
        path (_str_): _description_
        delim (_str_): _description_

    Returns:
        _dict_: _description_
    """

    # Initialized return value as an empty dict
    retu = {}

    with open(path_to_pwds, encoding="utf-8") as infile:

        # csv reader object constructed from file and given delimiter. 
        reader = csv.reader( infile, delimiter=delim)
        # Load lines into object
        next(reader)
        data = [ tuple(row) for row in reader ]

        # create domain crendentials dictionary 
        for row in data :
            domain = row[0]
            username = row[1]
            password = row[2]
            retu[ domain ] = { "usr":username, "pwd":password }

    return retu


def add_payload(tgt_dir, urls) :
    """_summary_

    Args:
        tgt_dir (_type_): _description_
        urls (_type_): _description_
    """
    rl, rl_d = get_fileobj('lists.json',tgt_dir)[0:2]
    rl_d["payload"].append(urls)
    with rl.open(mode="w+", encoding="utf-8") as outfile:
        json.dump(rl_d, outfile)

        

##########################################
# FETCHING
##########################################

def get_token (d_config, r):
    """_summary_

    Args:
        d_config (_type_): _description_
        r (_type_): _description_

    Returns:
        _type_: _description_
    """
    soup = BeautifulSoup( r.content, 'html.parser' )
    token_element = d_config["elements"]["token"]
    attrs = { 'name': token_element}
    token = soup.find('input', attrs=attrs)
    return token



def init_session (ov) :
    """_summary_

    Args:
        ov (_type_): _description_

    Returns:
        _type_: _description_
    """
    s = requests.Session()

    for domain, d_config in ov["d_configs"].items() :

        if domain in ov["skip_login"] or not d_config["login_required"] :
            continue

        payload = {
            "usr" : ov["pwds"][domain]["usr"],
            "pwd" : ov["pwds"][domain]["pwd"],
        }

        r = s.get( d_config["login"], headers=ov["headers"] )

        if d_config["token"] :

            token = get_token(d_config,r)
            if not token :
                sys.exit("ERROR: couhd not find `authenticity_token` on login form for '" + domain )
            payload.update(
                { d_config["elements"]["token"] : token.get('value').strip() }
            )
        p = s.post( d_config["login_url"] , data=payload, headers=ov["headers"])
        #print( domain + ": " + str(p.status_code) )
    return s



def check_env (ov, write=False, verbose=1) :

    # intitlize return value
    retu = {}

    ######### PRE ARCHIVE: DECLARE VARIABLES and LOAD FILES #########
    # simplify most used 
    tgt_dir = ov["PATHS"]["ARCHIVE_DIRECTORY"]
    bp = ov["BP"]

    # options
    opt = None
    if write :
        opt = "make"
    else :
        opt = "continue"

    # Verbose
    logger.info("Starting checks at %s with 'write' = '%s'", tgt_dir, write)

    # load
    ac,rc_d       = get_fileobj('config.yml',  tgt_dir, no_exist=opt, bp_in=bp["archive_config"],           )[:2]
    dc,dc_d       = get_fileobj('domains.yml', tgt_dir,                                                     )[:2]
    am,am_d,am_pd = get_fileobj('meta.json',   tgt_dir, no_exist=opt, bp_in=bp["archive_meta"],  clear=True )
    al,al_d       = get_fileobj('lists.json',  tgt_dir, no_exist=opt, bp_in=bp["archive_lists"], clear=True )[:2]

    ######### LOOP ARCHIVE: URLPATHS #########
    for up in iter_dir('archive', tgt_dir) :

        ######### PRE URLPATH: DECLARE VARIABLES and LOAD FILES #########
        # load
        uc, uc_d = get_fileobj('config.yml', up.absolute(), no_exist=opt,  bp_in=bp["urlpath_config"]           )[:2]
        um, um_d = get_fileobj('meta.json',  up.absolute(), no_exist=opt,  bp_in=bp["urlpath_meta"],  clear=True)[:2]
        ul, ul_d = get_fileobj('lists.json', up.absolute(), no_exist=opt,  bp_in=bp["urlpath_lists"], clear=True)[:2]

        # define url object
        urlpath = get_urlpath_from_dir(up.name)
        o = urlparse(um_d["scheme"]+urlpath)

        ######### LOOP URLPATHS: fetches #########
        p_items = [x for x in up.iterdir() if x.name not in ["config.yml", "meta.json", "lists.json"]]
        p_items.sort(key=lambda x: int(x.name), reverse=True)  

        for st in p_items :

            ######### fetch: DECLARE VARIABLES and LOAD FILES #########
            # load
            ht, ht_d = get_fileobj(up.name + '.html', st.absolute(),no_exist="continue",                       )[:2]
            sm, sm_d = get_fileobj("meta.json",       st.absolute(),no_exist=opt,        bp_in=bp["fetch_meta"])[:2]
            tm, tm_d = get_fileobj("meta.txt",        st.absolute(),no_exist="continue",                       )[:2]

            ######### fetch: VALIDATION and FIXES #########
            # missing placeholder html for '666' codes
            if not ht.is_file() :
                if str(sm_d["code"]) == "666":
                    if write :
                        with ht.open(mode="w+",encoding='utf-8') as outfile :
                            outfile.write("<html>666</html>")
                else :
                    sys.exit("ERROR: no html file at non-666 directory '" + str(st.absolute()) +"'" )

            # inserting response code into metas from legacy files
            if not sm_d["code"] :
                sm_d["code"] = tm_d.rstrip()
                if write :
                    tm.unlink()

            # make sure code is stored as string
            sm_d["code"] = str(sm_d['code'])
            code = sm_d["code"]

            # re-evaluate statuses
            if str(code) == "404" :
                sm_d["status"] = "lost"
            elif str(code) == "666" :
                sm_d["status"] = "bad"
            elif str(code) != "200" :
                sm_d["status"] = "miss" 
            elif str(o.netloc) not in dc_d.keys() :
                sm_d["status"] = "unkown"
            else :
                sm_d["status"] = "success"

            ######### fetch: STATS and WRITES #########
            sm_d["size"] = os.path.getsize(ht.absolute())
            um_d["size"] += sm_d["size"]
            am_d["size"] += + sm_d["size"]
            um_d["fetches"] += 1
            am_d["fetches"] += 1
            al_d["fetch_times"].append(st.name)
            ul_d["history"].append(
                {
                    "name" : st.name,
                    "code" : sm_d["code"],
                    "status" : sm_d["status"], 
                    "size" : sm_d["size"]
                }
            )

            if write :
                with sm.open(mode="w+", encoding="utf-8") as outfile :
                    json.dump(sm_d,outfile)

        ######### POST URLPATH: STATS and WRITES #########
        # define last fetch
        last_fetch=ul_d["history"][-1]
        last_status=last_fetch["status"]
        last_code=last_fetch["code"]

        um_d["last_code"]     = last_code
        um_d["last_status"]   = last_status
        um_d["last_fetched"]  = last_fetch["name"]
        um_d["first_fetched"] = ul_d["history"][0]["name"]

        # statuses
        if last_status not in al_d:
            al_d[last_status] = []
            am_d[last_status] = 0
        if last_status != "success" :
            al_d["fail"].append(o.geturl())
            am_d["fail"] += 1
        al_d[last_status].append(o.geturl())
        am_d[last_status] += 1
        
        # codes
        if last_code not in al_d["codes"]:
            al_d["codes"][last_code] = []
            am_d["codes"][last_code] = 0
        al_d["codes"][last_code].append(o.geturl())
        am_d["codes"][last_code] += 1

        # urls
        um_d["url"] = o.geturl()
        al_d["urls"].append(o.geturl())
        am_d["urls"] += 1

        # domains
        um_d["domain"] = o.netloc
        if o.netloc not in al_d["domains"] :
            al_d["domains"].append(o.netloc)
            am_d["domains"] += 1

        # write
        if write :
            with um.open(mode="w+", encoding="utf-8") as outfile :
                json.dump(um_d,outfile)
            with ul.open(mode="w+", encoding="utf-8") as outfile :
                json.dump(ul_d,outfile)
            with uc.open(mode="w+", encoding="utf-8") as outfile :
                json.dump(uc_d,outfile)
    
    ######### POST ARCHIVE: STATS and WRITES #########
    # write
    retu["fetch_times"] =  al_d.pop("fetch_times")
    retu["urls"] = al_d.pop("urls")

    if write :
        with al.open(mode="w", encoding="utf-8") as outfile :
            json.dump(al_d,outfile,indent=4)
        with am.open(mode="w", encoding="utf-8") as outfile :
            json.dump(am_d,outfile,indent=4)
        with dc.open(mode="w", encoding="utf-8") as outfile :
            yaml.dump(dc_d,outfile)
        with ac.open(mode="w", encoding="utf-8") as outfile :
            yaml.dump(rc_d,outfile)

    retu["meta"] = am_d
    retu["prev_meta"] = am_pd
    diff, out = gen_diff(am_d,am_pd)
    print(out)

    return retu

def get_headers(config,  *argv) :
    retu = {}
    headers = []
    if len(argv) > 0 :
        headers = argv[1:]
    else :
        headers = config["default_headers"]

    for header, num in headers :
        retu[header] = config[header][num]
    return retu
    
def fetch_urls (ov) :
    retu = {}

    # root files
    tgt_dir = ov["PATHS"]["ARCHIVE_DIRECTORY"]
    rp = iter_dir('archive', tgt_dir, givedir=True, no_exist="make")[0]
    dc, dc_d = get_fileobj('domains.yml', tgt_dir)[:2]
    rc, rc_d = get_fileobj('config.yml', tgt_dir)[:2]

    # load up ov
    ov["skip_login"] = rc_d["skip_login"]
    ov["headers"] = get_headers(rc, ['User-Agent', 0])
    ov["urls"] = import_urls(ov["PATHS"]["PATH_TO_URLS"])
    ov["pwds"] = import_pwds(ov["PATHS"]["PATH_TO_PWDS"], delim=' ')
    ov["d_config"] = dc_d
    ov["a_config"] = rc_d


    # begin session
    s = init_session(ov)
    sys.exit("ERROR")
    for url in ov["urls"]:

        # url object
        url = url.rstrip()
        o = urlparse(url)


        #urlpathfiles
        urlpath = o.netloc+"_"+o.path.replace("/","_")
        up = iter_dir(urlpath,               rp.absolute(),       givedir=True, no_exist="continue")[0]
        st = iter_dir(str(int(time.time())), up.absolute(),       givedir=True, no_exist="continue")[0]
        um, um_d = get_fileobj('meta.json', up.absolute(), no_exist="continue")[:2]
        ul, ul_d = get_fileobj('list.json', up.absolute(), no_exist="continue")[:2]
        uc, uc_d = get_fileobj('config.yml', up.absolute(), no_exist="continue")[:2]
        ht          = get_fileobj(up.name + '.html', st.absolute(), no_exist="continue")[0]
        rt          = get_fileobj('response.txt', st.absolute(), no_exist="continue")[0]
        sm, sm_d = get_fileobj('meta.json', st.absolute(), no_exist="continue",bp_in=bp["fetch_meta"])[:2]

        sm_d["scheme"] = o.scheme

        #########################

        if not up.is_dir() :
            up.mkdir()

            #latest = get_latest_strtime_dir(up)

            #if latest is None or len(os.listdir(latest.absolute())) == 0:
            #    sys.exit("ERROR: Bad directory at '"+str(up.absolute())+"'")

            #lsm, lsm_d = get_fileobj('meta.json', latest.absolute(),no_exist="continue")
            #if str(lsm_d["code"]) in ["200", "404"] :

        # skip
        #if o.netloc in ov["a_config"]["skip_domains"] :
        #    print("...skipping backup at '"  + url + "' at domain '" + str(o.netloc)+"'")
        #    continue
            #    continue

        st.mkdir()

        try :
            r = s.get(url, headers=ov["headers"])
        except requests.exceptions.ConnectionError:

            sm_d["code"] = "666"

            with ht.open(mode="w+",encoding='utf-8') as outfile :
                outfile.write("<html>666</html>")
            with sm.open(mode="w+",encoding='utf-8') as outfile :
                json.dump(sm_d, outfile)

            continue

        sm_d["code"] = r.status_code

        with ht.open(mode="w+",encoding='utf-8') as outfile :
            outfile.write(str(r.content))

        with sm.open(mode="w+",encoding='utf-8') as outfile :
            json.dump(sm_d, outfile)

        time.sleep(2)

    return retu



##########################################
# MAIN
##########################################

#check_env(ov,write=True)
fetch_urls(ov)
#retu = check_env(ov)
