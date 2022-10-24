from storage_utils import VideoRecorder
import numpy as np

vr = VideoRecorder()


for i in range(0, 255):
        img = np.ones((500, 500, 3), dtype=np.uint8)*i
        vr.nextFrame(img)
vr.saveAndStop()
