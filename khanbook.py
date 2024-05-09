from baresipy import BareSIP
import time
import os
from pydub import AudioSegment
import tempfile
import threading
import yspeech
import conversation

FRAME_RATE = 8000
to = "914828422"

gateway = "185.74.7.73"
user = "787777711"
pswd = "blablabla123A"

class Qongiroq(BareSIP):

    context = ""
    final = False

    def __init__(self, user, pswd, gateway):
        super().__init__(user, pswd, gateway, config_path="/root/.baresipy", debug=True)
        self.playing = False

    def handle_incoming_call(self, number):
        self.accept_call()

    def handle_call_established(self):
        self.accept_call()
        main_thread = threading.Thread(target=self.handle_state)
        main_thread.start()

    def handle_state(self):
        print("init");
        print(conversation.getInit()["data"]);
        # self.play_audio(yspeech.tts(conversation.getInit()["data"]))
        self.play_audio(AudioSegment.from_file(conversation.getInit()["data"], format="wav", frame_rate=FRAME_RATE, channels=2))
        self.final = False
        self.context = ""
        while not self.final:
            print("isFIAL")
            print(self.final)
            self.record_incoming_audio(3)
            text = yspeech.stt("recorded_audio.wav")
            res = conversation.getAnswer(self.context, text)
            self.context = res["context"]
            print(res)
            self.play_audio(AudioSegment.from_file(res["answer"]["data"], format="wav", frame_rate=FRAME_RATE, channels=2))
            
            if("hangup" in res["answer"]):
                self.final = res["answer"]["hangup"]
            # self.play_audio(yspeech.tts(res["answer"]["data"]))
        self.do_command("/hangup")
    
    def listenForClient(self):
        thread_play = threading.Thread(target=self.play_audio, args=(ilhomaka,))
        thread_play.start()
        thread_record = threading.Thread(target=self.record_incoming_audio, args=(15,))
        thread_record.start()
        yspeech.stt_real()

    def record_incoming_audio(self, seconds):
        if not self.call_established:
            print("Can't record audio without an active call!")
            return
        print("Recording incoming audio...")
        os.system("arecord -f S16_LE -r 8000 -c 1 -d "+str(seconds)+" -t wav /home/khanbook/qongiroq/recorded_audio.wav")  # Adjust path accordingly
    
    def play_audio(self, audio):
        if not self.call_established:
            print("Can't send audio without an active call!")
            return
        start_time = time.time()
        if len(audio) < 3000:
            audio = audio + AudioSegment.silent(
                duration=3000 - len(audio),
                frame_rate=FRAME_RATE,
            )
        audio = audio.set_frame_rate(FRAME_RATE)
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)
        wav_file = tempfile.NamedTemporaryFile(suffix=".wav").name
        audio.export(wav_file, format="wav")
        self.do_command("/ausrc gst," + "file://" + wav_file)
        print("Playing audio...")
        while time.time() - start_time < len(audio) / 1000 - 0.05:
            time.sleep(0.05)
        print("Done playing audio")
        self.do_command("/ausrc gst," + "file://" + "/root/baresipy/silence.wav")

    def handle_call_status(self, status):
        if status == "DISCONNECTED":
            self.handle_call_ended("DISCONNECTED")

b = Qongiroq(user, pswd, gateway)

b.call(to)

while b.running:
    time.sleep(0.5)
