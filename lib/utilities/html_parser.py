""" doc """
import time
import requests
from bs4 import BeautifulSoup
from lib.main import Main

class HtmlParser(Main):
    """ doc """

    url= None
    r = None
    content = None
    soup = None
    wait = 1
    timeout = 10


    def __init__(self,**kwargs):
        """ doc"""
        self.resolve_attrs(kwargs)

    def get_content (self, url=None, timeout=None, wait=None) :
        """ doc """

        wait = self.resolve_arg('wait',wait)
        timeout = self.resolve_arg('timeout',timeout)
        url = self.resolve_arg('url',url)

        time.sleep(wait)

        session = requests.Session()

        self.r = session.get(url)
        self.content = self.r.content
        self.soup = BeautifulSoup(self.content, 'html.parser')
