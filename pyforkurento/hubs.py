from .media_element import MediaElement

class Hub(MediaElement):
    def __init__(self, sess_id, hub_id, pipeline_class):
        super().__init__(sess_id, hub_id, pipeline_class)



# =============== ENDPOINTS =====================
class Composite(Hub):
    def __init__(self):
        pass


class Dispatcher(Hub):
    def __init__(self):
        pass


class DispatcherOneToMany(Hub):
    def __init__(self):
        pass