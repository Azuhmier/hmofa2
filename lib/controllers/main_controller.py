"""doc"""
import os

from lib.controllers.controller import Controller
from lib.controllers.general_controller import GeneralController

class MainController(Controller):
    """ doc """

    controller_type = 'main'
    p_root = os.path.abspath('.')

    def add(self, key_arg, **kwargs):
        """ doc """

        setattr(self, key_arg, GeneralController(
            key = key_arg,
            parent=self,
            top=self,
            **kwargs))

