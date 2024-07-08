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
import time
import glob
from urllib.parse import urlparse
import yaml
import requests
from bs4 import BeautifulSoup

bp = {
    "archive_meta" : { 
        "size" : 0,
        "total_url_paths" : 0,
        "total_domains" : 0,
        "total_files" : 0,
        "elapsed_time_max" : None,
        "elapsed_time_min" : None,
        "elapsed_time_avg" : None,
        "elapsed_time_total" : None,
    },
    "scrape_meta" : {
        "url" :None,
        "size" : None,
        "time_start" : None,
        "time_end" : None,
        "code" : None,
        "config" : None,
        "header" : None,
        "scheme" : None,
        "method" : None,

        "change" : None,
        "credentials" : None,
        "cookies" : None,
        "interrupted" : None,
    },
    "urlpath_meta" : {
        "url_path" : None,
        "domain" : None,
    },
    "archive_config" : {
    },
    "urlpath_config" : {
    },
    "archive_lists" : {
        "url_paths" : [],
        "domains" : [],
        "elapsed_times" : []
    }
}

PWDS_PATH = '/home/azuhmier/.pwds'
URL_PATH  = "/home/azuhmier/hmofa/hmofa/.ohm/output/paged_lists/objs/plain/url.txt"
ARCHIVE_PATH  = "/mnt/c/Users/Azuhmier/Desktop/test"

domains_config = {
    "archiveofourown.org" : {
        "login" : "https://archiveofourown.org/users/login",
        "usr" : "user[login]",
        "pwd" : 'user[password]',
        "token" : 'authenticity_token',
        "txt" : ['div', 'id', 'chapters'],
        "join" : 1,
        "find" : ['p','a'],
        "strip" : 1,
    },
    "sofurry.com" : {
        "login" : "https://www.sofurry.com/user/login",
        "usr" : "LoginForm[sfLoginUsername]",
        "pwd" : "LoginForm[sfLoginPassword]",
        "txt" : ['div', 'id', 'sfContentBody'],
        "find" : ['p', 'div'],
        "join" : 1,
        "token" : None,
    },
    "furaffinity.net" : {
        "login" : "https://www.furaffinity.net/login",
        "usr" : "name",
        "pwd" : "pass",
        "txt" : ['div', 'class', 'submission-description user-submitted-links'],
        "find" : ['i'],
        "join" : 1,
        "token" : None,
        "metod" : "login",
    },
}

domains_config = {
    "archiveofourown.org" : {
        "login" : "https://archiveofourown.org/users/login",
        "usr" : "user[login]",
        "pwd" : 'user[password]',
        "token" : 'authenticity_token',
        "txt" : ['div', 'id', 'chapters'],
        "join" : 1,
        "find" : ['p','a'],
        "strip" : 1,
    },
    "sofurry.com" : {
        "login" : "https://www.sofurry.com/user/login",
        "usr" : "LoginForm[sfLoginUsername]",
        "pwd" : "LoginForm[sfLoginPassword]",
        "txt" : ['div', 'id', 'sfContentBody'],
        "find" : ['p', 'div'],
        "join" : 1,
        "token" : None,
    },
    "furaffinity.net" : {
        "login" : "https://www.furaffinity.net/login",
        "usr" : "name",
        "pwd" : "pass",
        "txt" : ['div', 'class', 'submission-description user-submitted-links'],
        "find" : ['i'],
        "join" : 1,
        "token" : None,
        "metod" : "login",
    },
}

domains_config = {
    "archiveofourown.org" : {
        "view": "all",
        "tags" : {
            "csspath": "html body.logged-in div#outer.wrapper div#inner.wrapper div#main.works-show.region div.wrapper dl.work.meta.group",
            "xpath"   : "/html/body/div/div[1]/div/div[2]/dl",
        },
        "title" : {
            "csspath":"html body.logged-in div#outer.wrapper div#inner.wrapper div#main.works-show.region div#workskin div.preface.group h2.title.heading",
            "xpath":"/html/body/div/div[1]/div/div[3]/div[1]/h2",
        },
        "author" : {
            "csspath":"html body.logged-in div#outer.wrapper div#inner.wrapper div#main.works-show.region div#workskin div.preface.group h3.byline.heading a",
            "xpath":"/html/body/div/div[1]/div/div[3]/div[1]/h3/a",
        },
        "description" : {
            "csspath":"",
            "xpath":"",
        },
        "date_created" : {
            "csspath":"",
            "xpath":"",
        },
        "date_published" : {
            "csspath":"",
            "xpath":"",
        },
        "date_accessed" : {
            "csspath":"",
            "xpath":"",
        },
        "views" : {
            "csspath":"",
            "xpath":"",
        },
        "comments" : {
            "csspath":"",
            "xpath":"",
        },
        "credentials" : {
            "csspath":"",
            "xpath":"",
        },
        "mature_warning" : {
            "csspath":"",
            "xpath":"",
        },
        "full_view" : {
            "csspath":"",
            "xpath":"",
        },
        "download" : {
            "csspath":"",
            "xpath":"",
        },
        "stats" : {
            "csspath":"",
            "xpath":"",
        },
        "login_status" : {
            "csspath":"",
            "xpath":"",
        },
        "main_content" : {
            "csspath":"",
            "xpath":"",
        },
        "notes" : {
            "csspath":"",
            "xpath":"",
        },
        "chapters" : {
            "csspath":"",
            "xpath":"",
        },
        "author_home" : {
            "csspath":"",
            "xpath":"",
        },
        "author_home_stories" : {
            "csspath":"",
            "xpath":"",
        },
        "word_count" : {
            "csspath":"",
            "xpath":"",
        },
        "total_chapters" : {
            "csspath":"",
            "xpath":"",
        },
        "if_finished" : {
            "csspath":"",
            "xpath":"",
        },
        "art" : {
            "csspath":"",
            "xpath":"",
        },
        "pfp" : {
            "csspath":"",
            "xpath":"",
        },
    },
    "www.sofurry.com" : {
        "view": "limited",
    },
    "rentry.org" : {
        "view" : "all",
        "aliases" : ["rentry.co"],
    },
    "www.furaffinity.net" : {
        "view" : "limited",
    },
    "www.reddit.com" : {
    },
    "drive.google.com" : {
    },
    "docs.google.com" : {
    },
    "mega.nz" : {
    },
    "pastebin.com" : {
    },
    "fiction.live" : {
    },

    "www.fanfiction.net" : {
    },
    "www.literotica.com" : {
        "aliases" : ["literotica.com"]
    },
    "pastes.psstaudio.com" : {
    },
    "pastefs.com" : {
    },
    "hardbin.com" : {
    },
    "files.catbox.moe" : {
    },
    "catbox.moe" : {
    },
    "snootgame.xyz" : {
    },

    "mcstories.com" : {
    },
    "poneb.in" : {
    },

    "snekguy.com" : {
    },
    "blokfort.com" : {
    },

    "codanon.itch.io" : {
    },
    "frulepllc.itch.io" : {
    },
    "tetchyy.itch.io" : {
    },
    "oliver-hart.itch.io" : {
    },
    "spacedimsum.itch.io" : {
    },
    "eloisanon.itch.io" : {
    },
}


def get_latest(directory) :
    """_summary_

    Args:
        directory (_type_): _description_

    Returns:
        _type_: _description_
    """
    list_of_files = glob.glob(directory+"/*")
    retu =  max( [Path(x).stem for x in list_of_files] )
    return retu



def get_fileobj(name, parent_directory=None, make=False, bp=None, getdata=True, clear=False) :
    """_summary_

    Args:
        name (_type_): _description_
        parent_directory (_type_, optional): _description_. Defaults to None.
        make (bool, optional): _description_. Defaults to False.
        bp (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    # create fileob
    path=None
    if parent_directory :
        path = os.path.join(parent_directory, name)
    else :
        path = name
    p = Path(path)
    if clear :
        p.unlink()

    # initilize data
    data=bp

    if getdata :
        # JSON
        if p.suffix == ".json":
            if os.path.isfile(path) :
                with p.open(mode='r', encoding="utf-8") as infile:
                    data=json.load(infile)
            elif make:
                with p.open(mode='w+', encoding="utf-8") as outfile:
                    json.dump(bp,outfile)

        # YAML
        elif p.suffix == ".yml":
            if os.path.isfile(path) :
                with p.open(mode='r', encoding="utf-8") as infile:
                    data = yaml.safe_load(infile)
            elif make :
                with p.open(mode='w+', encoding="utf-8") as outfile:
                    data = yaml.dump(bp,outfile)

        # OTHER
        else :
            if os.path.isfile(path) :
                with p.open(mode='r',encoding='utf-8') as infile :
                    data = infile
            elif make :
                p.write_text(bp, encoding="utf-8")

    return p, data



def iter_dir(name, parent_directory=None, make=False, getdata=True) :
    """_summary_

    Args:
        name (_type_): _description_
        parent_directory (_type_, optional): _description_. Defaults to None.
        make (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """

    # create fileob
    path=None
    if parent_directory :
        path = os.path.join(parent_directory, name)
    else :
        path = name
    p = Path(path)

    # initilize retu
    retu = []

    if p.is_dir():
        directory_list = os.listdir(p.absolute())

        # IS EMPTY?
        if len(directory_list) != 0 :
            for item in directory_list :
                data=None
                item_path = os.path.join(path, item)
                p = Path(item_path)

                # json
                if not os.path.isdir(p.absolute()) and getdata:
                    if p.suffix == ".json":
                        with p.open(mode='r', encoding="utf-8") as infile:
                            data=json.load(infile)

                    # YAML
                    elif p.suffix == ".yml":
                        with p.open(mode='r', encoding="utf-8") as infile:
                            data = yaml.safe_load(infile)

                    # OTHER
                    else :
                        data = p.read_text(encoding="utf-8")

                retu.append([p, data])
    elif make:
        p.mkdir()

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



def check_env (tgt_dir) :

    am,am_data = get_fileobj('meta.json',tgt_dir, make=True, bp=bp["archive_meta"],clear=True)
    ac,ac_data = get_fileobj('config.yml',tgt_dir, make=False,bp=bp["archive_config"])
    dc,dc_data = get_fileobj('domains_config.yml',tgt_dir, make=False,bp=domains_config)
    al,al_data = get_fileobj('archive_lists.json',tgt_dir, make=True,bp=bp["archive_lists"],clear=True)

    #urlpaths
    for up,data in iter_dir('archive',tgt_dir) :

        urlpath = get_urlpath_from_dir(up.name)
        o = urlparse("https://"+urlpath)
        al_data["domains"].append(o.netloc)
        al_data["url_paths"].append(urlpath)

        uc, uc_data = get_fileobj('config.yml',up.absolute(), make=False,bp=bp["urlpath_config"])
        um, um_data = get_fileobj('meta.json',up.absolute(), make=False,bp=bp["urlpath_meta"])
        #um.unlink()

        # strtimes 
        for st, data in iter_dir(up.absolute()) :
            if st.name not in ["config.yml", "meta.json"]:
                start = time.time()
                ht, ht_data = get_fileobj(up.name + '.html', st.absolute(),getdata=True)
                end = time.time()
                al_data["elapsed_times"].append(end-start)
                sm, sm_data = get_fileobj("meta.json",st.absolute())
                am_data["size"] = am_data["size"] + sm_data["size"]
                am_data["total_files"] = am_data["total_files"] + 1
    
    al_data["domains"] = list(set(al_data["domains"]))
    am_data["total_url_paths"] = len(al_data["url_paths"])
    am_data["total_domains"] = len(al_data["domains"])
    am_data["elapsed_time_max"] = max(al_data["elapsed_times"])
    am_data["elapsed_time_min"] = min(al_data["elapsed_times"])
    am_data["elapsed_time_avg"] = sum(al_data["elapsed_times"])/len(al_data["elapsed_times"])
    am_data["elapsed_time_total"] = sum(al_data["elapsed_times"])

    with am.open(mode="w", encoding="utf-8") as outfile :
        json.dump(am_data,outfile)
    with al.open(mode="w", encoding="utf-8") as outfile :
        json.dump(al_data,outfile)






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

def get_payload (db, domain) :
    """_summary_

    Args:
        db (_type_): _description_
        domain (_type_): _description_

    Returns:
        _type_: _description_
    """
    config = db["config"]
    pwds   = db["pwds"]
    usr = config[domain]["usr"]
    pwd = config[domain]["pwd"]
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

def login ( db ) :
    """_summary_

    Args:
        db (_type_): _description_

    Returns:
        _type_: _description_
    """
    s = requests.Session()
    for domain in db["config"] :
        d_config = db["config"][domain]
        payload = get_payload(db, domain)
        if payload is not None :
            r = s.get( d_config["login"], headers=db["header"] )
            #print(r.text)
            #print(r.content)
            if d_config["token"] is not None :
                token = get_token(d_config, r)
                if token is None:
                    sys.exit("ERROR: could not find `authenticity_token` on login form for '" + domain )
                else :
                    payload.update(
                        { d_config["token"] : token.get('value').strip() }

                    )
            login_url = db["config"][domain]["login"]
            p = s.post( login_url , data=payload, headers=db["header"])
            print( domain + ": " + str(p.status_code) )
    return s



def scrape_urls (db, urls) :
    """_summary_

    Args:
        db (_type_): _description_
        urls (_type_): _description_
    """
    s = login( db)
    with open(ARCHIVE_PATH+"/verybad.txt","w+",encoding='utf-8') as outfile :
        outfile.write("")
    with open(ARCHIVE_PATH+"/bad.txt","w+",encoding='utf-8') as outfile :
        outfile.write("")
    for url in urls :
        print("")
        print("SCRAPING " +url.rstrip())

        o = urlparse(url)
        dirname = o.netloc+"_"+o.path.replace("/","_")
        bubdir = ARCHIVE_PATH+"/archive/"+dirname
        subdir = ARCHIVE_PATH+"/archive/"+dirname+"/"+str(int(time.time()))
        isExist = os.path.exists(bubdir)
        if o.netloc not in db["domains"]:
            db["domains"].append(o.netloc)
        if o.netloc in [ 'git.io','raw.githubusercontent.com'] :
            continue
        if isExist :
            list_of_files = glob.glob(bubdir+"/*") # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)
            fn = os.path.basename(latest_file)

            with open(bubdir+"/"+fn+"/meta.txt","r",encoding='utf-8') as outfile :
                Lines = outfile.readlines()
                line = Lines[0].rstrip()
                if line == "200" :
                    print("...skipping")
                    continue
                #elif line =="404":
                #    print("...skipping")
                #    continue

                #elif line =="503":
                #    print("...skipping")
                #    continue

                else :
                    print("...trying again")

        ## An authorised request.
        very_bad = False
        try :
            r = s.get(url, headers=db["header"])
        except requests.exceptions.ConnectionError:
            with open(ARCHIVE_PATH+"/verybad.txt","a",encoding='utf-8') as outfile :
                outfile.write(url.rstrip()+"\n")
            very_bad = True
        if very_bad :
            continue
        code = r.status_code
        print("... " +str(code))

        os.makedirs( subdir )
        with open(subdir+"/"+dirname+".html","w+",encoding='utf-8') as outfile :
            outfile.write(str(r.content))
        with open(subdir+"/meta.txt","w+",encoding='utf-8') as outfile :
            outfile.write(str(code))
        if str(code) != "200" :
            print("... BAD!!")
            with open(ARCHIVE_PATH+"/bad.txt","a",encoding='utf-8') as outfile :
                outfile.write(url.rstrip()+"\n")

        time.sleep(2)

    with open(ARCHIVE_PATH+"/domains.txt","w+",encoding='utf-8') as outfile :
        outfile.write("\n".join(db["domains"]))



##########################################
# MAIN
##########################################

# Imports
pwds = import_pwds(PWDS_PATH,' ') 
urls = import_urls(URL_PATH)

# db
db = {
    "domains" : [],
    "bad" : [],
    "config" : domains_config,
    "pwds" : pwds,
    "header" : {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
}


check_env(ARCHIVE_PATH)
# Scrape
#scrape_urls(db, urls)
