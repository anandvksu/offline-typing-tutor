import tkinter as tk
from tkinter import ttk, messagebox
import time

LESSONS = {
    "English - Home Row (Basic)": "asdf jkl; asdf jkl; dad sad fad lad ask all fall salad flask",
    "English - Top & Bottom Row": "qwerty uiop zxcv bnm the quick brown fox jumps over the lazy dog",
    "English - Official Paragraph": "The Deputy Collector Land Reforms court hears appeals regarding land mutation and boundary disputes in the sub-division.",
    "Hindi (Kruti Dev 010) - Home Row": "d s h f t y r k l ; d s h f t y r k l ; dkj dkj gkj lkj dgk",
    "Hindi (Kruti Dev 010) - Practice": "Hkwfe lq/kkj mi&lekgrkZ U;k;ky; esa nkf[ky&[kkfjt vihy okn dh lquokbZ dh tkrh gSA",
    "Hindi (Mangal / Unicode) - Practice": "भूमि सुधार उप-समाहर्ता न्यायालय में दाखिल-खारिज अपील वाद की सुनवाई की जाती है।"
}

class OfflineTypingTutor:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline Typing Tutor (English & Hindi - Kruti Dev / Mangal)")
        self.root.geometry("950x620")
        self.root.configure(bg="#f0f4f8")

        self.start_time = None
        self.timer_running = False
        self.time_left = 60
        self.selected_duration = 60

        self.setup_ui()
        self.load_lesson()

    def setup_ui(self):
        header = tk.Label(self.root, text="ऑफलाइन टाइपिंग ट्यूटर (English | Kruti Dev 010 | Mangal)", 
                          font=("Segoe UI", 16, "bold"), bg="#1a365d", fg="white", pady=10)
        header.pack(fill=tk.X)

        control_frame = tk.Frame(self.root, bg="#f0f4f8", pady=10)
        control_frame.pack(fill=tk.X, padx=20)

        tk.Label(control_frame, text="लेसन चुनें:", font=("Segoe UI", 11, "bold"), bg="#f0f4f8").pack(side=tk.LEFT, padx=5)
        self.lesson_var = tk.StringVar(value=list(LESSONS.keys())[0])
        self.lesson_combo = ttk.Combobox(control_frame, textvariable=self.lesson_var, values=list(LESSONS.keys()), width=38, state="readonly")
        self.lesson_combo.pack(side=tk.LEFT, padx=5)
        self.lesson_combo.bind("<<ComboboxSelected>>", lambda e: self.load_lesson())

        tk.Label(control_frame, text="समय (सेकंड):", font=("Segoe UI", 11, "bold"), bg="#f0f4f8").pack(side=tk.LEFT, padx=(20, 5))
        self.time_var = tk.StringVar(value="60")
        time_combo = ttk.Combobox(control_frame, textvariable=self.time_var, values=["60", "120", "300", "600"], width=8, state="readonly")
        time_combo.pack(side=tk.LEFT, padx=5)
        time_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_test())

        reset_btn = tk.Button(control_frame, text="रीसेट करें (Reset)", command=self.reset_test, 
                              bg="#2b6cb0", fg="white", font=("Segoe UI", 10, "bold"), padx=12, pady=3)
        reset_btn.pack(side=tk.RIGHT, padx=5)

        stats_frame = tk.Frame(self.root, bg="#e2e8f0", pady=8, bd=1, relief=tk.SOLID)
        stats_frame.pack(fill=tk.X, padx=20, pady=5)

        self.timer_label = tk.Label(stats_frame, text="समय: 60s", font=("Segoe UI", 13, "bold"), bg="#e2e8f0", fg="#c53030")
        self.timer_label.pack(side=tk.LEFT, expand=True)

        self.wpm_label = tk.Label(stats_frame, text="गति (WPM): 0", font=("Segoe UI", 13, "bold"), bg="#e2e8f0", fg="#2f855a")
        self.wpm_label.pack(side=tk.LEFT, expand=True)

        self.acc_label = tk.Label(stats_frame, text="सटीकता (Accuracy): 100%", font=("Segoe UI", 13, "bold"), bg="#e2e8f0", fg="#2b6cb0")
        self.acc_label.pack(side=tk.LEFT, expand=True)

        tk.Label(self.root, text="नीचे दिए गए मैटर को देखकर टाइप करें:", font=("Segoe UI", 10, "bold"), bg="#f0f4f8").pack(anchor="w", padx=20, pady=(10, 2))
        self.target_text = tk.Text(self.root, height=5, font=("Segoe UI", 16), wrap=tk.WORD, bg="#ffffff", fg="#1a202c", padx=10, pady=10, bd=2, relief=tk.GROOVE)
        self.target_text.pack(fill=tk.X, padx=20)
        self.target_text.config(state=tk.DISABLED)

        tk.Label(self.root, text="यहाँ टाइप करना शुरू करें (पहला अक्षर दबाते ही टाइमर चालू हो जाएगा):", font=("Segoe UI", 10, "bold"), bg="#f0f4f8").pack(anchor="w", padx=20, pady=(12, 2))
        self.input_text = tk.Text(self.root, height=5, font=("Segoe UI", 16), wrap=tk.WORD, bg="#fffaf0", fg="#000000", padx=10, pady=10, bd=2, relief=tk.GROOVE)
        self.input_text.pack(fill=tk.X, padx=20)
        self.input_text.bind("<KeyRelease>", self.on_key_release)

        custom_frame = tk.Frame(self.root, bg="#f0f4f8", pady=10)
        custom_frame.pack(fill=tk.X, padx=20)
        tk.Label(custom_frame, text="कस्टम पैराग्राफ पेस्ट करें:", font=("Segoe UI", 10), bg="#f0f4f8").pack(side=tk.LEFT)
        self.custom_entry = tk.Entry(custom_frame, width=55, font=("Segoe UI", 10))
        self.custom_entry.pack(side=tk.LEFT, padx=8)
        tk.Button(custom_frame, text="कस्टम मैटर लोड करें", command=self.load_custom_text, bg="#38a169", fg="white", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)

    def load_lesson(self):
        lesson_name = self.lesson_var.get()
        content = LESSONS[lesson_name]

        if "Kruti Dev" in lesson_name:
            font_style = ("Kruti Dev 010", 20)
        elif "Mangal" in lesson_name:
            font_style = ("Nirmala UI", 16)
        else:
            font_style = ("Consolas", 16)

        self.target_text.config(state=tk.NORMAL, font=font_style)
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert("1.0", content)
        self.target_text.config(state=tk.DISABLED)

        self.input_text.config(font=font_style)
        self.reset_test()

    def load_custom_text(self):
        custom = self.custom_entry.get().strip()
        if not custom:
            return
        self.target_text.config(state=tk.NORMAL, font=("Nirmala UI", 16))
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert("1.0", custom)
        self.target_text.config(state=tk.DISABLED)
        self.input_text.config(font=("Nirmala UI", 16))
        self.reset_test()

    def reset_test(self):
        self.timer_running = False
        self.start_time = None
        self.selected_duration = int(self.time_var.get())
        self.time_left = self.selected_duration
        self.timer_label.config(text=f"समय: {self.time_left}s")
        self.wpm_label.config(text="गति (WPM): 0")
        self.acc_label.config(text="सटीकता (Accuracy): 100%")
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete("1.0", tk.END)
        self.input_text.focus()

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"समय: {self.time_left}s")
            self.calculate_stats()
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.finish_test()

    def on_key_release(self, event):
        if not self.timer_running and self.time_left > 0:
            typed = self.input_text.get("1.0", "end-1c")
            if len(typed) > 0:
                self.timer_running = True
                self.start_time = time.time()
                self.update_timer()

        self.calculate_stats()

        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.
