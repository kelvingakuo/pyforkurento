from .exceptions import KurentoOperationException

class MediaElement(object):
    """ Base class for ALL media elements i.e. Endpoints, Filters, and Hubs
    """

    def __init__(self, session_id, elem_id, pipeline_class):
        self.pipeline = pipeline_class
        self.session_id = session_id
        self.elem_id = elem_id


    def _connect(self, external_sink = None):
        if(external_sink is not None):
            sink_id = external_sink.elem_id
        else:
            sink_id = self.elem_id

        params = {
            "object":self.elem_id,
            "operation":"connect",
            "operationParams":{
                "sink":sink_id
            },
            "sessionId":self.session_id
        }
    
        self.pipeline._invoke(params)

    def _subscribe(self, what):
        # Subscribe to server events
        params = {
            "object":self.elem_id,
            "type":what,
            "sessionId":self.session_id
        }

        self.pipeline._subscribe(params)

    def _on_event(self, what, callback):
        # Listen to server POSTs triggered by first subscribing, then invoking the operation
        self.pipeline._on_event(what, callback)

    def _add_event_listener(self, event, callback):
        """ [DO NOT OVERRIDE!!] Adds event listeners for events that all Media Elements can implement

        Params:
            - event: The event to listen for. Accepted:
                * MediaFlowIn - Invoked when media is ready for recording
                * MediaFlowOut - Invoked when media is no longer ready for recording
                * EndOfStream - Invoked when the stream that the element sends out is finished.
                * ElementConnected - Indicates that an element has been connected to other.
                * ElementDisconnected - Indicates that an element has been disconnected.
                * Error: An error related to the MediaObject has occurred.
            - callback: Function to be called when event is registered
        """
        
        expected = ["MediaFlowIn", "MediaFlowOut", "EndOfStream", "ElementConnected", "ElementDisconnected", "Error"]

        if(event not in expected):
            raise KurentoOperationException("Uknown event requested")
        else:
            if not callable(callback):
                raise RuntimeError("Callback has to be callable e.g. a function")

            else:
                self._subscribe(event)
                self._on_event(event, callback)