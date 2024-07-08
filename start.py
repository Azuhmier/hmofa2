""" doc """
import code
#from lib.fetcher.op_fetcher import OpFetcher
from lib.controllers.main_controller import MainController

ohmfa = MainController()
ohmfa.add('hmofa')
ohmfa.hmofa.add('threads')
ohmfa.hmofa.threads.add('fetcher')
ohmfa.hmofa.threads.fetcher.f.fname='bubba'
print(ohmfa.hmofa.threads.fetcher.f.fname)
print(ohmfa.hmofa.threads.fetcher.f.fnamext)
print(ohmfa.hmofa.threads.fetcher.f.subpath)
print(ohmfa.hmofa.threads.fetcher.f.relsubdir)
#code.interact(local=locals())
