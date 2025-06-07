# Player.py
import pygame
import pygwidgets
from Constants import * # 모든 상수를 임포트

class Player():
    def __init__(self, window, startingX, startingY):
        self.window = window
        # 초기 위치를 인자로 받아 이미지 생성 시 바로 적용합니다.
        self.image = pygwidgets.Image(window, (startingX, startingY), 'images/player.png')
        self.playerRect = self.image.getRect() # rect 저장
        self.maxX = WINDOW_WIDTH - self.playerRect.width
        self.maxY = GAME_HEIGHT - self.playerRect.height # 게임 영역 내로 제한
        self.startX = startingX # 초기 위치 저장
        self.startY = startingY

    # 플레이어 위치를 마우스 위치로 업데이트합니다.
    def update(self, x, y):
        # x- 및 y-좌표를 게임 영역 내로 제한합니다.
        if x < 0:
            x = 0
        elif x > self.maxX:
            x = self.maxX
        if y < 0:
            y = 0 
        elif y > self.maxY:
            y = self.maxY

        self.image.setLoc((x, y)) # 이미지 위치 업데이트
        return self.image.getRect() # 업데이트된 Rect 반환

    # 키보드 입력은 사용하지 않으므로 handleInputs 메서드를 제거합니다.
    # def handleInputs(self, keyPressedList):
    #     pass

    def draw(self):
        self.image.draw()

    def getRect(self): # rect 반환 메서드
        return self.image.getRect()

    # 플레이어 위치를 초기화하는 메서드
    def reset(self):
        self.image.setLoc((self.startX, self.startY))
        self.playerRect = self.image.getRect() # reset 후 rect 업데이트