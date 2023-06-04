import base64

import json
import time
from PIL import Image, ImageChops
from PIL import ImageFile
import io
import numpy as np
import math


ImageFile.LOAD_TRUNCATED_IMAGES = True


def binaryToNumpyArray(data):
    if type(data) is not bytes:
        return None
    image = Image.open(io.BytesIO(data))
    return np.array(image)

def binaryToPILImage(data):
    if type(data) is not bytes:
        return None
    image = Image.open(io.BytesIO(data))
    return image

def bas64ToNumpyArray(data):

    if type(data) is not str:
        return
    try:
        data = json.loads(data)
        b64 = data['frame']
        b64_decoded = base64.b64decode(b64)
        image = Image.open(io.BytesIO(b64_decoded))
    except Exception:
        return None
    return np.array(image)

# import cv2

class MotionDetector:
    def __init__(self, numFrameToUse=2, threshold=6.0, debug=False) -> None:
        self.numFramesToUse = numFrameToUse
        self.frames = []
        self.threshold = threshold
        self.debug = debug
        pass
    def setNewThreshold(self, th):
        self.threshold = th
    def nextFrame(self, frame):
        self.frames.append(frame)
        if len(self.frames) > self.numFramesToUse:
            self.frames.pop(0)
        if self.debug:
            print("nextFrame method: ", self.frames)
    def clearFrames(self):
        self.frames = []

    def detectMotion(self):
        if len(self.frames) >= self.numFramesToUse:
            
            frame1 = np.array(self.frames[0])  #first frame
            frame2 = np.array(self.frames[self.numFramesToUse - 1]) #last frame
            frame2_copy_for_contour = frame2
            frame2_copy = frame2

            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

            frame1 = cv2.GaussianBlur(src=frame1, ksize=(5,5), sigmaX=0)
            frame2 = cv2.GaussianBlur(src=frame2, ksize=(5,5), sigmaX=0)

            diff_frame = cv2.absdiff(src1=frame1, src2=frame2)
            kernel = np.ones((5, 5))
            diff_frame = cv2.dilate(diff_frame, kernel, 1)
            thresh_frame = cv2.threshold(src=diff_frame, thresh=60, maxval=255, type=cv2.THRESH_BINARY)[1]

            contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(image=frame2_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
            isMotion = False
            for contour in contours:
                if cv2.contourArea(contour) < 50:
                    # too small: skip!
                    continue
                isMotion = True
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(img=frame2_copy_for_contour, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)
            
            if isMotion:
                cv2.imwrite(f"./saved/images/{time.time()}.jpg", frame2_copy_for_contour)

            return isMotion, frame2_copy_for_contour, frame2_copy
        return False, None, None

        #     diff = ImageChops.difference(frame1, frame2)
        #     entropy = self.__image_entropy(diff)
        #     if self.debug:
        #         print("detectMotion, entorpy:", entropy)
        #     if entropy > self.threshold:
        #         return True
        #     return False

        # return False

    def __image_entropy(self, img):
        """calculate the entropy of an image"""
        # this could be made more efficient using numpy
        histogram = img.histogram()
        histogram_length = sum(histogram)
        samples_probability = [float(h) / histogram_length for h in histogram]
        return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])
    