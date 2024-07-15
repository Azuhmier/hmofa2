
class SameEvent(Exception):
    pass
j={}
j['t'] = False

def ggs():
    print('    ggs')
    gggs()
    print('    end')
def gggs():
    print('        gggs')
    raise SameEvent()
    print('        end')
def gs():
    print('ggs')
    def ry():
        if j['t']:
            raise SameEvent()
    try:
        ggs()

    except SameEvent:
        print("TRIGGERED")
        return j['t']

    print('end')
gs()
print('imhere')