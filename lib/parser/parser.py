""" doc """

class Parser():
    """ doc """
    def __init__(self, **args) :
        """ """
        if 'p_config' in args:
            self.p_config = args['p_config']
        self.do_args(**args)

    def do_args(self,**args):
        """ """
