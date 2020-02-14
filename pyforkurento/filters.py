from .exceptions import KurentoOperationException
from .media_element import MediaElement

class Filter(MediaElement):
    """ All filters base class
    """

    def __init__(self, sess_id, filter_id, pipeline_class):
        super().__init__(sess_id, filter_id, pipeline_class)


# =============== ENDPOINTS =====================
class FaceOverlayFilter(Filter):
    """ Detects faces in a video stream and overlays them with a configurable image.  
    """
    
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"FaceOverlayFilter ID: {self.elem_id} Session ID: {self.session_id}\n"
    
    def connect(self, sink_elem = None):
        """ Connect FaceOverlayFilter to another element

        Params:
            sink_elem (obj): Media Element to connect to. If left blank, the element connects to itself
        """

        super()._connect(sink_elem)

    def set_face_overlay_image(self, image_uri, offset_x = 0.0, offset_y = 0.0, width = 1.0, height = 1.0):
        """ Sets the image to overlay on a detected face

        Params:
            - image_uri (str): Location of image to use. Accepted URI schemas are:
                - file:///path/to/file (File on local file system)
                - http(s)://<server-ip>/path/to/file (File on HTTP server)
            - offset_x (float): How much left or right (a ratio of face width) to move the image in reference to detected face's upper right corner coordinates
            - offset_y (float): How much up or down (a ratio of face height) to move the image in reference to detected face's upper right corner coordinates
            - width (float) >=0.0 : How much of the face's width the image should cover e.g. 1.0 means cover the entire width
            - height (float) >=0.0: How much of the face's height the image should cover e.g. 1.0 means cover the entire height
        """

        params = {
            "object": self.elem_id,
            "operation": "setOverlayedImage",
            "operationParams": {
                "uri": image_uri,
                "offsetXPercent": offset_x,
                "offsetYPercent": offset_y,
                "widthPercent": width,
                "heightPercent": height

            },
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)

    def unset_face_overlay_image(self):
        """ Removes the image overlayed on faces
        """

        params = {
            "object": self.elem_id,
            "operation": "unsetOverlayedImage",
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)

    def add_event_listener(self, event, callback):
        """ Adds an event listener function for a specific FaceOverlayFilter event or a general MediaElement event
        """

        super()._add_event_listener(event, callback)



class ImageOverlayFilter(Filter):
    """ Overlays a configurable image on the video stream
    """

    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)
        self.image_id = ""

    def __str__(self):
        return f"ImageOverlayFilter ID: {self.elem_id} Session ID: {self.session_id}\n"
    
    def connect(self, sink_elem = None):
        """ Connect ImageOverlayFilter to another element

        Params:
            sink_elem (obj): Media Element to connect to. If left blank, the element connects to itself
        """

        super()._connect(sink_elem)

    def overlay_image(self, image_uri, image_id, offset_x = 0.0, offset_y = 0.0, relative_width = 1.0, relative_height = 1.0, keep_aspect_ratio = True, to_centre = True):
        """ Draws an image on the video feed at the specified location

        Params:
            - image_id (str): A unique identifier for the image. Recommendation: str(uuid.uuid4())
            - image_uri (str): Location of image to use. Accepted URI schemas are:
                - file:///path/to/file (File on local file system)
                - http(s)://<server-ip>/path/to/file (File on HTTP server)
            - offset_x (float) [0 - 1]: Percentage of image width to set overlay image left upper conner X coords
            - offset_y (float) [0 - 1]: Percentage of image height to set overlay image left upper conner Y coords
            - relative_width (float) [0 - 1]: Width of the overlay image in relation to the video stream e.g. 1.0 means full width
            - relative_height (float) [0 - 1]: Height of the overlay image in relation to the video stream e.g. 1.0 means full height
            - keep_aspect_ratio (bool): Whether to keep the image's aspect ratio
            - to_centre (bool): Whether to centre the image in the region defined
        """

        self.image_id = image_id
        params = {
            "object": self.elem_id,
            "operation": "addImage",
            "operationParams": {
                "id": self.image_id,
                "uri": image_uri,
                "offsetXPercent": offset_x,
                "offsetYPercent": offset_y,
                "widthPercent": relative_width,
                "heightPercent": relative_height,
                "keepAspectRatio": keep_aspect_ratio,
                "center": to_centre

            },
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params) 

    def remove_image(self):
        """ Remove the overlayed image from the stream
        """

        params = {
            "object": self.elem_id,
            "operation": "removeImage",
            "operationParams":{
                "id": self.image_id
            },
            "sessionId": self.session_id
        }
        self.pipeline._invoke(params)

    def add_event_listener(self, event, callback):
        """ Adds an event listener function for a specific ImageOverlayFilter event or a general MediaElement event
        """

        super()._add_event_listener(event, callback)


class ZBarFilter(Filter):
    """ Detects QR and bar codes in a video stream. When a code is found, the filter raises a CodeFoundEvent
    """

    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"ZBarFilter ID: {self.elem_id} Session ID: {self.session_id}\n"
    
    def connect(self, sink_elem = None):
        """ Connect ZBarFilter to another element

        Params:
            sink_elem (obj): Media Element to connect to. If left blank, the element connects to itself
        """

        super()._connect(sink_elem)

    def add_event_listener(self, event, callback):
        """ Adds an event listener function for a specific ZBarFilter event or a general MediaElement event

        Params:
            - event (str): The event to listen for. Accepted:
                * CodeFoundEvent - Triggered when a BarCode or QR code is found in the video stream
            - callback (func): Function to be called when event is registered
        """

        expected = ["CodeFoundEvent"]

        if(event not in expected):
            super()._add_event_listener(event, callback)
        else:        
            if not callable(callback):
                raise RuntimeError("Callback has to be callable e.g. a function")
            else:
                super()._subscribe(event)
                super()._on_event(event, callback)


class GStreamerFilter(Filter):
    """ A generic filter interface that allows usage of GStreamer filters in Kurento Media Pipelines.
    """

    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"GStreamerFilter ID: {self.elem_id} Session ID: {self.session_id}\n"

    def set_element_property(self):
        pass
    
    def connect(self, sink_elem = None):
        """ Connect GStreamerFilter to another element

        Params:
            sink_elem (obj): Media Element to connect to. If left blank, the element connects to itself
        """
        
        super()._connect(sink_elem)


    def add_event_listener(self, event, callback):
        """ Adds an event listener function for a specific GStreamerFilter event or a general MediaElement event
        """

        super()._add_event_listener(event, callback)