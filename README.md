# 📊 MochiHealth – Dashboard Mood Analyser

This is a lightweight internal tool for logging and visualizing the mood of support tickets in real time. Built using **Streamlit**, it allows users to log mood entries with optional notes, and view insightful visualizations such as mood trends and word clouds.

---

## 🌐 Live Demo

- **🔗 Website**: [mochi-health.onrender.com](https://mochi-health.onrender.com/)
- **📄 Google Sheet (backend data source)**: [Mood Log Spreadsheet](https://docs.google.com/spreadsheets/d/1H1gepSq8c_5qmXaHCneRBAXh4vyjc2OVuYeIUzaPMr4/edit?gid=0#gid=0)

---

## 🚀 Features

- Log moods using emojis: 😊 😠 😕 🎉
- Optional notes to capture context (e.g., "Delayed Rx", "Happy discharge")
- Mood trend bar chart by year with:
  - Emoji-based coloring (e.g., red for 😠, green for 😊)
  - Hover tooltips showing emotion names
- Filters for **year**, **month**, and **emoji**
- Auto-refreshing dashboard every 5 seconds
- Word cloud generated from mood notes

---

## 🛠️ Tech Stack

- 🐍 Python
- 🧼 Streamlit (UI)
- 📊 Plotly (Visualization)
- ☁️ Google Sheets API (Data storage)
- 🧠 WordCloud (for note analysis)

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/mochihealth-mood-analyser.git
cd mochihealth-mood-analyser
pip install -r requirements.txt

