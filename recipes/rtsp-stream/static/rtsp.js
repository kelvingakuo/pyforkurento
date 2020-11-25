const ws = new WebSocket("ws://127.0.0.1:8000/ws/rtsp/");

let webRtcPeer;

// UI
let rtspURL;
let uiRemoteVideo;
let uiState = null;
const UI_IDLE = 0;
const UI_STARTING = 1;
const UI_STARTED = 2;

window.onload = function()
{
  uiRemoteVideo = document.getElementById('uiRemoteVideo');
  uiSetState(UI_IDLE);
}

window.onbeforeunload = function()
{
  console.log("Page unload - Close WebSocket");
  ws.close();
}

function explainUserMediaError(err)
{
  const n = err.name;
  if (n === 'NotFoundError' || n === 'DevicesNotFoundError') {
    return "Missing webcam for required tracks";
  }
  else if (n === 'NotReadableError' || n === 'TrackStartError') {
    return "Webcam is already in use";
  }
  else if (n === 'OverconstrainedError' || n === 'ConstraintNotSatisfiedError') {
    return "Webcam doesn't provide required tracks";
  }
  else if (n === 'NotAllowedError' || n === 'PermissionDeniedError') {
    return "Webcam permission has been denied by the user";
  }
  else if (n === 'TypeError') {
    return "No media tracks have been requested";
  }
  else {
    return "Unknown error: " + err;
  }
}

function sendError(message)
{
  console.error(message);

  sendMessage({
    id: 'error',
    payload: message,
  });
}

function sendMessage(message)
{
  if (ws.readyState !== ws.OPEN) {
    console.error("WebSocket session isn't open");
    return;
  }

  const jsonMessage = JSON.stringify(message);
  ws.send(jsonMessage);
}



/* ============================= */
/* ==== WebSocket signaling ==== */
/* ============================= */

ws.onmessage = function(message)
{
  const jsonMessage = JSON.parse(message.data);
  console.log(jsonMessage);

  switch (jsonMessage.id) {
    case 'rtspConnection':
      console.log(jsonMessage)
      break;
    case 'sdpAnswer':
      handleProcessSdpAnswer(jsonMessage);
      break;
    case 'iceCandidate':
      handleAddIceCandidate(jsonMessage);
	  break;
	case 'info':
		console.log(jsonMessage)
		break;
    case 'error':
      console.error(jsonMessage);
      break;
    default:
      console.error("Invalid message, id: " + jsonMessage.id);
      break;
  }
}

// PROCESS_SDP_ANSWER ----------------------------------------------------------

function handleProcessSdpAnswer(jsonMessage)
{
  console.log("SDP Answer from Kurento, process in WebRTC Peer");

  if (webRtcPeer == null) {
    console.warn("Skip, no WebRTC Peer");
    return;
  }

  webRtcPeer.processAnswer(jsonMessage.payload, (err) => {
    if (err) {
      sendError("Error: " + err);
      stop();
      return;
    }

    console.log("[handleProcessSdpAnswer] SDP Answer ready; start remote video");
    startVideo(uiRemoteVideo);

    uiSetState(UI_STARTED);
  });
}

// ADD_ICE_CANDIDATE -----------------------------------------------------------

function handleAddIceCandidate(jsonMessage)
{
  if (webRtcPeer == null) {
    console.warn("Skip, no WebRTC Peer");
    return;
  }

  webRtcPeer.addIceCandidate(jsonMessage.payload, (err) => {
    if (err) {
      console.error("[handleAddIceCandidate] " + err);
      return;
    }
  });
}

// STOP ------------------------------------------------------------------------

function stop()
{
  if (uiState == UI_IDLE) {
    console.log("[stop] Skip, already stopped");
    return;
  }

  console.log("[stop]");

  if (webRtcPeer) {
    webRtcPeer.dispose();
    webRtcPeer = null;
  }

  uiSetState(UI_IDLE);

  sendMessage({
    id: 'stop',
  });
}

/* ==================== */
/* ==== UI actions ==== */
/* ==================== */

// Start -----------------------------------------------------------------------

function uiStart()
{
  console.log("[start] Create WebRtcPeerSendrecv");
  rtspURL = document.getElementById('rtspURL').value;
  sendMessage({
    id: 'rtspURL',
    payload: rtspURL,
  });

  const options = {
    remoteVideo: uiRemoteVideo,
    mediaConstraints: { audio: true, video: true },
    onicecandidate: (candidate) => sendMessage({
      id: 'addIce',
      payload: candidate,
    }),
  };

  webRtcPeer = new kurentoUtils.WebRtcPeer.WebRtcPeerSendrecv(options,
      function(err)
  {
    if (err) {
      sendError("[start/WebRtcPeerSendrecv] Error: "
          + explainUserMediaError(err));
      stop();
      return;
    }

    console.log("[start/WebRtcPeerSendrecv] Generate SDP Offer");
    webRtcPeer.generateOffer((err, sdpOffer) => {
      if (err) {
        sendError("[start/WebRtcPeerSendrecv/generateOffer] Error: " + err);
        stop();
        return;
      }

      sendMessage({
        id: 'processOffer',
        payload: sdpOffer,
      });

      console.log("[start/WebRtcPeerSendrecv/generateOffer] Done!");
      uiSetState(UI_STARTED);
    });
  });
}

// Stop ------------------------------------------------------------------------

function uiStop()
{
  stop();
}

// -----------------------------------------------------------------------------



/* ================== */
/* ==== UI state ==== */
/* ================== */

function uiSetState(newState)
{
  switch (newState) {
    case UI_IDLE:
      uiEnableElement('#uiStartBtn', 'uiStart()');
      uiDisableElement('#uiStopBtn');
      break;
    case UI_STARTING:
      uiDisableElement('#uiStartBtn');
      uiDisableElement('#uiStopBtn');
      break;
    case UI_STARTED:
      uiDisableElement('#uiStartBtn');
      uiEnableElement('#uiStopBtn', 'uiStop()');
      break;
    default:
      console.warn("[setState] Skip, invalid state: " + newState);
      return;
  }
  uiState = newState;
}

function uiEnableElement(id, onclickHandler)
{
  $(id).attr('disabled', false);
  if (onclickHandler) {
    $(id).attr('onclick', onclickHandler);
  }
}

function uiDisableElement(id)
{
  $(id).attr('disabled', true);
  $(id).removeAttr('onclick');
}

function startVideo(video)
{
  // Manually start the <video> HTML element
  // This is used instead of the 'autoplay' attribute, because iOS Safari
  // requires a direct user interaction in order to play a video with audio.
  // Ref: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video
  video.play().catch((err) => {
    if (err.name === 'NotAllowedError') {
      console.error("[start] Browser doesn't allow playing video: " + err);
    }
    else {
      console.error("[start] Error in video.play(): " + err);
    }
  });
}

/**
 * Lightbox utility (to display media pipeline image in a modal dialog)
 */
$(document).delegate('*[data-toggle="lightbox"]', 'click', function(event) {
  event.preventDefault();
  $(this).ekkoLightbox();
});
