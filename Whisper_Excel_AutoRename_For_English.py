# -*- coding: utf-8 -*-
# @description Whisper STT + Excel Matcher Auto Renamer (English)
# @author Claude
# @version 2.1

import os
import sys
import subprocess
import difflib
import tempfile

sys.path.insert(0, r"C:\Python311\Lib\site-packages")

from reaper_python import *

PYTHON_PATH = r"C:\Python311\python.exe"
FFMPEG_PATH = "ffmpeg"

_prog = {"proc": None, "file": None}

def _start_progress(total):
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
    tmp.write("STATUS:Initializing...\n")
    tmp.close()
    _prog["file"] = tmp.name
    scripts_dir = os.path.join(RPR_GetResourcePath(), "Scripts")
    prog_script = os.path.join(scripts_dir, "_Whisper_Progress.py")
    _prog["proc"] = subprocess.Popen([PYTHON_PATH, prog_script, _prog["file"]])

def _update(item=None, status=None):
    if not _prog["file"]:
        return
    try:
        with open(_prog["file"], 'a', encoding='utf-8') as f:
            if item is not None:
                f.write("ITEM:" + item + "\n")
            if status is not None:
                f.write("STATUS:" + status + "\n")
    except:
        pass

def _close_progress():
    if _prog["file"]:
        try:
            with open(_prog["file"], 'w', encoding='utf-8') as f:
                f.write("EXIT")
        except:
            pass
    if _prog["proc"]:
        try:
            _prog["proc"].wait(timeout=3)
        except:
            _prog["proc"].kill()
    if _prog["file"]:
        try:
            os.remove(_prog["file"])
        except:
            pass
    _prog["proc"] = None
    _prog["file"] = None

def extract_segment(file_path, start_offset, length):
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = tmp.name
    tmp.close()
    try:
        subprocess.check_output(
            [FFMPEG_PATH, "-y", "-ss", str(start_offset), "-t", str(length),
             "-i", file_path, tmp_path],
            stderr=subprocess.DEVNULL
        )
        return tmp_path
    except Exception as e:
        return None

def transcribe(file_path):
    script = (
        "import whisper, sys; "
        "sys.path.insert(0, r'C:\\Python311\\Lib\\site-packages'); "
        "model = whisper.load_model('small'); "
        "result = model.transcribe(r'" + file_path.replace("\\", "\\\\") + "', language='en'); "
        "print(result['text'].strip())"
    )
    try:
        result = subprocess.check_output(
            [PYTHON_PATH, "-c", script],
            stderr=subprocess.DEVNULL,
            env={**__import__('os').environ, "PYTHONIOENCODING": "utf-8"}
        )
        return result.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return ""

def read_excel(excel_path):
    script = (
        "import openpyxl, json, sys; "
        "sys.path.insert(0, r'C:\\Python311\\Lib\\site-packages'); "
        "wb = openpyxl.load_workbook(r'" + excel_path.replace("\\", "\\\\") + "', data_only=True); "
        "sheet = wb.active; "
        "rows = list(sheet.iter_rows(values_only=True)); "
        "header = [str(c).strip() if c else '' for c in rows[0]]; "
        "script_col = header.index('script') if 'script' in header else -1; "
        "name_col = header.index('file name') if 'file name' in header else -1; "
        "data = []; "
        "[data.append({'script': str(r[script_col]).strip(), 'name': str(r[name_col]).strip()}) "
        "for r in rows[1:] if script_col >= 0 and name_col >= 0 and r[script_col] and r[name_col]]; "
        "print(json.dumps(data, ensure_ascii=False))"
    )
    try:
        result = subprocess.check_output(
            [PYTHON_PATH, "-c", script],
            stderr=subprocess.DEVNULL
        )
        import json
        return json.loads(result.decode("utf-8", errors="ignore").strip())
    except Exception as e:
        return None

def calculate_similarity(str1, str2):
    if not str1 or not str2:
        return 0.0
    return difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def main():
    file_result = RPR_GetUserFileNameForRead("", "Select Excel File", "xlsx")
    excel_path = file_result[1] if len(file_result) > 1 else file_result[0]
    if not excel_path or not isinstance(excel_path, str):
        RPR_ShowConsoleMsg("No Excel file selected.\n")
        return

    item_count = RPR_CountSelectedMediaItems(0)
    if item_count == 0:
        RPR_ShowConsoleMsg("No media items selected.\n")
        return

    RPR_ShowConsoleMsg("--- Whisper + Excel Auto-Rename [English] (Processing " + str(item_count) + " items) ---\n")

    _start_progress(item_count)

    try:
        _update(status="Reading Excel...")
        RPR_ShowConsoleMsg("Reading Excel...\n")
        excel_data = read_excel(excel_path)
        if not excel_data:
            RPR_ShowConsoleMsg("Error: Could not read Excel. Check 'script' and 'file name' columns in row 1.\n")
            return
        RPR_ShowConsoleMsg("Excel loaded. " + str(len(excel_data)) + " entries found.\n")

        for i in range(item_count):
            item = RPR_GetSelectedMediaItem(0, i)
            take = RPR_GetActiveTake(item)
            if not take:
                continue

            source = RPR_GetMediaItemTake_Source(take)
            source_res = RPR_GetMediaSourceFileName(source, "", 512)
            file_path = source_res[1] if len(source_res) > 1 else source_res[0]

            if not file_path or not os.path.exists(file_path):
                RPR_ShowConsoleMsg("File not found: " + str(file_path) + "\n")
                continue

            start_offset = RPR_GetMediaItemTakeInfo_Value(take, "D_STARTOFFS")
            length = RPR_GetMediaItemInfo_Value(item, "D_LENGTH")

            fname = os.path.basename(file_path)
            RPR_ShowConsoleMsg("Transcribing: " + fname + " [" + str(round(start_offset, 2)) + "s ~ " + str(round(start_offset + length, 2)) + "s]\n")
            _update(
                item="[" + str(i + 1) + "/" + str(item_count) + "]  " + fname,
                status="Extracting segment..."
            )

            tmp_path = extract_segment(file_path, start_offset, length)
            if not tmp_path:
                RPR_ShowConsoleMsg("Failed to extract segment.\n")
                continue

            _update(status="Transcribing...")
            transcribed_text = transcribe(tmp_path)

            try:
                os.remove(tmp_path)
            except:
                pass

            if not transcribed_text:
                RPR_ShowConsoleMsg("No text detected.\n")
                _update(status="No text detected.")
                continue

            RPR_ShowConsoleMsg("STT Result: " + transcribed_text + "\n")
            _update(status="Matching...")

            best_name = None
            max_ratio = 0
            for entry in excel_data:
                ratio = calculate_similarity(transcribed_text, entry["script"])
                if ratio > max_ratio:
                    max_ratio = ratio
                    best_name = entry["name"]

            if max_ratio >= 0.8:
                RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", best_name, True)
                RPR_ShowConsoleMsg("[MATCH " + str(round(max_ratio * 100, 1)) + "%] -> " + best_name + "\n")
                _update(status="[MATCH " + str(round(max_ratio * 100, 1)) + "%]  ->  " + best_name)
            else:
                RPR_ShowConsoleMsg("[SKIP] Best match: " + str(round(max_ratio * 100, 1)) + "% (need 80%)\n")
                _update(status="[SKIP]  Best: " + str(round(max_ratio * 100, 1)) + "%")

        RPR_UpdateTimeline()
        RPR_ShowConsoleMsg("--- Process Completed ---\n")
        _update(status="Done!")

    finally:
        import time
        time.sleep(0.5)
        _close_progress()

if __name__ == "__main__":
    main()
