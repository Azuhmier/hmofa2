""" doc """
import code
#from lib.fetcher.op_fetcher import OpFetcher
from lib.controllers.main_controller import MainController

ohmfa = MainController()
ohmfa.add('hmofa')
ohmfa.config
print(ohmfa.root)
print(ohmfa.parent)
print(ohmfa.top)
print(ohmfa.hmofa.root)
print(ohmfa.hmofa.parent)
print(ohmfa.hmofa.top)
ohmfa.hmofa.config
ohmfa.hmofa.add('threads')
print(ohmfa.hmofa.threads)
ohmfa.hmofa.threads.config
print(ohmfa.hmofa.threads.root)
print(ohmfa.hmofa.threads.parent)
print(ohmfa.hmofa.threads.top)
ohmfa.hmofa.threads.add('fetcher')
ohmfa.hmofa.threads.fetcher
ohmfa.hmofa.threads.fetcher
#code.interact(local=locals())
