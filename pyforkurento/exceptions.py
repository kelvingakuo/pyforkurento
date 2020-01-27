class KurentoOperationException(Exception):
    """ Custom exception for dealing with Kurento error responses
    """
    def __init__(self, *args):
        self.args = args
