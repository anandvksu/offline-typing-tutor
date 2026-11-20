import json
import os
import sys
import time
import tkinter as tk
from tkinter import messagebox, ttk


def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


LESSONS_FILE = os.path.join(get_app_dir(), "typing_lessons.json")

DEFAULT_LESSONS = {
    "English": {
        "Home Row - Basic": "asdf jkl; asdf jkl; dad sad fad lad ask all fall salad flask",
        "Top & Bottom Row": "qwerty uiop zxcv bnm the quick brown fox jumps over the lazy dog",
        "Official Paragraph": "The Deputy Collector Land Reforms court hears appeals regarding land mutation and boundary disputes in the sub-division.",
    },
    "Kruti Dev 010": {
        "Home Row - Basic": "d s h f t y r k l ; d s h f t y r k l ; dkj dkj gkj lkj dgk",
        "Matra & Words": "fdrkuh] fdrkuh] vf/kdkjh] dk;kZy;] vfHkys[k] vkns'k",
        "Court / Office Matter": "Hkwfe lq/kkj mi&lekgrkZ U;k;ky; esa nkf[ky&[kkfjt vihy okn dh lquokbZ dh tkrh gSA",
    },
    "Mangal": {
        "Basic Words": "कमल नयन घर चल अब कल फल जल मन धन कर भर",
        "Office Words": "अधिकारी कार्यालय अभिलेख आदेश आवेदन प्रतिवेदन सुनवाई प्रमाण पत्र",
        "Official Paragraph": "भूमि सुधार उप-समाहर्ता कार्यालय में प्राप्त आवेदनों का अभिलेखीय सत्यापन समयबद्ध रूप से किया जाता है।",
    },
}

KEYBOARD_ROWS = [
    [
        ("`", "~", "Left Pinky"),
        ("1", "!", "Left Pinky"),
        ("2", "@", "Left Ring"),
        ("3", "#", "Left Middle"),
        ("4", "$", "Left Index"),
        ("5", "%", "Left Index"),
        ("6", "^", "Right Index"),
        ("7", "&", "Right Index"),
        ("8", "*", "Right Middle"),
        ("9", "(", "Right Ring"),
        ("0", ")", "Right Pinky"),
        ("-", "_", "Right Pinky"),
        ("=", "+", "Right Pinky"),
    ],
    [
        ("q", "Q", "Left Pinky"),
        ("w", "W", "Left Ring"),
        ("e", "E", "Left Middle"),
        ("r", "R", "Left Index"),
        ("t", "T", "Left Index"),
        ("y", "Y", "Right Index"),
        ("u", "U", "Right Index"),
        ("i", "I", "Right Middle"),
        ("o", "O", "Right Ring"),
        ("p", "P", "Right Pinky"),
        ("[", "{", "Right Pinky"),
        ("]", "}", "Right Pinky"),
        ("\\", "|", "Right Pinky"),
    ],
    [
        ("a", "A", "Left Pinky"),
        ("s", "S", "Left Ring"),
        ("d", "D", "Left Middle"),
        ("f", "F", "Left Index"),
        ("g", "G", "Left Index"),
        ("h", "H", "Right Index"),
        ("j", "J", "Right Index"),
        ("k", "K", "Right Middle"),
        ("l", "L", "Right Ring"),
        (";", ":", "Right Pinky"),
        ("'", '"', "Right Pinky"),
    ],
    [
        ("z", "Z", "Left Pinky"),
        ("x", "X", "Left Ring"),
        ("c", "C", "Left Middle"),
        ("v", "V", "Left Index"),
        ("b", "B", "Left Index"),
        ("n", "N", "Right Index"),
        ("m", "M", "Right Index"),
        (",", "<", "Right Middle"),
        (".", ">", "Right Ring"),
        ("/", "?", "Right Pinky"),
    ],
]

FINGER_HINDI_NAMES = {
    "Left Pinky": "बायाँ हाथ — सबसे छोटी उंगली (Left Pinky)",
    "Left Ring": "बायाँ हाथ — अनामिका / रिंग फिंगर (Left Ring)",
    "Left Middle": "बायाँ हाथ — मध्यमा / बीच की उंगली (Left Middle)",
    "Left Index": "बायाँ हाथ — तर्जनी / इंडेक्स फिंगर (Left Index)",
    "Right Index": "दायाँ हाथ — तर्जनी / इंडेक्स फिंगर (Right Index)",
    "Right Middle": "दायाँ हाथ — मध्यमा / बीच की उंगली (Right Middle)",
    "Right Ring": "दायाँ हाथ — अनामिका / रिंग फिंगर (Right Ring)",
    "Right Pinky": "दायाँ हाथ — सबसे छोटी उंगली (Right Pinky)",
    "Thumb": "अंगूठा — Spacebar (Thumb)",
}

# Kruti Dev 010 कस्टम की-टू-फिंगर व आउटपुट विवरण मैपिंग
KRUTIDEV_KEY_MAP = {
    # Number & Top-left row
    "`": ("`", "Left Pinky", "छोटी ई की मात्रा (ि) / चिह्न"),
    "~": ("~", "Left Pinky", "रेफ / चिह्न"),
    "1": ("1", "Left Pinky", "१ / चिह्न"),
    "!": ("!", "Left Pinky", "। / चिह्न"),
    "2": ("2", "Left Ring", "२ / चिह्न"),
    "@": ("@", "Left Ring", "/ (स्लैश)"),
    "3": ("3", "Left Middle", "३ / चिह्न"),
    "#": ("#", "Left Middle", "क्ष / चिह्न"),
    "4": ("4", "Left Index", "४ / चिह्न"),
    "$": ("$", "Left Index", "द्ध / चिह्न"),
    "5": ("5", "Left Index", "५ / चिह्न"),
    "%": ("%", "Left Index", "त्र / चिह्न"),
    "6": ("6", "Right Index", "६ / चिह्न"),
    "^": ("^", "Right Index", "ज्ञ / चिह्न"),
    "7": ("7", "Right Index", "७ / चिह्न"),
    "&": ("&", "Right Index", "श्र / चिह्न"),
    "8": ("8", "Right Middle", "८ / चिह्न"),
    "*": ("*", "Right Middle", "रु / चिह्न"),
    "9": ("9", "Right Ring", "९ / चिह्न"),
    "(": ("(", "Right Ring", "ऋ / चिह्न"),
    "0": ("0", "Right Pinky", "० / चिह्न"),
    ")": (")", "Right Pinky", "— / चिह्न"),
    "-": ("-", "Right Pinky", "चिह्न"),
    "_": ("_", "Right Pinky", "चिह्न"),
    "=": ("=", "Right Pinky", "ु (छोटा उ मात्रा)"),
    "+": ("+", "Right Pinky", "ू (बड़ा उ मात्रा)"),

    # QWERTY row (Top row)
    "q": ("q", "Left Pinky", "ु (छोटा उ मात्रा)"),
    "Q": ("Q", "Left Pinky", "फ / संयुक्त रूप"),
    "w": ("w", "Left Ring", "ू (बड़ा उ मात्रा)"),
    "W": ("W", "Left Ring", "ॅ / संयुक्त रूप"),
    "e": ("e", "Left Middle", "म (मकार)"),
    "E": ("E", "Left Middle", "म् (आधा म)"),
    "r": ("r", "Left Index", "त (तकार)"),
    "R": ("R", "Left Index", "त् (आधा त)"),
    "t": ("t", "Left Index", "ज (जकार)"),
    "T": ("T", "Left Index", "ज् (आधा ज)"),
    "y": ("y", "Right Index", "ल (लकार)"),
    "Y": ("Y", "Right Index", "ल् (आधा ल)"),
    "u": ("u", "Right Index", "न (नकार)"),
    "U": ("U", "Right Index", "न् (आधा न)"),
    "i": ("i", "Right Middle", "प (पकार)"),
    "I": ("I", "Right Middle", "प् (आधा प)"),
    "o": ("o", "Right Ring", "व (वकार)"),
    "O": ("O", "Right Ring", "व् (आधा व)"),
    "p": ("p", "Right Pinky", "च (चकार)"),
    "P": ("P", "Right Pinky", "च् (आधा च)"),
    "[": ("[", "Right Pinky", "ख (खकार)"),
    "{": ("{", "Right Pinky", "ख् (आधा ख)"),
    "]": ("]", "Right Pinky", "़ (नुक्ता / चिह्न)"),
    "}": ("}", "Right Pinky", "ह्र / चिह्न"),
    "\\": ("\\", "Right Pinky", "़ / हलंत चिह्न"),
    "|": ("|", "Right Pinky", "द्व / चिह्न"),

    # ASDF row (Home row)
    "a": ("a", "Left Pinky", "ं (अनुस्वार / बिंदी)"),
    "A": ("A", "Left Pinky", "ँ (चंद्रबिंदु)"),
    "s": ("s", "Left Ring", "े (ए की मात्रा)"),
    "S": ("S", "Left Ring", "ै (ऐ की मात्रा)"),
    "d": ("d", "Left Middle", "क (ककार)"),
    "D": ("D", "Left Middle", "क् (आधा क)"),
    "f": ("f", "Left Index", "ि (छोटी इ की मात्रा — शब्द से पहले)"),
    "F": ("F", "Left Index", "फ् / चिह्न"),
    "g": ("g", "Left Index", "ह (हकार)"),
    "G": ("G", "Left Index", "ह् (आधा ह)"),
    "h": ("h", "Right Index", "ी (बड़ी ई की मात्रा)"),
    "H": ("H", "Right Index", "ीं / चिह्न"),
    "j": ("j", "Right Index", "र (रकार)"),
    "J": ("J", "Right Index", "्र / रेफ"),
    "k": ("k", "Right Middle", "ा (आ की मात्रा)"),
    "K": ("K", "Right Middle", "ा / चिह्न"),
    "l": ("l", "Right Ring", "स (सकार)"),
    "L": ("L", "Right Ring", "स् (आधा स)"),
    ";": (";", "Right Pinky", "य (यकार)"),
    ":": (":", "Right Pinky", "य् (आधा य)"),
    "'": ("'", "Right Pinky", "ु / चिह्न"),
    '"': ('"', "Right Pinky", "ू / चिह्न"),

    # ZXCV row (Bottom row)
    "z": ("z", "Left Pinky", "र् (रेफ — शब्द के अंत/ऊपर)"),
    "Z": ("Z", "Left Pinky", "र् / चिह्न"),
    "x": ("x", "Left Ring", "ग (गकार)"),
    "X": ("X", "Left Ring", "ग् (आधा ग)"),
    "c": ("c", "Left Middle", "ब (बकार)"),
    "C": ("C", "Left Middle", "ब् (आधा ब)"),
    "v": ("v", "Left Index", "अ / अकार"),
    "V": ("V", "Left Index", "अ / चिह्न"),
    "b": ("b", "Left Index", "इ (इकार)"),
    "B": ("B", "Left Index", "ई (ईकार)"),
    "n": ("n", "Right Index", "द (दकार)"),
    "N": ("N", "Right Index", "द् / द्ध"),
    "m": ("m", "Right Index", "उ (उकार)"),
    "M": ("M", "Right Index", "ऊ (ऊकार)"),
    ",": (",", "Right Middle", "ए (एकार)"),
    "<": ("<", "Right Middle", "ऐ (ऐकार)"),
    ".": (".", "Right Ring", "ण (णकार)"),
    ">": (">", "Right Ring", "ण् (आधा ण)"),
    "/": ("/", "Right Pinky", "ध (धकार)"),
    "?": ("?", "Right Pinky", "ध् (आधा ध)"),
}


def load_lessons_data():
    if os.path.exists(LESSONS_FILE):
        try:
            with open(LESSONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for script in ["English", "Kruti Dev 010", "Mangal"]:
                if script not in data or not isinstance(data[script], dict) or not data[script]:
                    data[script] = dict(DEFAULT_LESSONS[script])
            return data
        except Exception:
            pass

    data = {k: dict(v) for k, v in DEFAULT_LESSONS.items()}
    save_lessons_data(data)
    return data


def save_lessons_data(data):
    try:
        with open(LESSONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as exc:
        messagebox.showwarning("Save Warning", f"लेसन फ़ाइल सेव करने में समस्या आई:\n{exc}")


class OfflineTypingTutor:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline Typing Tutor — English | Kruti Dev 010 | Mangal")
        self.root.geometry("1060x790")
        self.root.configure(bg="#f0f4f8")

        self.lessons_data = load_lessons_data()
        self.start_time = None
        self.timer_running = False
        self.time_left = 60
        self.selected_duration = 60
        self.key_buttons = {}
        self.space_btn = None

        self.setup_ui()
        self.refresh_lesson_dropdown(select_first=True)
        self.load_selected_lesson()

    def get_script_font(self, script, size=16):
        if script == "Kruti Dev 010":
            return ("Kruti Dev 010", size + 3)
        if script == "Mangal":
            return ("Nirmala UI", size)
        return ("Consolas", size)

    def setup_ui(self):
        header = tk.Label(
            self.root,
            text="ऑफलाइन टाइपिंग ट्यूटर (English | Kruti Dev 010 | Mangal)",
            font=("Segoe UI", 15, "bold"),
            bg="#1a365d",
            fg="white",
            pady=8,
        )
        header.pack(fill=tk.X)

        # 1. स्क्रिप्ट, लेसन, समय और रीसेट बार
        top_bar = tk.Frame(self.root, bg="#f0f4f8", pady=6)
        top_bar.pack(fill=tk.X, padx=16)

        tk.Label(top_bar, text="स्क्रिप्ट:", font=("Segoe UI", 10, "bold"), bg="#f0f4f8").pack(side=tk.LEFT)
        self.script_var = tk.StringVar(value="English")
        self.script_combo = ttk.Combobox(
            top_bar,
            textvariable=self.script_var,
            values=["English", "Kruti Dev 010", "Mangal"],
            width=15,
            state="readonly",
        )
        self.script_combo.pack(side=tk.LEFT, padx=(4, 12))
        self.script_combo.bind("<<ComboboxSelected>>", self.on_script_change)

        tk.Label(top_bar, text="लेसन:", font=("Segoe UI", 10, "bold"), bg="#f0f4f8").pack(side=tk.LEFT)
        self.lesson_var = tk.StringVar()
        self.lesson_combo = ttk.Combobox(top_bar, textvariable=self.lesson_var, width=28, state="readonly")
        self.lesson_combo.pack(side=tk.LEFT, padx=(4, 12))
        self.lesson_combo.bind("<<ComboboxSelected>>", lambda e: self.load_selected_lesson())

        tk.Label(top_bar, text="समय (s):", font=("Segoe UI", 10, "bold"), bg="#f0f4f8").pack(side=tk.LEFT)
        self.time_var = tk.StringVar(value="60")
        time_combo = ttk.Combobox(
            top_bar,
            textvariable=self.time_var,
            values=["60", "120", "300", "600"],
            width=7,
            state="readonly",
        )
        time_combo.pack(side=tk.LEFT, padx=(4, 10))
        time_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_test())

        tk.Button(
            top_bar,
            text="रीसेट (Reset)",
            command=self.reset_test,
            bg="#2b6cb0",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=2,
        ).pack(side=tk.RIGHT)

        # 2. लाइव स्कोरबोर्ड (Timer, WPM, Accuracy)
        stats_frame = tk.Frame(self.root, bg="#e2e8f0", pady=6, bd=1, relief=tk.SOLID)
        stats_frame.pack(fill=tk.X, padx=16, pady=4)

        self.timer_label = tk.Label(
            stats_frame, text="समय: 60s", font=("Segoe UI", 12, "bold"), bg="#e2e8f0", fg="#c53030"
        )
        self.timer_label.pack(side=tk.LEFT, expand=True)

        self.wpm_label = tk.Label(
            stats_frame, text="गति (WPM): 0", font=("Segoe UI", 12, "bold"), bg="#e2e8f0", fg="#2f855a"
        )
        self.wpm_label.pack(side=tk.LEFT, expand=True)

        self.acc_label = tk.Label(
            stats_frame, text="सटीकता (Accuracy): 100%", font=("Segoe UI", 12, "bold"), bg="#e2e8f0", fg="#2b6cb0"
        )
        self.acc_label.pack(side=tk.LEFT, expand=True)

        # 3. फिंगर गाइड बैनर
        finger_frame = tk.Frame(self.root, bg="#edf2f7", pady=6, padx=10, bd=1, relief=tk.GROOVE)
        finger_frame.pack(fill=tk.X, padx=16, pady=4)

        self.finger_label = tk.Label(
            finger_frame,
            text="अगली की: —  |  उंगली: —",
            font=("Segoe UI", 10, "bold"),
            bg="#edf2f7",
            fg="#1a202c",
        )
        self.finger_label.pack(side=tk.LEFT)

        self.hint_sublabel = tk.Label(
            finger_frame,
            text="पीले रंग से हाइलाइट की (Key) दबाएँ",
            font=("Segoe UI", 9),
            bg="#edf2f7",
            fg="#4a5568",
        )
        self.hint_sublabel.pack(side=tk.RIGHT)

        # 4. टारगेट टेक्स्ट और टाइपिंग बॉक्स
        tk.Label(
            self.root,
            text="देखकर टाइप करने वाला मैटर:",
            font=("Segoe UI", 9, "bold"),
            bg="#f0f4f8",
        ).pack(anchor="w", padx=16, pady=(4, 1))
        self.target_text = tk.Text(
            self.root,
            height=3,
            font=("Consolas", 15),
            wrap=tk.WORD,
            bg="#ffffff",
            fg="#1a202c",
            padx=8,
            pady=6,
            bd=2,
            relief=tk.GROOVE,
        )
        self.target_text.pack(fill=tk.X, padx=16)
        self.target_text.config(state=tk.DISABLED)

        tk.Label(
            self.root,
            text="यहाँ टाइप करें (पहला अक्षर दबाते ही टाइमर शुरू होगा):",
            font=("Segoe UI", 9, "bold"),
            bg="#f0f4f8",
        ).pack(anchor="w", padx=16, pady=(6, 1))
        self.input_text = tk.Text(
            self.root,
            height=3,
            font=("Consolas", 15),
            wrap=tk.WORD,
            bg="#fffaf0",
            fg="#000000",
            padx=8,
            pady=6,
            bd=2,
            relief=tk.GROOVE,
        )
        self.input_text.pack(fill=tk.X, padx=16)
        self.input_text.bind("<KeyRelease>", self.on_key_release)

        # 5. लेसन मैनेजमेंट पैनल (Add / Edit / Delete / Load)
        manage_frame = tk.LabelFrame(
            self.root,
            text="लेसन जोड़ें / बदलें / हटाएँ (चयनित स्क्रिप्ट के लिए सेव होगा)",
            font=("Segoe UI", 9, "bold"),
            bg="#f0f4f8",
            fg="#1a365d",
            padx=8,
            pady=6,
        )
        manage_frame.pack(fill=tk.X, padx=16, pady=6)

        row1 = tk.Frame(manage_frame, bg="#f0f4f8")
        row1.pack(fill=tk.X, pady=(0, 4))

        tk.Label(row1, text="लेसन का नाम:", font=("Segoe UI", 9, "bold"), bg="#f0f4f8").pack(side=tk.LEFT)
        self.lesson_title_entry = tk.Entry(row1, width=28, font=("Segoe UI", 9))
        self.lesson_title_entry.pack(side=tk.LEFT, padx=(4, 8))

        tk.Button(
            row1,
            text="नया लेसन जोड़ें (Add)",
            command=self.add_lesson,
            bg="#2f855a",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            padx=8,
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            row1,
            text="मौजूदा लेसन अपडेट करें (Edit/Save)",
            command=self.update_current_lesson,
            bg="#2b6cb0",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            padx=8,
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            row1,
            text="लेसन हटाएँ (Delete)",
            command=self.delete_current_lesson,
            bg="#c53030",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            padx=8,
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            row1,
            text="बॉक्स का मैटर प्रैक्टिस में डालें",
            command=self.load_editor_text_to_practice,
            bg="#6b46c1",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            padx=8,
        ).pack(side=tk.RIGHT)

        self.lesson_editor_text = tk.Text(
            manage_frame,
            height=2,
            font=("Consolas", 11),
            wrap=tk.WORD,
            bg="#ffffff",
            fg="#1a202c",
            padx=6,
            pady=4,
            bd=1,
            relief=tk.SOLID,
        )
        self.lesson_editor_text.pack(fill=tk.X)

        # 6. ऑन-स्क्रीन कीबोर्ड + फिंगर गाइड
        kb_frame = tk.LabelFrame(
            self.root,
            text="ऑन-स्क्रीन कीबोर्ड व उंगली गाइड (Finger Guide)",
            font=("Segoe UI", 9, "bold"),
            bg="#f0f4f8",
            fg="#1a365d",
            padx=6,
            pady=4,
        )
        kb_frame.pack(fill=tk.X, padx=16, pady=(2, 8))
        self.build_onscreen_keyboard(kb_frame)

    def build_onscreen_keyboard(self, parent):
        for row in KEYBOARD_ROWS:
            r_frame = tk.Frame(parent, bg="#f0f4f8")
            r_frame.pack(pady=1)
            for normal_ch, shift_ch, finger in row:
                lbl = tk.Label(
                    r_frame,
                    text=f"{normal_ch}\n{shift_ch}",
                    width=5,
                    height=2,
                    font=("Consolas", 8, "bold"),
                    bg="#ffffff",
                    fg="#1a202c",
                    bd=1,
                    relief=tk.RAISED,
                )
                lbl.pack(side=tk.LEFT, padx=1)
                self.key_buttons[normal_ch.lower()] = (lbl, finger)
                self.key_buttons[shift_ch] = (lbl, finger)

        space_row = tk.Frame(parent, bg="#f0f4f8")
        space_row.pack(pady=(2, 1))
        self.space_btn = tk.Label(
            space_row,
            text="SPACEBAR (Thumb / अंगूठा)",
            width=42,
            height=1,
            font=("Segoe UI", 8, "bold"),
            bg="#ffffff",
            fg="#1a202c",
            bd=1,
            relief=tk.RAISED,
        )
        self.space_btn.pack()

    def clear_key_highlights(self):
        for lbl, _ in self.key_buttons.values():
            lbl.config(bg="#ffffff", fg="#1a202c")
        if self.space_btn:
            self.space_btn.config(bg="#ffffff", fg="#1a202c")

    def update_finger_guide(self):
        self.clear_key_highlights()
        script = self.script_var.get()
        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")
        idx = len(typed)

        if idx >= len(target):
            self.finger_label.config(text="टेस्ट समाप्त! (Lesson Complete)")
            return

        next_char = target[idx]
        if next_char == " ":
            if self.space_btn:
                self.space_btn.config(bg="#f6e05e", fg="#000000")
            self.finger_label.config(text=f"अगली की: [SPACE]  |  {FINGER_HINDI_NAMES['Thumb']}")
            return

        if script == "Kruti Dev 010" and next_char in KRUTIDEV_KEY_MAP:
            key_sym, finger, kruti_desc = KRUTIDEV_KEY_MAP[next_char]
            if key_sym in self.key_buttons:
                lbl, _ = self.key_buttons[key_sym]
                lbl.config(bg="#f6e05e", fg="#000000")
            finger_hi = FINGER_HINDI_NAMES.get(finger, finger)
            shift_note = " + Shift" if (key_sym.isupper() or key_sym in "~!@#$%^&*()_+{}|:\"<>?") else ""
            self.finger_label.config(
                text=f"Kruti Dev की: '{key_sym}'{shift_note} ({kruti_desc})  |  {finger_hi}"
            )
            return

        if next_char in self.key_buttons:
            lbl, finger = self.key_buttons[next_char]
            lbl.config(bg="#f6e05e", fg="#000000")
            finger_hi = FINGER_HINDI_NAMES.get(finger, finger)
            extra = " + Shift" if next_char.isupper() or next_char in "~!@#$%^&*()_+{}|:\"<>?" else ""
            self.finger_label.config(text=f"अगली की: '{next_char}'{extra}  |  {finger_hi}")
        else:
            if script == "Kruti Dev 010":
                self.finger_label.config(
                    text=f"अगला अक्षर (Kruti Dev): '{next_char}'  |  कीबोर्ड लेआउट के अनुसार उंगली लगाएँ"
                )
            elif script == "Mangal":
                self.finger_label.config(
                    text=f"अगला अक्षर (Mangal): '{next_char}'  |  InScript / Remington कीबोर्ड से टाइप करें"
                )
            else:
                self.finger_label.config(text=f"अगली की: '{next_char}'")

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

        font_style = self.get_script_font(script, size=15)
        editor_font = self.get_script_font(script, size=11)

        self.target_text.config(state=tk.NORMAL, font=font_style)
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert("1.0", content)
        self.target_text.config(state=tk.DISABLED)

        self.input_text.config(font=font_style)
        self.lesson_editor_text.config(font=editor_font)
        self.lesson_editor_text.delete("1.0", tk.END)
        self.lesson_editor_text.insert("1.0", content)
        self.lesson_title_entry.delete(0, tk.END)
        self.lesson_title_entry.insert(0, lesson_name)

        self.reset_test()

    def add_lesson(self):
        script = self.script_var.get()
        title = self.lesson_title_entry.get().strip()
        body = self.lesson_editor_text.get("1.0", "end-1c").strip()

        if not title:
            messagebox.showwarning("नाम लिखें", "कृपया नए लेसन का नाम लिखें।")
            return
        if not body:
            messagebox.showwarning("मैटर लिखें", "कृपया लेसन का टाइपिंग मैटर लिखें या पेस्ट करें।")
            return

        if title in self.lessons_data[script]:
            messagebox.showinfo(
                "नाम पहले से मौजूद है",
                "इस नाम का लेसन पहले से है। इसे बदलने के लिए 'मौजूदा लेसन अपडेट करें' दबाएँ या नया नाम दें।",
            )
            return

        self.lessons_data[script][title] = body
        save_lessons_data(self.lessons_data)
        self.refresh_lesson_dropdown(select_name=title)
        self.load_selected_lesson()
        messagebox.showinfo("सफल", f"'{title}' ({script}) में जुड़ गया और सेव हो गया।")

    def update_current_lesson(self):
        script = self.script_var.get()
        old_name = self.lesson_var.get()
        new_name = self.lesson_title_entry.get().strip()
        body = self.lesson_editor_text.get("1.0", "end-1c").strip()

        if not old_name:
            messagebox.showwarning("लेसन चुनें", "अपडेट करने के लिए पहले कोई लेसन चुनें।")
            return
        if not new_name:
            messagebox.showwarning("नाम लिखें", "लेसन का नाम खाली नहीं हो सकता।")
            return
        if not body:
            messagebox.showwarning("मैटर लिखें", "लेसन का मैटर खाली नहीं हो सकता।")
            return

        if old_name != new_name and old_name in self.lessons_data[script]:
            del self.lessons_data[script][old_name]

        self.lessons_data[script][new_name] = body
        save_lessons_data(self.lessons_data)
        self.refresh_lesson_dropdown(select_name=new_name)
        self.load_selected_lesson()
        messagebox.showinfo("अपडेट हुआ", f"'{new_name}' अपडेट होकर सेव हो गया।")

    def delete_current_lesson(self):
        script = self.script_var.get()
        lesson_name = self.lesson_var.get()

        if not lesson_name:
            return
        if len(self.lessons_data[script]) <= 1:
            messagebox.showwarning("हटा नहीं सकते", f"{script} में कम से कम 1 लेसन रहना ज़रूरी है।")
            return

        confirm = messagebox.askyesno("पुष्टि करें", f"क्या आप '{lesson_name}' लेसन को हटाना चाहते हैं?")
        if not confirm:
            return

        del self.lessons_data[script][lesson_name]
        save_lessons_data(self.lessons_data)
        self.refresh_lesson_dropdown(select_first=True)
        self.load_selected_lesson()

    def load_editor_text_to_practice(self):
        script = self.script_var.get()
        body = self.lesson_editor_text.get("1.0", "end-1c").strip()
        if not body:
            return
        font_style = self.get_script_font(script, size=15)
        self.target_text.config(state=tk.NORMAL, font=font_style)
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert("1.0", body)
        self.target_text.config(state=tk.DISABLED)
        self.input_text.config(font=font_style)
        self.reset_test()

    def reset_test(self):
        self.timer_running = False
        self.start_time = None
        try:
            self.selected_duration = int(self.time_var.get())
        except ValueError:
            self.selected_duration = 60
        self.time_left = self.selected_duration
        self.timer_label.config(text=f"समय: {self.time_left}s")
        self.wpm_label.config(text="गति (WPM): 0")
        self.acc_label.config(text="सटीकता (Accuracy): 100%")
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete("1.0", tk.END)
        self.update_finger_guide()
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
        self.update_finger_guide()

        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")
        if len(typed) >= len(target):
            self.finish_test()

    def calculate_stats(self):
        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")

        if not typed:
            return

        correct_chars = sum(1 for i, ch in enumerate(typed) if i < len(target) and ch == target[i])
        accuracy = (correct_chars / len(typed)) * 100
        elapsed_minutes = max((self.selected_duration - self.time_left) / 60.0, 1 / 60.0)
        wpm = int((correct_chars / 5) / elapsed_minutes)

        self.wpm_label.config(text=f"गति (WPM): {wpm}")
        self.acc_label.config(text=f"सटीकता (Accuracy): {accuracy:.1f}%")

    def finish_test(self):
        self.timer_running = False
        self.clear_key_highlights()
        self.input_text.config(state=tk.DISABLED)
        self.calculate_stats()
        messagebox.showinfo(
            "परिणाम (Result)",
            f"टेस्ट पूरा हुआ!\n\n{self.wpm_label.cget('text')}\n{self.acc_label.cget('text')}",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = OfflineTypingTutor(root)
    root.mainloop()
