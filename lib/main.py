""" doc """
import copy
class Main():
    """ doc """

    def resolve_attrs(self, kwargs):
        """ doc """
        for name, value in kwargs.items():
            if value is not None:
                if hasattr(self,name) :
                    setattr(self, name, value)

    def resolve_dspt(self, kwargs, bp):
        """ doc """
        dspt = copy.deepcopy(bp)
        for name, value in kwargs.items():
            if value is not None:
                if name in dspt :
                    dspt[name] = value
        return dspt

    def resolve_arg(self, name, arg):
        """ doc """
        res = arg
        if res is None:
            res = getattr(self, name)
        return res
