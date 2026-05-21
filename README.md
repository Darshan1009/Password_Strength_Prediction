# 🔐 Password Strength Predictor

A modern, interactive web application that evaluates password security using **Machine Learning** and **Natural Language Processing**. Featuring a beautiful glassmorphism UI, a built-in password generator, and real-time strength feedback powered by a Logistic Regression model trained on 60,000+ password samples.

---

## 📸 Screenshots

### Password Strength Tester
The main page lets you check any password's strength in real time. Get instant feedback, helpful tips, and explore tabs covering security best practices.

![Password Strength Tester](screenshots/tester.png)

### Password Generator
Generate secure passwords with full control over length and character types. Each generated password is instantly scored and broken down by character composition.

![Password Generator](screenshots/generator.png)

---

## ✨ Features

- 🎯 **Real-time ML-Powered Analysis** — Logistic Regression classifier predicts weak / normal / strong with **~94% accuracy**
- 🔑 **Built-in Password Generator** — Customize length (4–32) and character classes (uppercase, lowercase, digits, symbols)
- 📊 **Strength Meter** — Visual gradient meter with detailed character breakdown (length, uppercase, lowercase, digits)
- 💡 **Educational Tabs** — *About*, *How to Use*, *Good Passwords*, *Compare*, and *More* sections teach password best practices
- 🎨 **Glassmorphism UI** — Frosted glass cards, soft gradients, and a fully responsive layout
- 🔒 **Privacy First** — All predictions run locally on your machine. Nothing is stored, logged, or transmitted
- 📜 **History** — Track recently tested passwords during your session

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask |
| **ML / NLP** | scikit-learn (Logistic Regression, TF-IDF char-level vectorizer) |
| **Data** | SQLite, pandas, NumPy |
| **Frontend** | HTML5, CSS3 (glassmorphism), Vanilla JavaScript |
| **Notebook** | Jupyter (model training & EDA) |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Darshan1009/Password_Strength_Prediction.git
cd Password_Strength_Prediction
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Build the dataset
The training dataset is not committed to the repo (it's generated locally). Run:
```bash
python _build_dataset.py
```
This creates `Datasets/password_data.sqlite` with **60,000 labeled passwords** (20k each of weak / normal / strong).

### 5. Train the model
```bash
python _train_model.py
```
This produces `model.pkl` and `vectorizer.pkl` (~94% test accuracy).

### 6. Run the app
```bash
python app.py
```
Then open **http://127.0.0.1:5000/** in your browser. 🎉

---

## 💡 How It Works

1. **Type a password** in the input box.
2. The character-level **TF-IDF vectorizer** transforms it into a feature vector.
3. Two engineered features (password length + lowercase frequency) are appended.
4. The trained **Logistic Regression model** predicts one of three classes:
   - 🔴 **Weak** (0) — Short, predictable, or single character class
   - 🟡 **Normal** (1) — Medium length, mixed character types
   - 🟢 **Strong** (2) — Long with mixed case, digits, and symbols
5. The UI updates the strength meter, color, and tips in real time.

---

## 📂 Project Structure

```
Password_Strength_Prediction/
├── app.py                          # Flask web app
├── decoding.py                     # Prediction helper utilities
├── NLP_Password_Prediction.ipynb   # Full training notebook (EDA + model)
├── _build_dataset.py               # Generates Datasets/password_data.sqlite
├── _train_model.py                 # Trains and saves model.pkl + vectorizer.pkl
├── requirements.txt
├── templates/                      # HTML templates (tester + generator pages)
├── Datasets/                       # SQLite dataset (gitignored — generated locally)
├── screenshots/                    # README screenshots
└── README.md
```

---

## 📈 Model Performance

| Metric | Score |
|---|---|
| **Accuracy** | 93.94% |
| **Weak (precision / recall)** | 0.92 / 0.92 |
| **Normal (precision / recall)** | 0.91 / 0.91 |
| **Strong (precision / recall)** | 0.99 / 0.99 |

---

## 🎨 Customization

- **UI Theme** — Edit the CSS in `templates/index.html` to change colors, gradients, or layout
- **Retrain the Model** — Modify `_build_dataset.py` to use your own dataset, then rerun `_train_model.py`
- **New Features** — Ideas: passphrase generator, breach checker (HaveIBeenPwned API), zxcvbn comparison

---

## 🔒 Privacy & Security

This project is built for **education and demonstration**. The app runs entirely on your local machine — **no passwords are stored, transmitted, or logged**. Never enter real passwords on public deployments of this (or any) tool.

---

## 📄 License & Copyright

**© 2026 Darshan. All Rights Reserved.**

This project is **proprietary** and provided for viewing and personal study only. See the [LICENSE](LICENSE) file for full terms.

> ⚠️ **You may NOT** copy, fork, redistribute, modify, or use this code (in whole or in part) in your own projects, portfolio, tutorials, or commercial products **without explicit written permission** from the author.

If you'd like to use any part of this project, [open an issue](https://github.com/Darshan1009/Password_Strength_Prediction/issues) or contact me through GitHub.

---

## 👤 Author

Created with ❤️ by **Darshan**
[GitHub @Darshan1009](https://github.com/Darshan1009)

⭐ If you like this project, please **star** the repo — it's the best way to support the work without copying it!
