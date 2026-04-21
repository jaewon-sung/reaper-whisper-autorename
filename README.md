# reaper-whisper-autorename

REAPER Python scripts that use OpenAI Whisper STT to automatically rename selected media item takes.

---

> **한국어 설명은 아래에 있습니다.**

---

## Scripts

| Script | Description |
|--------|-------------|
| `Whisper_AutoRename.py` | Base script — transcribes selected items with Whisper and renames takes using the transcript text |
| `Whisper_Excel_AutoRename_For_Korean.py` | Korean mode — transcribes with Whisper (`language='ko'`), then fuzzy-matches the transcript against a script Excel file to find the closest matching line and uses it as the take name |
| `Whisper_Excel_AutoRename_For_English.py` | Same as above but in English mode (`language='en'`) |
| `_Whisper_Progress.py` | Progress window helper — spawned as a subprocess to show live transcription progress; not meant to be run directly |

## Requirements

- REAPER with Python support enabled
- Python 3.8+ in system PATH
- `ffmpeg` on PATH
- `openpyxl` installed (`pip install openpyxl`) — for Excel-matching scripts
- A script Excel file (`.xlsx`) with one line of dialogue per row, first column — for Excel-matching scripts

## Setup

1. Copy all `.py` files into your REAPER `Scripts` folder  
   (`%APPDATA%\REAPER\Scripts\`)
2. In REAPER: **Actions > Show action list > Load** — add the main scripts you want to use
3. Assign keyboard shortcuts as needed

## Usage

### `Whisper_AutoRename.py`
1. Select one or more media items in the REAPER timeline
2. Run the action
3. Each item's active take is renamed to its Whisper transcript

### `Whisper_Excel_AutoRename_For_Korean.py` / `_For_English.py`
1. Prepare a script Excel file — one dialogue line per row, in column A
2. Select media items
3. Run the action — a file dialog will ask for the Excel file on first run
4. Each take is transcribed, fuzzy-matched against the script, and renamed to the best matching line

## Notes

- Python is auto-detected from system PATH — no hardcoded path required
- Whisper `base` model is used by default; change `load_model('base')` to `small`, `medium`, etc. for better accuracy at the cost of speed
- The Excel-matching scripts use `difflib.SequenceMatcher` for fuzzy matching

---

## 한국어 설명

OpenAI Whisper STT를 활용해 REAPER에서 선택한 미디어 아이템의 테이크 이름을 자동으로 변경하는 Python 스크립트 모음입니다.

### 스크립트 목록

| 스크립트 | 설명 |
|---------|------|
| `Whisper_AutoRename.py` | 기본 버전 — 선택한 아이템을 Whisper로 음성 인식한 뒤 전사 텍스트를 테이크 이름으로 지정 |
| `Whisper_Excel_AutoRename_For_Korean.py` | 한국어 버전 — Whisper로 음성 인식(`language='ko'`) 후, 대본 Excel 파일과 퍼지 매칭하여 가장 유사한 대사를 테이크 이름으로 지정 |
| `Whisper_Excel_AutoRename_For_English.py` | 영어 버전 — 위와 동일하나 `language='en'` 사용 |
| `_Whisper_Progress.py` | 진행 상태 창 헬퍼 — 전사 진행률을 별도 창으로 표시, 직접 실행하지 않아도 됨 |

### 사전 준비

- REAPER (Python 스크립트 실행 활성화 필요)
- Python 3.8 이상 (시스템 PATH에 등록되어 있어야 함)
- `openai-whisper` 설치: `pip install openai-whisper`
- `ffmpeg` (PATH에 등록)
- `openpyxl` 설치: `pip install openpyxl` (Excel 매칭 스크립트 사용 시)
- 대본 Excel 파일 (`.xlsx`) — A열에 대사를 한 줄씩 입력 (Excel 매칭 스크립트 사용 시)

### 설치 방법

1. 모든 `.py` 파일을 REAPER Scripts 폴더에 복사  
   경로: `%APPDATA%\REAPER\Scripts\`
2. REAPER에서 **Actions > Show action list > Load**로 사용할 스크립트 등록
3. 필요에 따라 단축키 지정

### 사용 방법

#### `Whisper_AutoRename.py`
1. REAPER 타임라인에서 미디어 아이템 선택
2. 액션 실행
3. 각 아이템의 활성 테이크가 음성 인식 결과로 자동 이름 변경

#### `Whisper_Excel_AutoRename_For_Korean.py` / `_For_English.py`
1. 대본 Excel 파일 준비 (A열에 대사 한 줄씩)
2. 미디어 아이템 선택
3. 액션 실행 — 파일 선택 다이얼로그에서 Excel 파일 지정
4. 각 테이크가 음성 인식 → 대본 퍼지 매칭 → 가장 유사한 대사로 이름 변경

### 참고 사항

- Python 경로는 시스템 PATH에서 자동 감지 — 별도 수정 불필요
- 기본 모델은 `base`; 정확도가 필요하면 `load_model('base')`를 `small`, `medium`, `large` 등으로 변경 (속도 느려짐)
- Excel 매칭은 `difflib.SequenceMatcher`를 사용한 유사도 비교 방식
