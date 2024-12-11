Welcome to the **Interactive Quiz Application**! Whether you're:
- 🐍 Strengthen your Python basics with beginner-friendly quizzes.
- 🚀 Preparing for the **AWS Certified AI Practitioner (AIF-C01)** exam,  

Built with Streamlit, this app offers a clean, user-friendly interface to practice, learn, and master essential topics interactively. 🎯


## ✨ Features You’ll Love

- 🎯 **Engaging Quiz Interface**:
  - Intuitive, interactive quiz design.
  - Supports Python basics and AWS AIF-C01 content.

- 📂 **Multiple Quiz Categories**:
  - 🐍 **Python Quizzes**: Perfect for coding beginners.
  - ☁️ **AWS Certification Quizzes**: Specifically tailored for AIF-C01 exam preparation.

- 🔄 **Randomized and Targeted Practice**:
  - Load specific JSON files for focused learning.
  - Randomize questions for a unique session every time.

- 📊 **Progress Tracking**:
  - Instant results with detailed feedback, hints, and explanations.

- 🛠️ **Custom Input Fields**:
  - Handle coding challenges directly in the app with real-time evaluation.


```plaintext

20241113_Python_AWS_AIF_C01_Quiz/
├── app.py                    # 🌐 Main Streamlit application
├── code/                     # 🧩 Core logic modules
│   ├── quiz_logic.py         # 🚦 Main quiz engine
│   ├── range_quiz.py         # 🎯 Logic for range-based quizzes
│   ├── random_30_quiz.py     # 🔄 Logic for randomized quizzes
│   └── customer_quiz.py      # 🤝 Custom quiz configurations
├── data/                     # 📊 Quiz data
│   ├── json/                 # 🗂️ JSON quiz files
│   │   ├── ai_data_applications_all_226.json   # AI Data Applications questions (226)
│   │   ├── aws_aif_c01_eng_87.json            # AWS AIF-C01 English (87)
│   │   ├── aws_aif_c01_sc_43.json             # AWS AIF-C01 Simplified Chinese (43)
│   │   ├── aws_aif_c01_sc_65.json             # AWS AIF-C01 Simplified Chinese (65)
│   │   ├── aws_aif_c01_all_195.json           # Combined AWS AIF-C01 (195)
│   │   ├── python_tabime_11.json              # Python Tabime (11)
│   │   ├── python_tabime_20.json              # Python Tabime (20)
│   │   ├── python_tabime_all_31.json          # Combined Python Tabime (31)
│   └── pdf/                  # 📄 PDF reference materials
│       ├── AIF_C01_part1_英87題.pdf           # AWS AIF-C01 Part 1 (87)
│       ├── AIF_C01_part2_簡中43題.pdf         # AWS AIF-C01 Part 2 (43)
│       ├── AIF_C01_part3_簡中65題.pdf         # AWS AIF-C01 Part 3 (65)
│       ├── python_part1_11題.pdf             # Python Part 1 (11)
│       ├── python_part2_20題.pdf             # Python Part 2 (20)
├── .venv/                    # ⚙️ Virtual environment
├── requirements.txt          # 📜 Python package dependencies
├── pyproject.toml            # 🛠️ Poetry configuration file
├── README.md                 # 📘 Project documentation
└── banner.png                # 🎨 App banner for branding


```

## 🚀 Get Started

### Install Dependencies:

Using Poetry:
```bash
poetry install
```
Or using pip:
```bash
pip install -r requirements.txt
```

### Run the App:
```bash
streamlit run app.py
```

### Start Practicing:

1. Select Python or AWS quizzes.
2. Answer questions, get feedback, and track your progress!

---

## 📚 What You’ll Learn

### Python Basics 🐍:
- Variables, data types, loops, and functions.
- Designed for beginners starting their coding journey.

### AWS AIF-C01 Certification ☁️:
- Cloud fundamentals, machine learning basics, and AWS AI tools.
- Includes real-world AIF-C01 exam-style questions.

---

## 🌟 Why Use This App?

- 🧠 Boost Your Knowledge: Strengthen key skills in Python and AWS.
- 🔥 Stay Motivated: Immediate feedback keeps you engaged.
- 🛠️ Build Confidence: Tackle real exam questions and Python problems.

---

## ⚠️ Disclaimer
- This app is for educational purposes only and should not be used for commercial distribution or sharing beyond personal use. Content referenced from TibaMe or AWS materials remains the property of its rightful owner.
- 本專案的下載和使用必須經過授權許可。請聯絡 劉晏瑜 <franliu3578@gmail.com> 獲取授權。
---


- 💡 Ready to learn and grow? Dive into the app and supercharge your Python and AWS skills today! 🚀✨


