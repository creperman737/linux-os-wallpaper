import os
import subprocess
import sys
import time

from Xlib import X, display
from Xlib.error import XError

VIDEO_PATH = sys.argv[1] if len(sys.argv) > 1 else "/home/cripos/Desktop/m/v/video.mp4"

if not os.path.exists(VIDEO_PATH):
    print(f"Xatolik: {VIDEO_PATH} fayli topilmadi!")
    raise SystemExit(1)

cmd = [
    "xwinwrap",
    "-b",
    "-fdt",
    "-fs",
    "-st",
    "-sp",
    "-ni",
    "-nf",
    "--",
    "mpv",
    "-wid",
    "WID",
    "--loop-file=inf",
    "--no-audio",
    "--no-osc",
    "--no-osd-bar",
    "--quiet",
    VIDEO_PATH,
]


def lower_wallpaper_window():
    x_display = display.Display()
    root = x_display.screen().root
    desktop_atom = x_display.intern_atom("_NET_WM_WINDOW_TYPE_DESKTOP")
    window_type_atom = x_display.intern_atom("_NET_WM_WINDOW_TYPE")

    for _ in range(20):
        try:
            for window in root.query_tree().children:
                window_types = window.get_full_property(window_type_atom, X.AnyPropertyType)
                if window_types and desktop_atom in window_types.value and window.get_wm_class() is None:
                    window.configure(stack_mode=X.Below)
                    x_display.sync()
                    return
        except XError:
            pass
        time.sleep(0.1)

    x_display.close()


try:
    subprocess.Popen(cmd)
    lower_wallpaper_window()
except FileNotFoundError as error:
    print(f"Xatolik: kerakli dastur topilmadi: {error.filename}")
    raise SystemExit(1)

print("🟢 Live Wallpaper muvaffaqiyatli ishga tushdi!")