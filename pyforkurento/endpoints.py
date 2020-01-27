class Endpoint(object):
    def __init__(self, sess_id, point_id, pipeline_class):
        self.pipeline = pipeline_class
        self.session_id = sess_id
        self.point_id = point_id

    def connect(self, external_sink= None):
        # Connect two media elements
        if(external_sink is not None):
            sink_id = external_sink
        else:
            sink_id = self.point_id

        params = {
            "object":self.point_id,
            "operation":"connect",
            "operationParams":{
                "sink":sink_id
                },
            "sessionId":self.session_id
        }
    
        self.pipeline.invoke(params)

    def subscribe(self, what):
        # Subscribe to server events
        params = {
            "object":self.point_id,
            "type":what,
            "sessionId":self.session_id
        }

        self.pipeline.subscribe(params)

    def on_event(self, what, callback):
        # Listen to server POSTs triggered by subscribe() -> invoke()
        self.pipeline.on_event(what, callback)


# =============== ENDPOINTS =====================
class PlayerEndpoint(Endpoint):
    def __init__(self, session_id, point_id, pipeline_class):
        super().__init__(session_id, point_id, pipeline_class)

    def __str__(self):
        return f"PlayerEndpoint ID: {self.point_id} Session ID: {self.session_id}\n"

    def connect(self, endpoint_to_connect_to = None):
        # Can connect to multiple things
        if(endpoint_to_connect_to is not None):
            sink = endpoint_to_connect_to.point_id
        else:
            sink = None

        return super().connect(sink)

    def play(self):
        # Play media connected to PlayerEndpoint
        params = {
            "object":self.point_id,
            "operation":"play",
            "sessionId": self.session_id
        }
        self.pipeline.invoke(params)

        

class WebRTCEndpoint(Endpoint):
    def __init__(self, session_id, point_id, pipeline_class):
        super().__init__(session_id, point_id, pipeline_class)

    def __str__(self):
        return f"WebRTCEndpoint ID: {self.point_id} Session ID: {self.session_id}\n"

    def connect(self):
        return super().connect()

    def process_offer(self, session_desc_offer):
        params = {
            "object":self.point_id,
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
            "object":self.point_id,
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
            "object":self.point_id,
            "operation":"gatherCandidates",
            "sessionId": self.session_id
        }
        if not callable(callback):
            raise RuntimeError("Callback has to be callable e.g. a function")
        else:
            self.pipeline.invoke(params)
            super().on_event("OnIceCandidate", callback)


class RTPEndpoint(Endpoint):
    def __init__(self, session_id, point_id, pipeline_class):
        super().__init__(session_id, point_id, pipeline_class)

    def __str__(self):
        return f"RTPEndpoint ID: {self.point_id} Session ID: {self.session_id}\n"


class HTTPPostEndpoint(Endpoint):
    def __init__(self, session_id, point_id, pipeline_class):
        super().__init__(session_id, point_id, pipeline_class)

    def __str__(self):
        return f"HTTPPostEndpoint ID: {self.point_id} Session ID: {self.session_id}\n"


class RecorderEndpoint(Endpoint):
    def __init__(self, session_id, point_id, pipeline_class):
        super().__init__(session_id, point_id, pipeline_class)

    def __str__(self):
        return f"RecorderEndpoint ID: {self.point_id} Session ID: {self.session_id}\n"