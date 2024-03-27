""" doc """
import requests
import time
import os
from lib.file_widget import Main

class Fetch(Main):
    """doc """

    r = None
    tgt_dir = None
    time_out = 1

    def do_args(self, args) :
        """ doc """
        self.check_args(args)
        self.do_special(args)

    def do_special(self,args):
        """ doc """


    def get_content (self, url) :
        """ doc """
        time.sleep(self.time_out)
        session = requests.Session()
        self.r = session.get(url)

    def get_path(self,file_name):
        """ doc """
        return os.path.join(self.tgt_dir,file_name)
