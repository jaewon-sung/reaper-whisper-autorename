# -*- coding: utf-8 -*-
# @description Whisper STT Auto Renamer
# @author Claude
# @version 2.0

import os
import sys
import subprocess
import json
import shutil

from reaper_python import *

def _find_python():
    for candidate in ("python", "python3"):
        path = shutil.which(candidate)
        if path:
            return path
    return "python"

PYTHON_PATH = _find_python()

def transcribe(file_path):
    script = (
        "import site, sys; sys.path.extend(site.getsitepackages()); "
        "import whisper; "
        "model = whisper.load_model('base'); "
        "result = model.transcribe(r'" + file_path.replace("\\", "\\\\") + "'); "
        "print(result['text'].strip())"
    )
    try:
        result = subprocess.check_output(
            [PYTHON_PATH, "-c", script],
            stderr=subprocess.DEVNULL
        )
        return result.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return ""

def main():
    item_count = RPR_CountSelectedMediaItems(0)
    if item_count == 0:
        RPR_ShowConsoleMsg("No media items selected.\n")
        return

    RPR_ShowConsoleMsg("--- Whisper STT Auto-Rename (Processing " + str(item_count) + " items) ---\n")

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

        RPR_ShowConsoleMsg("Transcribing: " + os.path.basename(file_path) + "...\n")

        transcribed_text = transcribe(file_path)

        if not transcribed_text:
            RPR_ShowConsoleMsg("No text detected: " + os.path.basename(file_path) + "\n")
            continue

        RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", transcribed_text, True)
        RPR_ShowConsoleMsg("[DONE] " + os.path.basename(file_path) + " -> " + transcribed_text + "\n")

    RPR_UpdateTimeline()
    RPR_ShowConsoleMsg("--- Process Completed ---\n")

if __name__ == "__main__":
    main()
