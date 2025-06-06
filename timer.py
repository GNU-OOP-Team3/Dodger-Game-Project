# Timer.py
import time

class Timer:
    def __init__(self, timeInSeconds, nickname=None, callBack=None):
        self.timeInSeconds = timeInSeconds
        self.nickname = nickname
        self.callBack = callBack
        self.savedSecondsElapsed = 0.0
        self.running = False
        self.startTime = 0.0 # startTime 초기화 추가

    def start(self, newTimeSeconds=None):
        if newTimeSeconds is not None:
            self.timeInSeconds = newTimeSeconds
        self.running = True
        self.startTime = time.time()

    def update(self):
        if not self.running:
            return False
        self.savedSecondsElapsed = time.time() - self.startTime
        if self.savedSecondsElapsed < self.timeInSeconds:
            return False
        else:
            self.running = False
            if self.callBack is not None:
                self.callBack(self.nickname)
            return True

    def getTime(self):
        if self.running:
            self.savedSecondsElapsed = time.time() - self.startTime
        return self.savedSecondsElapsed

    def stop(self):
        self.getTime()
        self.running = False

    def isRunning(self): # 이 메서드 추가
        return self.running
