import urllib.request
import json
from pydub import AudioSegment
import requests
import os
import time
import datetime

FRAME_RATE = 8000
# Set the folder ID and IAM token
FOLDER_ID = "b1gt2i306k1nhmrt57am"
IAM_TOKEN = "t1.9euelZqdlMqak82Tnp7Mz4mOkMaVyO3rnpWakseNmJnPx82dlp7KjpGKy5Pl8_cjVQ1O-e9bEAYP_t3z92MDC07571sQBg_-zef1656Vmo6SicnPkpSKi5mXkcmPj56Q7_zF656Vmo6SicnPkpSKi5mXkcmPj56Q.vYVQNlFtshfna8XA95yiieWT7ydovm4-Zgiox9ojdCo1LMYaWvhU1sEKCQFH_fqct2gWK5wenINZBM7lh_vsDA"

def stt(file_name):
  os.system("cp "+file_name+" temp/"+datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")+".wav")
  os.system("sox "+file_name+" out.ogg rate 22050")
  with open("out.ogg", "rb") as f:
      data = f.read()

  params = "&".join([
      "topic=general",
      "folderId=%s" % FOLDER_ID,
      "lang=uz-UZ"
  ])

  url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
  # Аутентификация через IAM-токен.
  url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

  responseData = urllib.request.urlopen(url).read().decode('UTF-8')
  decodedData = json.loads(responseData)
  print(decodedData)

  if decodedData.get("error_code") is None:
    f = open("temp/"+datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")+".txt", "a")
    f.write(decodedData["result"])
    f.close()
    print(decodedData["result"])
    return decodedData["result"]
  else:
    return ""

def stt_real():
  while True:
    time.sleep(2)
    stt("recorded_audio.wav")
   

def tts(text):
  url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
  headers = {
      'Authorization': 'Bearer ' + IAM_TOKEN,
  }

  data = {
      'text': text,
      'lang': 'uz-UZ',
      'voice': 'nigora',
      'folderId': FOLDER_ID,
      'format': 'lpcm',
      'sampleRateHertz': 48000,
  }

  data = urllib.parse.urlencode(data)
  data = data.encode('utf-8')

  req = urllib.request.Request(url, data=data, headers=headers)
  with urllib.request.urlopen(req) as resp:
      if resp.status != 200:
          raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status, resp.read().decode('utf-8')))
      with open("sound.raw", "wb") as f:
          f.write(resp.read())
      
      os.system("sox -r 48000 -b 16 -e signed-integer -c 1 sound.raw sound.wav")
      return AudioSegment.from_file("sound.wav", format="wav", frame_rate=FRAME_RATE, channels=2)