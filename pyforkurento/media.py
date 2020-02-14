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
    """ Base class for creating Media Elements
    """

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
        self.upstream._release(params)

    
    def __create_element(self, endpoint_obj, params):
        elem = self.upstream._create(params)
        elem_sess_id = elem["payload"]["sessionId"]
        elem_elem_id = elem["payload"]["value"]

        return endpoint_obj(elem_sess_id, elem_elem_id, self.upstream)

    
    def create_endpoint(self, endpoint, **kwargs):
        """ Creates an Endpoint Media Element

        Params:
            - endpoint (str): String representing the type of endpoint to create. Accepts:
                * WebRtcEndpoint
                * RtpEndpoint
                * HttpPostEndpoint
                * PlayerEndpoint
                * RecorderEndpoint

            - kwargs: Optional named arguments for different endpoints:
                - webrtc_recv_only (bool): Sets a WebRtcEndpoint to be a receiver only
                - webrtc_send_only (bool): Sets a WebRtcEndpoint to be a sender only
                - uri (str): Media URI for recorder & player endpoints only. 
                    * For PlayerEndpoint, it's the media to be played
                        Accepted URI schemas are:
                            - file:///path/to/file (File on local file system)
                            - rtsp://<server-ip> (IP camera RTSP URLs)
                            - http(s)://<server-ip>/path/to/file (File on HTTP server)
                    * For RecorderEndpoint, it's the location to record to
                        Accepted URI schemas are:
                            - file:///path/to/file (File on local file system)
                            - http(s)://<server-ip>/path/to/file (File on HTTP server)

        Returns:
            - Object of the requested endpoint
        """

        params = self.elem_params
        

        excepted_kwargs = ["uri", "webrtc_recv_only", "webrtc_send_only"]
        uknowns = set(kwargs.keys() - excepted_kwargs)
        if(len(uknowns) > 0):
            raise KurentoOperationException(f"Unkown keyword arguments {uknowns} passed")
        

        those_set = kwargs.keys()

        if("uri" not in those_set):
            uri = ''
        else:
            uri = kwargs["uri"]
        if("webrtc_recv_only" not in those_set):
            webrtc_recv_only = False
        else:
            webrtc_recv_only = kwargs["webrtc_recv_only"]
        if("webrtc_send_only" not in those_set):
            webrtc_send_only = False
        else:
            webrtc_send_only = kwargs["webrtc_send_only"]


        if(endpoint == "RecorderEndpoint" and uri == ''):
            raise KurentoOperationException("Please specify a URI for the endpoint to record to")

        if(endpoint == "WebRtcEndpoint"):
            params["type"] = "WebRtcEndpoint"
            params["constructorParams"]["recvonly"] = webrtc_recv_only
            params["constructorParams"]["sendonly"] = webrtc_send_only
            return self.__create_element(WebRTCEndpoint, params)

        elif(endpoint == "RtpEndpoint"):
            params["type"] = "RtpEndpoint"
            return self.__create_element(RTPEndpoint, params)

        elif(endpoint == "HttpPostEndpoint"):
            params["type"] = "HttpPostEndpoint"
            return self.__create_element(HTTPPostEndpoint, params)

        elif(endpoint == "PlayerEndpoint"):
            params["type"] = "PlayerEndpoint"
            params["constructorParams"]["uri"] = uri
            return self.__create_element(PlayerEndpoint, params)

        elif(endpoint == "RecorderEndpoint"):
            params["type"] = "RecorderEndpoint"
            params["constructorParams"]["uri"] = uri
            return self.__create_element(RecorderEndpoint, params)

        else:
            raise KurentoOperationException(f"Unknown endpoint {endpoint} requested")

        
    def apply_filter(self, filter, **kwargs):
        """ Applies a Filter to the stream

        Params:
            - filter (str): String representing the type of filter to create. Accepts:
                * FaceOverlayFilter - Overlays an image on a face detected
                * ZBarFilter - Triggers an event when a QR code is detected
                * GStreamerFilter - (https://gstreamer.freedesktop.org/documentation/installing/index.html)
                * ImageOverlayFilter - Overlays an image on the stream

            - kwargs: Optional named arguments for different endpoints:
                - command (str): The gstreamer command (https://gstreamer.freedesktop.org/documentation/tools/gst-launch.html)
                - filter_type (str): The type of the gstreamer filter (AUDIO, VIDEO, or AUTODETECT)

        Returns:
            - Object of the requested filter
        """

        params = self.elem_params

        excepted_kwargs = ["command", "filter_type"]
        uknowns = set(kwargs.keys() - excepted_kwargs)
        if(len(uknowns) > 0):
            raise KurentoOperationException(f"Unkown keyword arguments {uknowns} passed")

        those_set = kwargs.keys()

        if("command" not in those_set):
            command = "videobox fill=black top=20 bottom=20 left=-75 right=-75"
        else:
            command = kwargs["command"]

        if("filter_type" not in those_set):
            filter_type = "AUTODETECT"
        else:
            filter_type = kwargs["filter_type"]


        if(filter == "FaceOverlayFilter"):
            params["type"] = "FaceOverlayFilter"
            return self.__create_element(FaceOverlayFilter, params)

        elif(filter == "ZBarFilter"):
            params["type"] = "ZBarFilter"
            return self.__create_element(ZBarFilter, params)

        elif(filter == "GStreamerFilter"):
            params["type"] = "GStreamerFilter"
            params["constructorParams"]["command"] = command
            params["constructorParams"]["filterType"] = filter_type
            return self.__create_element(GStreamerFilter, params)

        elif(filter == "ImageOverlayFilter"):
            params["type"] = "ImageOverlayFilter"
            return self.__create_element(ImageOverlayFilter, params)

        else:
            raise KurentoOperationException(f"Unknown filter {filter} requested")

        

    def create_hub(self, hub, **kwargs):
        """ Creates a Hub Media Element

        Params:
            - hub (str): String representing the type of hub to create. Accepts:
                * Composite
                * Dispatcher
                * DispatcherOneToMany

        Returns:
            - Object of the requested hub
        """
        
        params = self.elem_params        

        if(hub == "Composite"):
            params["type"] = "Composite"
            return self.__create_element(Composite, params)

        elif(hub == "Dispatcher"):
            params["type"] = "Dispatcher"
            return self.__create_element(Dispatcher, params)

        elif(hub == "DispatcherOneToMany"):
            params["type"] = "DispatcherOneToMany"
            return self.__create_element(DispatcherOneToMany, params)

        else:
            raise KurentoOperationException(f"Unknown hub {hub} requested")

        



