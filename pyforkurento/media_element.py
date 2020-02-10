class MediaElement(object):
    """ Base class for ALL media elements
    """
    def __init__(self, session_id, elem_id, pipeline_class):
        self.pipeline = pipeline_class
        self.session_id = session_id
        self.elem_id = elem_id


    def connect(self, external_sink = None):
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
    
        self.pipeline.invoke(params)

    def subscribe(self, what):
        # Subscribe to server events
        params = {
            "object":self.elem_id,
            "type":what,
            "sessionId":self.session_id
        }

        self.pipeline.subscribe(params)

    def on_event(self, what, callback):
        # Listen to server POSTs triggered by subscribe() -> invoke()
        self.pipeline.on_event(what, callback)