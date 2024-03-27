""" doc  """
import sys
import os
from lib.controllers.file_controller import FileController

class SingleFileController(FileController):
    """ doc """

    tgt_dir = None
    fname = None
    fext = None
    fnamext = None
    subdir = None
    subpath = None
    relpath = None
    content = None


    def do_args(self, args):
        self.tgt_dir = self.lconfig['ops']['tgt_dir']

        
    def fname_commit(self, fname='', fext='', subdir=''):
        """ doc """
        self.resolve_path_parts('fname',fname)
        self.resolve_path_parts('fext',fext)
        self.resolve_path_parts('subdir',subdir)
        self.fnamext = os.path.join(self.fname,self.fext)
        self.subpath = os.path.join(self.subdir,self.fnamext)
        self.relpath = os.path.join(self.tgt_dir,self.subpath)

    def resolve_path_parts(self, name, arg):
        """ doc """
        if arg != '' :
            setattr(self,name,arg)


