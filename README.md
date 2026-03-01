# hotconnectwinandmac
윈도우, 맥 간 스크린샷 공유 MVP

## 1) 프로젝트 구조
```text
hotconnectwinandmac/
├─ requirements.txt
├─ README.md
├─ win_push/
│  └─ main.py
└─ mac_clip/
   └─ main.py
```

## 2) 의존성
- Python 3.11
- PySide6 (Windows 미리보기 UI)
- Pillow (이미지 핸들링)
- watchdog (폴더 감시)
- pywin32 (Windows 클립보드 시퀀스 감지)
- AppleScript (`osascript`, macOS 클립보드 반영)

설치:
```bash
python -m pip install -r requirements.txt
```

## 3) 앱 설명

### A. Windows 앱: `win_push`
- 클립보드 시퀀스를 주기적으로 확인합니다.
- 새 이미지가 들어오면 PySide6 미리보기 다이얼로그를 띄웁니다.
- 사용자가 저장(Save)을 누르면 `Z:\`에 `shot_YYYYMMDD_HHMMSS.jpg` 형식으로 저장합니다.

실행:
```bash
python win_push/main.py
```

### B. macOS 앱: `mac_clip`
- `~/IncomingShots` 폴더를 감시합니다.
- 새 `.jpg`, `.jpeg` 파일 생성 시 AppleScript로 해당 이미지를 클립보드에 설정합니다.

실행:
```bash
python mac_clip/main.py
```

## 4) MVP 수용 기준 (Acceptance Criteria)
1. Windows에서 클립보드에 이미지 복사 시 미리보기 창이 열린다.
2. 미리보기에서 Save 클릭 시 JPEG 파일이 `Z:\`에 저장된다.
3. 파일명은 타임스탬프(`shot_YYYYMMDD_HHMMSS.jpg`) 형식이다.
4. macOS에서 `~/IncomingShots`에 새 JPEG 파일이 생성되면 자동으로 클립보드 이미지가 갱신된다.
5. 두 앱 모두 단독 실행 가능하며, Ctrl+C 또는 창 종료로 안전하게 중단 가능하다.

## 5) 테스트 절차

### Windows (`win_push`)
1. `python win_push/main.py` 실행.
2. 캡처 도구 등으로 이미지 하나를 클립보드에 복사.
3. 미리보기 창 표시 확인.
4. Save 클릭 후 `Z:\`에 파일 생성 확인.
5. 생성 파일이 JPEG이며 열리는지 확인.

### macOS (`mac_clip`)
1. `python mac_clip/main.py` 실행.
2. `~/IncomingShots`에 `test.jpg` 복사/생성.
3. 로그에 `클립보드 업데이트` 출력 확인.
4. 미리보기 가능한 앱(예: 미리보기/메신저 입력창)에 붙여넣어 방금 파일 이미지가 들어가는지 확인.

## 6) 참고
- `Z:\` 드라이브는 네트워크 드라이브로 사전 연결되어 있어야 합니다.
- macOS에서 처음 실행 시 자동화/접근성 권한 요청이 뜰 수 있습니다.
