from .parse_payloads import rpc_payload
from .exceptions import KurentoOperationException

import json
import threading
import time
import websocket

from queue import Queue
from random import randint

class BaseKurentoClient(object):
    """ Base Kurento client
    """

    def __init__(self, kurento_server_url: str):
        """ Connect to the Kurento server

        Params:
            kurento_server_url (str) - The Kurento server WebSockets url
        """
        self.kurento_url = kurento_server_url
        self.conn_id = randint(5, 12345678)# Incremented everytime a transaction is complete
        self.kurento_conn = websocket.WebSocket()
        self.kurento_conn.connect(kurento_server_url)

        self.operations_queue = Queue() # Holds pending server responses
        self.subscriptions_queue = Queue() # Holds subscriptions responses from server
        self.tracking_q = Queue() # Contains None if all operations are finished

        self.thread = threading.Thread(target = self.listen_to_replies, args = (self.operations_queue, self.subscriptions_queue, self.tracking_q))
        self.thread.daemon = True
        self.thread.start()

        self.thread1 = threading.Thread(target = self.main, args = (self.operations_queue, self.tracking_q))
        self.thread1.daemon = True
        self.thread1.start()

        self.operations = [] # Holds pending server responses
        self.subscriptions = [] # Holds responses from the server, initialised via subscription

    
    def main(self, operations_q, tracking_q):
        try:
            work = True
            while work:
                if((tracking_q.get() is None)):
                    # No more info
                    operations_q.join()
                    tracking_q.join()
                    work = False

                else:
                    operation = operations_q.get(block = True)
                    self.operations.append(operation)
                    tracking_q.put(True)
        except Exception as e:
           raise KurentoOperationException(e)


    def __del__(self):
        # Destructor
        self.operations = []
        self.thread.join()
        self.thread1.join()
        self.kurento_conn.close()

    def listen_to_replies(self, operations_q, subscriptions_q, tracking_q):
        """ Seperate thread to listen for replies from the server
        """
        while self.kurento_conn.connected:
            try:
                self.parse_reply(self.kurento_conn.recv(), operations_q, subscriptions_q, tracking_q)
            except Exception as e:
                raise KurentoOperationException(e)


    # Deconstruct JSONRPC replies & add to queue
    def parse_reply(self, resp, operations_q, subscriptions_q, tracking_q):
        """ Listens for server response & deconstructs
        """
        try:
            if not self.kurento_conn.connected:
                self.reconnect()

            resp = json.loads(resp)

            if("method" not in resp):
                # Server responded to a request
                resp_id = resp["id"]

                if("error" in resp):
                    # An error occured
                    transaction = {"resp_id": resp_id, "resp_success": False, "payload": resp["error"]}

                elif("result" in resp):
                    # Server responded
                    transaction = {"resp_id": resp_id, "resp_success": True, "payload": resp["result"]}

                operations_q.put(transaction)    

            elif("method" in resp):
                # Server POSTed a message after subscription
                sub_params = resp["params"]["value"]
                subscription = {"method": resp["method"], "subscription_type": sub_params["type"], "subscriber": sub_params["object"], "payload": sub_params["data"]}
                subscriptions_q.put(subscription)

            else:
                # No data
                operations_q.put(None)
                subscriptions_q.put(None)
            
            self.conn_id = self.conn_id + 1
            tracking_q.put(True)

        except Exception as e:
            tracking_q.put(None)
            subscriptions_q.put(None)
            raise KurentoOperationException(e)

    # ===== UTILITY METHODS =====
    def reconnect(self):
        """ Reconnect to Kurento if connection was killed
        """
        if not self.kurento_conn.connected:
            try:
                self.kurento_conn.connect(self.kurento_url)
            except Exception as e:
                return e

    def close_connection(self):
        """ Close an existing connection to Kurento
        """
        if(self.kurento_conn.connected):
            self.kurento_conn.close()

    def send_payload(self, payload):
        """ Websockets send with delay
        """
        try:
            self.kurento_conn.send(payload)
            time.sleep(0.005) # Wait for reply
        except Exception as e:
            return e

    def get_response_from_queue(self, req_id):
        """ Find response dict from list of dicts by request id
        """
        resp = next((x for x in self.operations if x["resp_id"] == req_id), "ERROR: Operation not in queue")
        return resp

    def remove_response_from_queue(self, resp):
        self.operations = [op for op in self.operations if op != resp]


    def ping(self):
        """ Make a ping request to the server
        """
        req_id = self.conn_id + 1
        load = rpc_payload("ping", req_id, {})
        self.send_payload(load)

        # Get from queue
        no_success = True
        while no_success:
            resp = self.get_response_from_queue(req_id)
            if("resp_success" in resp):
                no_success = False

        # Remove from queue
        self.remove_response_from_queue(resp)
        
        # Parse and return
        if(resp["resp_success"]):
            print("pong")
        else:
            payload = resp["payload"]
            raise KurentoOperationException(f"Error: Code: {payload['code']} Message: {payload['message']}")

    # ===== API METHODS =====

    def _get_response(func):
        def wrapper(self, params):
            load, req_id = func(self, params)
            self.send_payload(load)
            resp = self.get_response_from_queue(req_id)
            self.remove_response_from_queue(resp)
            return resp

        return wrapper

    @_get_response
    def create(self, params):
        # Create a KMS Media Elements & Media Pipelines
        req_id = self.conn_id + 1
        load = rpc_payload("create", req_id, params)
        return load, req_id

    @_get_response
    def invoke(self, params):
        req_id = self.conn_id + 1
        load = rpc_payload("invoke", req_id, params)
        return load, req_id

    @_get_response
    def subscribe(self, params):
        req_id = self.conn_id + 1
        load = rpc_payload("subscribe", req_id, params)
        return load, req_id

    
    def parse_on_events(self, subs_q, tracking_q, callback, what_event):
        try:
            event = True
            while event:
                if((tracking_q.get() is None)):
                    # No more info
                    subs_q.join()
                    tracking_q.join()
                    event = False

                else:
                    subscription = subs_q.get(block = True)
                    if subscription is None:
                        subs_q.join()
                        event = False


                    # Ugly hack for when there are multiple event listeners for different events i.e. if not needed here, put back into queue
                    if(subscription["subscription_type"] == what_event):
                        callback(subscription)
                    else:
                        subs_q.put(subscription)

                    tracking_q.put(True)
        except Exception as e:
           raise KurentoOperationException(e)

    def on_event(self, what_event, callback):
        def cb(sub_resp):
            callback(sub_resp)

        sub_thread = threading.Thread(target = self.parse_on_events, args = (self.subscriptions_queue, self.tracking_q, cb, what_event))
        sub_thread.daemon = True
        sub_thread.start()

        return sub_thread

    @_get_response
    def unsubscribe(self, params):
        pass

    @_get_response
    def release(self, params):
        req_id = self.conn_id + 1
        load = rpc_payload("release", req_id, params)
        return load, req_id



        
