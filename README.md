# 🧠 AI Browser Agent (OpenAI + browser-use)

This project uses `browser-use`, `OpenAI`, and `Pydantic` to control a browser session, visit a webpage, and extract structured content using an LLM.

---

## 🚀 Features

- Opens Chrome browser using Playwright
- Uses GPT-4.1 to extract blog titles and content
- Validates output using Pydantic
- Runs headful or headless

---

## 📦 Requirements

- macOS (M1/M2/M3)
- Python 3.9 – 3.12 (Python 3.13 may not yet be fully compatible with some packages)
- Chrome installed (default macOS path used)

---

## 🛠️ Setup Instructions

### 1. Clone this Repository

```bash
git clone https://github.com/your-username/ai-browser-agent.git
cd ai-browser-agent


python3 -m venv venv
source venv/bin/activate



pip install --upgrade pip



pip install -r requirements.txt


.
├── main.py         # Entry point
├── .env            # Your OpenAI API key (not committed)
├── README.md       # This file
└── requirements.txt



python main.py
