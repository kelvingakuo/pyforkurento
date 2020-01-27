# Construct the JSONRPC requests
import json

def rpc_payload(method, id, args):
    """ Takes parameters, then constructs a JSONRPC payload for sending
    """

    payload = {
        "id": id,
        "method": method,
        "params": args,
        "jsonrpc": "2.0"
        }
    
    return json.dumps(payload)




