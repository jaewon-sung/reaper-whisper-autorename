# -*- coding: utf-8 -*-
import sys
import tkinter as tk
import threading
import time

def poll(filepath, var_item, var_status, root):
    while True:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if content == "EXIT":
                root.after(500, root.destroy)
                break
            lines = [l for l in content.split('\n') if l.strip()]
            for line in reversed(lines):
                if line.startswith("ITEM:"):
                    var_item.set(line[5:])
                    break
            for line in reversed(lines):
                if line.startswith("STATUS:"):
                    var_status.set(line[7:])
                    break
        except:
            pass
        time.sleep(0.2)

def main():
    if len(sys.argv) < 2:
        return
    filepath = sys.argv[1]

    root = tk.Tk()
    root.title("Whisper STT")
    root.attributes('-topmost', True)
    root.resizable(False, False)

    w, h = 460, 170
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text="Whisper STT Auto-Rename",
             font=("Segoe UI", 13, "bold"), bg="#f0f0f0").pack(pady=(22, 6))

    var_item = tk.StringVar(value="")
    var_status = tk.StringVar(value="Initializing...")

    tk.Label(root, textvariable=var_item,
             font=("Segoe UI", 9), fg="#888888", bg="#f0f0f0").pack()
    tk.Label(root, textvariable=var_status,
             font=("Segoe UI", 11), fg="#1a7abf", bg="#f0f0f0").pack(pady=10)

    t = threading.Thread(target=poll,
                         args=(filepath, var_item, var_status, root), daemon=True)
    t.start()
    root.mainloop()

if __name__ == "__main__":
    main()
