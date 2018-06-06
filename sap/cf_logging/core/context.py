""" Module Context """

_CORRELATION_ID_KEY = 'correlation_id'

class Context(object):
    """ Class for getting and setting context variables """

    def set(self, key, value, request):
        """ Store session variable """
        raise NotImplementedError

    def get(self, key, request):
        """ Get session variable """
        raise NotImplementedError

    def get_correlation_id(self, request=None):
        """ Gets the current correlation_id. Ensure that you are calling this method in the
        appropriate location of your code having in mind which framework you are using. """

        return self.get(_CORRELATION_ID_KEY, request)

    def set_correlation_id(self, value, request=None):
        """ Sets the current correlation_id. Ensure that you are calling this method in the
        appropriate location of your code having in mind which framework you are using. """

        return self.set(_CORRELATION_ID_KEY, value, request)
