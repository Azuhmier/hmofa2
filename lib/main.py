class Main():
    """ doc """

    def resolve_attr(self, name, arg):
        """ doc """
        if arg is not None:
            setattr(self, name, arg)

    def resolve_arg(self, name, arg):
        """ doc """
        res = arg
        if res is None:
            res = getattr(self, name)
        return res
