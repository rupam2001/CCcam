

def saveImage(img, path):
    img.save(path)

# import time
# import cv2
# class VideoRecorder:
#     fps = 15
#     frameSize = (1200,1600)
#     def __init__(self, video_chunks_duration=10) -> None:
#         self.frames = []
#         self.out = cv2.VideoWriter(f'{time.time()}.avi',cv2.VideoWriter_fourcc(*'DIVX'), self.fps, self.frameSize)
#         self.video_chunks_duration = video_chunks_duration
        
#     def reset(self):
#         self.out = cv2.VideoWriter(f'{time.time()}.avi',cv2.VideoWriter_fourcc(*'DIVX'), self.fps, self.frameSize)
#         self.frames = []

#     def nextFrame(self, frame):
#         self.frames.append(frame)
#         print("frame added", len(self.frames))
#         if (len(self.frames) // self.fps) >= self.video_chunks_duration:
#             self.saveAndStop()
#             self.reset()
            
#     def saveAndStop(self):
#         for frame in self.frames:
#             self.out.write(frame)
#         self.out.release()
#         print("Video saved")
#         self.frames = []
#     def __del__(self):
#         if len(self.frames):
#             self.saveAndStop()



    


    