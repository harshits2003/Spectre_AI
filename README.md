# 🌌 Spectre_AI - Agentic Voice Chatbot System

**Spectre_AI** is an intelligent, real-time, agentic voice chatbot system built for seamless, multi-user, voice-native conversational experiences. Unlike traditional chatbots, Spectre_AI offers highly responsive, context-aware interactions powered by dynamic tool orchestration and advanced memory.

---

## 🧠 Overview

Spectre_AI delivers next-generation conversational AI through:

- ⚡ Real-time voice responsiveness
- 🧠 Long-term contextual memory
- 🛠️ Dynamic tool usage (search, YouTube, image generation)
- 👥 Concurrent multi-user support

It is designed to handle complex, multi-turn dialogues while reasoning intelligently, managing per-user context, and integrating multimodal tools.

---

## 🚀 Key Features

- 🎙️ **Real-Time Voice Interaction**  
  Natural conversations via microphone and speaker for fluid user experience.

- 🧠 **Agentic Intelligence**  
  Complex reasoning, planning, and tool use enabled by LLMs and orchestration logic.

- 🧾 **Contextual Memory**  
  Maintains long-term memory for personalized and coherent interaction flow.

- 👥 **Multi-User Support**  
  Isolated sessions with independent memory for simultaneous users.

- 🧩 **Modular Architecture**  
  Clean separation of concerns: STT, LLM, TTS, GUI, memory, and orchestration.

- 🌐 **Web & Media Search Integration**  
  Perform real-time Google and YouTube searches within conversation context.

- 🖼️ **Image Generation**  
  Generate images as part of interactive conversations.

---

## 🧱 System Architecture


### ⚙️ Components

- **STT (Speech-to-Text):** Converts voice to text using Selenium and translation tools.
- **LLM Reasoning Engine:** GROQ + APIs enable intelligent responses with tool use.
- **Tool Plugins:** Web search, YouTube fetch, and image generation with HuggingFace APIs.
- **Memory Engine:** Stores user-specific context over time.
- **TTS (Text-to-Speech):** Converts responses to human-like audio.
- **Frontend GUI:** Interactive UI built using PyQt5.

---


## 🛠️ Installation

### 📥 Clone the Repository

```bash
git clone https://github.com/harshits2003/Spectre_AI.git
cd Spectre_AI
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ Set Up Environment Variables

```bash
cp .env.example .env
```

To run the assistant:
```bash
python main.py
```
### 🔧 Configuration

Edit .env for keys like GROQ API, YouTube API, etc.
Additional configuration (e.g., TTS voices, GUI preferences) may exist inside Backend/ or Frontend/.

---
### 🤝 Contributing
Contributions are welcome!

Fork this repository.
Create a new branch.
Make your changes.
Submit a Pull Request.

Let’s build the future of real-time AI assistants—together.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.




