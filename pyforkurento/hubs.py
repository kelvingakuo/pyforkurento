from .media_element import MediaElement

class Hub(MediaElement):
    """ All hubs base class
    """

    def __init__(self, sess_id, hub_id, pipeline_class):
        super().__init__(sess_id, hub_id, pipeline_class)



# =============== ENDPOINTS =====================
class Composite(Hub):
    """ A hub that mixes the audio stream of its connected inputs and constructs a grid with the video streams of them.
    """

    def __init__(self):
        pass


class Dispatcher(Hub):
    """ A hub that allows routing between arbitrary input-output HubPort pairs.
    """

    def __init__(self):
        pass


class DispatcherOneToMany(Hub):
    """ A hub that sends a given input to all the connected output HubPorts.
    """

    def __init__(self):
        pass