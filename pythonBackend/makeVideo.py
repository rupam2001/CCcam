from subprocess import Popen, PIPE

class MakeVideo:
    def __init__(self):
        self.fps, self.duration = 24, 100
        self.p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-r', '24', '-i', '-', '-vcodec', 'mpeg4', '-qscale', '5', '-r', '24', 'video.avi'], stdin=PIPE)


    def addFrame(self, img):
        img.save(self.p.stdin, "JPEG")
        
    def close(self):
        self.p.stdin.close() 
        self.p.wait()
    def __del__(self):
        self.close()