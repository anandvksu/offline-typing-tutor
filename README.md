# Offline Typing Tutor (English | Kruti Dev 010 | Mangal)

A 100% offline desktop typing tutor built with **Python (Tkinter)** and automatically compiled into a standalone Windows `.exe` via **GitHub Actions (PyInstaller)**.

## Key Features
- **Multi-Script Support:** English, Hindi (**Kruti Dev 010**), and Hindi (**Mangal**).
- **Visual Finger & Keyboard Guide:** Highlights the target key, active finger (Left/Right hand + Thumb), and Kruti Dev key mappings.
- **Two Typing Modes:**
  - **Strict Mode (`गलत पर रुकें`):** Blocks advancing on a wrong character until corrected.
  - **Exam Mode (`आगे बढ़ें`):** Allows continuous typing with live correct/wrong highlighting.
- **Weak Keys Practice:** Tracks error-prone characters per user and script, generating focused practice drills.
- **Multi-User Profiles:** Separate lessons and error stats per user (`typing_users.json`, `typing_lessons.json`, `typing_stats.json`).
- **Lesson Manager & `.txt` Import:** Add, edit, delete lessons, or import plain `.txt` files.
- **Typing Game (Word Rush):** Built-in falling-word speed game.

## Download Windows EXE
1. Go to the **Actions** tab in this repository.
2. Open the latest successful (`✅`) **Build Windows EXE** workflow run.
3. Download **`TypingTutor-Windows`** under **Artifacts** and extract `TypingTutor.exe`.

## How to Contribute
Want to add more typing lessons (Basic to Advance), improve Kruti Dev / Mangal mappings, or add new features? Check out [CONTRIBUTING.md](CONTRIBUTING.md)!
