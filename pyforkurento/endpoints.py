from .media_element import MediaElement

class Endpoint(MediaElement):
    def __init__(self, sess_id, point_id, pipeline_class):
        super().__init__(sess_id, point_id, pipeline_class)

    def connect(self, sink_elem = None):
        # Can connect to multiple things
        if(sink_elem is not None):
            sink = sink_elem.elem_id
        else:
            sink = None

        return super().connect(sink)


# =============== ENDPOINTS =====================
class PlayerEndpoint(Endpoint):
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"PlayerEndpoint ID: {self.elem_id} Session ID: {self.session_id}\n"

    def connect(self, sink_elem = None):
        return super().connect(sink_elem)

    def play(self):
        # Play media connected to PlayerEndpoint
        params = {
            "object":self.elem_id,
            "operation":"play",
            "sessionId": self.session_id
        }
        self.pipeline.invoke(params)
        

class WebRTCEndpoint(Endpoint):
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"WebRTCEndpoint ID: {self.elem_id} Session ID: {self.session_id}\n"

    def connect(self, sink_elem = None):
        return super().connect(sink_elem)

    def process_offer(self, session_desc_offer):
        params = {
            "object":self.elem_id,
            "operation":"processOffer",
            "operationParams":{
                "offer": session_desc_offer
            },
            "sessionId": self.session_id
        }
        sdp_load = self.pipeline.invoke(params)
        sdp_answer = sdp_load["payload"]["value"]
        return sdp_answer

    def on_ice_candidates(self):
        # Subscribe to onIceCandidate event
        super().subscribe("OnIceCandidate")

    def add_ice_candidate(self, candidate):
        # Add ICE candidates
        params = {
            "object":self.elem_id,
            "operation":"addIceCandidate",
            "operationParams":{
                "candidate": candidate
            },
            "sessionId": self.session_id
        }
        self.pipeline.invoke(params)

    def gather_ice_candidates(self, callback):
        # Start event listener for Ice candidates
        params = {
            "object":self.elem_id,
            "operation":"gatherCandidates",
            "sessionId": self.session_id
        }
        if not callable(callback):
            raise RuntimeError("Callback has to be callable e.g. a function")
        else:
            self.pipeline.invoke(params)
            super().on_event("OnIceCandidate", callback)


class RTPEndpoint(Endpoint):
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"RTPEndpoint ID: {self.elem_id} Session ID: {self.session_id}\n"



class HTTPPostEndpoint(Endpoint):
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"HTTPPostEndpoint ID: {self.elem_id} Session ID: {self.session_id}\n"


class RecorderEndpoint(Endpoint):
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"RecorderEndpoint ID: {self.elem_id} Session ID: {self.session_id}\n"