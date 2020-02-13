from .exceptions import KurentoOperationException
from .media_element import MediaElement

class Endpoint(MediaElement):
    def __init__(self, sess_id, point_id, pipeline_class):
        super().__init__(sess_id, point_id, pipeline_class)

# =============== ENDPOINTS =====================
class PlayerEndpoint(Endpoint):
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"PlayerEndpoint ID: {self.elem_id} Session ID: {self.session_id}\n"

    def connect(self, sink_elem = None):
        """ Connect PlayerEndpoint to another element

        Params:
            sink_elem (obj): Media Element to connect to. If left blank, the element connects to itself
        """

        return super()._connect(sink_elem)
    
    def play(self):
        """ Start playing the media item
        """

        params = {
            "object":self.elem_id,
            "operation":"play",
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)
    
    def pause(self):
        """ Pause playing the media item
        """

        params = {
            "object":self.elem_id,
            "operation":"pause",
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)

    def stop(self):
        """ Stop playing the media item
        """

        params = {
            "object":self.elem_id,
            "operation":"stop",
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)
        

class WebRTCEndpoint(Endpoint):
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"WebRTCEndpoint ID: {self.elem_id} Session ID: {self.session_id}\n"

    def connect(self, sink_elem = None):
        """ Connect WebRTCEndpoint to another element

        Params:
            sink_elem (obj): Media Element to connect to. If left blank, the element connects to itself
        """

        return super()._connect(sink_elem)

    def process_offer(self, session_desc_offer):
        """ Process the Session Description Protocol offer generated by the client

        Params:
            - session_desc_offer (str): SDP payload from a WebRTC client

        Returns:
            - sdp_answer (str): SDP answer from KMS. If a problem occured, sdp_answer is set to be 'error'
        """

        params = {
            "object":self.elem_id,
            "operation":"processOffer",
            "operationParams":{
                "offer": session_desc_offer
            },
            "sessionId": self.session_id
        }
        sdp_load = self.pipeline._invoke(params)
        sdp_answer = sdp_load["payload"]["value"]
        return sdp_answer

    def add_ice_candidate(self, candidate):
        """ Adds Ice Candidate recevied from the WebRTC client to KMS

        Params:
            - candidate (ICE): The ICE Candidate from the client

        """

        params = {
            "object":self.elem_id,
            "operation":"addIceCandidate",
            "operationParams":{
                "candidate": candidate
            },
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)

    def gather_ice_candidates(self):
        """ Triggers ICE candidate generation by KMS. Call this method AFTER adding an event listener for 'OnIceCandidate'
        """
        
        params = {
            "object":self.elem_id,
            "operation":"gatherCandidates",
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)

    def add_event_listener(self, event, callback):
        """ Adds an event listener function for a specific PlayerEndpoint event

        Params:
            - event (str): The event to listen for. Accepted:
                * OnIceCandidate - Invoked when KMS starts generating ICE candidates
                * OnIceGatheringDone - Invoked when KMS is done gathering ICE candidates
            - callback (func): Function to be called when event is registered
        """

        expected = ["OnIceCandidate", "OnIceGatheringDone"]

        if(event not in expected):
            super()._add_event_listener(event, callback)
        else:   
            if not callable(callback):
                raise RuntimeError("Callback has to be callable e.g. a function")
            else:
                super()._subscribe(event)
                super()._on_event(event, callback)



class RecorderEndpoint(Endpoint):
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"RecorderEndpoint ID: {self.elem_id} Session ID: {self.session_id}\n"

    def connect(self, sink_elem = None):
        """ Connect RecorderEndpoint to another element

        Params:
            sink_elem (obj): Media Element to connect to. If left blank, the element connects to itself
        """

        return super()._connect(sink_elem)

    def record(self):
        """ Start the recording the media item
        """

        params = {
            "object":self.elem_id,
            "operation":"record",
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)

    def stop(self):
        """ Stops the recording
        """

        params = {
            "object":self.elem_id,
            "operation":"stopAndWait",
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)

    def add_event_listener(self, event, callback):
        """ Adds an event listener function for a specific RecorderEndpoint event

        Params:
            - event (str): The event to listen for. Accepted:
                * Recording - Invoked when the media recording effectively starts
            - callback (func): Function to be called when event is registered

        """
        
        expected = ["Recording"]

        if(event not in expected):
            super()._add_event_listener(event, callback)
        else:
            if not callable(callback):
                raise RuntimeError("Callback has to be callable e.g. a function")
            else:
                super()._subscribe(event)
                super()._on_event(event, callback)



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
