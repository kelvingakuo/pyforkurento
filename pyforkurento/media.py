# MediaPipeline actions
from .endpoints import WebRTCEndpoint
from .endpoints import PlayerEndpoint
from .endpoints import HTTPPostEndpoint
from .endpoints import RTPEndpoint
from .endpoints import RecorderEndpoint

from .filters import FaceOverlayFilter
from .filters import ZBarFilter
from .filters import GStreamerFilter
from .filters import ImageOverlayFilter

from .hubs import Composite
from .hubs import Dispatcher
from .hubs import DispatcherOneToMany

from .exceptions import KurentoOperationException

class MediaPipeline(object):
    def __init__(self, session_id, pipeline_id, client_class):
        self.session_id = session_id
        self.pipeline_id = pipeline_id

        self.upstream = client_class # Passed from the Client class so that we can access functionality of the base class
        self.elem_params = {
            "type": "",
            "constructorParams": {
                "mediaPipeline": self.pipeline_id
            },
            "sessionId": self.session_id
        }

    def __str__(self):
        return f"MediaPipeline ID: {self.pipeline_id} Session ID: {self.session_id}\n"

    
    def dispose(self):
        params = {
            "object": self.pipeline_id,
            "sessionId": self.session_id
        }
        self.upstream.release(params)

    
    def __create_element(self, endpoint_obj):
        elem = self.upstream.create(self.elem_params)
        elem_sess_id = elem["payload"]["sessionId"]
        elem_elem_id = elem["payload"]["value"]

        return endpoint_obj(elem_sess_id, elem_elem_id, self.upstream)

    
    def create_endpoint(self, endpoint, **kwargs):
        """ Creates an Endpoint Media Element
        Params:
            - endpoint: String representing the type of endpoint to create. Accepts:
                * WebRtcEndpoint
                * RtpEndpoint
                * HttpPostEndpoint
                * PlayerEndpoint
                * RecorderEndpoint
            -> This function accepts optional named arguments for different endpoints:
                - uri: Media URI for recorder & player endpoints only. 
                    * For PlayerEndpoint, it's the media to be played
                        Accepted URI schemas are:
                            - file:///path/to/file (File on local file system)
                            - rtsp://<server-ip> (IP camera RTSP URLs)
                            - http(s)://<server-ip>/path/to/file (File on HTTP server)
                    * For RecorderEndpoint, it's the location to record to
                        Accepted URI schemas are:
                            - file:///path/to/file (File on local file system)
                            - http(s)://<server-ip>/path/to/file (File on HTTP server)
                - webrtc_recv_only: Sets a WebRtcEndpoint to be a receiver only
                - webrtc_send_only: Sets a WebRtcEndpoint to be a sender only

        Example: To create a WebRTCEndpoint: create_endpoint("WebRtcEndpoint", uri = "rtsp://<server-ip>", webrtc_recv_only = False, webrtc_send_only = False)

        Returns:
            - Object of the requested endpoint
        """

        excepted_kwargs = ["uri", "webrtc_recv_only", "webrtc_send_only"]
        uknowns = set(kwargs.keys() - excepted_kwargs)
        if(len(uknowns) > 0):
            raise KurentoOperationException(f"Unkown keyword arguments {uknowns} passed")

        if(len(kwargs) == 0):
            # Default values
            uri = ''
            webrtc_recv_only = False
            webrtc_send_only = False
        else:
            those_set = kwargs.keys()
            if("uri" in those_set):
                uri = kwargs["uri"]
            if("webrtc_recv_only" in those_set):
                webrtc_recv_only = kwargs["webrtc_recv_only"]
            if("webrtc_send_only" in those_set):
                webrtc_send_only = kwargs["webrtc_send_only"]

        if(endpoint == "RecorderEndpoint" and uri == ''):
            raise KurentoOperationException("Please specify a URI for the endpoint to record to")

        if(endpoint == "WebRtcEndpoint"):
            self.elem_params["type"] = "WebRtcEndpoint"
            self.elem_params["constructorParams"]["recvonly"] = webrtc_recv_only
            self.elem_params["constructorParams"]["sendonly"] = webrtc_send_only
            return self.__create_element(WebRTCEndpoint)

        elif(endpoint == "RtpEndpoint"):
            self.elem_params["type"] = "RtpEndpoint"
            return self.__create_element(RTPEndpoint)

        elif(endpoint == "HttpPostEndpoint"):
            self.elem_params["type"] = "HttpPostEndpoint"
            return self.__create_element(HTTPPostEndpoint)

        elif(endpoint == "PlayerEndpoint"):
            self.elem_params["type"] = "PlayerEndpoint"
            self.elem_params["constructorParams"]["uri"] = uri
            return self.__create_element(PlayerEndpoint)

        elif(endpoint == "RecorderEndpoint"):
            self.elem_params["type"] = "RecorderEndpoint"
            self.elem_params["constructorParams"]["uri"] = uri
            return self.__create_element(RecorderEndpoint)

        else:
            raise KurentoOperationException(f"Unknown endpoint {endpoint} requested")


    def create_filter(self, filter, **kwargs):
        """ Creates a Filter Media Element
        Params:
            - filter: String representing the type of filter to create. Accepts:
                * FaceOverlayFilter
                * ZBarFilter
                * GStreamerFilter
                * ImageOverlayFilter

        Returns:
            - Object of the requested filter
        """
        if(filter == "FaceOverlayFilter"):
            self.elem_params["type"] = "FaceOverlayFilter"
            return self.__create_element(FaceOverlayFilter)

        elif(filter == "ZBarFilter"):
            self.elem_params["type"] = "ZBarFilter"
            return self.__create_element(ZBarFilter)

        elif(filter == "GStreamerFilter"):
            self.elem_params["type"] = "GStreamerFilter"
            return self.__create_element(GStreamerFilter)

        elif(filter == "ImageOverlayFilter"):
            self.elem_params["type"] = "ImageOverlayFilter"
            return self.__create_element(ImageOverlayFilter)

        else:
            raise KurentoOperationException(f"Unknown filter {filter} requested")

    def create_hub(self, hub, **kwargs):
        """ Creates a Hub Media Element
        Params:
            - hub: String representing the type of hub to create. Accepts:
                * Composite
                * Dispatcher
                * DispatcherOneToMany

        Returns:
            - Object of the requested hub
        """
        if(hub == "Composite"):
            self.elem_params["type"] = "Composite"
            return self.__create_element(Composite)

        elif(hub == "Dispatcher"):
            self.elem_params["type"] = "Dispatcher"
            return self.__create_element(Dispatcher)

        elif(hub == "DispatcherOneToMany"):
            self.elem_params["type"] = "DispatcherOneToMany"
            return self.__create_element(DispatcherOneToMany)

        else:
            raise KurentoOperationException(f"Unknown hub {hub} requested")



