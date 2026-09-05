import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_PATH = "model"
SAMPLE_RATE = 16000

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
audio_queue = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))


def get_voice_command():
    print("\n🎤 MonSight is listening...")
    print("Say your command...")

    with sd.RawInputStream(
    device=1,
    samplerate=SAMPLE_RATE,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=callback
    ):
        
        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()

                if text:
                    print(f"🎤 You said: {text}")
                    return text


if __name__ == "__main__":
    command = get_voice_command()
    print("Command:", command)