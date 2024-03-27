""" doc """
import re
import time
import requests
from bs4 import BeautifulSoup
from lib.parser.parser import Parser
from lib.main import Main

class HtmlParser(Parser,Main):
    """ doc """

    url= None
    r = None
    content = None
    soup = None

    wait = 1
    timeout = 10

    #def do_args(self, **args):
        #self.resolve_attr('timeout',timeout)
        #self.resolve_attr('wait',wait)



    def get_content (self, url=None, timout=None,wait=None) :
        """ doc """

        wait = self.resolve_arg('wait',wait)
        timeout = self.resolve_arg('timeout',timeout)
        url = self.resolve_arg('url',url)

        time.sleep(wait)

        session = requests.Session()

        self.r = session.get(url)
        self.content = self.r.content
        self.soup = BeautifulSoup(self.content, 'html.parser')
