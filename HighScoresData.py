# HighScoresData.py

import json # JSON 파일 처리를 위해 임포트
from Constants import HIGH_SCORES_DATA, HIGH_SCORES_TO_SAVE # 상수 임포트

class HighScoresData:
    def __init__(self):
        # 점수 데이터를 저장할 리스트. 각 항목은 딕셔너리 {'score': 점수, 'name': 이름}
        self.highScores = []
        self.loadScores() # 객체 초기화 시 점수 로드

    def loadScores(self):
        """
        HIGH_SCORES_DATA 상수에 정의된 파일에서 점수를 로드합니다.
        파일이 없으면 빈 리스트로 초기화합니다.
        """
        try:
            with open(HIGH_SCORES_DATA, 'r') as file:
                self.highScores = json.load(file)
            print(f"HighScoresData: {HIGH_SCORES_DATA} 파일에서 점수 로드 완료.")
        except FileNotFoundError:
            # 파일이 없으면 새롭게 시작 (빈 리스트)
            self.highScores = []
            print(f"HighScoresData: {HIGH_SCORES_DATA} 파일을 찾을 수 없어 빈 점수 리스트로 시작합니다.")
        except json.JSONDecodeError:
            # JSON 형식이 잘못되었을 경우
            self.highScores = []
            print(f"HighScoresData: {HIGH_SCORES_DATA} 파일의 JSON 형식이 잘못되었습니다. 빈 점수 리스트로 시작합니다.")
        
        self.sortScores() # 로드 후 점수를 정렬합니다.

    def saveScores(self):
        """
        현재 점수 리스트를 HIGH_SCORES_DATA 상수에 정의된 파일에 저장합니다.
        """
        try:
            with open(HIGH_SCORES_DATA, 'w') as file:
                json.dump(self.highScores, file, indent=4) # 읽기 좋게 indent 추가
            print(f"HighScoresData: 점수를 {HIGH_SCORES_DATA} 파일에 성공적으로 저장했습니다.")
        except IOError as e:
            print(f"오류: 점수 파일 저장 실패 - {e}")

    def addScore(self, newScore, newName):
        """
        새로운 점수를 추가하고, 정렬 후 N_HIGH_SCORES만큼 유지합니다.
        """
        # 새 점수를 딕셔너리 형태로 추가
        self.highScores.append({'score': newScore, 'name': newName})
        self.sortScores() # 추가 후 정렬

        # HIGH_SCORES_TO_SAVE만큼만 유지
        self.highScores = self.highScores[:HIGH_SCORES_TO_SAVE]
        self.saveScores() # 변경사항 저장

    def getScores(self):
        """
        현재 최고 점수 리스트를 반환합니다.
        """
        return self.highScores

    def sortScores(self):
        """
        점수를 내림차순으로 정렬합니다.
        """
        self.highScores.sort(key=lambda x: x['score'], reverse=True)