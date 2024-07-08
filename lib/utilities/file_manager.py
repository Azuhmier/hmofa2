"""doc"""
import sys
import os
import json
import copy
from lib.main import Main



class FileManager(Main):
    """ doc """

    reldir = None
    subdir = None
    fname = None
    fext = None
    _relpath = None
    root = None
    content = None
    dspts = {}
    selected = None
    bp = {
        'reldir' : None,
        'subdir' : None,
        'fname' : None,
        'fext' : None,
        'content' : None, }

    def __init__(self, root=None, selected = None, dspts = None):
        """doc"""
        self.selected = selected
        self.root = root
        if dspts is not None :
            for dspt in dspts:
                self.add_dspt(dspt)
        if self.selected is not None:
            self.select()

    def select(self):
        """ doc """
        dspt = self.dspts[self.selected]
        self.resolve_attrs(dspt)

    def add_dspt(self, dspt_arg):
        """ doc """
        dspt = copy.deepcopy(dspt_arg)
        name = dspt.pop('name')
        dspt = self.resolve_dspt(dspt,self.bp)
        self.dspts[name] = dspt


    def resolve_selection(self, key, value, select):
        """ doc """
        res = None
        if select is None :
            res = self.resolve_arg(key,value)
        else :
            res = self.dspts[select][key]
        return res
            

    def get_abs_path(self, relpath=None,select=None):
        """ doc """
        relpath = self.resolve_selection('relpath', relpath, select)
        res = os.path.join(self.root, relpath)
        return res if res is not None else sys.exit(" Error: NoneType Returned")


    def list_dir(self, reldir=None, no_file_ext=True, select=None):
        """ doc """

        reldir = self.resolve_selection('reldir', reldir, select)
        path = self.get_abs_path(reldir)
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


    def export_to(self, relpath=None, content=None,select=None):
        """ doc """

        relpath = self.resolve_selection('relpath', relpath, select)
        content = self.resolve_selection('content', content, select)
        fext = self.resolve_selection('fext', None, select)

        path = self.get_abs_path(relpath)

        data = None
        if fext == '.json' :
            data = json.dumps(content, indent=4)
        else :
            data = content

        file_dir = os.path.dirname(path)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

        with open(path, "w+",encoding='utf-8') as outfile :
            outfile.write(data)



    def import_from(self, relpath=None, select=None):
        """ doc """
        relpath = self.resolve_selection('relpath', relpath, select)
        fext = self.resolve_selection('fext', None, select)

        path = self.get_abs_path(relpath)


        with open(path, "r",encoding='utf-8') as openfile :

            if fext == '.json' :
                self.content = json.load(openfile)
            else :
                self.content = openfile.read().splitlines()


    @property
    def fnamext(self):
        """ doc """
        fext = self.fext
        fname = self.fname
        if self.fext is None:
            fext = ''
        return fname + fext

    @property
    def subpath(self):
        """ doc """
        fext = self.fext
        fname = self.fname
        subdir = self.subdir

        if self.fext is None:
            fext = ''

        fnamext =  fname + fext

        if subdir is None:
            subdir = ''

        return os.path.join(subdir, fnamext)

    @property
    def relsubdir(self):
        """ doc """
        return os.path.join(self.reldir,self.subdir)

    @property
    def relpath(self):
        """ doc """
        return os.path.join(self.relsubdir,self.fnamext)
