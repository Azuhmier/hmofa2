"""doc"""
import os
import json


class Controller:
    """ doc """

    g_config = None
    l_config = None
    name = None
    type = None

    def __init__(self, name=None,args=None):
        """ doc """
        # Global Config
        root = os.path.abspath('.')
        g_config_path = os.path.join(root,".ohmfa/global/config.json")
        with open(g_config_path, "r", encoding='utf-8') as openfile:
            self.g_config = json.load(openfile)
        self.g_config['root'] = root

        # Local Config
        if name is not None :
            self.name = name
            l_config_path = os.path.join(root,".ohmfa/"+self.name+"/config.json")
            with open(l_config_path, "r", encoding='utf-8') as openfile:
                self.l_config = json.load(openfile)

        self.do_args(args)

    def do_args(self,args):
        """ doc """
