import json
import os
import random
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


APP_DIR = get_app_dir()
LESSONS_FILE = os.path.join(APP_DIR, "typing_lessons.json")
STATS_FILE = os.path.join(APP_DIR, "typing_stats.json")

DEFAULT_LESSONS = {
    "English": {
        "Lesson 1 - Home Row (asdf jkl;)": "asdf jkl; asdf jkl; ff jj dd kk ss ll aa ;; ask lad fall flask salad dad sad fad",
        "Lesson 2 - Top & Bottom Row": "qwerty uiop zxcv bnm the quick brown fox jumps over the lazy dog pack box with five dozen liquor jugs",
        "Lesson 3 - Official & Speed": "The Deputy Collector Land Reforms court hears appeals regarding land mutation and boundary disputes in the sub-division.",
    },
    "Kruti Dev 010": {
        "Lesson 1 - Home Row (d s h f t y r k l ;)": "d s h f t y r k l ; d s h f t y r k l ; dkj dkj gkj lkj dgk fdj fdj fdl",
        "Lesson 2 - Matra & Conjuncts": "fdrkuh] fdrkuh] vf/kdkjh] dk;kZy;] vfHkys[k] vkns'k] lwpuk] izfrosnu] Kku] {ks=] Jheku",
        "Lesson 3 - Court & Office Matter": "Hkwfe lq/kkj mi&lekgrkZ U;k;ky; esa nkf[ky&[kkfjt vihy okn dh lquokbZ dh tkrh gSA vfHkys[kksa dh tkap dj fu;ekuqlkj vkns'k ikfjr fd;k tkrk gSA",
    },
    "Mangal": {
        "Lesson 1 - Basic Words": "कमल नयन घर चल अब कल फल जल मन धन कर भर हर पल जन धन वन",
        "Lesson 2 - Office & Matra Words": "अधिकारी कार्यालय अभिलेख आदेश आवेदन प्रतिवेदन सुनवाई प्रमाण पत्र संशोधन पंजीकरण",
        "Lesson 3 - Official Paragraph": "भूमि सुधार उप-समाहर्ता न्यायालय में प्राप्त आवेदनों का अभिलेखीय सत्यापन समयबद्ध रूप से किया जाता है।",
    },
}

GAME_WORDS = {
    "English": [
        "type", "fast", "focus", "skill", "speed", "accuracy", "practice", "keyboard",
        "finger", "lesson", "record", "office", "court", "order", "notice", "window",
    ],
    "Kruti Dev 010": [
        "dkj", "gkj", "lkj", "dgk", "vkns'k", "lwpuk", "dk;kZy;", "vf/kdkjh",
        "vfHkys[k", "izfrosnu", "lquokbZ", "izek.k", "vihy", "okn", "Hkwfe", "U;k;ky;",
    ],
    "Mangal": [
        "कमल", "नयन", "आदेश", "सूचना", "कार्यालय", "अधिकारी", "अभिलेख", "प्रतिवेदन",
        "सुनवाई", "प्रमाण", "अपील", "वाद", "भूमि", "न्यायालय", "आवेदन", "सत्यापन",
    ],
}

KEYBOARD_ROWS = [
    [
        ("`", "~", "Left Pinky", "#dbeafe"),
        ("1", "!", "Left Pinky", "#dbeafe"),
        ("2", "@", "Left Ring", "#fee2e2"),
        ("3", "#", "Left Middle", "#dcfce7"),
        ("4", "$", "Left Index", "#f3e8ff"),
        ("5", "%", "Left Index", "#f3e8ff"),
        ("6", "^", "Right Index", "#ffedd5"),
        ("7", "&", "Right Index", "#ffedd5"),
        ("8", "*", "Right Middle", "#dcfce7"),
        ("9", "(", "Right Ring", "#fee2e2"),
        ("0", ")", "Right Pinky", "#dbeafe"),
        ("-", "_", "Right Pinky", "#dbeafe"),
        ("=", "+", "Right Pinky", "#dbeafe"),
    ],
    [
        ("q", "Q", "Left Pinky", "#dbeafe"),
        ("w", "W", "Left Ring", "#fee2e2"),
        ("e", "E", "Left Middle", "#dcfce7"),
        ("r", "R", "Left Index", "#f3e8ff"),
        ("t", "T", "Left Index", "#f3e8ff"),
        ("y", "Y", "Right Index", "#ffedd5"),
        ("u", "U", "Right Index", "#ffedd5"),
        ("i", "I", "Right Middle", "#dcfce7"),
        ("o", "O", "Right Ring", "#fee2e2"),
        ("p", "P", "Right Pinky", "#dbeafe"),
        ("[", "{", "Right Pinky", "#dbeafe"),
        ("]", "}", "Right Pinky", "#dbeafe"),
        ("\\", "|", "Right Pinky", "#dbeafe"),
    ],
    [
        ("a", "A", "Left Pinky", "#dbeafe"),
        ("s", "S", "Left Ring", "#fee2e2"),
        ("d", "D", "Left Middle", "#dcfce7"),
        ("f", "F", "Left Index", "#f3e8ff"),
        ("g", "G", "Left Index", "#f3e8ff"),
        ("h", "H", "Right Index", "#ffedd5"),
        ("j", "J", "Right Index", "#ffedd5"),
        ("k", "K", "Right Middle", "#dcfce7"),
        ("l", "L", "Right Ring", "#fee2e2"),
        (";", ":", "Right Pinky", "#dbeafe"),
        ("'", '"', "Right Pinky", "#dbeafe"),
    ],
    [
        ("z", "Z", "Left Pinky", "#dbeafe"),
        ("x", "X", "Left Ring", "#fee2e2"),
        ("c", "C", "Left Middle", "#dcfce7"),
        ("v", "V", "Left Index", "#f3e8ff"),
        ("b", "B", "Left Index", "#f3e8ff"),
        ("n", "N", "Right Index", "#ffedd5"),
        ("m", "M", "Right Index", "#ffedd5"),
        (",", "<", "Right Middle", "#dcfce7"),
        (".", ">", "Right Ring", "#fee2e2"),
        ("/", "?", "Right Pinky", "#dbeafe"),
    ],
]

FINGER_HINDI_NAMES = {
    "Left Pinky": "बायाँ हाथ — छोटी उंगली (Left Pinky)",
    "Left Ring": "बायाँ हाथ — रिंग फिंगर (Left Ring)",
    "Left Middle": "बायाँ हाथ — मध्यमा / बीच की उंगली (Left Middle)",
    "Left Index": "बायाँ हाथ — तर्जनी / इंडेक्स फिंगर (Left Index)",
    "Right Index": "दायाँ हाथ — तर्जनी / इंडेक्स फिंगर (Right Index)",
    "Right Middle": "दायाँ हाथ — मध्यमा / बीच की उंगली (Right Middle)",
    "Right Ring": "दायाँ हाथ — रिंग फिंगर (Right Ring)",
    "Right Pinky": "दायाँ हाथ — छोटी उंगली (Right Pinky)",
    "Thumb": "अंगूठा — Spacebar (Thumb)",
}

KRUTIDEV_KEY_MAP = {
    "`": ("`", "Left Pinky", "छोटी ई मात्रा (ि) / चिह्न"),
    "~": ("~", "Left Pinky", "रेफ / चिह्न"),
    "1": ("1", "Left Pinky", "१"),
    "!": ("!", "Left Pinky", "।"),
    "2": ("2", "Left Ring", "२"),
    "@": ("@", "Left Ring", "/"),
    "3": ("3", "Left Middle", "३"),
    "#": ("#", "Left Middle", "क्ष"),
    "4": ("4", "Left Index", "४"),
    "$": ("$", "Left Index", "द्ध"),
    "5": ("5", "Left Index", "५"),
    "%": ("%", "Left Index", "त्र"),
    "6": ("6", "Right Index", "६"),
    "^": ("^", "Right Index", "ज्ञ"),
    "7": ("7", "Right Index", "७"),
    "&": ("&", "Right Index", "श्र"),
    "8": ("8", "Right Middle", "८"),
    "*": ("*", "Right Middle", "रु"),
    "9": ("9", "Right Ring", "९"),
    "(": ("(", "Right Ring", "ऋ"),
    "0": ("0", "Right Pinky", "०"),
    ")": (")", "Right Pinky", "—"),
    "=": ("=", "Right Pinky", "ु"),
    "+": ("+", "Right Pinky", "ू"),
    "q": ("q", "Left Pinky", "ु"),
    "Q": ("Q", "Left Pinky", "फ"),
    "w": ("w", "Left Ring", "ू"),
    "W": ("W", "Left Ring", "ॅ"),
    "e": ("e", "Left Middle", "म"),
    "E": ("E", "Left Middle", "म्"),
    "r": ("r", "Left Index", "त"),
    "R": ("R", "Left Index", "त्"),
    "t": ("t", "Left Index", "ज"),
    "T": ("T", "Left Index", "ज्"),
    "y": ("y", "Right Index", "ल"),
    "Y": ("Y", "Right Index", "ल्"),
    "u": ("u", "Right Index", "न"),
    "U": ("U", "Right Index", "न्"),
    "i": ("i", "Right Middle", "प"),
    "I": ("I", "Right Middle", "प्"),
    "o": ("o", "Right Ring", "व"),
    "O": ("O", "Right Ring", "व्"),
    "p": ("p", "Right Pinky", "च"),
    "P": ("P", "Right Pinky", "च्"),
    "[": ("[", "Right Pinky", "ख"),
    "{": ("{", "Right Pinky", "ख्"),
    "]": ("]", "Right Pinky", "़"),
    "}": ("}", "Right Pinky", "ह्र"),
    "\\": ("\\", "Right Pinky", "़ / हलंत"),
    "|": ("|", "Right Pinky", "द्व"),
    "a": ("a", "Left Pinky", "ं"),
    "A": ("A", "Left Pinky", "ँ"),
    "s": ("s", "Left Ring", "े"),
    "S": ("S", "Left Ring", "ै"),
    "d": ("d", "Left Middle", "क"),
    "D": ("D", "Left Middle", "क्"),
    "f": ("f", "Left Index", "ि"),
    "F": ("F", "Left Index", "फ्"),
    "g": ("g", "Left Index", "ह"),
    "G": ("G", "Left Index", "ह्"),
    "h": ("h", "Right Index", "ी"),
    "H": ("H", "Right Index", "ीं"),
    "j": ("j", "Right Index", "र"),
    "J": ("J", "Right Index", "्र"),
    "k": ("k", "Right Middle", "ा"),
    "K": ("K", "Right Middle", "ा"),
    "l": ("l", "Right Ring", "स"),
    "L": ("L", "Right Ring", "स्"),
    ";": (";", "Right Pinky", "य"),
    ":": (":", "Right Pinky", "य्"),
    "'": ("'", "Right Pinky", "ु"),
    '"': ('"', "Right Pinky", "ू"),
    "z": ("z", "Left Pinky", "र्"),
    "Z": ("Z", "Left Pinky", "र्"),
    "x": ("x", "Left Ring", "ग"),
    "X": ("X", "Left Ring", "ग्"),
    "c": ("c", "Left Middle", "ब"),
    "C": ("C", "Left Middle", "ब्"),
    "v": ("v", "Left Index", "अ"),
    "V": ("V", "Left Index", "अ"),
    "b": ("b", "Left Index", "इ"),
    "B": ("B", "Left Index", "ई"),
    "n": ("n", "Right Index", "द"),
    "N": ("N", "Right Index", "द्"),
    "m": ("m", "Right Index", "उ"),
    "M": ("M", "Right Index", "ऊ"),
    ",": (",", "Right Middle", "ए"),
    "<": ("<", "Right Middle", "ऐ"),
    ".": (".", "Right Ring", "ण"),
    ">": (">", "Right Ring", "ण्"),
    "/": ("/", "Right Pinky", "ध"),
    "?": ("?", "Right Pinky", "ध्"),
}


def load_json_file(path, default_factory):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    data = default_factory()
    save_json_file(path, data)
    return data


def save_json_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def default_lessons():
    return {k: dict(v) for k, v in DEFAULT_LESSONS.items()}


def default_stats():
    return {
        "English": {},
        "Kruti Dev 010": {},
        "Mangal": {},
    }


def format_mm_ss(seconds):
    seconds = max(int(seconds), 0)
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"


class OfflineTypingTutor:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline Typing Tutor — English | Kruti Dev 010 | Mangal")
        self.root.geometry("1160x840")
        self.root.configure(bg="#eef2f6")

        self.lessons_data = load_json_file(LESSONS_FILE, default_lessons)
        for script in ["English", "Kruti Dev 010", "Mangal"]:
            if script not in self.lessons_data or not self.lessons_data[script]:
                self.lessons_data[script] = dict(DEFAULT_LESSONS[script])

        self.stats_data = load_json_file(STATS_FILE, default_stats)
        for script in ["English", "Kruti Dev 010", "Mangal"]:
            self.stats_data.setdefault(script, {})

        self.start_time = None
        self.timer_running = False
        self.time_left = 60
        self.selected_duration = 60
        self.key_buttons = {}
        self.space_btn = None
        self.left_hand_dots = {}
        self.right_hand_dots = {}
        self.last_wrong_char = None
        self.strict_errors_count = 0
        self.counted_error_positions = set()

        self.setup_ui()
        self.refresh_lesson_dropdown(select_first=True)
        self.load_selected_lesson()

    def get_script_font(self, script, size=18):
        if script == "Kruti Dev 010":
            return ("Kruti Dev 010", size + 4)
        if script == "Mangal":
            return ("Nirmala UI", size)
        return ("Consolas", size)

    def setup_ui(self):
        # शीर्ष पट्टी
        header = tk.Frame(self.root, bg="#1e3a5f", pady=8, padx=14)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="ऑफलाइन टाइपिंग ट्यूटर (English | Kruti Dev 010 | Mangal)",
            font=("Segoe UI", 15, "bold"),
            bg="#1e3a5f",
            fg="white",
        ).pack(side=tk.LEFT)

        tk.Button(
            header,
            text="गेम खेलें (Typing Game)",
            command=self.open_game_window,
            bg="#d97706",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=3,
        ).pack(side=tk.RIGHT, padx=(6, 0))

        tk.Button(
            header,
            text="कमज़ोर कीज़ प्रैक्टिस",
            command=self.practice_weak_keys,
            bg="#7c3aed",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=3,
        ).pack(side=tk.RIGHT, padx=(6, 0))

        tk.Button(
            header,
            text="लेसन मैनेज करें",
            command=self.open_lesson_manager,
            bg="#059669",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=3,
        ).pack(side=tk.RIGHT)

        # कंट्रोल बार (साफ़ और व्यवस्थित)
        ctrl = tk.Frame(self.root, bg="#eef2f6", pady=6, padx=14)
        ctrl.pack(fill=tk.X)

        tk.Label(ctrl, text="भाषा/स्क्रिप्ट:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.script_var = tk.StringVar(value="English")
        self.script_combo = ttk.Combobox(
            ctrl,
            textvariable=self.script_var,
            values=["English", "Kruti Dev 010", "Mangal"],
            width=14,
            state="readonly",
        )
        self.script_combo.pack(side=tk.LEFT, padx=(4, 10))
        self.script_combo.bind("<<ComboboxSelected>>", self.on_script_change)

        tk.Label(ctrl, text="लेसन:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.lesson_var = tk.StringVar()
        self.lesson_combo = ttk.Combobox(ctrl, textvariable=self.lesson_var, width=30, state="readonly")
        self.lesson_combo.pack(side=tk.LEFT, padx=(4, 10))
        self.lesson_combo.bind("<<ComboboxSelected>>", lambda e: self.load_selected_lesson())

        tk.Label(ctrl, text="समय:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.time_var = tk.StringVar(value="1 Min")
        self.time_combo = ttk.Combobox(
            ctrl,
            textvariable=self.time_var,
            values=["1 Min", "2 Min", "5 Min", "10 Min"],
            width=8,
            state="readonly",
        )
        self.time_combo.pack(side=tk.LEFT, padx=(4, 10))
        self.time_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_test())

        tk.Label(ctrl, text="मोड:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.mode_var = tk.StringVar(value="गलत पर रुकें")
        self.mode_combo = ttk.Combobox(
            ctrl,
            textvariable=self.mode_var,
            values=["गलत पर रुकें", "आगे बढ़ें"],
            width=14,
            state="readonly",
        )
        self.mode_combo.pack(side=tk.LEFT, padx=(4, 10))
        self.mode_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_test())

        self.disable_backspace_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            ctrl,
            text="Backspace बंद",
            variable=self.disable_backspace_var,
            bg="#eef2f6",
            font=("Segoe UI", 9),
        ).pack(side=tk.LEFT, padx=4)

        self.sound_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            ctrl,
            text="बीप",
            variable=self.sound_var,
            bg="#eef2f6",
            font=("Segoe UI", 9),
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            ctrl,
            text="रीसेट",
            command=self.reset_test,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=2,
        ).pack(side=tk.RIGHT)

        # स्कोर पट्टी (ऑरेंज/स्लेट प्रोफेशनल बार)
        stats_bar = tk.Frame(self.root, bg="#ea580c", pady=6, padx=10)
        stats_bar.pack(fill=tk.X, padx=14, pady=(0, 6))

        self.timer_label = tk.Label(
            stats_bar, text="01:00 Min.", font=("Segoe UI", 12, "bold"), bg="#ea580c", fg="white"
        )
        self.timer_label.pack(side=tk.LEFT, expand=True)

        self.signs_label = tk.Label(
            stats_bar, text="00 Signs", font=("Segoe UI", 12, "bold"), bg="#ea580c", fg="white"
        )
        self.signs_label.pack(side=tk.LEFT, expand=True)

        self.wpm_label = tk.Label(
            stats_bar, text="00 WPM (Net)", font=("Segoe UI", 12, "bold"), bg="#ea580c", fg="white"
        )
        self.wpm_label.pack(side=tk.LEFT, expand=True)

        self.err_label = tk.Label(
            stats_bar, text="00 Errors", font=("Segoe UI", 12, "bold"), bg="#ea580c", fg="white"
        )
        self.err_label.pack(side=tk.LEFT, expand=True)

        self.acc_label = tk.Label(
            stats_bar, text="100.0% Acc.", font=("Segoe UI", 12, "bold"), bg="#ea580c", fg="white"
        )
        self.acc_label.pack(side=tk.LEFT, expand=True)

        # फिंगर गाइड व अलर्ट लाइन
        guide_bar = tk.Frame(self.root, bg="#ffffff", pady=6, padx=12, bd=1, relief=tk.SOLID)
        guide_bar.pack(fill=tk.X, padx=14, pady=(0, 6))

        self.finger_label = tk.Label(
            guide_bar,
            text="उंगली गाइड: —",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#1e293b",
        )
        self.finger_label.pack(side=tk.LEFT)

        self.alert_label = tk.Label(
            guide_bar,
            text="पहला अक्षर दबाते ही समय शुरू होगा",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#2563eb",
        )
        self.alert_label.pack(side=tk.RIGHT)

        # बड़ा टाइपिंग मैटर बॉक्स (टारगेट)
        self.target_text = tk.Text(
            self.root,
            height=5,
            font=("Consolas", 18),
            wrap=tk.WORD,
            bg="#f8fafc",
            fg="#0f172a",
            padx=12,
            pady=10,
            bd=2,
            relief=tk.GROOVE,
        )
        self.target_text.pack(fill=tk.X, padx=14, pady=(0, 6))
        self.target_text.tag_config("correct", foreground="#15803d", background="#dcfce7")
        self.target_text.tag_config("wrong", foreground="#b91c1c", background="#fee2e2")
        self.target_text.tag_config("current", foreground="#000000", background="#93c5fd", underline=True)
        self.target_text.config(state=tk.DISABLED)

        # यूज़र इनपुट टाइपिंग बॉक्स
        self.input_text = tk.Text(
            self.root,
            height=3,
            font=("Consolas", 17),
            wrap=tk.WORD,
            bg="#ffffff",
            fg="#0f172a",
            padx=12,
            pady=8,
            bd=2,
            relief=tk.GROOVE,
        )
        self.input_text.pack(fill=tk.X, padx=14, pady=(0, 8))
        self.input_text.bind("<KeyPress>", self.on_key_press)
        self.input_text.bind("<KeyRelease>", self.on_key_release)

        # निचला पैनल: बायाँ हाथ + कीबोर्ड + दायाँ हाथ
        bottom_panel = tk.Frame(self.root, bg="#eef2f6", padx=14, pady=4)
        bottom_panel.pack(fill=tk.BOTH, expand=True)

        self.left_hand_dots = self.build_hand_panel(bottom_panel, "बायाँ हाथ (Left Hand)", side=tk.LEFT)
        kb_center = tk.Frame(bottom_panel, bg="#eef2f6", padx=8)
        kb_center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.build_onscreen_keyboard(kb_center)
        self.right_hand_dots = self.build_hand_panel(bottom_panel, "दायाँ हाथ (Right Hand)", side=tk.RIGHT)

    def build_hand_panel(self, parent, title, side):
        frame = tk.LabelFrame(
            parent,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#1e3a5f",
            padx=8,
            pady=6,
            width=165,
        )
        frame.pack(side=side, fill=tk.Y)
        frame.pack_propagate(False)

        prefix = "Left" if side == tk.LEFT else "Right"
        fingers = [
            (f"{prefix} Pinky", "छोटी (Pinky)"),
            (f"{prefix} Ring", "रिंग (Ring)"),
            (f"{prefix} Middle", "मध्यमा (Middle)"),
            (f"{prefix} Index", "तर्जनी (Index)"),
        ]
        dots = {}
        for f_key, f_label in fingers:
            row = tk.Frame(frame, bg="#ffffff", pady=3)
            row.pack(fill=tk.X)
            dot = tk.Label(
                row,
                text="  ",
                bg="#e2e8f0",
                relief=tk.SOLID,
                bd=1,
                width=3,
            )
            dot.pack(side=tk.LEFT, padx=(0, 6))
            tk.Label(row, text=f_label, font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#334155").pack(side=tk.LEFT)
            dots[f_key] = dot

        thumb_row = tk.Frame(frame, bg="#ffffff", pady=(10, 2))
        thumb_row.pack(fill=tk.X)
        t_dot = tk.Label(thumb_row, text="  ", bg="#e2e8f0", relief=tk.SOLID, bd=1, width=3)
        t_dot.pack(side=tk.LEFT, padx=(0, 6))
        tk.Label(thumb_row, text="अंगूठा (Space)", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#334155").pack(
            side=tk.LEFT
        )
        dots["Thumb"] = t_dot
        return dots

    def build_onscreen_keyboard(self, parent):
        kb_box = tk.LabelFrame(
            parent,
            text="ऑन-स्क्रीन कीबोर्ड (पीला/लाल = सक्रिय की)",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#1e3a5f",
            padx=6,
            pady=5,
        )
        kb_box.pack(fill=tk.BOTH, expand=True)

        for row in KEYBOARD_ROWS:
            r_frame = tk.Frame(kb_box, bg="#ffffff")
            r_frame.pack(pady=1)
            for normal_ch, shift_ch, finger, base_color in row:
                lbl = tk.Label(
                    r_frame,
                    text=f"{normal_ch}\n{shift_ch}",
                    width=5,
                    height=2,
                    font=("Consolas", 8, "bold"),
                    bg=base_color,
                    fg="#0f172a",
                    bd=1,
                    relief=tk.RAISED,
                )
                lbl.pack(side=tk.LEFT, padx=1)
                self.key_buttons[normal_ch.lower()] = (lbl, finger, base_color)
                self.key_buttons[shift_ch] = (lbl, finger, base_color)

        space_row = tk.Frame(kb_box, bg="#ffffff")
        space_row.pack(pady=(3, 1))
        self.space_btn = tk.Label(
            space_row,
            text="SPACEBAR (Thumb / अंगूठा)",
            width=46,
            height=1,
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9",
            fg="#0f172a",
            bd=1,
            relief=tk.RAISED,
        )
        self.space_btn.pack()

    def clear_highlights(self):
        for lbl, _, base_color in self.key_buttons.values():
            lbl.config(bg=base_color, fg="#0f172a")
        if self.space_btn:
            self.space_btn.config(bg="#f1f5f9", fg="#0f172a")
        for dot in self.left_hand_dots.values():
            dot.config(bg="#e2e8f0")
        for dot in self.right_hand_dots.values():
            dot.config(bg="#e2e8f0")

    def highlight_finger(self, finger):
        if finger in self.left_hand_dots:
            self.left_hand_dots[finger].config(bg="#ef4444")
        if finger in self.right_hand_dots:
            self.right_hand_dots[finger].config(bg="#ef4444")
        if finger == "Thumb":
            if "Thumb" in self.left_hand_dots:
                self.left_hand_dots["Thumb"].config(bg="#ef4444")
            if "Thumb" in self.right_hand_dots:
                self.right_hand_dots["Thumb"].config(bg="#ef4444")

    def record_error_char(self, ch):
        if not ch or ch == "\n":
            return
        script = self.script_var.get()
        script_map = self.stats_data.setdefault(script, {})
        script_map[ch] = script_map.get(ch, 0) + 1
        save_json_file(STATS_FILE, self.stats_data)

    def beep_error(self):
        if self.sound_var.get():
            try:
                self.root.bell()
            except Exception:
                pass

    def get_selected_seconds(self):
        mapping = {"1 Min": 60, "2 Min": 120, "5 Min": 300, "10 Min": 600}
        return mapping.get(self.time_var.get(), 60)

    def on_key_press(self, event):
        if event.keysym == "BackSpace" and self.disable_backspace_var.get():
            self.alert_label.config(text="Backspace बंद है!", fg="#b91c1c")
            return "break"

        if str(self.input_text.cget("state")) == "disabled":
            return "break"

        if self.mode_var.get() == "गलत पर रुकें":
            if event.char and event.isprintable() and event.keysym not in ("Return", "Tab"):
                target = self.target_text.get("1.0", "end-1c")
                typed = self.input_text.get("1.0", "end-1c")
                idx = len(typed)
                if idx < len(target):
                    expected_char = target[idx]
                    if event.char != expected_char:
                        self.strict_errors_count += 1
                        self.last_wrong_char = event.char
                        self.record_error_char(expected_char)
                        self.beep_error()
                        self.alert_label.config(
                            text=f"गलत की '{event.char}'! सही की '{expected_char}' दबाएँ",
                            fg="#b91c1c",
                        )
                        self.calculate_stats()
                        self.update_finger_guide()
                        return "break"
                    else:
                        self.last_wrong_char = None
                        self.alert_label.config(text="सही!", fg="#15803d")
        return None

    def update_target_highlights(self):
        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")

        self.target_text.config(state=tk.NORMAL)
        self.target_text.tag_remove("correct", "1.0", tk.END)
        self.target_text.tag_remove("wrong", "1.0", tk.END)
        self.target_text.tag_remove("current", "1.0", tk.END)

        limit = min(len(typed), len(target))
        for i in range(limit):
            s_idx = f"1.0+{i}c"
            e_idx = f"1.0+{i+1}c"
            if typed[i] == target[i]:
                self.target_text.tag_add("correct", s_idx, e_idx)
            else:
                self.target_text.tag_add("wrong", s_idx, e_idx)
                if i not in self.counted_error_positions:
                    self.counted_error_positions.add(i)
                    self.record_error_char(target[i])
                    self.beep_error()

        if len(typed) < len(target):
            c_start = f"1.0+{len(typed)}c"
            c_end = f"1.0+{len(typed)+1}c"
            self.target_text.tag_add("current", c_start, c_end)
            self.target_text.see(c_start)

        self.target_text.config(state=tk.DISABLED)

    def update_finger_guide(self):
        self.clear_highlights()
        script = self.script_var.get()
        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")
        idx = len(typed)

        if self.last_wrong_char:
            if self.last_wrong_char == " " and self.space_btn:
                self.space_btn.config(bg="#fca5a5")
            elif self.last_wrong_char in self.key_buttons:
                w_lbl, _, _ = self.key_buttons[self.last_wrong_char]
                w_lbl.config(bg="#fca5a5")

        if idx >= len(target):
            self.finger_label.config(text="लेसन पूरा हुआ!")
            return

        next_char = target[idx]
        if next_char == " ":
            if self.space_btn:
                self.space_btn.config(bg="#fde047")
            self.highlight_finger("Thumb")
            self.finger_label.config(text=f"अगली की: [SPACE]  |  {FINGER_HINDI_NAMES['Thumb']}")
            return

        if script == "Kruti Dev 010" and next_char in KRUTIDEV_KEY_MAP:
            key_sym, finger, desc = KRUTIDEV_KEY_MAP[next_char]
            if key_sym in self.key_buttons:
                lbl, _, _ = self.key_buttons[key_sym]
                lbl.config(bg="#fde047")
            self.highlight_finger(finger)
            shift_txt = " + Shift" if (key_sym.isupper() or key_sym in "~!@#$%^&*()_+{}|:\"<>?") else ""
            self.finger_label.config(
                text=f"Kruti Dev की: '{key_sym}'{shift_txt} ({desc})  |  {FINGER_HINDI_NAMES.get(finger, finger)}"
            )
            return

        if next_char in self.key_buttons:
            lbl, finger, _ = self.key_buttons[next_char]
            lbl.config(bg="#fde047")
            self.highlight_finger(finger)
            shift_txt = " + Shift" if (next_char.isupper() or next_char in "~!@#$%^&*()_+{}|:\"<>?") else ""
            self.finger_label.config(
                text=f"अगली की: '{next_char}'{shift_txt}  |  {FINGER_HINDI_NAMES.get(finger, finger)}"
            )
        else:
            self.finger_label.config(text=f"अगला अक्षर ({script}): '{next_char}'")

    def refresh_lesson_dropdown(self, select_first=False, select_name=None):
        script = self.script_var.get()
        names = list(self.lessons_data.get(script, {}).keys())
        self.lesson_combo["values"] = names
        if not names:
            self.lesson_var.set("")
            return
        if select_name and select_name in names:
            self.lesson_var.set(select_name)
        elif select_first or self.lesson_var.get() not in names:
            self.lesson_var.set(names[0])

    def on_script_change(self, event=None):
        self.refresh_lesson_dropdown(select_first=True)
        self.load_selected_lesson()

    def load_selected_lesson(self):
        script = self.script_var.get()
        lesson_name = self.lesson_var.get()
        content = self.lessons_data.get(script, {}).get(lesson_name, "")
        self.set_practice_text(content, label_text=f"लेसन: {lesson_name}")

    def set_practice_text(self, content, label_text=""):
        script = self.script_var.get()
        font_style = self.get_script_font(script, size=18)
        input_font = self.get_script_font(script, size=17)

        self.target_text.config(state=tk.NORMAL, font=font_style)
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert("1.0", content)
        self.target_text.config(state=tk.DISABLED)
        self.input_text.config(font=input_font)
        self.reset_test(custom_status=label_text or None)

    def practice_weak_keys(self):
        script = self.script_var.get()
        err_map = self.stats_data.get(script, {})
        sorted_chars = [c for c, _ in sorted(err_map.items(), key=lambda x: x[1], reverse=True) if c.strip()]

        if not sorted_chars:
            messagebox.showinfo(
                "कमज़ोर कीज़ डेटा नहीं है",
                f"{script} में अभी तक कोई गलती दर्ज नहीं हुई है। पहले थोड़ा टाइप करें, फिर यह बटन आपके सबसे ज़्यादा गलत होने वाले अक्षरों का प्रैक्टिस सेट बना देगा।",
            )
            return

        top_chars = sorted_chars[:6]
        drill_items = []
        for ch in top_chars:
            drill_items.extend([ch * 2, ch * 3])
        if len(top_chars) >= 2:
            for i in range(len(top_chars) - 1):
                drill_items.append(top_chars[i] + top_chars[i + 1])

        random.shuffle(drill_items)
        drill_text = " ".join(drill_items * 3)
        self.set_practice_text(drill_text, label_text=f"कमज़ोर कीज़ फ़ोकस ({script}): {' '.join(top_chars)}")

    def open_lesson_manager(self):
        script = self.script_var.get()
        win = tk.Toplevel(self.root)
        win.title(f"लेसन मैनेजर — {script}")
        win.geometry("760x440")
        win.configure(bg="#f8fafc")

        top = tk.Frame(win, bg="#f8fafc", padx=12, pady=8)
        top.pack(fill=tk.X)

        tk.Label(top, text="लेसन का नाम:", font=("Segoe UI", 10, "bold"), bg="#f8fafc").pack(side=tk.LEFT)
        title_entry = tk.Entry(top, width=32, font=("Segoe UI", 10))
        title_entry.pack(side=tk.LEFT, padx=(6, 12))
        title_entry.insert(0, self.lesson_var.get())

        tk.Button(
            top,
            text=".txt फ़ाइल चुनें",
            command=lambda: self.load_txt_into_editor(title_entry, body_box),
            bg="#d97706",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=8,
        ).pack(side=tk.RIGHT)

        body_box = tk.Text(
            win,
            height=11,
            font=self.get_script_font(script, size=14),
            wrap=tk.WORD,
            bg="#ffffff",
            padx=10,
            pady=8,
        )
        body_box.pack(fill=tk.BOTH, expand=True, padx=12)
        current_body = self.lessons_data.get(script, {}).get(self.lesson_var.get(), "")
        body_box.insert("1.0", current_body)

        btns = tk.Frame(win, bg="#f8fafc", padx=12, pady=10)
        btns.pack(fill=tk.X)

        def on_add():
            t = title_entry.get().strip()
            b = body_box.get("1.0", "end-1c").strip()
            if not t or not b:
                messagebox.showwarning("अधूरी जानकारी", "लेसन का नाम और मैटर दोनों लिखें।", parent=win)
                return
            if t in self.lessons_data[script]:
                messagebox.showinfo("पहले से मौजूद", "इस नाम का लेसन पहले से है। अपडेट करें या नया नाम दें।", parent=win)
                return
            self.lessons_data[script][t] = b
            save_json_file(LESSONS_FILE, self.lessons_data)
            self.refresh_lesson_dropdown(select_name=t)
            self.load_selected_lesson()
            messagebox.showinfo("सेव हुआ", f"'{t}' जुड़ गया।", parent=win)

        def on_update():
            old_t = self.lesson_var.get()
            new_t = title_entry.get().strip()
            b = body_box.get("1.0", "end-1c").strip()
            if not old_t or not new_t or not b:
                messagebox.showwarning("अधूरी जानकारी", "नाम और मैटर दोनों भरें।", parent=win)
                return
            if old_t != new_t and old_t in self.lessons_data[script]:
                del self.lessons_data[script][old_t]
            self.lessons_data[script][new_t] = b
            save_json_file(LESSONS_FILE, self.lessons_data)
            self.refresh_lesson_dropdown(select_name=new_t)
            self.load_selected_lesson()
            messagebox.showinfo("अपडेट हुआ", f"'{new_t}' अपडेट हो गया।", parent=win)

        def on_delete():
            cur_t = self.lesson_var.get()
            if len(self.lessons_data[script]) <= 1:
                messagebox.showwarning("हटा नहीं सकते", f"{script} में कम से कम 1 लेसन रहना ज़रूरी है।", parent=win)
                return
            if not messagebox.askyesno("पुष्टि करें", f"क्या '{cur_t}' हटाना चाहते हैं?", parent=win):
                return
            del self.lessons_data[script][cur_t]
            save_json_file(LESSONS_FILE, self.lessons_data)
            self.refresh_lesson_dropdown(select_first=True)
            self.load_selected_lesson()
            title_entry.delete(0, tk.END)
            title_entry.insert(0, self.lesson_var.get())
            body_box.delete("1.0", tk.END)
            body_box.insert("1.0", self.lessons_data[script][self.lesson_var.get()])

        tk.Button(btns, text="नया लेसन जोड़ें (Add)", command=on_add, bg="#059669", fg="white", font=("Segoe UI", 9, "bold"), padx=10).pack(side=tk.LEFT, padx=3)
        tk.Button(btns, text="अपडेट करें (Edit)", command=on_update, bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), padx=10).pack(side=tk.LEFT, padx=3)
        tk.Button(btns, text="हटाएँ (Delete)", command=on_delete, bg="#dc2626", fg="white", font=("Segoe UI", 9, "bold"), padx=10).pack(side=tk.LEFT, padx=3)
        tk.Button(btns, text="बंद करें", command=win.destroy, bg="#64748b", fg="white", font=("Segoe UI", 9, "bold"), padx=10).pack(side=tk.RIGHT)

    def load_txt_into_editor(self, title_entry, body_box):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                txt = f.read().strip()
        except UnicodeDecodeError:
            with open(path, "r", encoding="cp1252", errors="ignore") as f:
                txt = f.read().strip()
        if txt:
            title_entry.delete(0, tk.END)
            title_entry.insert(0, os.path.splitext(os.path.basename(path))[0])
            body_box.delete("1.0", tk.END)
            body_box.insert("1.0", txt)

    def open_game_window(self):
        script = self.script_var.get()
        words = GAME_WORDS.get(script, GAME_WORDS["English"])

        game_win = tk.Toplevel(self.root)
        game_win.title(f"टाइपिंग गेम (Word Rush) — {script}")
        game_win.geometry("680x460")
        game_win.configure(bg="#0f172a")

        state = {
            "score": 0,
            "lives": 5,
            "word": random.choice(words),
            "y": 30,
            "active": True,
        }

        top = tk.Frame(game_win, bg="#1e293b", pady=6, padx=12)
        top.pack(fill=tk.X)

        score_lbl = tk.Label(top, text="स्कोर: 0", font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="#4ade80")
        score_lbl.pack(side=tk.LEFT, padx=10)
        lives_lbl = tk.Label(top, text="लाइव: 5", font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="#f87171")
        lives_lbl.pack(side=tk.LEFT, padx=10)

        canvas = tk.Canvas(game_win, bg="#1e293b", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        entry = tk.Entry(game_win, font=self.get_script_font(script, size=14), bg="#f8fafc", fg="#0f172a")
        entry.pack(fill=tk.X, padx=12, pady=(0, 12))
        entry.focus()

        def spawn_word():
            state["word"] = random.choice(words)
            state["y"] = 25

        def check_entry(event=None):
            if not state["active"]:
                return
            typed_w = entry.get().strip()
            if typed_w == state["word"]:
                state["score"] += 10
                score_lbl.config(text=f"स्कोर: {state['score']}")
                entry.delete(0, tk.END)
                spawn_word()

        entry.bind("<KeyRelease>", check_entry)

        def tick():
            if not state["active"] or not game_win.winfo_exists():
                return
            canvas.delete("all")
            w_width = max(canvas.winfo_width(), 400)
            w_height = max(canvas.winfo_height(), 240)
            canvas.create_text(
                w_width // 2,
                state["y"],
                text=state["word"],
                fill="#fde047",
                font=self.get_script_font(script, size=18),
            )
            state["y"] += 5
            if state["y"] >= w_height - 20:
                state["lives"] -= 1
                lives_lbl.config(text=f"लाइव: {state['lives']}")
                entry.delete(0, tk.END)
                if state["lives"] <= 0:
                    state["active"] = False
                    messagebox.showinfo("गेम समाप्त", f"आपका कुल स्कोर: {state['score']}", parent=game_win)
                    game_win.destroy()
                    return
                spawn_word()
            game_win.after(90, tick)

        game_win.protocol("WM_DELETE_WINDOW", lambda: (state.update({"active": False}), game_win.destroy()))
        game_win.after(200, tick)

    def reset_test(self, custom_status=None):
        self.timer_running = False
        self.start_time = None
        self.last_wrong_char = None
        self.strict_errors_count = 0
        self.counted_error_positions.clear()

        self.selected_duration = self.get_selected_seconds()
        self.time_left = self.selected_duration
        self.timer_label.config(text=f"{format_mm_ss(self.time_left)} Min.")
        self.signs_label.config(text="00 Signs")
        self.wpm_label.config(text="00 WPM (Net)")
        self.err_label.config(text="00 Errors")
        self.acc_label.config(text="100.0% Acc.")

        if custom_status:
            self.alert_label.config(text=custom_status, fg="#7c3aed")
        else:
            self.alert_label.config(text="पहला अक्षर दबाते ही समय शुरू होगा", fg="#2563eb")

        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete("1.0", tk.END)
        self.update_target_highlights()
        self.update_finger_guide()
        self.input_text.focus()

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"{format_mm_ss(self.time_left)} Min.")
            self.calculate_stats()
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.finish_test()

    def on_key_release(self, event):
        if str(self.input_text.cget("state")) == "disabled":
            return

        if not self.timer_running and self.time_left > 0:
            typed = self.input_text.get("1.0", "end-1c")
            if len(typed) > 0:
                self.timer_running = True
                self.start_time = time.time()
                self.update_timer()

        self.update_target_highlights()
        self.calculate_stats()
        self.update_finger_guide()

        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")
        if len(typed) >= len(target) and len(target) > 0:
            self.finish_test()

    def calculate_stats(self):
        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")

        elapsed_sec = max(self.selected_duration - self.time_left, 1)
        elapsed_min = elapsed_sec / 60.0

        if self.mode_var.get() == "गलत पर रुकें":
            correct_chars = len(typed)
            errors = self.strict_errors_count
            total_attempts = correct_chars + errors
            acc = (correct_chars / total_attempts) * 100 if total_attempts > 0 else 100.0
            net_wpm = int((correct_chars / 5) / elapsed_min)
        else:
            correct_chars = sum(1 for i, ch in enumerate(typed) if i < len(target) and ch == target[i])
            errors = max(len(typed) - correct_chars, 0)
            acc = (correct_chars / len(typed)) * 100 if len(typed) > 0 else 100.0
            net_wpm = int((correct_chars / 5) / elapsed_min)

        self.signs_label.config(text=f"{len(typed):02d} Signs")
        self.wpm_label.config(text=f"{net_wpm:02d} WPM (Net)")
        self.err_label.config(text=f"{errors:02d} Errors")
        self.acc_label.config(text=f"{acc:.1f}% Acc.")

    def finish_test(self):
        self.timer_running = False
        self.clear_highlights()
        self.input_text.config(state=tk.DISABLED)
        self.calculate_stats()
        messagebox.showinfo(
            "परिणाम (Result)",
            f"टेस्ट पूरा हुआ!\n\n"
            f"{self.wpm_label.cget('text')}  |  {self.acc_label.cget('text')}\n"
            f"{self.err_label.cget('text')}  |  {self.signs_label.cget('text')}",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = OfflineTypingTutor(root)
    root.mainloop()
