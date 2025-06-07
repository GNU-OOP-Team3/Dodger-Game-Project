# ScenePlayStage.py
import pygame
import pygwidgets
import pyghelpers
from Constants import (SCENE_PLAY_STAGE, SCENE_HIGH_SCORES, 
                        DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD, 
                        PLAYER_START_X, PLAYER_START_Y, # Player 초기 위치 사용 (Constants.py에 정의 필요)
                        BADDY_POINTS, GOODIE_POINTS, BADDY_SPEED_MULTIPLIER,
                        BADDY_SPAWN_INTERVAL, GOODIE_SPAWN_INTERVAL, GAME_DURATION_STAGE_MODE,
                        STATE_PLAYING) # STATE_PLAYING 추가 (updateGameplay에서 사용)
from ScenePlay import ScenePlay # ScenePlay를 상속받음
# import pygame.mixer # 사운드 제거로 인해 주석 처리 또는 제거

class ScenePlayStage(ScenePlay):
    def __init__(self, window):
        super().__init__(window) # 부모 클래스 ScenePlay의 생성자 호출
        self.currentDifficulty = DIFFICULTY_EASY # 기본 난이도 설정 (enter 메서드에서 재설정됨)
        self.baddySpeedMultiplier = BADDY_SPEED_MULTIPLIER[self.currentDifficulty]
        self.baddySpawnInterval = BADDY_SPAWN_INTERVAL[self.currentDifficulty]
        self.goodieSpawnInterval = GOODIE_SPAWN_INTERVAL[self.currentDifficulty]
        self.gameDuration = GAME_DURATION_STAGE_MODE # 스테이지 모드 시간

        self.lastBaddySpawnTime = pygame.time.get_ticks()
        self.lastGoodieSpawnTime = pygame.time.get_ticks()

    def getSceneKey(self):
        return SCENE_PLAY_STAGE

    def enter(self, data):
        # 데이터에서 난이도 설정
        if 'difficulty' in data:
            self.currentDifficulty = data['difficulty']
            self.baddySpeedMultiplier = BADDY_SPEED_MULTIPLIER[self.currentDifficulty]
            self.baddySpawnInterval = BADDY_SPAWN_INTERVAL[self.currentDifficulty]
            self.goodieSpawnInterval = GOODIE_SPAWN_INTERVAL[self.currentDifficulty]
        
        super().enter(data) # 부모 클래스의 enter 메서드 호출

    def updateGameplay(self):
        # 마우스 현재 위치 가져오기
        mouseX, mouseY = pygame.mouse.get_pos()
        # 플레이어 위치 업데이트 (마우스 위치 전달)
        playerRect = self.oPlayer.update(mouseX, mouseY) # <-- 이 줄을 이렇게 수정합니다.

        # Baddy 생성 로직
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastBaddySpawnTime > self.baddySpawnInterval:
            self.oBaddieMgr.addBaddy(self.baddySpeedMultiplier)
            self.lastBaddySpawnTime = currentTime

        # Goodie 생성 로직
        if currentTime - self.lastGoodieSpawnTime > self.goodieSpawnInterval:
            self.oGoodieMgr.addGoodie()
            self.lastGoodieSpawnTime = currentTime

        # 충돌 감지
        baddiesHit = self.oBaddieMgr.update(playerRect)
        self.score -= baddiesHit * BADDY_POINTS # 점수 감소
        
        goodiesHit = self.oGoodieMgr.update(playerRect)
        self.score += goodiesHit * GOODIE_POINTS # 점수 증가 (사운드 제거)
        # if goodiesHit > 0 and self.isSoundOn: # 사운드 제거
        #     self.goodieSound.play()

        # 점수 업데이트
        self.scoreText.setValue(f'Score: {self.score}')

        # 게임 시간 체크
        if currentTime - self.startTime > self.gameDuration:
            self.endGame()

    def reset(self):
        super().reset() # 부모 클래스의 reset 메서드 호출
        self.startTime = pygame.time.get_ticks() # 게임 시작 시간 기록

    def endGame(self):
        # pygame.mixer.music.stop() # 사운드 제거
        # if self.isSoundOn: # 사운드 제거
        #    self.gameOverSound.play()
        self.playingState = STATE_GAME_OVER # 게임 오버 상태로 전환
        finalScore = self.score

        prompt = f'Game Over! Final Score: {finalScore}\nDo you want to play again?'
        self.dialogPromptText.setValue(prompt)
        # pyghelpers.customYesNoDialog 호출 시 버튼은 별도로 인스턴스화하지 않습니다.
        result = self.oSceneMgr.showCustomYesNoDialog(self.dialogPromptText, 
                                                     yesButtonText='Yes, please!', 
                                                     noButtonText='No, thanks.')
        
        if result == 'Yes': # DIALOG_YES 대신 직접 문자열 'Yes' 사용
            self.goToScene(SCENE_PLAY_STAGE, {'difficulty': self.currentDifficulty})
        else: # DIALOG_NO 대신 직접 문자열 'No' 사용
            self.goToScene(SCENE_HIGH_SCORES, {'score': finalScore})