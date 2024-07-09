#!/usr/bin/env python3
"""_summary_

Returns:
    _type_: _description_
"""
import os
from pathlib import Path
import json
import sys
import csv
import re
from io import StringIO, BytesIO
from lxml import etree
import time
import glob
from urllib.parse import urlparse
import yaml
import requests
import copy
from bs4 import BeautifulSoup

bp = {
    "archive_meta" : { 
        "failed" : 0,
        "size" : 0,
        "total_domains" : 0,
        "total_files" : 0,
        "total_url_paths" : 0,
    },
    "archive_config" : {
        "name" : None,
    },
    "archive_lists" : {
        "domains" : [],
        "failed" : [],
        "urlpaths" : [],
    },
    "urlpath_meta" : {
        "domain" : None,
        "path" : None,
        "size" :0,
        "state" : None,
        "total_scrapes" : 0,
        "urlpath" : None,
    },
    "urlpath_config" : {
        "skip" : "",
    },
    "urlpath_lists" : {
        "changes" : [],
        "codes" : [],
        "strtimes" : [],
        "updated" : [],
    },
    "scrape_meta" : {
        "code" : None,
        "config" : None,
        "header" : None,
        "scheme" : None,
        "size" : None,
        "state" : None,
        "time_end" : None,
        "time_start" : None,
    },
}

PWDS_PATH     = '/home/azuhmier/.pwds'
URL_PATH      = "/home/azuhmier/hmofa/hmofa/.ohm/output/paged_lists/objs/plain/url.txt"
ARCHIVE_PATH  = "/home/azuhmier/hmofa/test"

def get_latest_strtime_dir(directory) :
    """returns the strtime directory with the newest time

    Modules: Path from pathlib

    Args:
        directory (_str_): _description_

    Returns:
        _str_: self explainatory
    """
    list_of_files = glob.glob(directory+"/*")
    latest =  max( [Path(x).stem for x in list_of_files] )
    retu = Path(os.path.join(directory,latest))
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
        make (bool, optional): _description_. Defaults to False.
        bp (_type_, optional): _description_. Defaults to None.

    Returns:
        _posixpath_, _type : 
    """
    if no_exist not in ["error", "make", "continue"] :
        sys.exit("ERROR: 'Invalid value for parameter 'no_exist' - '" + no_exist + "' ")

    # create file_object. 
    path = name
    if parent_directory :
        path = os.path.join(parent_directory, name)
    p = Path(path)

    # clear option
    if clear and os.path.isfile(p.absolute()):
        p.unlink()

    # initilize data
    bp_copy = copy.deepcopy(bp_in)
    data=bp_copy

    # JSON
    if p.is_file() :
        with p.open(mode='r', encoding="utf-8") as infile:
            if p.suffix == ".json":
                data=json.load(infile)
            elif p.suffix == ".yml":
                data = yaml.safe_load(infile)
            else :
                data = infile

    elif no_exist == "make":
        with p.open(mode='w+', encoding="utf-8") as outfile:
            if p.suffix == ".json":
                json.dump(bp_copy,outfile)
            elif p.suffix == ".yml":
                yaml.dump(bp_copy,outfile)
            else :
                p.write_text(bp_copy, encoding="utf-8")

    elif no_exist == "error" :
        sys.exit("ERROR: '" + p.absolute() + "' does not Exist")

    return p, data



def iter_dir(name, parent_directory=None, no_exist = "error", givedir=False) :
    """_summary_

    Args:
        name (_type_): _description_
        parent_directory (_type_, optional): _description_. Defaults to None.
        make (bool, optional): _description_. Defaults to False.

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
    elif no_exist == 'error' :
        sys.exit("ERROR: '" + p.absolute() + "' does not Exist")
    elif not givedir :
        directory_list = p.iterdir()

        #IS EMPTY?
        if len(directory_list) != 0 :
            for p_item in directory_list :
                retu.append(p_item)
    else :
        retu.append(p)

    return retu



def check_env (tgt_dir,bp) :
    re_io = re.compile(".+(io|live|xyz)$")
    # ARCHIVE

    # meta
    am,am_data = get_fileobj('meta.json',          tgt_dir, no_exist="make", bp_in=bp["archive_meta"],  clear=True )
    ac,ac_data = get_fileobj('config.yml',         tgt_dir, no_exist="make", bp_in=bp["archive_config"],           )
    dc,dc_data = get_fileobj('domains_config.yml', tgt_dir, no_exist="make", bp_in=domains_config,                 )
    al,al_data = get_fileobj('lists.json',         tgt_dir, no_exist="make", bp_in=bp["archive_lists"],  clear=True)

    # URLPATHS
    for up in iter_dir('archive', tgt_dir) :

        urlpath = get_urlpath_from_dir(up.name)
        o = urlparse("https://"+urlpath)
        al_data["domains"].append(o.netloc)
        al_data["urlpaths"].append(urlpath)

        uc, uc_data = get_fileobj('config.yml', up.absolute(), no_exist="make",  bp_in=bp["urlpath_config"],           )
        um, um_data = get_fileobj('meta.json',  up.absolute(), no_exist="make",  bp_in=bp["urlpath_meta"],   clear=True)
        ul, ul_data = get_fileobj('lists.json', up.absolute(), no_exist="make",  bp_in=bp["urlpath_lists"],  clear=True)

        #print(um_data["domain"])
        um_data["domain"] = o.netloc
        um_data["urlpath"] = urlpath


        # STRTIMES 
        for st in up.iter_dir() :
            if st.name not in ["config.yml", "meta.json", "lists.json"]:

                ht, ht_data = get_fileobj(up.name + '.html', st.absolute())
                sm, sm_data = get_fileobj("meta.json",       st.absolute())

                ul_data["codes"].append(sm_data["code"])
                am_data["size"]        = am_data["size"] + sm_data["size"]
                am_data["total_files"] = am_data["total_files"] + 1


        m = re_io.match(str(um_data["domain"]))
        if ul_data["codes"][-1] != "200" :
            al_data["failed"].append(urlpath)
            if  um_data["domain"] == "archiveofourown.org" :
                um_data["state"] = "deleted"
            else :
                um_data["state"] = "error"
        elif  m:
            um_data["state"] = "unsatisfactory"
        else :
            um_data["state"] = "satisfactory"

        with um.open(mode="w+", encoding="utf-8") as outfile :
            json.dump(um_data,outfile)
        with ul.open(mode="w+", encoding="utf-8") as outfile :
            json.dump(ul_data,outfile)
    
    # Archive Post Processing

    # lists
    al_data["domains"]            = list(set(al_data["domains"]))
    with al.open(mode="w", encoding="utf-8") as outfile :
        json.dump(al_data,outfile)

    # meta
    #al_data["failed"].sort()
    am_data["failed"]    = len(al_data["failed"])
    am_data["total_url_paths"]    = len(al_data["urlpaths"])
    am_data["total_domains"]      = len(al_data["domains"])
    with am.open(mode="w", encoding="utf-8") as outfile :
        json.dump(am_data,outfile)
    







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



##########################################
# SCRAPING
##########################################

def get_payload (d_config, pwds, domain) :
    """_summary_

    Args:
        db (_type_): _description_
        domain (_type_): _description_

    Returns:
        _type_: _description_
    """
    usr = d_config["usr"]
    pwd = d_config["pwd"]
    payload = None
    if usr  is not None and pwd is not None :
        payload = {
            usr : pwds[domain]["usr"],
            pwd : pwds[domain]["pwd"],
        }

    return payload

def get_token (d_config, r):
    """_summary_

    Args:
        d_config (_type_): _description_
        r (_type_): _description_

    Returns:
        _type_: _description_
    """
    soup  = BeautifulSoup( r.content, 'html.parser' )
    token = soup.find('input', attrs={'name': d_config["token"]})
    return token

def login ( dc_data, pwds, header ) :
    """_summary_

    Args:
        db (_type_): _description_

    Returns:
        _type_: _description_
    """
    s = requests.Session()
    for domain in dc_data :
        d_config = dc_data[domain]
        payload = get_payload(d_config, pwds, domain)
        if payload is not None :
            r = s.get( d_config["login"], headers=header )
            if d_config["token"] is not None :
                token = get_token(d_config, r)
                if token is None:
                    sys.exit("ERROR: could not find `authenticity_token` on login form for '" + domain )
                else :
                    payload.update(
                        { d_config["token"] : token.get('value').strip() }

                    )
            login_url = d_config["login"]
            p = s.post( login_url , data=payload, headers=header)
            #print( domain + ": " + str(p.status_code) )
    return s



def scrape_urls (tgt_dir) :

    pwds = import_pwds(PWDS_PATH,' ')
    urls = import_urls(URL_PATH)

    ap = iter_dir('archive', tgt_dir, givedir=True, no_exist="make")[0]
    dc, dc_data = get_fileobj('domains_config.yml', tgt_dir)
    ac, ac_data = get_fileobj('domains_config.yml', tgt_dir)

    s = login(dc_data,pwds,ac["header"])
    for url in urls :

        o = urlparse(url)
        urlpath = o.netloc+o.path.replace("/","_")

        up = iter_dir(urlpath,               ap.absolute(),       givedir=True, no_exist="make")[0]
        st = iter_dir(str(int(time.time())), up.absolute(),       givedir=True, no_exist="make")[0]

        ht = get_fileobj('lists.json', st.absolute(), no_exist="continue")[0]
        rt = get_fileobj('response.txt', st.absolute(), no_exist="continue")[0]
        sm, sm_data = get_fileobj('meta.json', st.absolute(), no_exist="continue")

        if o.netloc in [ 'git.io','raw.githubusercontent.com'] :
            continue

        if up.is_dir() :
            latest = get_latest_strtime_dir(up.absolute())
            lsm, lsm_data = get_fileobj('meta.json', latest.absolute())
            if lsm_data["code"] == "200" :
                continue

        ## An authorised request.
        try :
            r = s.get(url, headers=ac_data["header"])
        except requests.exceptions.ConnectionError:
            sm_data["code"] = 666
            continue
        sm_data["code"] = r.status_code

        with ht.open(mode="w+",encoding='utf-8') as outfile :
            outfile.write(str(r.content))
        with sm.open(mode="w+",encoding='utf-8') as outfile :
            json.dump(outfile, sm_data)

        time.sleep(2)



##########################################
# MAIN
##########################################

check_env(ARCHIVE_PATH,bp)
#scrape_urls(urls,db,ARCHIVE_PATH,bp)
