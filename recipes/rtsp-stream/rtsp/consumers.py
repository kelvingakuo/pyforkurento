import json
from channels.generic.websocket import WebsocketConsumer
from pyforkurento import client

class RTSPStreamConsumer(WebsocketConsumer):
	def connect(self):
		self.accept()
		self.cli = client.KurentoClient("ws://localhost:8888/kurento")
		try:
			print(self.cli.ping()) # Test connection with KMS
			self.send(text_data=json.dumps({
				"id": "info",
				"payload": "KMS Connected"
			}))
			self.pipeline = self.cli.create_media_pipeline()
			self.rtc = self.pipeline.add_endpoint("WebRtcEndpoint")
		except Exception as e:
			self.send(text_data=json.dumps({
				"id": "error",
				"payload": f"KMS could not connect -> {e}"
			}))
	def sendICE(self, resp):
		""" This callback function gets an ICE candidate from KMS, then sends it back to the client
		"""
		ice = resp["payload"]["candidate"]
		self.send(text_data = json.dumps({
			"id": "iceCandidate",
			"payload": ice
   		 }))

	def receive(self, text_data):
		data = json.loads(text_data)
		action = data["id"]

		if(action == "rtspURL"):
			rtsp_url = data["payload"]
			try:
				self.ply = self.pipeline.add_endpoint("PlayerEndpoint", uri = rtsp_url)
				self.ply.connect(self.rtc)
				self.ply.play()

				self.send(text_data = json.dumps({
					"id": "rtspConnection",
					"payload": "PlayerEndpoint started"
				}))
			except Exception as e:
				self.send(text_data = json.dumps({
					"id": "rtspConnection",
					"payload": f"PlayerEndpoint error occured -> {e}"
				}))

		elif(action == "processOffer"):
			offer = data["payload"]
			kms_sdp = self.rtc.process_offer(offer)

			self.send(text_data = json.dumps({
				"id": "sdpAnswer",
				"payload": kms_sdp
			}))

			self.rtc.add_event_listener("OnIceCandidate", self.sendICE)
			self.rtc.gather_ice_candidates()

		elif(action == "addIce"):
			candidate = data["payload"]
			self.rtc.add_ice_candidate(candidate)

		elif(action == "error" or action == "stop"):
			print("Something weird happened in the frontend")


	def disconnect(self, close_code):
		""" Runs when the JS client disconnects
		"""
		self.cli.__del__()
		self.close()
	