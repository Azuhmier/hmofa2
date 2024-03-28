"""doc"""
import os
import json
from lib.utilities.file_manager import FileManager
from lib.main import Main
class Controller(Main):
    """ doc """

    controller_type = None
    p_root = None
    p_config = None
    f=None

    def __init__(self, key=None,parent=None,top=None,**kwargs):
        """ doc """
        if parent is None :
            key = 'global'
        self.key=key
        self.parent = parent
        self.top = top
        self.gen_file_manager()
        self.do_args(**kwargs)

    def do_args(self, **kwargs):
        """ doc """
    

    def gen_file_manager(self):
        """ doc """

        selected = None
        dspts = None

        if "file_managers" in self.config :
            dspts = self.config["file_managers"]

        if "selected_file" in self.config :
            selected = self.config["selected_file"]

        self.f= FileManager(root=self.root,dspts=dspts, selected=selected)

    @property
    def root(self):
        """ doc """

        if self.p_root is None:
            self.p_root = self.top.p_root
        return self.p_root 

    @property
    def config(self):
        """ doc """

        if self.p_config is None:

            if self.controller_type in ['main', 'general']:
                config_path = os.path.join(self.root,".ohmfa/"+self.key+"/config.json")
                with open(config_path, "r", encoding='utf-8') as openfile:
                    self.p_config = json.load(openfile)
            else :
                self.p_config = self.parent.p_config[self.key]
        return self.p_config