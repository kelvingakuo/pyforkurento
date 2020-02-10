from .media_element import MediaElement

class Filter(MediaElement):
    def __init__(self, sess_id, filter_id, pipeline_class):
        super().__init__(sess_id, filter_id, pipeline_class)


# =============== ENDPOINTS =====================
class FaceOverlayFilter(Filter):
    # Overlays an image on detecting a face in the stream   
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"FaceOverlayFilter ID: {self.elem_id} Session ID: {self.session_id}\n"
    
    def connect(self, sink_elem = None):
        """ Connect FaceOverlayFilter to another element
        Params:
            sink_elem: Media Element to connect to. If left blank, the element connects to itself
        """
        return super().connect(sink_elem)

    def set_face_overlay_image(self, image_uri, offset_x = 0.0, offset_y = 0.0, width = 1.0, height = 1.0):
        """ Sets the image to overlay on a detected face
        Params:
            - image_uri: Location of image to use e.g. /etc/over.jpg
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
        self.pipeline.invoke(params)

    def unset_face_overlay_image(self):
        """ Removes the image overlayed on faces
        """
        params = {
            "object": self.elem_id,
            "operation": "unsetOverlayedImage",
            "sessionId": self.session_id
        }
        self.pipeline.invoke(params)



class ImageOverlayFilter(Filter):
    # Overlays an image on the video stream
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)
        self.image_id = ""

    def __str__(self):
        return f"ImageOverlayFilter ID: {self.elem_id} Session ID: {self.session_id}\n"
    
    def connect(self, sink_elem = None):
        """ Connect ImageOverlayFilter to another element
        Params:
            sink_elem: Media Element to connect to. If left blank, the element connects to itself
        """
        return super().connect(sink_elem)

    def overlay_image(self, image_uri, image_id, offset_x = 0.0, offset_y = 0.0, relative_width = 1.0, relative_height = 1.0, keep_aspect_ratio = True, to_centre = True):
        """ Draws an image on the video feed at the specified location
        Params:
            - image_id: A unique identifier for the image. Recommendation: str(uuid.uuid4())
            - image_uri: Location of image to use e.g. /etc/over.jpg
            - offset_x (float) [0 - 1]: Percentage of image width to set overlay image left upper conner X coords
            - offset_y (float) [0 - 1]: Percentage of image height to set overlay image left upper conner Y coords
            - relative_width (float) [0 - 1]: Width of the overlay image in relation to the video stream e.g. 1.0 means full width
            - relative_height (float) [0 - 1]: Height of the overlay image in relation to the video stream e.g. 1.0 means full height
            - keep_aspect_ratio: Whether to keep the image's aspect ratio
            - to_centre: Whether to centre the image in the region defined
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
        self.pipeline.invoke(params) 

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
        self.pipeline.invoke(params)


class ZBarFilter(Filter):
    # Detects QR and bar codes in the stream
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"ZBarFilter ID: {self.elem_id} Session ID: {self.session_id}\n"

    def code_found_event(self, callback):
        """ Triggered when a BarCode or QR code is found in the video stream
        Params:
            - callback : A Function to be called when a barcode is found
        """
        if not callable(callback):
            raise RuntimeError("Callback has to be callable e.g. a function")
        else:
            super().on_event("CodeFoundEvent", callback)

class GStreamerFilter(Filter):
    def __init__(self, session_id, elem_id, pipeline_class):
        super().__init__(session_id, elem_id, pipeline_class)

    def __str__(self):
        return f"GStreamerFilter ID: {self.elem_id} Session ID: {self.session_id}\n"