""" doc """
import os
import re
import json

def importFromJson(filePath):
    with open(filePath, "r") as openfile:
        jsonDict = json.load(openfile)
    return jsonDict

def get_abs_path(rel_path) :
    """ doc """
    pwd = os.path.dirname(__file__)
    messy_abs_path = os.path.join(pwd, rel_path)
    abs_path = os.path.abspath(messy_abs_path)
    return abs_path

def read_file(file_path):
    """ doc """
    with open(file_path, "r", encoding="utf-8") as outfile :
        lines = outfile.read().splitlines()
    return lines

def __import_regexs():
    """ doc """
    file_path = get_abs_path('../../.ohmfa/hmofa/ops_regex.txt')
    lines = read_file(file_path)
    res = {}
    for line in lines :
        if line[0] != ' ' :
            node_type = line
            res[node_type]=[]
        else :
            line.rstrip()
            line=line.replace(' ','')
            res[node_type].append(line)
    for key in res :
        res[key] = ''.join(res[key])
    return res

regexes = __import_regexs()

def gen_lvls() :

        file_path = get_abs_path('../../.ohmfa/hmofa/ops_config.json')
        file_path2 = get_abs_path('../../.ohmfa/global/config.json')
        h = importFromJson(file_path)
        g = importFromJson(file_path2)
        lvls={}
        for type in g['types'] :
            lvls[type] = g['types'][type]['lvl']
        for type in h['types'] :
            rellvl = h['types'][type]['rel_lvl'][0]
            gtype = h['types'][type]['rel_lvl'][1]
            lvl = g['types'][gtype]['lvl']
            lvls[type] = rellvl+lvl
        print(lvls)
        diff = 1 - min(list(lvls.values())) 
        for key in lvls :
            lvls[key] = lvls[key] + diff
        print(lvls)

gen_lvls()
