import sys
sys.path.append( '/home/azuhmier/progs/ohmfa/lib/python' )
from ohmfa.main import Main

ov = Main(ohmfa_dir = "/home/azuhmier/hmofa/hmofa2/")
ov.fetch('threads',read_only=False)
f = ov.jobs[0]
p = f.page
t = p.thread

f.auto()
