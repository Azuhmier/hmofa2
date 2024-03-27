""" doc """
from lib.parser.html_parser import HtmlParser

class SingleHtmlParser(HtmlParser):
    """ doc  """

    idx = -1
    url = None

    def start(self, url=None,list=None):
        self.url = url

        """ doc """

    def next(self):
        print('lol')
        """ doc  """
        self.url = None
        self.url = self.exists_next() 
        if self.url is not None:
            self.idx=self.idx+1
            self.get_content()
        return self.do()

    def do(self):
        return self.url

    def exists_next(self):
        """ doc """


