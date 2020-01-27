# Media Elements & Pipelines
from .endpoints import WebRTCEndpoint
from .endpoints import PlayerEndpoint

from .exceptions import KurentoOperationException

class MediaPipeline(object):
    def __init__(self, session_id, pipeline_id, client_class):
        self.session_id = session_id
        self.pipeline_id = pipeline_id

        self.upstream = client_class # Passed from the Client class so that we can access functionality of the base class

    def __str__(self):
        return f"MediaPipeline ID: {self.pipeline_id} Session ID: {self.session_id}\n"
    
    def create_web_rtc_endpoint(self):
        params =  {
            "type": "WebRtcEndpoint",
            "constructorParams": {
                "mediaPipeline": self.pipeline_id
            },
            "properties": {},
            "sessionId": self.session_id
        }
        
        
        rtc = self.upstream.create(params)
        sess_id = rtc["payload"]["sessionId"]
        point_id = rtc["payload"]["value"]

        rtc_endpoint = WebRTCEndpoint(sess_id, point_id, self.upstream)
        return rtc_endpoint


    def create_player_endpoint(self, media_uri = ""):
        params =  {
            "type": "PlayerEndpoint",
            "constructorParams": {
                "mediaPipeline": self.pipeline_id,
                "uri": media_uri
            },
            "properties": {},
            "sessionId": self.session_id
        }

        player = self.upstream.create(params)
        sess_id = player["payload"]["sessionId"]
        player_id = player["payload"]["value"]

        player_endpoint = PlayerEndpoint(sess_id, player_id, self.upstream)
        return player_endpoint

    def dispose(self):
        params = {
            "object": self.pipeline_id,
            "sessionId": self.session_id
        }
        self.upstream.release(params)



