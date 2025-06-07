# SceneHighScores.py

import pygame
import pygwidgets
import pyghelpers
import json # JSON 파일 처리를 위해 임포트
from Constants import (WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, FONT_NAME,
                        HIGH_SCORES_DATA, HIGH_SCORES_TO_SAVE,
                        SCENE_SPLASH, SCENE_HIGH_SCORES) # K_SCENE_SPLASH 대신 SCENE_SPLASH로 변경

class SceneHighScores(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        self.scores = [] # 최고 점수 리스트
        self.loadHighScores() # 파일에서 최고 점수 로드

        # UI 요소
        self.titleText = pygwidgets.DisplayText(self.window, (0, 50), 'HIGH SCORES',
                                               fontSize=60, textColor=WHITE, justified='center', width=WINDOW_WIDTH)
        self.scoreListText = pygwidgets.DisplayText(self.window, (0, 150), '', # 점수 목록 표시
                                                   fontSize=36, textColor=WHITE, justified='center', width=WINDOW_WIDTH)
        
        self.instructionsText = pygwidgets.DisplayText(self.window, (0, WINDOW_HEIGHT - 60),
                                                    'Click anywhere to return to the Main Menu',
                                                    fontSize=28, textColor=WHITE, justified='center', width=WINDOW_WIDTH)
        
        self.updateScoreListDisplay() # 점수 목록 UI 업데이트

    def getSceneKey(self):
        return SCENE_HIGH_SCORES # 변경 없음

    def enter(self, data):
        # 씬 진입 시 데이터 확인 및 최고 점수 업데이트
        if 'score' in data: # 새로운 점수가 있다면
            newScore = data['score']
            self.addHighScore(newScore)
            self.updateScoreListDisplay()

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == QUIT:
                self.quit()
            elif event.type == MOUSEBUTTONDOWN:
                self.goToScene(SCENE_SPLASH) # SCENE_SPLASH로 돌아감

    def update(self):
        pass # 특별한 애니메이션이나 게임 로직 없음

    def draw(self):
        self.window.fill(BLACK)
        self.titleText.draw()
        self.scoreListText.draw()
        self.instructionsText.draw()

    def loadHighScores(self):
        """파일에서 최고 점수를 로드합니다."""
        try:
            with open(HIGH_SCORES_DATA, 'r') as file:
                self.scores = json.load(file)
        except FileNotFoundError:
            self.scores = [] # 파일이 없으면 빈 리스트로 시작
        except json.JSONDecodeError:
            self.scores = [] # JSON 디코딩 오류 시 빈 리스트로 시작 (파일이 비어있거나 손상된 경우)

    def saveHighScores(self):
        """최고 점수를 파일에 저장합니다."""
        with open(HIGH_SCORES_DATA, 'w') as file:
            json.dump(self.scores, file)

    def addHighScore(self, newScore):
        """새로운 점수를 최고 점수 목록에 추가하고 정렬합니다."""
        if isinstance(newScore, dict) and 'score' in newScore and 'name' in newScore:
            self.scores.append(newScore)
        else: # 이름이 없는 경우 (예: 게임 오버 시 바로 넘어온 점수)
            # 이름을 입력받는 다이얼로그를 사용할 수도 있지만, 여기서는 단순히 'Player'로 추가
            self.scores.append({'name': 'Player', 'score': newScore})
            # 또는 pyghelpers.customInputDialog를 사용하여 이름을 입력받을 수 있음

        self.scores.sort(key=lambda item: item['score'], reverse=True) # 점수를 내림차순 정렬
        self.scores = self.scores[:HIGH_SCORES_TO_SAVE] # 저장할 개수만큼만 유지
        self.saveHighScores()

    def updateScoreListDisplay(self):
        """UI에 표시될 점수 목록 텍스트를 업데이트합니다."""
        displayScores = []
        for i, entry in enumerate(self.scores):
            displayScores.append(f'{i+1}. {entry["name"]}: {entry["score"]}')
        
        if not displayScores:
            self.scoreListText.setText('No high scores yet!')
        else:
            self.scoreListText.setText('\n'.join(displayScores))