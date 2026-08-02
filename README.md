# 🤖 Desktop AI Assistant

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=flat-square)](https://python.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-black?style=flat-square)](LICENSE)

A modern **multimodal desktop AI assistant** that combines **voice interaction**, **desktop vision**, **webcam awareness**, and **large language models** into a single intelligent application.

Unlike traditional chatbots, this assistant understands the **visual context of your desktop**, allowing it to explain code, summarize webpages, debug errors, and answer questions based on what is currently visible on your screen.

---

# ✨ Features

### 🧠 AI Capabilities

- Multimodal reasoning using Google Gemini
- Context-aware conversations
- Conversation history
- Image + text understanding

### 🖥 Desktop Understanding

- Live desktop screenshot capture
- Explain source code
- Debug programming errors
- Summarize webpages
- Interpret charts and graphs

### 📷 Vision

- Live desktop preview
- Live webcam preview
- Real-time screenshot analysis

### 🎤 Voice Interaction

- Continuous speech recognition
- Keyboard input support
- Offline Text-to-Speech (pyttsx3)
- OpenAI TTS support (optional)

### 🎨 User Interface

- Modern Streamlit dashboard
- Dark theme
- Chat interface
- Live desktop preview
- Live webcam preview
- Status indicators

### 🔌 AI Provider Support

- ✅ Google Gemini
- ✅ OpenAI
- ✅ OpenRouter
- ✅ Groq
- ✅ Ollama (Local)

---

# 🏗 Architecture

```text
                 Streamlit UI
                       │
                       ▼
               assistant.py Backend
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
 Desktop Capture    Webcam        Voice Input
       │               │               │
       └───────────────┼───────────────┘
                       ▼
              Prompt Construction
                       ▼
          Google Gemini Multimodal API
                       ▼
                AI Generated Response
                       ▼
             UI + Voice Output (TTS)
```

---

# 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| Language | Python 3.13 |
| AI | Google Gemini API |
| Framework | LangChain |
| UI | Streamlit |
| Vision | OpenCV, Pillow |
| Speech Recognition | SpeechRecognition |
| Speech Synthesis | pyttsx3 |
| Audio | PyAudio |
| Environment | python-dotenv |
| Numerical Processing | NumPy |

---

# 📁 Project Structure

```text
desktop-ai-assistant/

│
├── app.py                 # Streamlit UI
├── assistant.py           # AI backend
├── requirements.txt
├── README.md
├── .env.example
│
├── assets/
│   ├── dashboard.png
│   ├── desktop-preview.png
│   └── webcam.png
│
└── docs/
```

---

# 🚀 Installation

Clone the repository.

```bash
git clone -b master https://github.com/<your-username>/ai-desktop-assistant.git

cd ai-desktop-assistant
```

Create a virtual environment.

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# ⚙ Configuration

Create a `.env` file.

```env
MODEL_PROVIDER=gemini

GOOGLE_API_KEY=YOUR_GOOGLE_AI_STUDIO_API_KEY

GEMINI_MODEL=gemini-flash-latest

MICROPHONE_INDEX=1
```

Get your API key from:

https://aistudio.google.com/app/apikey

---

# ▶ Running the Project

### Streamlit Dashboard

```bash
streamlit run app.py
```

### Voice Assistant Mode

```bash
python assistant.py
```

The Streamlit interface provides:

- Modern dashboard
- AI chat interface
- Live desktop preview
- Live webcam preview

The standalone assistant additionally supports:

- Continuous voice interaction
- Background microphone listener
- OpenCV preview windows

---

# 💬 Example Prompts

```text
Explain this Python error.

Summarize this webpage.

What do you see on my screen?

Explain this code.

Describe the graph on my desktop.

Can this code be optimized?

What is wrong with this exception?
```

---

# 📸 Screenshots

> Screenshots will be added soon.

- Dashboard
- Desktop Preview
- Webcam Preview
- AI Conversation

---

# 🚀 Roadmap

- [x] Desktop screenshot understanding
- [x] Voice interaction
- [x] Live webcam preview
- [x] Streamlit dashboard
- [x] Multi-provider AI support
- [ ] Native PySide6 desktop application
- [ ] Wake-word detection
- [ ] Browser automation
- [ ] Desktop automation
- [ ] OCR integration
- [ ] Long-term memory
- [ ] Plugin architecture
- [ ] Windows executable (.exe)

---

# 🔒 Security

API keys are loaded through environment variables and are never committed to the repository.

Ensure your `.env` file is included in `.gitignore`.

---

# 🤝 Contributing

Contributions, feature requests, and issues are welcome.

If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Your_Name**

B.Tech Computer Science Engineering

Python Developer • AI Enthusiast • Backend Developer

---

⭐ If you found this project useful, consider giving it a star!
