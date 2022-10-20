
import io
import os
import sys
import time
from flask import Flask
from flask import send_from_directory
from flask_sock import Sock
import numpy as np
import base64
import json
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from makeVideo import MakeVideo


mv = MakeVideo()

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return 'Server running'

@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('reports', path)

 
viewerSock = None

@sock.route('/viewer')
def viewer(sock):
    global viewerSock
    viewerSock = sock
    while True:
        data = sock.receive()
        # print(data)
        sock.send(data)
    pass

@sock.route("/cam")
def cam(sock):
    while True:
        data = sock.receive()
        print(type(data))
        processImage(data)

        if viewerSock is not None:
            try:
                if type(data) is bytes:
                    viewerSock.send(data)
            except Exception:
                print("error")
    pass



def processImage(data):
    global mv
    if type(data) is not str:
        return
    try:
        data = json.loads(data)
        b64 = data['frame']
        b64_decoded = base64.b64decode(b64)
        image = Image.open(io.BytesIO(b64_decoded))
    except Exception:
        return
    # image.save(f"./saved/images/{time.time()}.png")
    mv.addFrame(image)
    
    image_np = np.array(image)
    print(type(image_np))
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',threaded=True)