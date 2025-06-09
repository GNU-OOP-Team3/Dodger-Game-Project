# Goodie and GoodieMgr classes
import pygame
import pygwidgets
import random
from Constants import *
from PowerUps import PowerUp  # 상속을 위한 import

class Goodie(PowerUp):
    IMAGE_FILE = 'images/goodie.png'
    TYPE = 'score'
    DURATION = 0  # 지속효과 없음

    def __init__(self, window):
        super().__init__(window)  # PowerUp에서 공통 초기화 수행
        # Goodie 전용 속성 정의 필요 시 여기에 추가 가능

    def apply_effect(self, scenePlay):
        pass  # 점수는 ScenePlay 쪽에서 처리

# 기존 GoodieMgr 유지
class GoodieMgr():
    GOODIE_RATE_LO = 90
    GOODIE_RATE_HI = 111

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # Called when starting a new game
        self.goodiesList = []
        self.nFramesTilNextGoodie = GoodieMgr.GOODIE_RATE_HI

    def update(self, thePlayerRect):
        nGoodiesHit = 0
        goodiesListCopy = self.goodiesList.copy()
        for oGoodie in goodiesListCopy:
            deleteMe = oGoodie.update()
            if deleteMe:
                self.goodiesList.remove(oGoodie)
            elif oGoodie.collide(thePlayerRect):
                self.goodiesList.remove(oGoodie)
                nGoodiesHit += 1

        self.nFramesTilNextGoodie -= 1
        if self.nFramesTilNextGoodie == 0:
            oGoodie = Goodie(self.window)
            self.goodiesList.append(oGoodie)
            self.nFramesTilNextGoodie = random.randrange(
                GoodieMgr.GOODIE_RATE_LO,
                GoodieMgr.GOODIE_RATE_HI)

        return nGoodiesHit

    def draw(self):
        for oGoodie in self.goodiesList:
            oGoodie.draw()
