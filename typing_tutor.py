import hashlib
import json
import os
import random
import sys
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


APP_DIR = get_app_dir()
STATS_FILE = os.path.join(APP_DIR, "typing_stats.json")
USERS_FILE = os.path.join(APP_DIR, "typing_users.json")

PASS_ACCURACY_THRESHOLD = 90.0

# अपनी गोपनीय अनुमति की (Key) यहाँ रखें (इंस्टॉल के समय नहीं मांगी जाएगी)
MASTER_ACTIVATION_KEYS = {
    "ANAND-OFFLINE-2026",
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


def expand_long_lesson(seed_text, repeat_count=28):
    """हर लेसन को 4-5 पेज के बराबर लंबा (लगभग 1500-2500 शब्द/कैरेक्टर) बनाता है।"""
    parts = [seed_text.strip()]
    for i in range(2, repeat_count + 1):
        parts.append(f"[{i}] {seed_text.strip()}")
    return "  ".join(parts)


ENGLISH_SEEDS = [
    ("L1: Light Home f j", "ffjfj ffjjf jffjj jjfjf jjffj fjjfj ffjjf fjjff fjfjf fjjff jfjjf ffjjf jfjfj jjffj jffjf jffjf"),
    ("L2: Light Home d k", "ddkkd kdkdd kddkd ddkdk kdkkd dkkdk dkdkd dkkdk kddkd kddkk kkddk ddkdk dkkdd kkdkd dkdkk dkkdd"),
    ("L3: Light Home s l", "llssl sslls lssll sslls sslsl slsls llssl lssls sllss sllsl llsls slsls lslss sllsl lssls lslls"),
    ("L4: Light Home a ;", "aa;;a a;;aa ;aa;; ;;a;a ;a;a; aa;;a a;;a; a;;aa a;;a; aa;a; ;a;a; a;a;; a;;a; a;;a; a;;;a ;;a;a"),
    ("L5: Light Combo f j d k", "ffjd dkfj jdfk kdfd jfjk dksf jfkd dkfs fjjd kffj dkkd jfdk sflj dkjf kdlf jskd flkj djfs"),
    ("L6: Light Combo s l a ;", "sl;a a;ls l;as ;sla sals l;sa as;l ;las slal ;asl lsa; asla ;l;a slas ;l;a sa;l l;as a;sl"),
    ("L7: Light Home Drill 1", "asdf jkl; asdf jkl; ffjj ddkk ssll aa;; fjdk sla; ask lad fall flask salad dad sad fad"),
    ("L8: Light Keys g h", "gghhg hggdd hhggf ggffh hhjjg gghjh hhfgd ggkls hhaj; gghgh hggfg hhjkd ggsl; hhdfj gghgh"),
    ("L9: Light Home + g h", "asdfgh jkl;gh fg hj dkgf slhj afgk ;lhj ghfjdk ghsla; had flagash gag half hall dash"),
    ("L10: Light Home Full", "asdfghjkl; ;lkjhgfdsa ffjj ddkk ssll aa;; gghh ask dad lad gag had jakal flask salad dash"),
    ("L11: Light Home Rhythm", "ffjjddkkssllaa;;gghh fjdksl;gh asdfghjkl; ask lad fall flask salad dad sad fad gag half"),
    ("L12: Light Top r u", "rruur urrur uruur rruur urrur rruur rruur urrur urrur rruur urrur urrur urruu uurru urrur"),
    ("L13: Light Top e i", "eeiie ieeii ieeie eeiei eieie eieie eeiie ieeie eii ee eieil ieeie ieeie ieeii iieei ieeie"),
    ("L14: Light Top w o", "wwoow owwow owwow wwoow owwow owwow wwoow owwow owwow wwoow owwow owwow wwoow oowwo owwow"),
    ("L15: Light Top q p", "qqppq pqqpp pqqpp qqppq pqqpp pqqpp qqppq pqqpp pqqpp qqppq pqqpp pqqpp qqppq ppqqp pqqpp"),
    ("L16: Light Top r u e i", "ru ei ruei iure erui irue ruri eiei ruie ireu ruer eiru urie euri rieu urei riee urii"),
    ("L17: Light Top w o q p", "wo qp woqp pqow owpq qpow wowo qpqp woip qopu wopo qpip owqo pqwo wopq qpow woow qppq"),
    ("L18: Light Top Drill", "qwertyuiop poiuytrewq qwer tyui opqw erui wopq true wire quiet power poor rope pour pure"),
    ("L19: Light Top + Home", "qwerty asdf uiop jkl; qwer asdf tyui jkl; opqw ;lkj true wire quiet power ask lad fall"),
    ("L20: Light Simple Words", "the two quick red foxes jump over the dark logs at four or five quiet hours each day with care"),
    ("L21: Light Top Complete", "qwertyuiop qwertyuiop poiuytrewq poiuytrewq qwer tyui opqw erui wopq true wire quiet power"),
    ("L22: Light Home + Top", "asdf qwerty jkl; uiop fjdk ruei sl;a wopq ghhj qwer tyui opqw true wire quiet power ask"),
    ("L23: Light Speed Words", "the quick brown fox jumps over the lazy dog while four quiet workers type fast and clear words"),
    ("L24: Light Accuracy Drill", "as df jk l; qw er ty ui op qwer asdf tyui jkl; opqw ;lkj fjdk ruei sl;a wopq ghhj true"),
    ("L25: Light Bottom v m", "vvm mv mvv mv mvv vm mvv mv mvv vm mvv mv mvv vm mvv mv mvv vm mvv mv mvv vm mvv mv mvv"),
    ("L26: Light Bottom c ,", "cc,,c ,cc,, ,cc,, cc,c ,c,c ,c,c cc,,c ,c,c c,,cc cc,,c ,c,c ,c,c cc,,, cc,c cc,c cc,,c"),
    ("L27: Light Bottom x .", "xx..x .xx.. .xx.. xx.x .x.x .x.x xx..x .x.x x..xx xx..x .x.x .x.x xx... xx.x xx.x xx..x"),
    ("L28: Light Bottom z /", "zz//z /zz// /zz// zz/z /z/z /z/z zz//z /z/z z//zz zz//z /z/z /z/z zz/// zz/z zz/z zz//z"),
    ("L29: Light Bottom v m c ,", "vm c, vm,c cm,v mvc, cvm, vmc, ,mvc c,vm mv,c cv,m vmcm ,c,c vmmv c,vm mvc, cv,m vmc,"),
    ("L30: Light Bottom x . z /", "x. z/ x./z zx/. .xz/ z/x. x.z/ /zx. .z/x zx.z /.x/ x.x. z/z/ x.z/ /zx. .z/x zx/. x.z/"),
    ("L31: Medium Keys b n", "bbnnb nbbnn nbbnn bbnbn bnbnb bnbnb bbnnb nbbnb bnnbb bbnnb nbbnn nbbnn bbnnn bbnbn bbnbn"),
    ("L32: Medium Drill v m c , b", "vmc,b bvmc cbmv mvbc ,bcv vmbc bcmv ,vmc bcbm vmbc ,cvm bcvn mvbc vmbc bcmv ,vmc bcbm"),
    ("L33: Medium Drill x . z / n", "x.z/n nx.z /nx. .znx z/nx x.nz /nzx .n/z zx.n /.x/n x.n. z/n/ x.nz /nzx .n/z zx.n x.nz"),
    ("L34: Medium Bottom Row Full", "zxcvbnm,./ zxcvbnm,./ /.,mnbvcxz /.,mnbvcxz zxcv bnm, ./zxcv vbm, cxz. bnm/ zxcv bnm,"),
    ("L35: Medium Home + Bottom", "asdf zxcv jkl; bnm, fjdk vmc, sl;a x.z/ ghhj bnm, zxcv bnm, ask lad fall flask zxcv vbm,"),
    ("L36: Medium 3 Rows Basic", "asdf qwerty zxcv jkl; uiop bnm, the quick brown fox jumps over the lazy dog zxcvbnm,./"),
    ("L37: Medium 3 Rows Mix", "asdfghjkl; qwertyuiop zxcvbnm,./ the quick brown fox jumps over the lazy dog pack box five dozen"),
    ("L38: Medium Shift Home", "AS DF JK L; ASDF JKL; FJDK SLA; GH HJ ASK LAD FALL FLASK SALAD DAD SAD FAD ASDF JKL;"),
    ("L39: Medium Shift Top", "QW ER TY UI OP QWERTY UIOP RUEI WOPQ TRUE WIRE QUIET POWER ROPE POUR PURE QWERTY UIOP"),
    ("L40: Medium Shift + 3 Rows", "The Quick Brown Fox Jumps Over The Lazy Dog. ASDF JKL; QWERTY UIOP ZXCV BNM. Practice Makes Perfect."),
    ("L41: Medium Shift Bottom", "ZX CV BN M ZXCV BNM VMC, X.Z/ BNM, ZXCVBNM ZXC VBNM VMCB XZN. BNM. ZXCV BNM VMC, X.Z/"),
    ("L42: Medium Symbols 1", ':" <> ? {} | :"<>?{}| :";\' ,.<> /?., [{]} \\| :";\' ,.<> /?., [{]} \\|'),
    ("L43: Medium Shift + Home", "FJDK SLA; ASDF JKL; THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. ACCURACY AND SPEED GROW DAILY."),
    ("L44: Medium Shift + Top", "QWERTY UIOP RUEI WOPQ THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. KEEP FINGERS ON HOME ROW."),
    ("L45: Medium Shift + Bottom", "ZXCV BNM,./ VMC, X.Z/ THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. DO NOT LOOK AT KEYBOARD."),
    ("L46: Medium Shift Words", 'The Quick Brown Fox Jumps Over The Lazy Dog! "Practice, Patience, and Precision" build speed.'),
    ("L47: Medium Numbers 1-4", "1122 3344 1234 4321 1212 3434 1324 4231 1122 3344 1234 4321 1212 3434 1324 4231 1122 3344"),
    ("L48: Medium Numbers 5-6", "5566 5656 6565 5665 6556 5566 5656 6565 5665 6556 5566 5656 6565 5665 6556 5566 5656 6565"),
    ("L49: Medium Numbers 1-6", "123456 654321 12 34 56 135 246 14 25 36 123456 654321 12 34 56 135 246 14 25 36 123456"),
    ("L50: Medium Numbers 7-0", "7788 9900 7890 0987 7878 9090 7980 0897 7788 9900 7890 0987 7878 9090 7980 0897 7788 9900"),
    ("L51: Medium Full Numbers", "1234567890 0987654321 123 456 789 012 10 20 30 40 50 60 70 80 90 100 2026 1989 1991"),
    ("L52: Medium Symbols !@#$%^", "!@#$%^ ^%$#@! !@ #$ %^ !@# $%^ !@ #$ %^ !@#$%^ ^%$#@! !@ #$ %^ !@# $%^ !@#$%^"),
    ("L53: Medium Symbols &*()_+", "&*()_+ +_)(*& &* () _+ &*( )_+ &* () _+ &*()_+ +_)(*& &* () _+ &*( )_+ &*()_+"),
    ("L54: Medium Shift + Numbers", "!@#$%^&*()_+ +_)(*&^%$#@! 1234567890 !@# $%^ &*( )_+ 2026 @ 100% #1 & #2 (Test) [Done]"),
    ("L55: Medium Office Numbers", "Order #1024 dated 20-11-2026 has 350 items at Rs. 45 each. Total amount is Rs. 15,750 only."),
    ("L56: Medium Record Numbers", "Ref. No. 88/2026: Please verify 12 files, 45 pages, and 90 records before 05:30 PM today."),
    ("L57: Medium Speed Para 1", "Consistent daily practice builds muscle memory in your fingers. Focus first on accuracy rather than raw speed, and your typing speed will grow naturally over time."),
    ("L58: Medium Speed Para 2", "Good posture, relaxed shoulders, and light keystrokes prevent fatigue during long typing sessions. Keep your eyes on the screen or source text instead of looking down at the keys."),
    ("L59: Medium Speed Para 3", "In office and administrative work, accuracy matters as much as speed. A single wrong number or spelling mistake in a report or record can cause unnecessary delay."),
    ("L60: Medium Intensive Para", "Every word you type smoothly is a step toward mastery. Keep practicing home row, top row, and bottom row combinations until your hands move effortlessly across the keyboard."),
    ("L61: Hard Rhythm & Pace", "Rhythm and steady pace help maintain high accuracy even when typing unfamiliar words or longer sentences. Stay calm when you make an error and correct it cleanly without breaking focus."),
    ("L62: Hard Endurance Para", "Longer passages test both concentration and stamina. Breathe steadily, keep your wrists straight, and maintain a balanced speed from the beginning to the end of every timed test."),
    ("L63: Hard Numbers & Punct", "10, 20, 30, 40, 50; 100, 250, 500, 1000. Date: 20/11/2026; Time: 16:20; Code: KT-80-MN; Ref: #4092."),
    ("L64: Hard Digits & Codes", "7890, 8901, 9012, 7089, 8097, 9870, 1234567890, 0987654321, Ref-2026/11/20, Batch-A1/B2."),
    ("L65: Hard Statistical Para", "Record ID #4092 (2026): 1,250 units processed with 99.4% accuracy in 05:00 minutes across sub-division registers."),
    ("L66: Hard Number Drills", "11 22 33 44 55 66 77 88 99 00 123 456 789 012 345 678 901 2026 100 500 1000 98765 54321"),
    ("L67: Hard Slash & Quotes", 'a/b c/d e/f ? / : ; \' " a/b ? c:d ; e\'f " 1/2 3/4 5/6 7/8 9/10 "Hello, World!" \'Test\''),
    ("L68: Hard Hyphen & Brackets", "well-known, up-to-date, day-to-day, co-worker; item-1, item-2, item-3; [draft], [final], (check)."),
    ("L69: Hard Colon & Quotes", "it's, don't, can't, won't, user's, file's, system's; status: active, pending, completed."),
    ("L70: Hard Underscore & Code", "file_name_01, lesson_80, typing_tutor, user_data, error_stats, test_mode_v1, verification_key."),
    ("L71: Hard Shift + Symbols", '! @ # $ % ^ & * ( ) _ + ~ | { } : " < > ? 1 2 3 4 5 6 7 8 9 0 !@#$%^&*()_+'),
    ("L72: Hard Full Keyboard", 'The quick brown fox jumps over the lazy dog 1234567890 !@#$%^&*()_+-=[]{}|;:\'",./<>?'),
    ("L73: Hard Speed Passage", "Practice typing complete sentences with numbers, punctuation, and capital letters without pausing to look at your hands. Steady rhythm leads to higher net speed and dependable accuracy."),
    ("L74: Hard Accuracy Passage", "Careful attention to every keystroke improves both speed and reliability. Check spelling, spacing, and punctuation so every paragraph is clean, complete, and error-free under pressure."),
    ("L75: Hard General Para", "Learning to type without looking at the keyboard takes patience at first, but once your fingers learn the exact positions of each key, typing becomes effortless. Start slowly, keep your fingers curved over the home row, and build consistency every single day."),
    ("L76: Hard Office Para", "Proper documentation and timely record maintenance are essential in every administrative office. Every application, register entry, and reference number should be recorded accurately so that files can be retrieved quickly whenever verification or review is required."),
    ("L77: Hard Legal Para", "During proceedings and hearings, clear and accurate records play a vital role. Statements, dates, case numbers, and annexures must be entered carefully without altering meanings, ensuring complete clarity for future reference and official orders."),
    ("L78: Hard Speed Test Para", "A skilled typist balances speed with precision. Rushing blindly often leads to frequent mistakes and extra time spent fixing errors, whereas a smooth, controlled rhythm delivers higher net words per minute and cleaner final text."),
    ("L79: Hard Endurance Para", "Sustained focus over several minutes is key to performing well in timed typing tests. Keep your breathing steady, relax your fingers between words, and read a few words ahead so your hands keep moving smoothly across the rows."),
    ("L80: Hard Final Master Para", "Mastering touch typing is a practical lifelong skill that saves time every day in drafting, coding, data entry, and correspondence. Regular practice across letters, numbers, symbols, and full paragraphs prepares you for any speed or accuracy test with confidence."),
]

KRUTIDEV_SEEDS = [
    ("L1: Light Kruti f j", "ffjjf jffjj ffjfj jjffj fjjfj ffjjf jffjf fjfjf jffjj ffjfj jjfjf fjjff ffjjf jffjf fjfjf"),
    ("L2: Light Kruti d k", "ddkkd kdkdd kddkd ddkdk kdkkd dkkdk dkdkd dkkdk kddkd kddkk kkddk ddkdk dkkdd kkdkd dkdkk"),
    ("L3: Light Kruti s l", "llssl sslls lssll sslls sslsl slsls llssl lssls sllss sllsl llsls slsls lslss sllsl lssls"),
    ("L4: Light Kruti a ;", "aa;;a a;;aa ;aa;; ;;a;a ;a;a; aa;;a a;;a; a;;aa a;;a; aa;a; ;a;a; a;a;; a;;a; a;;a; a;;;a"),
    ("L5: Light Kruti f j d k", "ffjd dkfj jdfk kdfd jfjk dksf jfkd dkfs fjjd kffj dkkd jfdk sflj dkjf kdlf jskd flkj"),
    ("L6: Light Kruti s l a ;", "sl;a a;ls l;as ;sla sals l;sa as;l ;las slal ;asl lsa; asla ;l;a slas ;l;a sa;l l;as"),
    ("L7: Light Home Drill 1", "d s h f t y r k l ; d s h f t y r k l ; dkj dkj gkj lkj dgk fdj fdj fdl jkl;"),
    ("L8: Light Kruti g h", "gghhg hggdd hhggf ggffh hhjjg gghjh hhfgd ggkls hhaj; gghgh hggfg hhjkd ggsl; hhdfj"),
    ("L9: Light Home + g h", "dsghf tlyrk ;gh fg hj dkgf slhj afgk ;lhj ghfjdk ghsla; dkj gkj lkj dgk hkj gsj"),
    ("L10: Light Home Full", "d s h f t y r k l ; ; l k j h g f d s a dkj gkj lkj dgk fdj fdl hkj gsj flk dsl"),
    ("L11: Light Home Speed", "dkj gkj lkj dgk fdj fdj fdl hkj gsj d s h f t y r k l ; ; l k j h g f d s a"),
    ("L12: Light Top r u", "rruur urrur uruur rruur urrur rruur rruur urrur urrur rruur urrur urrur urruu uurru"),
    ("L13: Light Top e i", "eeiie ieeii ieeie eeiei eieie eieie eeiie ieeie eii ee eieil ieeie ieeie ieeii iieei"),
    ("L14: Light Top w o", "wwoow owwow owwow wwoow owwow owwow wwoow owwow owwow wwoow owwow owwow wwoow oowwo"),
    ("L15: Light Top q p", "qqppq pqqpp pqqpp qqppq pqqpp pqqpp qqppq pqqpp pqqpp qqppq pqqpp pqqpp qqppq ppqqp"),
    ("L16: Light Top r u e i", "ru ei ruei iure erui irue ruri eiei ruie ireu ruer eiru urie euri rieu urei riee"),
    ("L17: Light Top w o q p", "wo qp woqp pqow owpq qpow wowo qpqp woip qopu wopo qpip owqo pqwo wopq qpow woow"),
    ("L18: Light Top Drill", "q w e r t y u i o p p o i u y t r e w q ruel wopq qwer tyui opqw pqr uio ewr tyo"),
    ("L19: Light Top + Home", "qwer asdf tyui jkl; opqw ;lkj dkj gkj lkj ruel wopq pqr uio d s h f t y r k l ;"),
    ("L20: Light Top + Home Mix", "dkj ruel gkj wopq lkj pqr dgk uio fdj tyui hkj ruei d s h f t y r k l ; q w e r"),
    ("L21: Light Top Complete", "q w e r t y u i o p q w e r t y u i o p p o i u y t r e w q ruel wopq qwer tyui"),
    ("L22: Light Home + Top", "asdf qwer jkl; tyui dkj ruel gkj wopq lkj pqr dgk uio q w e r t y u i o p d s h f"),
    ("L23: Light Home + Top Speed", "dkj ruel gkj wopq lkj pqr dgk uio fdj tyui hkj ruei qwer tyui asdf jkl; dkj gkj"),
    ("L24: Light Home + Top Acc", "ds hf tj yk l; qw er ty ui op qwer asdf tyui jkl; opqw ;lkj dkj ruel gkj wopq"),
    ("L25: Light Bottom v m", "vvm mv mvv mv mvv vm mvv mv mvv vm mvv mv mvv vm mvv mv mvv vm mvv mv mvv vm mvv"),
    ("L26: Light Bottom c ,", "cc,,c ,cc,, ,cc,, cc,c ,c,c ,c,c cc,,c ,c,c c,,cc cc,,c ,c,c ,c,c cc,,, cc,c cc,c"),
    ("L27: Light Bottom x .", "xx..x .xx.. .xx.. xx.x .x.x .x.x xx..x .x.x x..xx xx..x .x.x .x.x xx... xx.x xx.x"),
    ("L28: Light Bottom z /", "zz//z /zz// /zz// zz/z /z/z /z/z zz//z /z/z z//zz zz//z /z/z /z/z zz/// zz/z zz/z"),
    ("L29: Light Bottom v m c ,", "vm c, vm,c cm,v mvc, cvm, vmc, ,mvc c,vm mv,c cv,m vmcm ,c,c vmmv c,vm mvc, cv,m"),
    ("L30: Light Bottom x . z /", "x. z/ x./z zx/. .xz/ z/x. x.z/ /zx. .z/x zx.z /.x/ x.x. z/z/ x.z/ /zx. .z/x zx/."),
    ("L31: Medium Keys b n", "bbnnb nbbnn nbbnn bbnbn bnbnb bnbnb bbnnb nbbnb bnnbb bbnnb nbbnn nbbnn bbnnn bbnbn"),
    ("L32: Medium Drill v m c , b", "vmc,b bvmc cbmv mvbc ,bcv vmbc bcmv ,vmc bcbm vmbc ,cvm bcvn mvbc vmbc bcmv ,vmc"),
    ("L33: Medium Drill x . z / n", "x.z/n nx.z /nx. .znx z/nx x.nz /nzx .n/z zx.n /.x/n x.n. z/n/ x.nz /nzx .n/z zx.n"),
    ("L34: Medium Bottom Full", "zxcvbnm,./ zxcvbnm,./ /.,mnbvcxz /.,mnbvcxz zxcv bnm, ./zxcv vbm, cxz. bnm/ zxcv"),
    ("L35: Medium Home + Bottom", "asdf zxcv jkl; bnm, vmc, x.z/ zxcv bnm, dkj gkj lkj dgk zxcvbnm,./ d s h f t y"),
    ("L36: Medium 3 Rows Basic", "asdf qwer zxcv jkl; tyui bnm, zxcvbnm,./ qwer tyui asdf jkl; dkj ruel gkj wopq"),
    ("L37: Medium 3 Rows Mix", "fdrkuh] fdrkuh] vf/kdkjh dk;kZy; vfHkys[k vkns'k lwpuk izfrosnu dkj gkj lkj dgk fdj"),
    ("L38: Medium Shift Home", "AS DF JK L; ASDF JKL; D K S L F J G H ASDF JKL; D K S L F J G H"),
    ("L39: Medium Shift Top", "QW ER TY UI OP QWERTY UIOP R T E W Y U I O P Q QWERTY UIOP R T E W Y U I O P Q"),
    ("L40: Medium Shift + 3 Rows", "vf/kdkjh dk;kZy; vfHkys[k vkns'k lwpuk izfrosnu Kku {ks= Jheku fdrkuh] fdrkuh]"),
    ("L41: Medium Shift Bottom", "ZX CV BN M ZXCV BNM VMC, X.Z/ BNM, ZXCVBNM ZXC VBNM VMCB XZN. BNM."),
    ("L42: Medium Symbols 1", ':" <> ? {} | :"<>?{}| :";\' ,.<> /?., [{]} \\| :";\' ,.<> /?., [{]} \\|'),
    ("L43: Medium Shift + Home", "vf/kdkjh dk;kZy; vfHkys[k vkns'k lwpuk izfrosnu dkj gkj lkj dgk fdj fdl hkj gsj"),
    ("L44: Medium Shift + Top", "vkns'k lwpuk izfrosnu vf/kdkjh dk;kZy; vfHkys[k ruel wopq qwer tyui opqw"),
    ("L45: Medium Shift + Bottom", "Kku {ks= Jheku zxcv bnm, vmc, x.z/ zxcvbnm,./ vbm, cxz. bnm/"),
    ("L46: Medium Office Line", "Hkwfe lq/kkj mi&lekgrkZ U;k;ky; esa nkf[ky&[kkfjt vihy okn dh lquokbZ dh tkrh gSA"),
    ("L47: Medium Numbers 1-4", "1122 3344 1234 4321 1212 3434 1324 4231 1122 3344 1234 4321 1212 3434 1324 4231"),
    ("L48: Medium Numbers 5-6", "5566 5656 6565 5665 6556 5566 5656 6565 5665 6556 5566 5656 6565 5665 6556"),
    ("L49: Medium Numbers 1-6", "123456 654321 12 34 56 135 246 14 25 36 123456 654321 12 34 56 135 246 14 25 36"),
    ("L50: Medium Numbers 7-0", "7788 9900 7890 0987 7878 9090 7980 0897 7788 9900 7890 0987 7878 9090 7980 0897"),
    ("L51: Medium Full Numbers", "1234567890 0987654321 123 456 789 012 10 20 30 40 50 60 70 80 90 100 2026 1989 1991"),
    ("L52: Medium Symbols !@#$%^", "!@#$%^ ^%$#@! !@ #$ %^ !@# $%^ !@ #$ %^ !@#$%^ ^%$#@! !@ #$ %^ !@# $%^"),
    ("L53: Medium Symbols &*()_+", "&*()_+ +_)(*& &* () _+ &*( )_+ &* () _+ &*()_+ +_)(*& &* () _+ &*( )_+"),
    ("L54: Medium Shift + Numbers", "!@#$%^&*()_+ +_)(*&^%$#@! 1234567890 !@# $%^ &*( )_+ 2026 @ 100% #1 & #2"),
    ("L55: Medium Office Numbers", "vkns'k la[;k 1024 fnukad 20-11-2026 ds rgr 350 vfHkys[kksa dh tkap 45 fnuksa esa iw.kZ djuh gSA"),
    ("L56: Medium Record Numbers", "lanHkZ la[;k 88/2026% 12 Qkbyksa] 45 i`\"Bksa vkSj 90 vfHkys[kksa dk lR;kiu vkt 05%30 cts rd djsaA"),
    ("L57: Medium Speed Para 1", "izfrfnu vH;kl djus ls m¡xfy;ksa dh xfr vkSj lVhdrk nksuksa esa lq/kkj gksrk gSA tYnckth ds ctk; 'kq)rk ij /;ku nsaA"),
    ("L58: Medium Speed Para 2", "dk;kZy;hu dk;Z esa lgh orZuh vkSj le;c)rk cgqr egRoiw.kZ gksrh gSA fdlh Hkh vkns'k ;k izfrosnu esa =qfV ls cpkuk pkfg,"),
    ("L59: Medium Speed Para 3", "vfHkys[kksa ds lR;kiu rFkk iathdj.k dk dk;Z fu;ekuqlkj vkSj ikjn'khZ rjhds ls fd;k tkuk pkfg, rkfd vkosndksa dks lqfo/kk feysA"),
    ("L60: Medium Intensive Para", "Hkwfe lq/kkj mi&lekgrkZ U;k;ky; esa nkf[ky&[kkfjt vihy okn dh lquokbZ dh tkrh gSA vfHkys[kksa dh tkap dj fu;ekuqlkj vkns'k ikfjr fd;k tkrk gSA"),
    ("L61: Hard Rhythm & Pace", "yk; vkSj lUrqfyr xfr ls Vkbfiax djus ij yacs vuqPNsn Hkh vklkuh ls vkSj fcuk FkdkoV ds fy[ks tk ldrs gSaA"),
    ("L62: Hard Endurance Para", "yEcs le; rd Vkbfiax djrs le; dafY;ksa dks lh/kk j[ksa] m¡xfy;ksa dks gYdk j[ksa vkSj lkszr eSVj ij /;ku cuk, j[ksaA"),
    ("L63: Hard Numbers & Punct", "10] 20] 30] 40] 50! 100] 250] 500] 1000A fnukad% 20/11/2026! le;% 16%20! dksM% KT-80-MN!"),
    ("L64: Hard Digits & Codes", "7890] 8901] 9012] 7089] 8097] 9870] 1234567890] 0987654321] lanHkZ-2026/11/20A"),
    ("L65: Hard Record Accuracy", "vfHkys[k la[;k #4092 (2026)% 1]250 enksa dk fuLrkj.k 99.4% 'kq)rk ds lkFk 05%00 feuV esa fd;k x;kA"),
    ("L66: Hard Number Drills", "11 22 33 44 55 66 77 88 99 00 123 456 789 012 345 678 901 2026 100 500 1000"),
    ("L67: Hard Slash & Quotes", 'd/k [k/x p/N ? / % ! \' " d/k ? p%N ! [k\'x " 1/2 3/4 5/6 7/8 9/10 "dk;kZy;" \'vkns\'k\''),
    ("L68: Hard Hyphen & Brackets", "mi&lekgrkZ] nkf[ky&[kkfjt] fnu&izfrfnu! en-1] en-2] en-3! izk:] vafre] tkapA"),
    ("L69: Hard Colon & Quotes", "vf/kdkjh% dk;kZy;% vfHkys[k% vkns'k% izfrosnu% lwpuk% fLFkfr% lfØ;] yafcr] iw.kZA"),
    ("L70: Hard Underscore & Code", "Qkby_01] ikB_80] Vkbfiax_V~;wVj] ;wtj_MsVk] =kqfV_LVSV] eksM_v1A"),
    ("L71: Hard Shift + Symbols", '! @ # $ % ^ & * ( ) _ + ~ | { } % " < > ? 1 2 3 4 5 6 7 8 9 0'),
    ("L72: Hard Full Keyboard", "Hkwfe lq/kkj mi&lekgrkZ U;k;ky; esa 2026 esa 1234567890 vfHkys[kksa dk lR;kiu fd;k x;kA"),
    ("L73: Hard Speed Passage", "fcuk dhcksMZ ns[ks Vkbfiax djus dk vH;kl djus ls xfr vkSj lVhdrk nksuksa esa rsth ls c<+ksrjh gksrh gSA"),
    ("L74: Hard Accuracy Passage", "izR;sd 'kCn vkSj ek=k dks /;kuiwoZd ns[kdj Vkbfiax djsa rkfd vafre eSVj iwjh rjg 'kq) vkSj =qfVjfgr gksA"),
    ("L75: Hard General Para", "fcuk dhcksMZ ns[ks Vkbfiax lh[kus esa 'kq#vkr esa /kS;Z dh vko';drk gksrh gS] ysfdu tc m¡xfy;ksa dks izR;sd dh dh lgh fLFkfr ;kn gks tkrh gS rks Vkbfiax vklku gks tkrh gSA izfrfnu fu;fer vH;kl djrs jguk pkfg,A"),
    ("L76: Hard Office Para", "iz'kklfud dk;kZy;ksa esa vfHkys[kksa dk lgh la/kkj.k vkSj le; ij lR;kiu vR;ar vko';d gSA izR;sd vkosnu] iath izfof\"V vkSj lanHkZ la[;k dks 'kq)rk ls ntZ fd;k tkuk pkfg, rkfd vko';drk iM+us ij Qkby rqjUr miyC/k gks ldsA"),
    ("L77: Hard Legal Para", "U;kf;d vkSj jktLo oknksa dh lquokbZ ds nkSjku Li\"V vkSj lVhd vfHkys[k egRoiw.kZ Hkwfedk fuHkkmrs gSaA c;ku] frfFk;ka] okn la[;k vkSj layXu dkxtkrksa dks lko/kkuh ls ntZ djuk pkfg, rkfd vkns'k ikfjr djus esa dksbZ Hkze u jgsA"),
    ("L78: Hard Speed Test Para", ",d dq'ky VkbfiLV xfr vkSj 'kq)rk ds chp lUrqyu cuk, j[krk gSA fcuk lksps rs\"k Vkbfiax djus ls vf/kd =qfV;ka gksrh gSa] tcfd fLFkj vkSj fu;af=r y; ls vf/kd 'kq) xfr vkSj lkQ eSVj izkIr gksrk gSA"),
    ("L79: Hard Endurance Para", "yEcs le; rd ,dkxzrk cuk, j[kuk le;c) Vkbfiax ijh{kk esa vPNs izn'kZu dh dqath gSA 'kCnksa ds chp m¡xfy;ksa dks gYdk j[ksa vkSj vkxs ds 'kCnksa ij utj j[ksa rkfd gkFk lqpk: :i ls pyrs jgsaA"),
    ("L80: Hard Final Master Para", "Li'kZ Vkbfiax ,d O;kogkfjd dkS'ky gS tks izfrfnu Mªkf¶Vax] MsVk ,aVªh vkSj i=kpkj esa le; cprk gSA v{kjksa] ek=kvksa] vadksa vkSj iwjs vuqPNsnksa dk fu;fer vH;kl vkidks fdlh Hkh ijh{kk ds fy, rS;kj djrk gSA"),
]

MANGAL_SEEDS = [
    ("L1: Light Mangal ि र", "किर रकि ककिर ररकिर किरर रककिर किरक ररकक ककरक ररकक रककिर ककिरक रकिरक ररककिर रककिर"),
    ("L2: Light Mangal ा क", "काका काकका ककाका काकाक ककाका काकका काकका काकका ककाका काकका काकका काकका काकका काकका काकका"),
    ("L3: Light Mangal े स", "सेसे सेससे सेसेस सेसेक सेससे सेसेस सेसेस सेससे सेसेस सेससे सेससे सेसेस सेससे सेसेस सेससे"),
    ("L4: Light Mangal ं य", "यंयं यंययं यंयंय यंयंयं यंयंय यंयंय यंयंय यंयंय यंयंय यंयंय यंयंय यंयंय यंयंय यंयंय यंयंय"),
    ("L5: Light क का कि की", "क का कि की काक किक कीक किका काकि किकि कीकी ककाक किकाक कि की का की कि की काक किक कीक किका"),
    ("L6: Light स से यं य", "स से यं य सस सेसे यंयं यय सयं सेयं यसं यंसे सेयं ससे यंय सस सेसे यंयं यय सयं सेयं यसं"),
    ("L7: Light क ख ग घ", "क ख ग घ च छ ज झ ट ठ ठ ज च घ ख क ग घ च छ ज झ ट ठ कख गघ चछ जझ टठ कग चज टठ घझ"),
    ("L8: Light ु ू", "कु कू कुकु कुकू कुकुउ कुकूउ कुकुक कुकूउ कुकुक कुकूउ कुकूउ कुकुक कुकुक कुकूउ कुकुक कुकूउ कुकुक"),
    ("L9: Light Home + ु ू", "क ख ग घ च छ ज झ ट ठ कु कू कख गघ चछ जझ टठ कुकू कग चज टठ घझ छठ कुकू कुकुक कखगघ"),
    ("L10: Light Home Full", "क ख ग घ च छ ज झ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श ष स ह कख गघ चछ जझ टठ तथ दध"),
    ("L11: Light Home Speed", "कख गघ चछ जझ टठ तथ दध पफ बभ मय रल क ख ग घ च छ ज झ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल"),
    ("L12: Light त न", "तत नन तन नत तनत नतन तनन तत नन तन नत तनत नतन तनन तत नन तन नत तनत नतन तनन तत नन"),
    ("L13: Light म प", "मम पप मप पम मपम पमप पम्म मम पप मप पम मपम पमप पम्म मम पप मप पम मपम पमप पम्म मम पप"),
    ("L14: Light ू व", "वव वू ववू वूव ववूव वूवव ववू वव वू ववू वूव ववूव वूवव ववू वव वू ववू वूव ववूव वूवव ववू"),
    ("L15: Light ु च", "चच चु चचु चुच चचुच चुचच चचु चच चु चचु चुच चचुच चुचच चचु चच चु चचु चुच चचुच चुचच चचु"),
    ("L16: Light त न म प", "तन मप तमन पनत मनप पतम नतप मतन पमत तपन नमत तनम पमन तन मप तमन पनत मनप पतम नतप मतन"),
    ("L17: Light व च ु ू", "वच चव वुच चुव वूच चूप वचव चुवच वुचव चवु वच चव वुच चुव वूच चूप वचव चुवच वुचव चवु"),
    ("L18: Light Top Row", "प व च त न म पवन चमन नमन वतन चरण तपन पवन चमन नमन वतन चरण तपन पवन चमन नमन वतन चरण"),
    ("L19: Light Top + Home", "पवन चमन नमन वतन चरण तपन कमल नयन घर चल अब कल फल जल मन धन कर भर पवन चमन नमन वतन"),
    ("L20: Light Top + Home Mix", "कमल नयन घर चल अब कल फल जल पवन चमन नमन वतन चरण तपन मन धन कर भर हर पल जन धन वन"),
    ("L21: Light Top Complete", "प व च त न म र ल व स य ह पवन चमन नमन वतन चरण तपन सरस सरल नगर खबर महल कलम पवन चमन"),
    ("L22: Light Home + Top", "कमल नयन घर चल पवन चमन नमन वतन सरस सरल नगर खबर महल कलम अब कल फल जल मन धन कर भर"),
    ("L23: Light Home + Top Speed", "कमल नयन घर चल पवन चमन नमन वतन चरण तपन सरस सरल नगर खबर महल कलम मन धन कर भर हर पल"),
    ("L24: Light Home + Top Acc", "कमल नयन घर चल पवन चमन नमन वतन चरण तपन सरस सरल नगर खबर महल कलम अब कल फल जल मन धन"),
    ("L25: Light अ उ", "अअ उउ अउ उअ अउअ उअउ अउउ अअ उउ अउ उअ अउअ उअउ अउउ अअ उउ अउ उअ अउअ उअउ अउउ अअ उउ"),
    ("L26: Light ब ए", "बब एए बए एब बएब एबए बएए बब एए बए एब बएब एबए बएए बब एए बए एब बएब एबए बएए बब एए"),
    ("L27: Light ग ण", "गग णण गणा णग गणाग णगण गणाग गग णण गणा णग गणाग णगण गणाग गग णण गणा णग गणाग णगण गणाग"),
    ("L28: Light र ध", "रर धध रध धर रधर धरण रधध रर धध रध धर रधर धरण रधध रर धध रध धर रधर धरण रधध रर धध"),
    ("L29: Light अ उ ब ए", "अब एब उब बए अबल एबक उबग बएव अब एब उब बए अबल एबक उबग बएव अब एब उब बए अबल एबक"),
    ("L30: Light ग ण र ध", "गर धर गण रध गरम धरम गणन रथ गर धर गण रध गरम धरम गणन रथ गर धर गण रध गरम धरम"),
    ("L31: Medium इ द", "इइ दद इद दइ इदइ दइद इदद इइ दद इद दइ इदइ दइद इदद इइ दद इद दइ इदइ दइद इदद इइ दद"),
    ("L32: Medium अ उ ब ए इ", "अब इब उब बइ अबल इबक उबग बइव अब इब उब बइ अबल इबक उबग बइव अब इब उब बइ अबल इबक"),
    ("L33: Medium ग ण र ध द", "गर दर गण दन गरम दरम गणन दशन गर दर गण दन गरम दरम गणन दशन गर दर गण दन गरम दरम"),
    ("L34: Medium Bottom Full", "अ इ उ ए ण ध ग ब द र अबल इबक उबग बएव गरम धरम गणन दशन अबल इबक उबग बएव गरम धरम"),
    ("L35: Medium Home + Bottom", "कमल नयन घर चल अबल इबक उबग बएव गरम धरम गणन दशन अब कल फल जल मन धन कर भर"),
    ("L36: Medium 3 Rows Basic", "कमल नयन घर चल पवन चमन नमन वतन अबल इबक उबग बएव गरम धरम गणन दशन सरस सरल नगर खबर"),
    ("L37: Medium 3 Rows Mix", "कमल नयन पवन चमन अबल इबक सरस सरल नगर खबर महल कलम दशन गणन घर चल अब कल फल जल मन धन"),
    ("L38: Medium Shift स्वर", "आ ई ऊ ऐ औ आऊ ईद ऊन ऐन औजार आ ई ऊ ऐ औ आऊ ईद ऊन ऐन औजार आ ई ऊ ऐ औ आऊ ईद ऊन"),
    ("L39: Medium Shift संयुक्त", "क्ष त्र ज्ञ श्र क्षमा त्रुटि ज्ञान श्रम क्ष त्र ज्ञ श्र क्षमा त्रुटि ज्ञान श्रम क्ष त्र ज्ञ श्र"),
    ("L40: Medium Shift + 3 Rows", "क्षमा त्रुटि ज्ञान श्रम आऊ ईद ऊन ऐन औजार कमल नयन पवन चमन सरस सरल नगर खबर महल कलम"),
    ("L41: Medium Shift चिह्न", "ऋषि दुःख हँसी ँच ऋषि दुःख हँसी ँच ऋषि दुःख हँसी ँच ऋषि दुःख हँसी ँच ऋषि दुःख हँसी ँच"),
    ("L42: Medium विराम चिह्न", "। , . : ; ? । , . : ; ? । , . : ; ? । , . : ; ? । , . : ; ? । , . : ; ?"),
    ("L43: Medium Shift + Home", "आऊ ईद ऊन ऐन औजार कमल नयन घर चल अब कल फल जल मन धन कर भर हर पल जन धन वन"),
    ("L44: Medium Shift + Top", "क्षमा त्रुटि ज्ञान श्रम पवन चमन नमन वतन चरण तपन सरस सरल नगर खबर महल कलम"),
    ("L45: Medium Shift + Bottom", "अबल इबक उबग बएव गरम धरम गणन दशन क्षमा त्रुटि ज्ञान श्रम आऊ ईद ऊन ऐन औजार"),
    ("L46: Medium Office Words", "अधिकारी कार्यालय अभिलेख आदेश आवेदन प्रतिवेदन सुनवाई प्रमाण पत्र संशोधन पंजीकरण क्षमा त्रुटि ज्ञान श्रम"),
    ("L47: Medium अंक १-४", "११ २२ ३३ ४४ १२३४ ४३२१ १२१२ ३४३४ १३२४ ४२३१ ११ २२ ३३ ४४ १२३४ ४३२१ १२१२ ३४३४ १३२४ ४२३१"),
    ("L48: Medium अंक ५-६", "५५ ६६ ५६५६ ६५६५ ५६६५ ६५५६ ५५ ६६ ५६५६ ६५६५ ५६६५ ६५५६ ५५ ६६ ५६५६ ६५६५ ५६६५ ६५५६"),
    ("L49: Medium अंक १-६", "१२३४५६ ६५४३२१ १२ ३४ ५६ १३५ २४६ १४ २५ ३६ १२३४५६ ६५४३२१ १२ ३४ ५६ १३५ २४६ १४ २५ ३६"),
    ("L50: Medium अंक ७-०", "७७ ८८ ९९ ०० ७८९० ०९८७ ७८७८ ९०९० ७९८० ०८९७ ७७ ८८ ९९ ०० ७८९० ०९८७ ७८७८ ९०९० ७९८० ०८९७"),
    ("L51: Medium पूरे अंक", "१२३४५६७८९० ०९८७६५४३२१ १२३ ४५६ ७८९ ०१२ १० २० ३० ४० ५० ६० ७० ८० ९० १०० २०२६ १९८९ १९९१"),
    ("L52: Medium चिह्न !@#$%^", "! @ # $ % ^ ^ $ # @ ! !@ #$ %^ !@# $%^ !@#$%^ ^%$#@! ! @ # $ % ^ ^ $ # @ !"),
    ("L53: Medium चिह्न &*()_+", "& * ( ) _ + + _ ) ( * & &* () _+ &*( )_+ &*()_+ +_)(*& & * ( ) _ + + _ ) ( * &"),
    ("L54: Medium Shift + अंक", "!@#$%^&*()_+ +_)(*&^%$#@! १२३४५६७८९० !@# $%^ &*( )_+ २०२६ @ १००% #१ & #२"),
    ("L55: Medium कार्यालय अंक", "आदेश संख्या १०२४ दिनांक २०-११-२०२६ के तहत ३५० अभिलेखों की जांच ४५ दिनों में पूर्ण करनी है।"),
    ("L56: Medium अभिलेख अंक", "संदर्भ संख्या ८८/२०२६: १२ फाइलों, ४५ पृष्ठों और ९० अभिलेखों का सत्यापन आज ०५:३० बजे तक करें।"),
    ("L57: Medium गति अनुच्छेद 1", "प्रतिदिन अभ्यास करने से उंगलियों की गति और सटीकता दोनों में सुधार होता है। जल्दबाजी के बजाय शुद्धता पर ध्यान दें।"),
    ("L58: Medium गति अनुच्छेद 2", "कार्यालयीन कार्य में सही वर्तनी और समयबद्धता बहुत महत्वपूर्ण होती है। किसी भी आदेश या प्रतिवेदन में त्रुटि से बचना चाहिए।"),
    ("L59: Medium गति अनुच्छेद 3", "अभिलेखों के सत्यापन तथा पंजीकरण का कार्य नियमानुसार और पारदर्शी तरीके से किया जाना चाहिए ताकि आवेदकों को सुविधा मिले।"),
    ("L60: Medium गहन अनुच्छेद", "भूमि सुधार उप-समाहर्ता न्यायालय में प्राप्त आवेदनों का अभिलेखीय सत्यापन समयबद्ध रूप से किया जाता है।"),
    ("L61: Hard लय व गति", "लय और संतुलित गति से टाइपिंग करने पर लंबे अनुच्छेद भी आसानी से और बिना थकावट के लिखे जा सकते हैं।"),
    ("L62: Hard धैर्य अनुच्छेद", "लंबे समय तक टाइपिंग करते समय कलाइयों को सीधा रखें, उंगलियों को हल्का रखें और स्रोत मैटर पर ध्यान बनाए रखें।"),
    ("L63: Hard अंक व विराम", "१०, २०, ३०, ४०, ५०; १००, २५०, ५००, १०००। दिनांक: २०/११/२०२६; समय: १६:२०; कोड: KT-80-MN।"),
    ("L64: Hard उच्च अंक व कोड", "७८९०, ८९०१, ९०१२, ७०८९, ८०९७, ९८७०, १२३४५६७८९०, ०९८७६५४३२१, संदर्भ-२०२६/११/२०।"),
    ("L65: Hard अभिलेख शुद्धता", "अभिलेख संख्या #४०९२ (२०२६): १,२५० मदों का निस्तारण ९९.४% शुद्धता के साथ ०५:०० मिनट में किया गया।"),
    ("L66: Hard नंबर रो ड्रिल", "११ २२ ३३ ४४ ५५ ६६ ७७ ८८ ९९ ०० १२३ ४५६ ७८९ ०१२ ३४५ ६७८ ९०१ २०२६ १०० ५०० १०००"),
    ("L67: Hard स्लैश व उद्धरण", "क/ख ग/घ च/छ ? / : ; ' \" क/ख ? च:छ ; ग'घ \" १/२ ३/४ ५/६ ७/८ ९/१० \"कार्यालय\" 'आदेश'"),
    ("L68: Hard हाइफन व कोष्ठक", "उप-समाहर्ता, दाखिल-खारिज, दिन-प्रतिदिन; मद-१, मद-२, मद-३; प्रारूप, अंतिम, जांच।"),
    ("L69: Hard विराम व स्थिति", "अधिकारी: कार्यालय: अभिलेख: आदेश: प्रतिवेदन: सूचना: स्थिति: सक्रिय, लंबित, पूर्ण।"),
    ("L70: Hard अंडरस्कोर व कोड", "फाइल_०१, पाठ_८०, टाइपिंग_ट्यूटर, यूजर_डेटा, त्रुटि_टेस्ट, मोड_v1।"),
    ("L71: Hard Shift + नंबर रो", "! @ # $ % ^ & * ( ) _ + ~ | { } : \" < > ? १ २ ३ ४ ५ ६ ७ ८ ९ ०"),
    ("L72: Hard Full Keyboard", "भूमि सुधार उप-समाहर्ता न्यायालय में २०२६ में १२३४५६७८९० अभिलेखों का सत्यापन किया गया।"),
    ("L73: Hard गति अनुच्छेद", "बिना कीबोर्ड देखे टाइपिंग करने का अभ्यास करने से गति और सटीकता दोनों में तेजी से बढ़ोतरी होती है।"),
    ("L74: Hard शुद्धता अनुच्छेद", "प्रत्येक शब्द और मात्रा को ध्यानपूर्वक देखकर टाइपिंग करें ताकि अंतिम मैटर पूरी तरह शुद्ध और त्रुटिरहित हो।"),
    ("L75: Hard सामान्य अनुच्छेद", "बिना कीबोर्ड देखे टाइपिंग सीखने में शुरुआत में धैर्य की आवश्यकता होती है, लेकिन जब उंगलियों को प्रत्येक की की सही स्थिति याद हो जाती है तो टाइपिंग आसान हो जाती है। प्रतिदिन नियमित अभ्यास करते रहना चाहिए।"),
    ("L76: Hard कार्यालय अनुच्छेद", "प्रशासनिक कार्यालयों में अभिलेखों का सही संधारण और समय पर सत्यापन अत्यंत आवश्यक है। प्रत्येक आवेदन, पंजी प्रविष्टि और संदर्भ संख्या को शुद्धता से दर्ज किया जाना चाहिए ताकि आवश्यकता पड़ने पर फाइल तुरंत उपलब्ध हो सके।"),
    ("L77: Hard न्यायालय अनुच्छेद", "न्यायिक और राजस्व वादों की सुनवाई के दौरान स्पष्ट और सटीक अभिलेख महत्वपूर्ण भूमिका निभाते हैं। बयान, तिथियां, वाद संख्या और संलग्न कागजातों को सावधानी से दर्ज करना चाहिए ताकि आदेश पारित करने में कोई भ्रम न रहे।"),
    ("L78: Hard परीक्षा अनुच्छेद", "एक कुशल टाइपिस्ट गति और शुद्धता के बीच संतुलन बनाए रखता है। बिना सोचे तेज टाइपिंग करने से अधिक त्रुटियां होती हैं, जबकि स्थिर और नियंत्रित लय से अधिक शुद्ध गति और साफ मैटर प्राप्त होता है।"),
    ("L79: Hard दीर्घ अनुच्छेद", "लंबे समय तक एकाग्रता बनाए रखना समयबद्ध टाइपिंग परीक्षा में अच्छे प्रदर्शन की कुंजी है। शब्दों के बीच उंगलियों को हल्का रखें और आगे के शब्दों पर नजर रखें ताकि हाथ सुचारु रूप से चलते रहें।"),
    ("L80: Hard अंतिम अनुच्छेद", "स्पर्श टाइपिंग एक व्यावहारिक कौशल है जो प्रतिदिन ड्राफ्टिंग, डेटा एंट्री और पत्राचार में समय बचाता है। अक्षरों, मात्राओं, अंकों और पूरे अनुच्छेदों का नियमित अभ्यास आपको किसी भी परीक्षा के लिए तैयार करता है।"),
]

ENGLISH_80 = [(title, expand_long_lesson(body, repeat_count=28)) for title, body in ENGLISH_SEEDS]
KRUTIDEV_80 = [(title, expand_long_lesson(body, repeat_count=28)) for title, body in KRUTIDEV_SEEDS]
MANGAL_80 = [(title, expand_long_lesson(body, repeat_count=28)) for title, body in MANGAL_SEEDS]

LESSONS_BY_SCRIPT = {
    "English": ENGLISH_80,
    "Kruti Dev 010": KRUTIDEV_80,
    "Mangal": MANGAL_80,
}

CATEGORIES = {
    "Beginner (L1-L30)": (0, 30),
    "Medium (L31-L60)": (30, 60),
    "Advance (L61-L80)": (60, 80),
}


def hash_password(password_text):
    return hashlib.sha256(password_text.encode("utf-8")).hexdigest()


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


def make_script_stats():
    return {"English": {}, "Kruti Dev 010": {}, "Mangal": {}}


def make_script_progress():
    return {"English": 0, "Kruti Dev 010": 0, "Mangal": 0}


def default_users():
    return {
        "active_user": "Default User",
        "users": ["Default User"],
        "passwords": {},
        "offline_licensed": {},
    }


def format_mm_ss(seconds):
    seconds = max(int(seconds), 0)
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"


class OfflineTypingTutor:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline Typing Tutor — English | Kruti Dev 010 | Mangal")
        self.root.geometry("1300x900")
        self.root.configure(bg="#eef2f6")

        self.users_data = load_json_file(USERS_FILE, default_users)
        if not self.users_data.get("users"):
            self.users_data = default_users()
        self.users_data.setdefault("passwords", {})
        self.users_data.setdefault("offline_licensed", {})

        if self.users_data.get("active_user") not in self.users_data["users"]:
            self.users_data["active_user"] = self.users_data["users"][0]

        self.all_stats = load_json_file(STATS_FILE, dict)
        self.all_progress = {}
        self.ensure_user_data(self.current_user())

        self.start_time = None
        self.timer_running = False
        self.time_left = 600
        self.selected_duration = 600
        self.word_font_size = 24
        self.key_width = 9
        self.key_height = 3
        self.key_font_size = 11
        self.key_buttons = {}
        self.space_btn = None
        self.hand_shapes = {}
        self.last_wrong_char = None
        self.strict_errors_count = 0
        self.counted_error_positions = set()
        self.current_lesson_global_index = 0
        self.app_locked = False

        self.setup_ui()
        self.bind_hidden_key_shortcut()
        self.refresh_user_dropdown()
        self.on_category_change()
        self.apply_access_state(self.current_user(), show_popup=False)

    def bind_hidden_key_shortcut(self):
        self.root.bind_all("<Control-Shift-K>", lambda e: self.prompt_hidden_access_key())
        self.root.bind_all("<Control-Shift-k>", lambda e: self.prompt_hidden_access_key())

    def current_user(self):
        return self.users_data["active_user"]

    def is_user_key_authorized(self, username):
        return bool(self.users_data.get("offline_licensed", {}).get(username, False))

    def set_controls_enabled(self, enabled):
        if not self.root.winfo_exists():
            return
        state_val = "readonly" if enabled else "disabled"
        btn_state = tk.NORMAL if enabled else tk.DISABLED
        txt_state = tk.NORMAL if enabled else tk.DISABLED

        for w in [self.script_combo, self.category_combo, self.lesson_combo, self.time_combo, self.mode_combo]:
            if w.winfo_exists():
                w.config(state=state_val)
        for b in [self.reset_btn, self.weak_btn, self.game_btn, self.add_user_btn]:
            if b.winfo_exists():
                b.config(state=btn_state)
        if self.input_text.winfo_exists():
            self.input_text.config(state=txt_state)

    def apply_access_state(self, username, show_popup=False):
        if not self.root.winfo_exists():
            return
        allowed = self.is_user_key_authorized(username)
        self.app_locked = not allowed
        if allowed:
            self.set_controls_enabled(True)
            if self.alert_label.winfo_exists():
                self.alert_label.config(text="अनुमति सक्रिय — 90%+ सटीकता पर अगला लेसन खुलेगा", fg="#15803d")
            if self.input_text.winfo_exists():
                self.input_text.focus()
        else:
            self.set_controls_enabled(False)
            self.clear_highlights()
            if self.alert_label.winfo_exists():
                self.alert_label.config(
                    text="बिना अनुमति/की के ऐप लॉक है — Ctrl+Shift+K या Help -> Activate / Key से की डालें",
                    fg="#b91c1c",
                )
            if show_popup:
                messagebox.showwarning(
                    "अनुमति आवश्यक (Locked)",
                    f"'{username}' के लिए आपकी अनुमति की (Key) सक्रिय नहीं है।\n"
                    "यह ऐप बिना आपकी अनुमति के नहीं चलाया जा सकता।",
                    parent=self.root,
                )

    def prompt_hidden_access_key(self):
        if not self.root.winfo_exists():
            return
        u = self.current_user()
        key_input = simpledialog.askstring(
            "System Verification",
            f"Enter access key for '{u}':",
            show="*",
            parent=self.root,
        )
        if not key_input:
            return
        if key_input.strip() in MASTER_ACTIVATION_KEYS:
            self.users_data.setdefault("offline_licensed", {})[u] = True
            save_json_file(USERS_FILE, self.users_data)
            self.apply_access_state(u, show_popup=False)
            self.on_category_change()
            messagebox.showinfo("Verified", f"'{u}' के लिए अनुमति सक्रिय हो गई है।", parent=self.root)
        else:
            messagebox.showerror("Invalid Key", "की (Key) सही नहीं है।", parent=self.root)

    def ensure_user_data(self, username):
        if username not in self.all_stats or not isinstance(self.all_stats[username], dict):
            self.all_stats[username] = make_script_stats()
        for script in ["English", "Kruti Dev 010", "Mangal"]:
            self.all_stats[username].setdefault(script, {})

        if username not in self.all_progress or not isinstance(self.all_progress[username], dict):
            self.all_progress[username] = make_script_progress()
        for script in ["English", "Kruti Dev 010", "Mangal"]:
            self.all_progress[username].setdefault(script, 0)

        save_json_file(STATS_FILE, self.all_stats)

    def get_unlocked_index(self, script=None):
        s = script or self.script_var.get()
        u = self.current_user()
        self.ensure_user_data(u)
        return min(int(self.all_progress[u].get(s, 0)), 79)

    def unlock_next_lesson(self, completed_idx):
        script = self.script_var.get()
        u = self.current_user()
        self.ensure_user_data(u)
        current_unlocked = int(self.all_progress[u].get(script, 0))
        if completed_idx >= current_unlocked and completed_idx + 1 < 80:
            self.all_progress[u][script] = completed_idx + 1
            return True
        return False

    def get_user_stats_for_script(self, script=None):
        s = script or self.script_var.get()
        u = self.current_user()
        self.ensure_user_data(u)
        return self.all_stats[u][s]

    def get_script_font(self, script, size=None):
        base = self.word_font_size if size is None else size
        if script == "Kruti Dev 010":
            return ("Kruti Dev 010", base + 6)
        if script == "Mangal":
            return ("Nirmala UI", base)
        return ("Consolas", base)

    def adjust_word_size(self, delta):
        self.word_font_size = max(14, min(42, self.word_font_size + delta))
        script = self.script_var.get()
        self.target_text.config(font=self.get_script_font(script, self.word_font_size))
        self.input_text.config(font=self.get_script_font(script, max(13, self.word_font_size - 2)))
        self.word_size_lbl.config(text=f"Word: {self.word_font_size}")

    def adjust_keyboard_size(self, delta):
        self.key_width = max(5, min(14, self.key_width + delta))
        self.key_font_size = max(8, min(15, self.key_font_size + delta))
        if delta > 0 and self.key_width >= 8:
            self.key_height = 3
        elif delta < 0 and self.key_width <= 6:
            self.key_height = 2

        for lbl, _, _ in self.key_buttons.values():
            lbl.config(width=self.key_width, height=self.key_height, font=("Consolas", self.key_font_size, "bold"))

        if self.space_btn:
            space_w = self.key_width * 9 + 12
            space_h = 2 if self.key_height >= 3 else 1
            self.space_btn.config(width=space_w, height=space_h, font=("Segoe UI", max(8, self.key_font_size - 1), "bold"))

        self.key_size_lbl.config(text=f"Key: {self.key_width}")

    def setup_ui(self):
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Offline Typing Tutor v1.0", parent=self.root))
        help_menu.add_command(label="Activate / Key", command=self.prompt_hidden_access_key)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

        header = tk.Frame(self.root, bg="#1e3a5f", pady=7, padx=14)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="ऑफलाइन टाइपिंग ट्यूटर (English | Kruti Dev 010 | Mangal)",
            font=("Segoe UI", 14, "bold"),
            bg="#1e3a5f",
            fg="white",
        ).pack(side=tk.LEFT)

        self.game_btn = tk.Button(
            header,
            text="गेम खेलें (Typing Game)",
            command=self.open_game_window,
            bg="#d97706",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=3,
        )
        self.game_btn.pack(side=tk.RIGHT, padx=(6, 0))

        self.weak_btn = tk.Button(
            header,
            text="कमज़ोर कीज़ प्रैक्टिस",
            command=self.practice_weak_keys,
            bg="#7c3aed",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=3,
        )
        self.weak_btn.pack(side=tk.RIGHT)

        ctrl = tk.Frame(self.root, bg="#eef2f6", pady=5, padx=12)
        ctrl.pack(fill=tk.X)

        tk.Label(ctrl, text="यूज़र:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(ctrl, textvariable=self.user_var, width=13, state="readonly")
        self.user_combo.pack(side=tk.LEFT, padx=(2, 2))
        self.user_combo.bind("<<ComboboxSelected>>", self.on_user_change)

        self.add_user_btn = tk.Button(
            ctrl,
            text="+ यूज़र",
            command=self.add_new_user,
            bg="#0f766e",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            padx=5,
            pady=1,
        )
        self.add_user_btn.pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(ctrl, text="स्क्रिप्ट:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.script_var = tk.StringVar(value="English")
        self.script_combo = ttk.Combobox(
            ctrl,
            textvariable=self.script_var,
            values=["English", "Kruti Dev 010", "Mangal"],
            width=12,
            state="readonly",
        )
        self.script_combo.pack(side=tk.LEFT, padx=(2, 6))
        self.script_combo.bind("<<ComboboxSelected>>", self.on_script_change)

        tk.Label(ctrl, text="कैटेगरी:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="Beginner (L1-L30)")
        self.category_combo = ttk.Combobox(
            ctrl,
            textvariable=self.category_var,
            values=list(CATEGORIES.keys()),
            width=16,
            state="readonly",
        )
        self.category_combo.pack(side=tk.LEFT, padx=(2, 6))
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_change)

        tk.Label(ctrl, text="लेसन:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.lesson_var = tk.StringVar()
        self.lesson_combo = ttk.Combobox(ctrl, textvariable=self.lesson_var, width=22, state="readonly")
        self.lesson_combo.pack(side=tk.LEFT, padx=(2, 6))
        self.lesson_combo.bind("<<ComboboxSelected>>", self.on_lesson_select)

        tk.Label(ctrl, text="समय:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.time_var = tk.StringVar(value="10 Min")
        self.time_combo = ttk.Combobox(
            ctrl,
            textvariable=self.time_var,
            values=["10 Min", "15 Min", "20 Min"],
            width=7,
            state="readonly",
        )
        self.time_combo.pack(side=tk.LEFT, padx=(2, 6))
        self.time_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_test())

        tk.Label(ctrl, text="मोड:", font=("Segoe UI", 9, "bold"), bg="#eef2f6").pack(side=tk.LEFT)
        self.mode_var = tk.StringVar(value="गलत पर रुकें")
        self.mode_combo = ttk.Combobox(
            ctrl,
            textvariable=self.mode_var,
            values=["गलत पर रुकें", "आगे बढ़ें"],
            width=12,
            state="readonly",
        )
        self.mode_combo.pack(side=tk.LEFT, padx=(2, 6))
        self.mode_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_test())

        word_ctrl = tk.Frame(ctrl, bg="#dbeafe", padx=3, pady=1, bd=1, relief=tk.SOLID)
        word_ctrl.pack(side=tk.LEFT, padx=2)
        tk.Button(word_ctrl, text="W-", command=lambda: self.adjust_word_size(-2), font=("Segoe UI", 8, "bold"), padx=3, pady=0).pack(side=tk.LEFT)
        self.word_size_lbl = tk.Label(word_ctrl, text=f"Word: {self.word_font_size}", font=("Segoe UI", 8, "bold"), bg="#dbeafe", fg="#1e3a8a", padx=2)
        self.word_size_lbl.pack(side=tk.LEFT)
        tk.Button(word_ctrl, text="W+", command=lambda: self.adjust_word_size(2), font=("Segoe UI", 8, "bold"), padx=3, pady=0).pack(side=tk.LEFT)

        key_ctrl = tk.Frame(ctrl, bg="#fef3c7", padx=3, pady=1, bd=1, relief=tk.SOLID)
        key_ctrl.pack(side=tk.LEFT, padx=2)
        tk.Button(key_ctrl, text="K-", command=lambda: self.adjust_keyboard_size(-1), font=("Segoe UI", 8, "bold"), padx=3, pady=0).pack(side=tk.LEFT)
        self.key_size_lbl = tk.Label(key_ctrl, text=f"Key: {self.key_width}", font=("Segoe UI", 8, "bold"), bg="#fef3c7", fg="#92400e", padx=2)
        self.key_size_lbl.pack(side=tk.LEFT)
        tk.Button(key_ctrl, text="K+", command=lambda: self.adjust_keyboard_size(1), font=("Segoe UI", 8, "bold"), padx=3, pady=0).pack(side=tk.LEFT)

        self.disable_backspace_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            ctrl,
            text="No BS",
            variable=self.disable_backspace_var,
            bg="#eef2f6",
            font=("Segoe UI", 8),
        ).pack(side=tk.LEFT, padx=2)

        self.sound_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            ctrl,
            text="बीप",
            variable=self.sound_var,
            bg="#eef2f6",
            font=("Segoe UI", 8),
        ).pack(side=tk.LEFT, padx=2)

        self.reset_btn = tk.Button(
            ctrl,
            text="रीसेट",
            command=self.reset_test,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=2,
        )
        self.reset_btn.pack(side=tk.RIGHT)

        stats_bar = tk.Frame(self.root, bg="#ea580c", pady=5, padx=10)
        stats_bar.pack(fill=tk.X, padx=14, pady=(0, 5))

        self.timer_label = tk.Label(
            stats_bar, text="10:00 Min.", font=("Segoe UI", 12, "bold"), bg="#ea580c", fg="white"
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

        guide_bar = tk.Frame(self.root, bg="#ffffff", pady=5, padx=12, bd=1, relief=tk.SOLID)
        guide_bar.pack(fill=tk.X, padx=14, pady=(0, 5))

        self.finger_label = tk.Label(
            guide_bar,
            text="उंगली गाइड: —",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#1e293b",
        )
        self.finger_label.pack(side=tk.LEFT)

        self.alert_label = tk.Label(
            guide_bar,
            text="कम से कम 90% सटीकता पर अगला लेसन खुलेगा",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#2563eb",
        )
        self.alert_label.pack(side=tk.RIGHT)

        self.target_text = tk.Text(
            self.root,
            height=4,
            font=("Consolas", self.word_font_size),
            wrap=tk.WORD,
            bg="#f8fafc",
            fg="#0f172a",
            padx=14,
            pady=10,
            bd=2,
            relief=tk.GROOVE,
        )
        self.target_text.pack(fill=tk.X, padx=14, pady=(0, 5))
        self.target_text.tag_config("correct", foreground="#15803d", background="#dcfce7")
        self.target_text.tag_config("wrong", foreground="#b91c1c", background="#fee2e2")
        self.target_text.tag_config("current", foreground="#000000", background="#93c5fd", underline=True)
        self.target_text.config(state=tk.DISABLED)

        self.input_text = tk.Text(
            self.root,
            height=2,
            font=("Consolas", self.word_font_size - 2),
            wrap=tk.WORD,
            bg="#ffffff",
            fg="#0f172a",
            padx=14,
            pady=8,
            bd=2,
            relief=tk.GROOVE,
        )
        self.input_text.pack(fill=tk.X, padx=14, pady=(0, 6))
        self.input_text.bind("<KeyPress>", self.on_key_press)
        self.input_text.bind("<KeyRelease>", self.on_key_release)

        bottom_panel = tk.Frame(self.root, bg="#eef2f6", padx=14, pady=2)
        bottom_panel.pack(fill=tk.BOTH, expand=True)

        self.build_visual_hand(bottom_panel, "बायाँ हाथ (Left Hand)", side=tk.LEFT, is_left=True)
        kb_center = tk.Frame(bottom_panel, bg="#eef2f6", padx=6)
        kb_center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.build_onscreen_keyboard(kb_center)
        self.build_visual_hand(bottom_panel, "दायाँ हाथ (Right Hand)", side=tk.RIGHT, is_left=False)

    def build_visual_hand(self, parent, title, side, is_left):
        frame = tk.LabelFrame(
            parent,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#1e3a5f",
            padx=6,
            pady=4,
            width=195,
        )
        frame.pack(side=side, fill=tk.Y)
        frame.pack_propagate(False)

        canvas = tk.Canvas(frame, width=178, height=195, bg="#ffffff", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        canvas.create_oval(38, 105, 140, 172, fill="#fde68a", outline="#92400e", width=2)

        if is_left:
            finger_specs = [
                ("Left Pinky", 26, 56, 44, 112, "Pinky"),
                ("Left Ring", 48, 34, 68, 106, "Ring"),
                ("Left Middle", 72, 24, 92, 105, "Middle"),
                ("Left Index", 96, 36, 116, 108, "Index"),
                ("Thumb", 122, 92, 156, 134, "Thumb"),
            ]
        else:
            finger_specs = [
                ("Thumb", 22, 92, 56, 134, "Thumb"),
                ("Right Index", 62, 36, 82, 108, "Index"),
                ("Right Middle", 86, 24, 106, 105, "Middle"),
                ("Right Ring", 110, 34, 130, 106, "Ring"),
                ("Right Pinky", 134, 56, 152, 112, "Pinky"),
            ]

        for f_name, x1, y1, x2, y2, short_lbl in finger_specs:
            shape_id = canvas.create_oval(x1, y1, x2, y2, fill="#f1f5f9", outline="#475569", width=2)
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            canvas.create_text(cx, cy, text=short_lbl[0], font=("Segoe UI", 8, "bold"), fill="#1e293b")
            self.hand_shapes[f_name] = (canvas, shape_id)

        active_lbl = tk.Label(
            frame,
            text="सक्रिय उंगली: —",
            font=("Segoe UI", 8, "bold"),
            bg="#ffffff",
            fg="#b91c1c",
            wraplength=175,
        )
        active_lbl.pack(side=tk.BOTTOM, pady=2)
        self.hand_shapes[f"label_{'L' if is_left else 'R'}"] = active_lbl

    def refresh_user_dropdown(self):
        users = self.users_data.get("users", ["Default User"])
        self.user_combo["values"] = users
        self.user_var.set(self.current_user())

    def add_new_user(self):
        if self.app_locked:
            messagebox.showwarning("लॉक है", "पहले अनुमति की (Key) से ऐप अनलॉक करें।", parent=self.root)
            return
        name = simpledialog.askstring("नया यूज़र", "नए यूज़र का नाम लिखें:", parent=self.root)
        if not name:
            return
        clean_name = name.strip()
        if not clean_name:
            return
        if clean_name in self.users_data["users"]:
            messagebox.showwarning("नाम मौजूद है", "इस नाम का यूज़र पहले से है। कोई दूसरा नाम चुनें।", parent=self.root)
            return

        pwd = simpledialog.askstring("पासवर्ड सेट करें", f"'{clean_name}' के लिए पासवर्ड लिखें (कम से कम 4 अक्षर):", show="*", parent=self.root)
        if not pwd or len(pwd.strip()) < 4:
            messagebox.showwarning("कमज़ोर/खाली पासवर्ड", "कृपया कम से कम 4 अक्षरों का पासवर्ड दें।", parent=self.root)
            return

        self.users_data["users"].append(clean_name)
        self.users_data["passwords"][clean_name] = hash_password(pwd.strip())
        self.users_data.setdefault("offline_licensed", {})[clean_name] = True
        self.users_data["active_user"] = clean_name
        self.ensure_user_data(clean_name)
        save_json_file(USERS_FILE, self.users_data)
        self.refresh_user_dropdown()
        self.on_category_change()
        self.apply_access_state(clean_name, show_popup=False)
        messagebox.showinfo("यूज़र तैयार", f"'{clean_name}' की पासवर्ड-सुरक्षित प्रोफ़ाइल बन गई है।", parent=self.root)

    def on_user_change(self, event=None):
        selected = self.user_var.get()
        if not selected or selected == self.current_user():
            return

        stored_hash = self.users_data.get("passwords", {}).get(selected)
        if stored_hash:
            entered = simpledialog.askstring(
                "पासवर्ड डालें",
                f"'{selected}' की प्रोफ़ाइल खोलने के लिए पासवर्ड दर्ज करें:",
                show="*",
                parent=self.root,
            )
            if not entered or hash_password(entered) != stored_hash:
                messagebox.showerror("गलत पासवर्ड", "पासवर्ड सही नहीं है! प्रोफ़ाइल नहीं बदली गई।", parent=self.root)
                self.user_var.set(self.current_user())
                return

        self.users_data["active_user"] = selected
        self.ensure_user_data(selected)
        save_json_file(USERS_FILE, self.users_data)
        self.on_category_change()
        self.apply_access_state(selected, show_popup=False)

    def build_onscreen_keyboard(self, parent):
        kb_box = tk.LabelFrame(
            parent,
            text="ऑन-स्क्रीन कीबोर्ड (पीला = अगली की | लाल = गलत की)",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#1e3a5f",
            padx=8,
            pady=6,
        )
        kb_box.pack(fill=tk.BOTH, expand=True)

        for row in KEYBOARD_ROWS:
            r_frame = tk.Frame(kb_box, bg="#ffffff")
            r_frame.pack(pady=2)
            for normal_ch, shift_ch, finger, base_color in row:
                lbl = tk.Label(
                    r_frame,
                    text=f"{normal_ch}\n{shift_ch}",
                    width=self.key_width,
                    height=self.key_height,
                    font=("Consolas", self.key_font_size, "bold"),
                    bg=base_color,
                    fg="#0f172a",
                    bd=1,
                    relief=tk.RAISED,
                )
                lbl.pack(side=tk.LEFT, padx=2)
                self.key_buttons[normal_ch.lower()] = (lbl, finger, base_color)
                self.key_buttons[shift_ch] = (lbl, finger, base_color)

        space_row = tk.Frame(kb_box, bg="#ffffff")
        space_row.pack(pady=4)
        self.space_btn = tk.Label(
            space_row,
            text="SPACEBAR (Thumb / अंगूठा)",
            width=self.key_width * 9 + 12,
            height=2 if self.key_height >= 3 else 1,
            font=("Segoe UI", max(8, self.key_font_size - 1), "bold"),
            bg="#f1f5f9",
            fg="#0f172a",
            bd=1,
            relief=tk.RAISED,
        )
        self.space_btn.pack()

    def clear_highlights(self):
        if not self.root.winfo_exists():
            return
        for lbl, _, base_color in self.key_buttons.values():
            if lbl.winfo_exists():
                lbl.config(bg=base_color, fg="#0f172a")
        if self.space_btn and self.space_btn.winfo_exists():
            self.space_btn.config(bg="#f1f5f9", fg="#0f172a")
        for key, val in self.hand_shapes.items():
            if key.startswith("label_"):
                if val.winfo_exists():
                    val.config(text="सक्रिय उंगली: —")
            else:
                canvas, shape_id = val
                if canvas.winfo_exists():
                    canvas.itemconfig(shape_id, fill="#f1f5f9")

    def highlight_finger(self, finger):
        if self.app_locked or not self.root.winfo_exists():
            return
        if finger in self.hand_shapes:
            canvas, shape_id = self.hand_shapes[finger]
            if canvas.winfo_exists():
                canvas.itemconfig(shape_id, fill="#ef4444")
        if finger.startswith("Left") and "label_L" in self.hand_shapes and self.hand_shapes["label_L"].winfo_exists():
            self.hand_shapes["label_L"].config(text=f"सक्रिय: {finger.replace('Left ', '')}")
        elif finger.startswith("Right") and "label_R" in self.hand_shapes and self.hand_shapes["label_R"].winfo_exists():
            self.hand_shapes["label_R"].config(text=f"सक्रिय: {finger.replace('Right ', '')}")
        elif finger == "Thumb":
            if "label_L" in self.hand_shapes and self.hand_shapes["label_L"].winfo_exists():
                self.hand_shapes["label_L"].config(text="सक्रिय: Thumb (Space)")
            if "label_R" in self.hand_shapes and self.hand_shapes["label_R"].winfo_exists():
                self.hand_shapes["label_R"].config(text="सक्रिय: Thumb (Space)")

    def record_error_char(self, ch):
        if not ch or ch == "\n":
            return
        script_map = self.get_user_stats_for_script()
        script_map[ch] = script_map.get(ch, 0) + 1
        save_json_file(STATS_FILE, self.all_stats)

    def beep_error(self):
        if self.sound_var.get():
            try:
                self.root.bell()
            except Exception:
                pass

    def sync_time_options_for_category(self):
        if not self.root.winfo_exists() or not self.time_combo.winfo_exists():
            return
        cat = self.category_var.get()
        if cat.startswith("Advance"):
            vals = ["5 Min", "10 Min", "15 Min", "20 Min"]
            default_t = "10 Min"
        else:
            vals = ["10 Min", "15 Min", "20 Min"]
            default_t = "10 Min"
        self.time_combo["values"] = vals
        if self.time_var.get() not in vals:
            self.time_var.set(default_t)

    def get_selected_seconds(self):
        mapping = {"5 Min": 300, "10 Min": 600, "15 Min": 900, "20 Min": 1200}
        return mapping.get(self.time_var.get(), 600)

    def on_script_change(self, event=None):
        self.on_category_change()

    def on_category_change(self, event=None):
        if not self.root.winfo_exists():
            return
        self.sync_time_options_for_category()
        if not self.lesson_combo.winfo_exists():
            return
        script = self.script_var.get()
        cat = self.category_var.get()
        start_idx, end_idx = CATEGORIES[cat]
        unlocked = self.get_unlocked_index(script)
        all_lessons = LESSONS_BY_SCRIPT[script]

        display_names = []
        for idx in range(start_idx, end_idx):
            title, _ = all_lessons[idx]
            status = " [Unlocked]" if idx <= unlocked else " [Locked]"
            display_names.append(f"{title}{status}")

        self.lesson_combo["values"] = display_names

        target_idx = min(max(unlocked, start_idx), end_idx - 1)
        self.current_lesson_global_index = target_idx
        self.lesson_var.set(display_names[target_idx - start_idx])
        self.load_lesson_by_index(target_idx)

    def on_lesson_select(self, event=None):
        if self.app_locked or not self.root.winfo_exists():
            return
        script = self.script_var.get()
        cat = self.category_var.get()
        start_idx, end_idx = CATEGORIES[cat]
        unlocked = self.get_unlocked_index(script)
        all_lessons = LESSONS_BY_SCRIPT[script]

        sel_pos = self.lesson_combo.current()
        if sel_pos < 0:
            return
        chosen_idx = start_idx + sel_pos

        if chosen_idx > unlocked:
            req_title, _ = all_lessons[unlocked]
            messagebox.showwarning(
                "लेसन लॉक है",
                f"अगला लेसन खोलने के लिए पहले '{req_title}' को कम से कम {PASS_ACCURACY_THRESHOLD:.0f}% सटीकता के साथ पूरा करें।",
                parent=self.root,
            )
            cur_pos = min(max(self.current_lesson_global_index - start_idx, 0), end_idx - start_idx - 1)
            self.lesson_var.set(self.lesson_combo["values"][cur_pos])
            return

        self.current_lesson_global_index = chosen_idx
        self.load_lesson_by_index(chosen_idx)

    def load_lesson_by_index(self, idx):
        script = self.script_var.get()
        title, content = LESSONS_BY_SCRIPT[script][idx]
        self.set_practice_text(content, label_text=f"{self.current_user()} | {title} (90%+ Acc. से अगला खुलेगा)")

    def set_practice_text(self, content, label_text=""):
        if not self.root.winfo_exists():
            return
        script = self.script_var.get()
        font_style = self.get_script_font(script, self.word_font_size)
        input_font = self.get_script_font(script, max(13, self.word_font_size - 2))

        self.target_text.config(state=tk.NORMAL, font=font_style)
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert("1.0", content)
        self.target_text.config(state=tk.DISABLED)
        self.input_text.config(font=input_font)
        self.reset_test(custom_status=label_text or None)

    def practice_weak_keys(self):
        if self.app_locked or not self.root.winfo_exists():
            return
        script = self.script_var.get()
        user = self.current_user()
        err_map = self.get_user_stats_for_script(script)
        sorted_chars = [c for c, _ in sorted(err_map.items(), key=lambda x: x[1], reverse=True) if c.strip()]

        if not sorted_chars:
            messagebox.showinfo(
                "कमज़ोर कीज़ डेटा नहीं है",
                f"{user} के लिए {script} में अभी तक कोई गलती दर्ज नहीं हुई है। पहले थोड़ा टाइप करें, फिर यह बटन आपके सबसे ज़्यादा गलत होने वाले अक्षरों का प्रैक्टिस सेट बना देगा।",
                parent=self.root,
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
        drill_text = " ".join(drill_items * 15)
        self.set_practice_text(drill_text, label_text=f"{user} — कमज़ोर कीज़ ({script}): {' '.join(top_chars)}")

    def open_game_window(self):
        if self.app_locked or not self.root.winfo_exists():
            return
        script = self.script_var.get()
        user = self.current_user()
        words = GAME_WORDS.get(script, GAME_WORDS["English"])

        game_win = tk.Toplevel(self.root)
        game_win.title(f"टाइपिंग गेम (Word Rush) — {user} ({script})")
        game_win.geometry("680x460")
        game_win.configure(bg="#0f172a")

        state = {"score": 0, "lives": 5, "word": random.choice(words), "y": 30, "active": True}

        top = tk.Frame(game_win, bg="#1e293b", pady=6, padx=12)
        top.pack(fill=tk.X)

        tk.Label(top, text=f"यूज़र: {user}", font=("Segoe UI", 10, "bold"), bg="#1e293b", fg="#93c5fd").pack(side=tk.LEFT, padx=6)
        score_lbl = tk.Label(top, text="स्कोर: 0", font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="#4ade80")
        score_lbl.pack(side=tk.LEFT, padx=10)
        lives_lbl = tk.Label(top, text="लाइव: 5", font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="#f87171")
        lives_lbl.pack(side=tk.LEFT, padx=10)

        canvas = tk.Canvas(game_win, bg="#1e293b", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        entry = tk.Entry(game_win, font=self.get_script_font(script, 15), bg="#f8fafc", fg="#0f172a")
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
                font=self.get_script_font(script, 20),
            )
            state["y"] += 5
            if state["y"] >= w_height - 20:
                state["lives"] -= 1
                lives_lbl.config(text=f"लाइव: {state['lives']}")
                entry.delete(0, tk.END)
                if state["lives"] <= 0:
                    state["active"] = False
                    messagebox.showinfo("गेम समाप्त", f"{user} का कुल स्कोर: {state['score']}", parent=game_win)
                    game_win.destroy()
                    return
                spawn_word()
            game_win.after(90, tick)

        game_win.protocol("WM_DELETE_WINDOW", lambda: (state.update({"active": False}), game_win.destroy()))
        game_win.after(200, tick)

    def on_key_press(self, event):
        if self.app_locked or str(self.input_text.cget("state")) == "disabled":
            return "break"

        if event.keysym == "BackSpace" and self.disable_backspace_var.get():
            self.alert_label.config(text="Backspace बंद है!", fg="#b91c1c")
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
        if not self.root.winfo_exists():
            return
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
        if self.app_locked or not self.root.winfo_exists():
            if self.finger_label.winfo_exists():
                self.finger_label.config(text="उंगली गाइड: लॉक (Key आवश्यक)")
            return

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

    def reset_test(self, custom_status=None):
        if not self.root.winfo_exists():
            return
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

        if self.app_locked:
            self.alert_label.config(text="बिना अनुमति/की के ऐप लॉक है", fg="#b91c1c")
            self.input_text.config(state=tk.DISABLED)
            self.clear_highlights()
            return

        if custom_status:
            self.alert_label.config(text=custom_status, fg="#7c3aed")
        else:
            self.alert_label.config(text="कम से कम 90% सटीकता पर अगला लेसन खुलेगा", fg="#2563eb")

        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete("1.0", tk.END)
        self.update_target_highlights()
        self.update_finger_guide()
        self.input_text.focus()

    def update_timer(self):
        if self.app_locked or not self.root.winfo_exists():
            return
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"{format_mm_ss(self.time_left)} Min.")
            self.calculate_stats()
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.finish_test()

    def on_key_release(self, event):
        if self.app_locked or str(self.input_text.cget("state")) == "disabled":
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

    def get_current_accuracy(self):
        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")
        if self.mode_var.get() == "गलत पर रुकें":
            correct_chars = len(typed)
            total_attempts = correct_chars + self.strict_errors_count
            return (correct_chars / total_attempts) * 100 if total_attempts > 0 else 100.0
        correct_chars = sum(1 for i, ch in enumerate(typed) if i < len(target) and ch == target[i])
        return (correct_chars / len(typed)) * 100 if len(typed) > 0 else 100.0

    def calculate_stats(self):
        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")

        elapsed_sec = max(self.selected_duration - self.time_left, 1)
        elapsed_min = elapsed_sec / 60.0
        acc = self.get_current_accuracy()

        if self.mode_var.get() == "गलत पर रुकें":
            correct_chars = len(typed)
            errors = self.strict_errors_count
            net_wpm = int((correct_chars / 5) / elapsed_min)
        else:
            correct_chars = sum(1 for i, ch in enumerate(typed) if i < len(target) and ch == target[i])
            errors = max(len(typed) - correct_chars, 0)
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

        target = self.target_text.get("1.0", "end-1c")
        typed = self.input_text.get("1.0", "end-1c")
        acc = self.get_current_accuracy()
        completed_full = len(typed) >= len(target) and len(target) > 0

        if completed_full and acc >= PASS_ACCURACY_THRESHOLD:
            unlocked_new = self.unlock_next_lesson(self.current_lesson_global_index)
            extra_msg = "\n\nबधाई! अगला लेसन अनलॉक हो गया है।" if unlocked_new else "\n\nलेसन अच्छी तरह पूरा हुआ!"
            messagebox.showinfo(
                "लेसन पूर्ण (Passed)",
                f"यूज़र: {self.current_user()}\n"
                f"{self.wpm_label.cget('text')}  |  {self.acc_label.cget('text')}\n"
                f"{self.err_label.cget('text')}  |  {self.signs_label.cget('text')}{extra_msg}",
                parent=self.root,
            )
            if unlocked_new:
                next_idx = self.current_lesson_global_index + 1
                for cat_name, (s_i, e_i) in CATEGORIES.items():
                    if s_i <= next_idx < e_i:
                        self.category_var.set(cat_name)
                        break
                self.on_category_change()
        else:
            messagebox.showwarning(
                "फिर से प्रयास करें",
                f"अगला लेसन खोलने के लिए पूरा मैटर और कम से कम {PASS_ACCURACY_THRESHOLD:.0f}% सटीकता ज़रूरी है।\n\n"
                f"आपकी सटीकता: {acc:.1f}%\n"
                f"{self.wpm_label.cget('text')}  |  {self.err_label.cget('text')}",
                parent=self.root,
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = OfflineTypingTutor(root)
    root.mainloop()
