# reaper-whisper-autorename

REAPER Python scripts that use OpenAI Whisper STT to automatically rename selected media item takes.

## Scripts

| Script | Description |
|--------|-------------|
| `Whisper_AutoRename.py` | Base script — transcribes selected items with Whisper and renames takes using the transcript text |
| `Whisper_Excel_AutoRename_For_Korean.py` | Korean mode — transcribes with Whisper (`language='ko'`), then fuzzy-matches the transcript against a script Excel file to find the closest matching line and uses it as the take name |
| `Whisper_Excel_AutoRename_For_English.py` | Same as above but in English mode (`language='en'`) |
| `_Whisper_Progress.py` | Progress window helper — spawned as a subprocess to show live transcription progress; not meant to be run directly |

## Requirements

- REAPER with Python support enabled
- Python 3.11 at `C:\Python311\python.exe`
- `openai-whisper` installed (`pip install openai-whisper`)
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

- Python path and ffmpeg path are hardcoded at the top of each script — edit if your setup differs
- Whisper `base` model is used by default; change `load_model('base')` to `small`, `medium`, etc. for better accuracy at the cost of speed
- The Excel-matching scripts use `difflib.SequenceMatcher` for fuzzy matching
