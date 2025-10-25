from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import speech_recognition as sr
from livekit import rtc
from livekit.agents import (
    APIConnectionError,
    APIConnectOptions,
    stt,
)
from livekit.agents.stt import SpeechEventType, STTCapabilities
from livekit.agents.utils import AudioBuffer


@dataclass
class _GoogleSTTOptions:
    language: str
    show_all: bool
    phrase_threshold: Optional[float] = None
    energy_threshold: int = 300


class GoogleSTT(stt.STT):
    """
    Google Speech Recognition implementation for LiveKit agents

    This class requires the SpeechRecognition library:
    pip install SpeechRecognition
    """
    def __init__(
        self,
        *,
        language: Optional[str] = "en-US",
        show_all: bool = False,
        phrase_threshold: Optional[float] = None,
        energy_threshold: int = 300,
        api_key: Optional[str] = None,
    ):
        super().__init__(
            capabilities=STTCapabilities(streaming=False, interim_results=False)
        )
        self._api_key = api_key or os.getenv("GOOGLE_SPEECH_API_KEY")
        self._opts = _GoogleSTTOptions(
            language=language or "en-US",
            show_all=show_all,
            phrase_threshold=phrase_threshold,
            energy_threshold=energy_threshold,
        )
        self._recognizer = sr.Recognizer()
        self._recognizer.energy_threshold = energy_threshold
        if phrase_threshold is not None:
            self._recognizer.phrase_threshold = phrase_threshold

    def update_options(self, *, language: Optional[str] = None) -> None:
        """Update the language option for the STT engine"""
        self._opts.language = language or self._opts.language

    async def _recognize_impl(
        self,
        buffer: AudioBuffer,
        *,
        language: str | None,
        conn_options: APIConnectOptions,
    ) -> stt.SpeechEvent:
        try:
            # Override with provided language if available
            config_language = language or self._opts.language
            
            # Convert LiveKit audio buffer to WAV format for SpeechRecognition
            wav_bytes = rtc.combine_audio_frames(buffer).to_wav_bytes()
            
            # Create an audio source from bytes
            # The sample rate and width must match the buffer's properties.
            # LiveKit uses 16-bit PCM, which is 2 bytes per sample.
            audio_data = sr.AudioData(wav_bytes, 
                                     sample_rate=buffer.sample_rate,
                                     sample_width=2)
            
            # Perform recognition
            text = ""
            if self._api_key:
                # Use API key if provided
                text = self._recognizer.recognize_google(
                    audio_data=audio_data,
                    key=self._api_key,
                    language=config_language,
                    show_all=self._opts.show_all
                )
            else:
                # Use free tier if no API key
                text = self._recognizer.recognize_google(
                    audio_data=audio_data,
                    language=config_language,
                    show_all=self._opts.show_all
                )
                
            # Handle possible dict response when show_all=True
            if isinstance(text, dict):
                if 'alternative' in text and len(text['alternative']) > 0:
                    text = text['alternative'][0].get('transcript', '')
                else:
                    text = ""
                    
            return self._create_speech_event(text=text, language=config_language)
            
        except sr.UnknownValueError:
            # Speech was unintelligible
            return self._create_speech_event(text="", language=config_language)
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            raise APIConnectionError(f"Google Speech Recognition error: {e}") from e
        except Exception as e:
            raise APIConnectionError(f"Error in speech recognition: {e}") from e

    def _create_speech_event(
        self, text: str, language: str, event_type=SpeechEventType.FINAL_TRANSCRIPT
    ) -> stt.SpeechEvent:
        """Create a speech event from recognized text"""
        return stt.SpeechEvent(
            type=event_type,
            alternatives=[stt.SpeechData(text=text, language=language)],
        )

    async def aclose(self) -> None:
        """Close any resources used by this STT implementation"""
        pass

    @staticmethod
    def load() -> "GoogleSTT":
        """Load the GoogleSTT plugin. Added for LiveKit plugin convention."""
        return GoogleSTT()
