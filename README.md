## 📖 Overview

**LiveKit-Plugins-Googlesr** is a custom **Speech-to-Text (STT)** plugin built for the  
[LiveKit Agents](https://github.com/livekit/agents) framework.

It integrates the **Google Speech Recognition** to provide accurate, real-time, multilingual transcription — including **Arabic (`ar-EG`)** — for your LiveKit voice agents.

---

## 🚀 Installation

```
pip install livekit-plugins-googlesr
````

---

## 🧠 Usage Example

Use the plugin in your LiveKit Agent session:

```python
from livekit_plugins_googlesr import GoogleSTT
from livekit.agents import AgentSession, inference

session = AgentSession(
    stt=GoogleSTT(language="ar-EG"),
    # ... other components (llm, tts, vad, turn_detection)
)
```


## 🌍 Notes on Arabic Turn Detection (`ar-EG`)

LiveKit’s **Multilingual Turn Detector** currently supports a subset of languages —
**Arabic (`ar-EG`)** is not yet explicitly listed.

You might see this message:

```
2025-10-25 16:59:28,265 - INFO livekit.agents - Turn detector does not support language ar-EG
```


Keep an eye on [LiveKit Docs](https://docs.livekit.io/) for future updates on multilingual support.

---

## 🧩 Features

* ✅ Plug-and-Play integration with LiveKit Agents
* 🌐 Supports 100+ languages via Google Speech API
* ⚡ Real-time low-latency transcription
* 🗣️ Native support for Arabic (`ar-EG`)

---

## 🧪 Quick Demo (Optional)

You can also test the plugin directly without LiveKit:

```python
from livekit_plugins_googlesr import GoogleSTT

stt = GoogleSTT(language="en-US", api_key="YOUR_GOOGLE_SPEECH_API_KEY")
text = stt.transcribe("path/to/audio.wav")
print(text)
```

---

## 💡 Development & Contributing

Want to improve the plugin? Clone and install it locally:

```bash
git clone https://github.com/haitham-ramadan/livekit-plugins-googlesr.git
cd livekit-plugins-googlesr
pip install -e .
```

Pull requests and issues are welcome!
Please open an issue before submitting major changes.

---

## 🧾 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Haitham Ramadan**
💬 [GitHub](https://github.com/haitham-ramadan)

---

## ⭐ Support

If you find this project useful, please ⭐ star the repo and share it with others!
