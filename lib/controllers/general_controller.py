
"""doc"""
from lib.controllers.controller import Controller
from lib.controllers.media_controller import MediaController

class GeneralController(Controller):
    """ doc """

    controller_type = 'general'

    def add(self, key_arg, **kwargs):
        """ doc """

        setattr(self, key_arg, MediaController(
            key=key_arg,
            parent=self,
            top=self.top,
            **kwargs))
