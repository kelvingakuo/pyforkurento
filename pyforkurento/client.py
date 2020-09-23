from .base import BaseKurentoClient
from .pipeline import MediaPipeline

from .exceptions import KurentoOperationException


class KurentoClient(BaseKurentoClient):
    """ pyforkurento entry point
    """

    def __init__(self, kurento_server_url):
        super().__init__(kurento_server_url)

    def __del__(self):
        super().__del__()

    # A hacky decorator for dealing with failed operations due to badly designed multithreading in the base class
    def _validate_response(func):
        def wrapper(self, params):
                no_output = True # A hack to deal with failed operations
                while no_output:
                    ret = func(self, params)
                    if("resp_success" in ret):
                        no_output = False

                        if(ret["resp_success"]):
                            return ret
                        else:
                            load = ret["payload"]
                            if(load["code"] == 40208): # SDP_ENDPOINT_ALREADY_NEGOTIATED ERROR
                                return {"payload": {"value": "error"}}
                            else:
                                err = f"Kurento Server responded with the error code-> {load['code']}, an error of type-> {load['data']['type']}, with the message-> {load['message']}"
                                raise KurentoOperationException(err)
        return wrapper

    @_validate_response    
    def _create(self, params):
        return super().create(params)

    @_validate_response
    def _invoke(self, params):
        return super().invoke(params)

    def _on_event(self, what_event, callback):
        return super().on_event(what_event, callback)

    @_validate_response
    def _release(self, params):
        return super().release(params)

    @_validate_response
    def _subscribe(self, params):
        return super().subscribe(params)

    @_validate_response
    def _unsubscribe(self, params):
        return super().unsubscribe(params)

    def ping(self):
        """ Prints 'pong' if a connection to KMS is available. Otherwise, an expection is thrown
        """

        return super().ping()

    def create_media_pipeline(self):
        """ Create a Media Pipeline. This HAS TO BE the first operation when dealing with KMS. Every other element is created by a pipeline

        Returns:
            - MediaPipeline object
        """
        
        constructor_params = {
            "type": "MediaPipeline",
            "constructorParams": {},
            "properties": {}
        }

        sess = self._create(constructor_params)

        sess_id = sess["payload"]["sessionId"]
        pipe_id = sess["payload"]["value"]

        pipeline = MediaPipeline(sess_id, pipe_id, self)
        return pipeline




    