""" doc """
from lib.controllers.controller import Controller
from lib.jobs.fetcher.thread_fetcher import ThreadFetcher

class MediaController(Controller):
    """ doc """

    def add(self, key_arg, **kwargs):
        """ doc """

        setattr(self, key_arg, ThreadFetcher(
            key = key_arg,
            parent=self,
            top=self,
            **kwargs))
