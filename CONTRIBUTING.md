# Contributing to Offline Typing Tutor

Contributions are welcome! Whether you want to add progressive typing lessons, improve Hindi (Kruti Dev 010 / Mangal) layouts, or enhance features, please follow these guidelines:

## 1. Adding Lessons
- Keep **Kruti Dev 010** lessons in plain ASCII Kruti Dev text (do not convert to Unicode/Mangal).
- Keep **Mangal** lessons in clean UTF-8 Devanagari text.
- Organize lessons clearly by difficulty (e.g., *Home Row*, *Top/Bottom Row*, *Matras & Conjuncts*, *Official/Speed Paragraphs*).

## 2. Code & UI Changes
- Main application logic lives in `typing_tutor.py` (Python 3.11+, Tkinter standard library).
- Avoid adding heavy external dependencies so the Windows `.exe` build stays lightweight and offline-friendly.
- Test your changes locally before opening a Pull Request or committing to `main`.

## 3. Submitting Changes
1. Fork the repository or create a branch.
2. Make your edits and commit with a clear commit message.
3. Verify that the **Build Windows EXE** GitHub Actions workflow passes (`✅`).
