from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import rtsp.routing

application = ProtocolTypeRouter({
	# (http->django views is added by default)
	'websocket': AuthMiddlewareStack(
		URLRouter(
			rtsp.routing.websocket_urlpatterns
		)
	),
})