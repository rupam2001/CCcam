from glob import glob
import json
import time
from flask import Flask
from flask import send_from_directory
from flask_sock import Sock
from flask_cors import CORS

from image_processing import binaryToPILImage, binaryToNumpyArray
from image_processing import MotionDetector
from storage_utils import saveImage

motionDetector = MotionDetector(debug=False)

from storage_utils import VideoRecorder

videoRedorder = None

# mv = MakeVideo()

app = Flask(__name__)
CORS(app)
sock = Sock(app)

@app.route('/')
def index():
    return 'Server running'

@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('reports', path)


takeASnap = False

start_recording = False
stop_recording = False


@app.route("/takeasnap")
def snap():
    print("snap request")
    global takeASnap
    takeASnap = True
    return ""

@app.route("/startrecording")
def startRecording():
    print("start recording request")
    global start_recording, videoRedorder
    start_recording = True
    videoRedorder = VideoRecorder()
    return ""

@app.route("/stoprecording")
def stopRecording():
    print("stop recording request")
    global start_recording, videoRedorder
    start_recording = False
    if videoRedorder is not None:
        videoRedorder.saveAndStop()
        videoRedorder = None
    return ""


 
viewerSock = None
viewerSockAuth = False

isLiveStreamOn = True
isMotionDetectorOn = False

lastLiveActive = None




auth_key_viewer = "iamthegod"

@sock.route('/viewer')
def viewer(sock):
    global viewerSock
    # viewerSock = sock
    print("Viewer joined", str(sock))
    while True:
        data = sock.receive()
        authenticateViewer(data, sock)
        # sock.send(data)


def authenticateViewer(data, sock):
    global viewerSockAuth, viewerSock

    data = json.loads(data)
    if 'authentication' in data:
        auth_key = data['authentication']
        if auth_key == auth_key_viewer:
            viewerSock = sock
            viewerSockAuth = True
        else:
            sock.send(json.dumps({"error":"Authentication key missmatched"}))
            viewerSock = None
            print(data)
    else:
        sock.send(json.dumps({"error":"Please Authenticate"}))
        viewerSock = None
            


cam_data_count = 0
@sock.route("/cam")
def cam(sock):
    global takeASnap
    global viewerSock, cam_data_count
    while True:
        data = sock.receive()
        lastLiveActive = round(time.time()*1000)
        print(type(data), cam_data_count)
        cam_data_count += 1

        if isMotionDetectorOn:
            motionDetector.nextFrame(binaryToPILImage(data))
            isMotionDetected, motionSegmantedFrame, originalFrame = motionDetector.detectMotion()

            if isMotionDetected:
                messageToViewer = {"motiondetected": True}
                print("motion detected")
                if viewerSock is not None and viewerSockAuth is True:
                    viewerSock.send(json.dumps(messageToViewer))
        else:
            motionDetector.clearFrames()
        
        if viewerSock is not None and viewerSockAuth is True:
            try:
                if type(data) is bytes and isLiveStreamOn == True:
                    viewerSock.send(data)
                    viewerSock.send(json.dumps({"lastLiveActive": lastLiveActive}))
                    if takeASnap:
                        saveImage(binaryToPILImage(data), f'.\saved\images{time.time()}.jpg')
                        print("image saved")
                        
                        takeASnap = False
                    if start_recording:
                        videoRedorder.nextFrame(binaryToNumpyArray(data))
                
            except Exception:
                print("error")
                viewerSock = None
   





    





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',threaded=True)