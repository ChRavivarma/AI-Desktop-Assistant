import base64
import os
from threading import Lock, Thread
import time
import warnings
import numpy
import cv2
import openai
from PIL import ImageGrab
from cv2 import VideoCapture, imencode
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()
print("=" * 40)
print("GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY"))
print("MODEL_PROVIDER =", os.getenv("MODEL_PROVIDER"))
print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("=" * 40)

try:
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
except ImportError:
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

try:
    from langchain_core.messages import SystemMessage
except ImportError:
    from langchain.schema.messages import SystemMessage

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from pyaudio import PyAudio, paInt16
from speech_recognition import Microphone, Recognizer, UnknownValueError, RequestError

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

load_dotenv()


class DesktopScreenshot:
    def __init__(self):
        self.screenshot = None
        self.running = False
        self.lock = Lock()

    def start(self):
        if self.running:
            return self

        self.running = True
        self.thread = Thread(target=self.update, daemon=True)
        self.thread.start()
        return self

    def update(self):
        while self.running:
            try:
                screenshot = ImageGrab.grab()
                screenshot = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)
                with self.lock:
                    self.screenshot = screenshot
            except Exception:
                pass
            time.sleep(0.1)

    def read(self, encode=False):
        with self.lock:
            screenshot = self.screenshot.copy() if self.screenshot is not None else None

        if encode and screenshot is not None:
            _, buffer = imencode(".jpeg", screenshot)
            return base64.b64encode(buffer)

        return screenshot

    def stop(self):
        self.running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join(timeout=1.0)


class WebcamStream:
    def __init__(self):
        self.stream = VideoCapture(index=0)
        self.frame = None
        if self.stream.isOpened():
            _, self.frame = self.stream.read()
        self.running = False
        self.lock = Lock()

    def start(self):
        if self.running:
            return self

        self.running = True
        self.thread = Thread(target=self.update, daemon=True)
        self.thread.start()
        return self

    def update(self):
        while self.running:
            if self.stream.isOpened():
                grabbed, frame = self.stream.read()
                if grabbed:
                    with self.lock:
                        self.frame = frame
            time.sleep(0.03)

    def read(self, encode=False):
        with self.lock:
            frame = self.frame.copy() if self.frame is not None else None

        if frame is None:
            return None

        if encode:
            _, buffer = imencode(".jpeg", frame)
            return base64.b64encode(buffer)

        return frame

    def stop(self):
        self.running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        if self.stream.isOpened():
            self.stream.release()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop()


class Assistant:
    def __init__(self, model):
        self.chain = self._create_inference_chain(model)

    def answer(self, prompt, image):
        if not prompt:
            return

        print("\n" + "="*50)
        print("User Question:", prompt)
        print("="*50)

        image_str = image.decode() if isinstance(image, bytes) else ""

        try:
            response = self.chain.invoke(
                {"prompt": prompt, "image_base64": image_str},
                config={"configurable": {"session_id": "unused"}},
            ).strip()

            print("\nAssistant Response:", response)
            print("="*50 + "\n")

            if response:
                self._tts(response)
        except Exception as e:
            print(f"\n[AI Model Error]: {e}")
            err_msg = str(e)
            if "NOT_FOUND" in err_msg or "404" in err_msg:
                print("[TIP] Gemini Model 404 Error: Make sure GOOGLE_API_KEY in .env is created at https://aistudio.google.com/app/apikey (starts with 'AIzaSy').")
                print("[TIP] You can also try setting GEMINI_MODEL=gemini-2.0-flash or GEMINI_MODEL=gemini-1.5-flash-latest in .env")
            elif "402" in err_msg or "credits" in err_msg:
                print("[TIP] OpenRouter credit limit reached. Switch to OPENROUTER_MODEL=openai/gpt-4o-mini in .env")
            elif any(err in err_msg for err in ["401", "User not found", "Incorrect API key", "API_KEY"]):
                print("[ERROR] API Key issue detected. Please check your .env file configuration.")

    def _tts(self, response):
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key and not api_key.startswith("sk-or-v1-"):
            try:
                player = PyAudio().open(format=paInt16, channels=1, rate=24000, output=True)
                client = openai.OpenAI(api_key=api_key)
                with client.audio.speech.with_streaming_response.create(
                    model="tts-1",
                    voice="alloy",
                    response_format="pcm",
                    input=response,
                ) as stream:
                    for chunk in stream.iter_bytes(chunk_size=1024):
                        player.write(chunk)
                player.stop_stream()
                player.close()
                return
            except Exception as e:
                print(f"[OpenAI TTS Notice] Fallback to offline TTS: {e}")

        # Offline TTS fallback using pyttsx3
        if pyttsx3:
            try:
                engine = pyttsx3.init()
                engine.say(response)
                engine.runAndWait()
            except Exception as tts_err:
                print(f"[TTS Audio Error]: {tts_err}")
        else:
            print("[TTS Notice] pyttsx3 not installed for offline speech.")

    def _create_inference_chain(self, model):
        SYSTEM_PROMPT = """
        You are a witty assistant that will use the chat history and the image 
        provided by the user to answer its questions. Your job is to answer 
        questions.

        Use few words on your answers. Go straight to the point. Do not use any
        emoticons or emojis. 

        Be friendly and helpful. Show some personality.
        """

        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    [
                        {"type": "text", "text": "{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": "data:image/jpeg;base64,{image_base64}",
                        },
                    ],
                ),
            ]
        )

        chain = prompt_template | model | StrOutputParser()

        chat_message_history = ChatMessageHistory()
        return RunnableWithMessageHistory(
            chain,
            lambda _: chat_message_history,
            input_messages_key="prompt",
            history_messages_key="chat_history",
        )
# ============================================================
# Initialization (shared by terminal app and Streamlit)
# ============================================================

print("Initializing webcam and desktop screenshot streams...")
webcam_stream = WebcamStream().start()
desktop_screenshot = DesktopScreenshot().start()

print("Initializing AI Model...")

provider = os.getenv("MODEL_PROVIDER", "").lower()
google_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY", "")
groq_key = os.getenv("GROQ_API_KEY")

model = None

if provider == "gemini" or (not provider and google_key):
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI

        gemini_model = os.getenv(
            "GEMINI_MODEL",
            "gemini-flash-latest"
        )

        print(f"Using Google Gemini Model ({gemini_model})...")

        model = ChatGoogleGenerativeAI(
            model=gemini_model,
            google_api_key=google_key
        )

    except Exception as e:
        print(f"[Gemini Init Notice] {e}")

if model is None and (provider == "groq" or (not provider and groq_key)):
    try:
        from langchain_groq import ChatGroq

        groq_model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        )

        print(f"Using Groq Model ({groq_model})...")

        model = ChatGroq(
            model_name=groq_model,
            groq_api_key=groq_key
        )

    except Exception as e:
        print(f"[Groq Init Notice] {e}")

if model is None and provider == "ollama":
    try:
        from langchain_community.chat_models import ChatOllama

        ollama_model = os.getenv(
            "OLLAMA_MODEL",
            "llama3.2-vision"
        )

        model = ChatOllama(model=ollama_model)

    except Exception as e:
        print(f"[Ollama Init Notice] {e}")

if model is None:

    if openai_key.startswith("sk-or-v1-"):

        openrouter_model = os.getenv(
            "OPENROUTER_MODEL",
            "openai/gpt-4o-mini"
        )

        model = ChatOpenAI(
            model=openrouter_model,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=openai_key,
        )

    else:

        openai_model = os.getenv(
            "OPENAI_MODEL",
            "gpt-4o"
        )

        model = ChatOpenAI(
            model=openai_model,
            openai_api_key=openai_key,
        )

assistant = Assistant(model)


def ask_ai(prompt):

    screenshot_data = desktop_screenshot.read(
        encode=True
    )

    image_str = screenshot_data.decode() if screenshot_data else ""

    response = assistant.chain.invoke(
        {
            "prompt": prompt,
            "image_base64": image_str,
        },
        config={
            "configurable": {
                "session_id": "streamlit"
            }
        },
    )

    return str(response)
# ============================================================
# Voice Callback
# ============================================================

def audio_callback(recognizer, audio):

    print("\n[Audio detected] Processing speech...")

    prompt = None

    try:

        try:
            prompt = recognizer.recognize_google(
                audio,
                language="en-US",
            )

            print(f'[Speech STT (Google)]: "{prompt}"')

        except (UnknownValueError, RequestError) as google_err:

            try:

                prompt = recognizer.recognize_whisper(
                    audio,
                    model="base",
                    language="english",
                )

                print(f'[Speech STT (Whisper)]: "{prompt}"')

            except Exception:

                print(
                    f"[Audio STT Notice] Could not understand speech: {google_err}"
                )
                return

        if prompt and prompt.strip():

            print(f"\nUser (Voice): {prompt.strip()}")

            screenshot_data = desktop_screenshot.read(
                encode=True
            )

            assistant.answer(
                prompt.strip(),
                screenshot_data,
            )

        else:

            print("[Audio] No clear speech recognized.")

    except Exception as e:

        print(f"[Audio Processing Error]: {e}")

def main():

    print("\nSetting up microphone...")

    recognizer = Recognizer()

    recognizer.energy_threshold = 150
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_ratio = 1.2
    recognizer.pause_threshold = 0.6
    recognizer.phrase_threshold = 0.2

    mic_names = Microphone.list_microphone_names()

    mic_index_env = os.getenv("MICROPHONE_INDEX")

    selected_mic_idx = None

    if mic_index_env:

        try:

            idx = int(mic_index_env)

            if 0 <= idx < len(mic_names):

                selected_mic_idx = idx

        except ValueError:

            pass

    if selected_mic_idx is None:

        print("Available audio input devices:")

        for idx, name in enumerate(mic_names):

            lower = name.lower()

            if (
                any(k in lower for k in ["mic", "array", "input"])
                and not any(k in lower for k in ["speaker", "output"])
            ):

                print(f"  Index {idx}: {name}")

                if selected_mic_idx is None:

                    selected_mic_idx = idx

    if selected_mic_idx is not None:

        print(
            f"Using microphone Index {selected_mic_idx}: {mic_names[selected_mic_idx]}"
        )

        microphone = Microphone(device_index=selected_mic_idx)

    else:

        print("Using default microphone.")

        microphone = Microphone()

    with microphone as source:

        print("Calibrating ambient noise (0.5s)...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5,
        )

    if recognizer.energy_threshold > 500:

        recognizer.energy_threshold = 300

    print(
        f"Microphone sensitivity threshold set to: {int(recognizer.energy_threshold)}"
    )

    print("Starting background audio listener...")

    stop_listening = recognizer.listen_in_background(
        microphone,
        audio_callback,
    )
    def terminal_input_thread():

        time.sleep(1.0)

        print("\n" + "=" * 65)
        print("  AI ASSISTANT IS ACTIVE & READY!")
        print("  1. SPEAK into your mic (voice mode)")
        print("  2. OR TYPE questions in this terminal and press Enter!")
        print("  3. Press 'q' or ESC on OpenCV video window to exit.")
        print("=" * 65 + "\n")

        while True:

            try:

                user_text = input()

                if user_text and user_text.strip():

                    clean_text = user_text.strip()

                    if clean_text.lower() in ["exit", "quit"]:
                        break

                    print(f"\nUser (Typed): {clean_text}")

                    screenshot_data = desktop_screenshot.read(
                        encode=True
                    )

                    assistant.answer(
                        clean_text,
                        screenshot_data,
                    )

            except (EOFError, KeyboardInterrupt):
                break

    input_thread = Thread(
        target=terminal_input_thread,
        daemon=True,
    )

    input_thread.start()

    try:

        while True:

            webcam_frame = webcam_stream.read()

            if webcam_frame is not None:
                cv2.imshow(
                    "Webcam Stream",
                    webcam_frame,
                )

            screenshot = desktop_screenshot.read()

            if screenshot is not None:
                cv2.imshow(
                    "Desktop Screenshot",
                    screenshot,
                )

            key = cv2.waitKey(30)

            if key in [27, ord("q")]:
                break

    except KeyboardInterrupt:

        print("\nShutdown requested...")

    print("Shutting down assistant...")

    webcam_stream.stop()
    desktop_screenshot.stop()

    cv2.destroyAllWindows()

    try:
        stop_listening(wait_for_stop=False)
    except Exception:
        pass

    print("Shutdown complete.")

if __name__ == "__main__":
        main()