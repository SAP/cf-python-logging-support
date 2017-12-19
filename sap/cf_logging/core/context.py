""" Module Context """


class Context(object):
    """ Class for getting and setting context variables """

    def set(self, key, value, request):
        """ Store session variable """
        raise NotImplementedError

    def get(self, key, request):
        """ Get session variable """
        raise NotImplementedError
