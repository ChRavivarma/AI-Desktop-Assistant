# Desktop AI Assistant

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=flat-square)](https://python.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-black?style=flat-square)](LICENSE)

A multimodal desktop AI assistant that understands both **natural language** and the **visual context of your desktop**.

Unlike conventional chatbots, this assistant continuously listens for voice commands, captures the current desktop, and uses Google's Gemini multimodal models to answer questions about what the user is seeing. Responses are delivered both as text and speech, enabling a natural desktop interaction experience.

---

## Overview

The assistant combines speech recognition, desktop vision, conversational memory, and text-to-speech into a single application.

Typical use cases include:

- Explaining programming errors
- Understanding source code
- Summarizing documentation
- Interpreting charts and graphs
- Answering questions about webpages
- Assisting with learning and debugging

The project is designed with modular components, making it easy to extend with automation, browser control, OCR, and additional AI providers.

---

## Demo

> **Coming Soon**

The repository will include:

- Application walkthrough
- Voice interaction demo
- Screen understanding examples
- Architecture visualization

---

## Features

### Multimodal Understanding

- Desktop screenshot analysis using Gemini Vision
- Context-aware responses based on both text and visual input
- Session-based conversational memory

### Voice Interaction

- Continuous microphone listening
- Speech-to-text conversion
- Offline text-to-speech responses
- Terminal text input as an alternative

### Computer Vision

- Real-time desktop capture
- Live webcam preview
- Modular vision pipeline

### AI Provider Support

The assistant has been designed to support multiple inference providers.

Currently supported:

- Google Gemini
- OpenAI
- OpenRouter
- Groq
- Ollama (Local)

---

# Architecture

```

+-------------------------+
\| User (Voice / Keyboard) |
+------------+------------+
|
v
Speech Recognition
|
v
Prompt Builder
|
+----------------------+
| |
v v
Desktop Screenshot Conversation History
| |
+-----------+----------+
|
v
Gemini Multimodal Model
|
v
Generated Response
|
+------------------+
| |
v v
Terminal Text Speech Output

```

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| Language | Python 3.13 |
| AI | Google Gemini API |
| Framework | LangChain |
| Vision | OpenCV, Pillow |
| Speech Recognition | SpeechRecognition |
| Speech Synthesis | pyttsx3 |
| Audio | PyAudio |
| Environment | python-dotenv |
| Numerical Processing | NumPy |

---

## Project Structure

```

ai-voice-assistant/

├── assistant.py
├── requirements.txt
├── .env.example
├── README.md
│
├── docs/
│ ├── architecture.png
│ ├── demo.gif
│ └── screenshots/
│
└── assets/

```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/<username>/desktop-ai-assistant.git

cd desktop-ai-assistant
```

Create a virtual environment.

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file.

```env
MODEL_PROVIDER=gemini

GOOGLE_API_KEY=YOUR_API_KEY

GEMINI_MODEL=gemini-flash-latest

MICROPHONE_INDEX=1
```

Obtain a Google AI Studio API key from:

https://aistudio.google.com/

---

## Running

```bash
python assistant.py
```

The application initializes:

- Webcam stream
- Desktop capture
- AI model
- Microphone
- Background listener

You may interact through either:

- Voice
- Keyboard

---

## Example Prompts

```
Explain this Python error.

Summarize this webpage.

What is wrong with this code?

Describe this graph.

Explain the algorithm shown on my screen.

What does this exception mean?

Can this code be optimized?
```

---

## Current Limitations

The assistant currently focuses on multimodal understanding.

Not yet implemented:

- Wake-word activation
- Internet search
- Desktop automation
- Browser control
- File management
- Long-term memory
- OCR pipeline
- Webcam reasoning

---

## Roadmap

- [ ] Wake-word detection
- [ ] Browser automation
- [ ] OCR integration
- [ ] File assistant
- [ ] Desktop control
- [ ] Long-term memory
- [ ] Calendar integration
- [ ] Email assistant
- [ ] Plugin architecture
- [ ] Streaming AI responses

---

## Security

API keys are loaded through environment variables and are never stored in the repository.

Ensure your `.env` file is included in `.gitignore`.

---

## Contributing

Contributions, issues, and feature requests are welcome.

If you would like to contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Author

**Ravi Varma**

Computer Science Engineering Student

Python Developer • AI Enthusiast

GitHub: https://github.com/<your-username>

LinkedIn: https://linkedin.com/in/<your-profile>
