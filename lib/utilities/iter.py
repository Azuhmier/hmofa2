""" doc """
from lib.main import Main

class Iter(Main):
    """ doc  """

    idx = -1
    tgt_name = None

    def next(self):
        """ doc  """
        setattr(self, self.tgt_name, None)
        setattr(self, self.tgt_name, self.exists_next())
        tgt = getattr(self,self.tgt_name)
        if tgt is not None:
            self.idx=self.idx+1
            self.get_tgt()
        return self.do()

    def do(self):
        """ doc """
        return 0

    def exists_next(self):
        """ doc """
        return 0

    def get_tgt(self):
        """ doc """

