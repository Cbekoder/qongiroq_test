import conversation
import yspeech
from pydub.playback import play
import sounddevice as sd
from pydub import AudioSegment
from scipy.io.wavfile import write

def record_audio(duration, file_name):
    # Set the sampling frequency and channels
    fs = 48000  # 44.1 kHz
    # Record audio
    print("Recording...")
    audio_data = sd.rec( int ( duration * fs ) , samplerate = fs , channels = 1 )
    sd.wait()
    print("Recording complete.")
    write(file_name,fs,audio_data)
    return audio_data, fs

hangup = False
context = ""

def answer(data):
  print("B:"+data["data"])

FRAME_RATE = 8000
answer(conversation.getInit())
play(yspeech.tts(conversation.getInit()["data"]))
# play(AudioSegment.from_file(conversation.getInit()["data"], format="wav", frame_rate=FRAME_RATE, channels=2))
while not(hangup):
  record_audio(3, "rec.wav")
  q = yspeech.stt("rec.wav")
  res = conversation.getAnswer(context, q)
  print(res)
  answer(res["answer"])
  play(yspeech.tts(res["answer"]["data"]))
  # play(AudioSegment.from_file(res["answer"]["data"], format="wav", frame_rate=FRAME_RATE, channels=2))
  context = res["context"]
  print(context)
  if "hangup" in res["answer"]:
    hangup = res["answer"]["hangup"]