import pyaudio
import os
import wave
import numpy as np
from datetime import datetime

CHUNK_SIZE = 2**10
baseFile = "turkish-march.wav"

p = pyaudio.PyAudio()
# 再生準備
wf = wave.open(baseFile, 'rb')
playStream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
 
# 音データフォーマット
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

# 閾値
threshold = 0.1

# 音の取込開始
stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = chunk
)

playFrame = 0 # どこまで再生したか

while True:
    # 再生データの取得
    playData = wf.readframes(CHUNK_SIZE)
    if len(playData) > 0:
      playStream.write(playData)
      playFrame = playFrame + len(playData)
    else:
      break

    # 音データの取得
    data = stream.read(chunk)
    # ndarrayに変換
    x = np.frombuffer(data, dtype="int16") / 32768.0

    # 閾値以上の場合はファイルに保存
    if x.max() > threshold:
        filename = os.path.join("out", os.path.splitext(baseFile)[0] +  "-" +  str(playFrame) + ".wav")
        print(filename)

        # 2秒間の音データを取込
        all = []
        all.append(data)
        isContinue = True
        print("stop play at frame:" + str(playFrame))
        while isContinue:
            isContinue = False
            print("next record")
            for i in range(0, int(RATE / chunk * int(RECORD_SECONDS))):
                data = stream.read(chunk)
                if isContinue == False:
                    # ndarrayに変換
                    x = np.frombuffer(data, dtype="int16") / 32768.0
                    if x.max() > threshold:
                        isContinue = True
                        print("detect sound")
                all.append(data)
        print("finish record")
        data = b''.join(all)

        # 音声ファイルとして出力
        out = wave.open(filename,'w')
        out.setnchannels(CHANNELS)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(data)
        out.close()
        print("Saved.")

stream.close()

playStream.stop_stream()
playStream.close()

p.terminate()

