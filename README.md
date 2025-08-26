# EchoMind

A single-request voice assistant powered by GPT-3.5-turbo.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Folder Structure](#folder-structure)
- [License](#license)
- [Author](#author)

## Description

**EchoMind** is a Python-based, single-query voice assistant designed for accurate, fact-based information retrieval. The assistant listens for a wake word, records and transcribes your voice command, and responds audibly using natural-sounding speech synthesis.  
EchoMind uses OpenAI's GPT-3.5-turbo model as its "brain," ensuring you get smart, context-aware answers to your questions. However, it does **not** access real-time or up-to-the-minute information, focusing instead on reliable factual knowledge.

The project is currently implemented as a single Python file (`EchoMind.py`) for simplicity and rapid prototyping. Future iterations will modularize the codebase with components like `assistant.py` and `speaker.py` for better scalability and maintainability.

## Features

-  **Wake Word Activation**: Listens for customizable wake words to start the assistant ("wake up", "are you there", etc.)
-  **Voice Recognition**: Uses Whisper and SpeechRecognition for robust transcription from microphone input
-  **Natural Language Understanding**: Processes your request using OpenAI GPT-3.5-turbo
-  **High-Quality Text-to-Speech**: ElevenLabs TTS delivers realistic, expressive voice responses
-  **Single-Query Simplicity**: Handles one request at a time for streamlined, distraction-free interaction
-  **Error Handling**: Graceful feedback for API or network issues

## Getting Started

### Prerequisites
- Python 3.10 or later
- [OpenAI API key](https://platform.openai.com/)
- [ElevenLabs API key](https://elevenlabs.io/)
- [Whisper](https://github.com/openai/whisper)
- Packages: `openai`, `elevenlabs`, `python-dotenv`, `pygame`, `speechrecognition`, `whisper`, `playsound`

### Installation

```bash
git clone https://github.com/yourusername/EchoMind.git
cd EchoMind
pip install openai elevenlabs python-dotenv pygame speechrecognition whisper playsound
```

Add your API keys to a `.env` file in the project root:
```
OPENAI_API_KEY=your-openai-key
ELEVENLABS_API_KEY=your-elevenlabs-key
```

### Running the App

```bash
python EchoMind.py
```

## Usage

1. Start the app and wait for the wake word prompt.
2. Say a wake word (e.g., "wake up", "start up", "initiate").
3. After the startup sound, speak your question or command.
4. EchoMind will transcribe, process, and respond using realistic speech.

**Sample Session:**
```text
Awaiting wake command...
Heard: wake up
EchoMind online. Awaiting your command sir.
Listening...
Recognizing...
Transcribing with Whisper...
You said: what is the capital of Japan?
EchoMind says: The capital of Japan is Tokyo.
```

## Screenshots

> Coming Soon...

## Folder Structure

```
EchoMind/
├── EchoMind.py      # Main assistant script
├── .env             # API keys (not tracked in version control)
├── README.md        # Project documentation
└── startup.mp3      # Optional: wake sound effect
```

_Modularization planned for future versions:_
```
EchoMind/
├── assistant.py     # Assistant logic
├── speaker.py       # Voice synthesis & playback
...
```

## License

Licensed under the MIT License. See `LICENSE` for more info.

## Author

Spencer Fisher  
[https://github.com/spncr1](https://github.com/spncr1) | Portfolio
