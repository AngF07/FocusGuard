
import tkinter as tk
import csv
from datetime import datetime
import os

LOG_FILE = "study_log.csv"

# -------------------- THEMES --------------------
LIGHT_THEME = {
    "bg": "#f1f5f9",
    "card": "#ffffff",
    "primary": "#4f46e5",
    "secondary": "#14b8a6",
    "accent": "#22c55e",
    "danger": "#ef4444",
    "info": "#0ea5e9",
    "text": "#0f172a",
    "subtext": "#475569"
}

DARK_THEME = {
    "bg": "#020617",
    "card": "#020617",
    "primary": "#818cf8",
    "secondary": "#2dd4bf",
    "accent": "#4ade80",
    "danger": "#f87171",
    "info": "#38bdf8",
    "text": "#e5e7eb",
    "subtext": "#94a3b8"
}

current_theme = LIGHT_THEME

# -------------------- MAIN WINDOW --------------------
root = tk.Tk()
root.title("FocusGuard")
root.geometry("520x480")
root.resizable(False, False)

# -------------------- VARIABLES --------------------
study_seconds = 0
active_seconds = 0
running = False

# -------------------- LOGIC --------------------
def update_timer():
    global study_seconds, active_seconds
    active_seconds += 1

    if running:
        study_seconds += 1
        h = study_seconds // 3600
        m = (study_seconds % 3600) // 60
        s = study_seconds % 60
        timer_label.config(text=f"{h:02}:{m:02}:{s:02}")

    root.after(1000, update_timer)


def start_study():
    global running
    running = True


def stop_study():
    global running
    running = False


def reset_timer():
    global study_seconds, running
    running = False
    study_seconds = 0
    timer_label.config(text="00:00:00")


def calculate_focus():
    if active_seconds == 0:
        return 0
    return (study_seconds / active_seconds) * 100


def save_session():
    focus = round(calculate_focus(), 2)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d"),
            study_seconds,
            focus
        ])


def open_analytics():
    win = tk.Toplevel(root)
    win.title("Analytics")
    win.geometry("460x300")
    win.configure(bg=current_theme["bg"])

    tk.Label(
        win,
        text="📊 Analytics Overview",
        font=("Segoe UI", 18, "bold"),
        bg=current_theme["bg"],
        fg=current_theme["primary"]
    ).pack(pady=15)

    total = 0
    focuses = []
    best_day = "N/A"
    best_score = 0

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for row in csv.reader(f):
                if len(row) != 3:
                    continue
                date, secs, score = row
                secs = int(secs)
                score = float(score)
                total += secs
                focuses.append(score)
                if score > best_score:
                    best_score = score
                    best_day = date

    hrs = total // 3600
    mins = (total % 3600) // 60
    avg = round(sum(focuses) / len(focuses), 1) if focuses else 0

    stats = [
        f"⏱ Total Study Time: {hrs}h {mins}m",
        f"🎯 Average Focus Score: {avg}%",
        f"🏆 Best Day: {best_day} ({best_score}%)"
    ]

    for stat in stats:
        tk.Label(
            win,
            text=stat,
            font=("Segoe UI", 12),
            bg=current_theme["bg"],
            fg=current_theme["text"]
        ).pack(pady=8)

# -------------------- DARK MODE TOGGLE --------------------
def toggle_theme():
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    apply_theme()


def apply_theme():
    root.configure(bg=current_theme["bg"])
    container.configure(bg=current_theme["bg"])
    card.configure(bg=current_theme["card"])

    title_label.config(bg=current_theme["bg"], fg=current_theme["primary"])
    subtitle_label.config(bg=current_theme["bg"], fg=current_theme["subtext"])
    timer_label.config(bg=current_theme["card"], fg=current_theme["primary"])
    focus_label.config(bg=current_theme["card"], fg=current_theme["subtext"])

    for btn, color in button_map.items():
        btn.config(bg=color, fg="white", activebackground=color)

# -------------------- UI --------------------
container = tk.Frame(root, bg=current_theme["bg"])
container.pack(fill="both", expand=True, padx=20, pady=20)

title_label = tk.Label(
    container,
    text="FocusGuard",
    font=("Segoe UI", 24, "bold"),
    bg=current_theme["bg"],
    fg=current_theme["primary"]
)
title_label.pack()

subtitle_label = tk.Label(
    container,
    text="Build focus. Measure progress.",
    font=("Segoe UI", 11),
    bg=current_theme["bg"],
    fg=current_theme["subtext"]
)
subtitle_label.pack(pady=(0, 20))

card = tk.Frame(container, bg=current_theme["card"])
card.pack(fill="both", expand=True, padx=10, pady=10)

timer_label = tk.Label(
    card,
    text="00:00:00",
    font=("Segoe UI", 36, "bold"),
    bg=current_theme["card"],
    fg=current_theme["primary"]
)
timer_label.pack(pady=20)

focus_label = tk.Label(
    card,
    text="Today's Focus Score: 0%",
    font=("Segoe UI", 12),
    bg=current_theme["card"],
    fg=current_theme["subtext"]
)
focus_label.pack(pady=5)

btn_row = tk.Frame(card, bg=current_theme["card"])
btn_row.pack(pady=15)

start_btn = tk.Button(btn_row, text="Start", width=10, command=start_study)
stop_btn = tk.Button(btn_row, text="Stop", width=10, command=stop_study)
reset_btn = tk.Button(btn_row, text="Reset", width=10, command=reset_timer)

start_btn.grid(row=0, column=0, padx=6)
stop_btn.grid(row=0, column=1, padx=6)
reset_btn.grid(row=0, column=2, padx=6)

save_btn = tk.Button(card, text="Save Session", width=30, command=save_session)
analytics_btn = tk.Button(card, text="View Analytics", width=30, command=open_analytics)
theme_btn = tk.Button(card, text="Toggle Dark Mode", width=30, command=toggle_theme)

save_btn.pack(pady=6)
analytics_btn.pack(pady=6)
theme_btn.pack(pady=(6, 20))

button_map = {
    start_btn: current_theme["accent"],
    stop_btn: current_theme["secondary"],
    reset_btn: current_theme["danger"],
    save_btn: current_theme["primary"],
    analytics_btn: current_theme["info"],
    theme_btn: "#64748b"
}

apply_theme()

# -------------------- LIVE UPDATE --------------------
def update_focus_label():
    score = calculate_focus()
    focus_label.config(text=f"Today's Focus Score: {score:.1f}%")
    root.after(3000, update_focus_label)

update_focus_label()
update_timer()

root.mainloop()


