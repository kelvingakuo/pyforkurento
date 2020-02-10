from .media_element import MediaElement

class Filter(MediaElement):
    def __init__(self, sess_id, filter_id, pipeline_class):
        super().__init__(sess_id, filter_id, pipeline_class)



# =============== ENDPOINTS =====================
class FaceOverlayFilter(Filter):
    def __init__(self):
        pass


class ZBarFilter(Filter):
    def __init__(self):
        pass

class GStreamerFilter(Filter):
    def __init__(self):
        pass