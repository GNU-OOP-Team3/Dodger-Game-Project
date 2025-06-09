## 🚀 PowerUp 시스템 및 구조 확장 (JSP 브랜치 변경사항 요약)

이번 업데이트에서는 다양한 파워업 효과를 구현하고, 기존 Goodie 시스템을 확장하는 리팩토링을 진행했습니다. 전체 변경 사항은 다음과 같이 네 가지 주요 영역(PowerUps, Goodies, Baddies, ScenePlay)에 걸쳐 적용되었습니다.

---

### 🧩 PowerUps: 신규 모듈 도입 및 파워업 구현

`PowerUps.py` 모듈이 새로 추가되어, 다양한 파워업을 클래스로 정의하고 공통 인터페이스로 관리할 수 있도록 구조화하였습니다.

#### ✅ 핵심 변경 사항
- **`PowerUp` 상위 클래스 도입**: 모든 파워업 아이템(Score2X, SlowMotion, Invincibility)의 부모 역할. 위치, 속도, 이미지 처리 등의 공통 로직 제공.
- **`apply_effect()` 메서드**: 각 파워업 효과를 ScenePlay에 전달하는 공통 인터페이스.
- **파워업 클래스 종류**:
  - `Score2X`: 점수 2배, 즉시 적용
  - `SlowMotion`: 적 정지 (5초), 중복 시 시간만 연장
  - `Invincibility`: 무적 상태 (5초)

---

### 🍀 Goodies: 구조 리팩토링 및 PowerUp 통합

기존 `Goodie` 클래스를 `PowerUp` 하위 클래스로 변경하여 코드 중복을 줄이고, 향후 다양한 Goodie를 쉽게 추가할 수 있도록 개선하였습니다.

#### ✅ 핵심 변경 사항
- `Goodie` → `PowerUp` 상속 구조로 변경
- `TYPE = 'score'` 속성 추가 (타입 분류 시스템)
- `apply_effect()` 구현 (점수 Goodie는 pass 처리)
- `GoodieMgr`는 구조 변경 없이 유지됨 (기존 기능 완전 보존)

---

### 😈 Baddies: 슬로우모션 연동을 위한 속도 제어 기능 추가

`SlowMotion` 파워업과 연동하기 위해 Baddie의 낙하 속도를 외부에서 조절할 수 있도록 확장했습니다.

#### ✅ 핵심 변경 사항
- `Baddie.update(scale=1.0)` / `BaddieMgr.update(scale=1.0)` → **속도 조절 파라미터 `scale` 추가**
- `scale = 0`일 경우 Baddie 정지 (슬로우모션 효과)
- 기존 충돌 판정, 생성 주기, 제거 로직은 그대로 유지됨

#### 📌 요약
- 속도 제어 기능 도입을 통해 SlowMotion과 같은 파워업과 연동 가능
- 기본값을 1.0으로 설정하여 기존 동작과 완전 호환 유지

---

### 🎮 ScenePlay: 파워업 시스템 통합 및 상태 관리

`ScenePlay.py`에 새로운 파워업 매니저(`PowerUpMgr`)를 도입하고, 상태 변화 관리 로직을 추가하여 다양한 파워업을 자연스럽게 통합했습니다.

#### ✅ 핵심 변경 사항
- `PowerUpMgr` 클래스 정의 및 인스턴스화
- `update()`에서 파워업 충돌 감지 → `apply_effect(scenePlay)` 호출
- `activeTimers` 리스트로 지속 효과 시간 추적 및 자동 해제 처리
  - `slowFactor`, `invincible`, `scoreMultiplier` 자동 복귀
- `draw()`에서도 파워업 렌더링 추가 → UI 통일감 확보

#### 📌 요약
- 새로운 파워업을 도입하되 기존 게임 흐름을 손상하지 않고 자연스럽게 통합
- 파워업 효과의 충돌 처리, 지속 시간, 자동 해제를 일관된 방식으로 처리

---

## 🧠 설계 의도 및 기대 효과

- **확장성 확보**: 새로운 Goodie/PowerUp을 클래스 하나만 추가하면 시스템에 통합 가능
- **중복 제거**: 공통 기능은 PowerUp에서 처리 → Goodie, 특수 아이템은 효과만 정의
- **유지보수성 향상**: 코드 흐름이 명확해지고, 개별 요소의 독립성이 보장됨

---

✅ 이제 이 구조 위에서 새로운 파워업이나 Goodie를 계속 추가해 나갈 수 있습니다!
