import pygame
import pygwidgets
import random
from Constants import *

class PowerUp:
    MIN_SIZE, MAX_SIZE = 10, 40
    MIN_SPEED, MAX_SPEED = 1, 8
    LLEFT, LRIGHT = 'left', 'right'

    IMAGE_FILE = 'images/goodie.png'  # 기본 이미지
    TYPE = 'score'                    # 기본 파워업 종류
    DURATION = 0                      # 0이면 지속효과 없음

    def __init__(self, window):
        self.window = window
        size = random.randrange(self.MIN_SIZE, self.MAX_SIZE + 1)
        self.y = random.randrange(0, GAME_HEIGHT - size)
        self.dir = random.choice([self.LLEFT, self.LRIGHT])

        self.x = WINDOW_WIDTH if self.dir == self.LLEFT else -size
        speed = random.randrange(self.MIN_SPEED, self.MAX_SPEED + 1)
        self.vx = -speed if self.dir == self.LLEFT else speed

        self.image = pygwidgets.Image(window, (self.x, self.y), pygame.image.load(self.IMAGE_FILE))
        self.image.scale(int((size * 100) / self.MAX_SIZE), False)

    def update(self):
        self.x += self.vx
        self.image.setLoc((self.x, self.y))
        return (self.x < -self.image.getRect().width) or (self.x > WINDOW_WIDTH)

    def draw(self):
        self.image.draw()

    def collide(self, playerRect) -> bool:
        return self.image.overlaps(playerRect)

    def apply_effect(self, scenePlay):
        pass  # 하위 클래스에서 효과 구현


class Score2X(PowerUp):
    IMAGE_FILE = 'images/goodie_double.png'
    TYPE = 'score_x2'
    DURATION = 0  # 지속 효과 없음 (바로 점수만 줌)

    def apply_effect(self, scenePlay):
        scenePlay.score += POINTS_FOR_GOODIE * 2  # 초록 goodie 2개만큼 점수 부여
        scenePlay.dingSound.play()



class SlowMotion(PowerUp):
    IMAGE_FILE = 'images/goodie_slow.png'
    TYPE = 'slow'
    DURATION = 200  # 약 5초간 정지

    def apply_effect(self, scenePlay):
        # 중복 방지: 이미 정지 중이면 시간만 연장
        already_active = False
        for i, (key, frames) in enumerate(scenePlay.activeTimers):
            if key == 'slow':
                scenePlay.activeTimers[i] = (key, frames + self.DURATION)
                already_active = True
                break

        if not already_active:
            scenePlay.slowFactor = 0  # 속도 0 = 정지
            scenePlay.activeTimers.append(('slow', self.DURATION))



class Invincibility(PowerUp):
    IMAGE_FILE = 'images/goodie_invincibility.png'
    TYPE = 'invincible'
    DURATION = 300

    def apply_effect(self, scenePlay):
        scenePlay.invincible = True
        scenePlay.activeTimers.append(('invincible', self.DURATION))
