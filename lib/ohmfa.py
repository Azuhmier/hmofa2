""" doc """
import json
import sys
import os

class Ohmfa :
    """ doc """
    h = {}
    b = {}
    p = {
        'top': '../..',
        'bt_values':'db/buffers/t_values',
        'bvalues':'db/buffers/values.txt',
        'ht_uids':'db/parse/opsTypes.json',
        'huidStats':'db/analysis/uidStats.json',
        'ht_values':'db/analysis/opsValues.json',
        'huids':'db/parse/ops.json',
        'ht_valueStats':'db/analysis/uidStats.json',
        'ht_valueAliases':'db/resolve/t_valueAliases.json' },
    c = {}
    
    def __init__(self, name):
        """ doc """
        self.name = name

