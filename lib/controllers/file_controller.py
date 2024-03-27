"""doc"""

import sys
import os
import json
from lib.controllers.controller import Controller


class FileController(Controller):
    """ doc """


    def get_abs_path(self, rel_path):
        """ doc """
        root = self.g_config['root']
        res = os.path.join(root, rel_path)
        return res if res is not None else sys.exit(" Error: NoneType Returned")


    def list_dir(self, rel_path, no_file_ext=True):
        """ doc """

        path = self.get_abs_path(rel_path)
        dir_list = list(os.listdir(path))

        res = None

        if no_file_ext :
            res = dir_list

        else :
            res = []
            for fname in dir_list:
                fext = self.get_file_ext(fname)
                res.append(fname+fext)

        return res if res is not None else sys.exit(" Error: NoneType Returned")


    def get_file_ext(self, any_path):
        """ doc """
        split_tup = os.path.splitext(any_path)
        res = split_tup[1]
        return res if res is not None else sys.exit(" Error: NoneType Returned")

    def get_file_name(self, any_path):
        """ doc """
        split_tup = os.path.splitext( any_path)
        res = split_tup[0]
        return res if res is not None else sys.exit(" Error: NoneType Returned")


    def export_to(self, rel_path, data):
        """ doc """
        path = self.get_abs_path(rel_path)
        file_ext = self.get_file_ext(path)

        content=None

        if file_ext == '.json' :
            content = json.dumps(data, indent=4)
        else :
            content = data

        file_dir = os.path.dirname(path)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

        with open(path, "w+",encoding='utf-8') as outfile :
            outfile.write(content)

        res = content

        return res if res is not None else sys.exit(" Error: NoneType Returned")


    def import_from(self, rel_path):
        """ doc """

        path = self.get_abs_path(rel_path)
        file_ext = self.get_file_ext(path)

        res=None

        with open(path, "r",encoding='utf-8') as openfile :

            if file_ext == '.json' :
                res = json.load(openfile)
            else :
                res = openfile.read().splitlines()

        return res if res is not None else sys.exit(" Error: NoneType Returned")
