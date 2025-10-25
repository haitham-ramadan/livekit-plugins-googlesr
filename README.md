# LiveKit Google Speech Recognition (Googlesr) Plugin

This is a custom Speech-to-Text (STT) plugin for the LiveKit Agents framework, utilizing the `SpeechRecognition` library to access the Google Speech Recognition API.

## Installation

\`\`\`bash
pip install livekit-plugins-googlesr
\`\`\`

## Usage

The plugin can be used in your LiveKit Agent session as follows:

\`\`\`python
from livekit_plugins_googlesr import GoogleSTT
from livekit.agents import AgentSession, inference

session = AgentSession(
    stt=GoogleSTT(language="ar-EG"),
    # ... other components (llm, tts, vad, turn_detection)
)
\`\`\`

You can optionally pass your Google API key to the constructor or set it as an environment variable:

\`\`\`python
# Using an API key
session = AgentSession(
    stt=GoogleSTT(language="ar-EG", api_key="YOUR_GOOGLE_SPEECH_API_KEY"),
    # ...
)
\`\`\`

## Note on Turn Detection for Arabic (\`ar-EG\`)

The LiveKit Multilingual Turn Detector model currently supports a set of 14 languages, but **Arabic is not explicitly listed**.

When you use a language like \`ar-EG\` (Arabic - Egyptian) with the \`MultilingualModel\`, you may receive a warning:

\`\`\`
2025-10-25 16:59:28,265 - INFO livekit.agents - Turn detector does not support language ar-EG
\`\`\`

This warning indicates that the turn detection model will fall back to a less language-specific mode, which may slightly reduce its accuracy for turn-taking in Arabic conversations. The STT itself (via Google Speech Recognition) will still function correctly in Arabic.

To avoid this warning, you can:
1. **Omit the \`turn_detection\` component** if you are comfortable relying solely on the VAD (Voice Activity Detection) endpointing.
2. **Use the \`MultilingualModel\` and accept the warning**, knowing that the STT is working and the turn detection will use its best-effort, non-language-specific logic.

For the best experience, keep an eye on the official LiveKit documentation for updates on multilingual turn detection support.
\`\`\`
