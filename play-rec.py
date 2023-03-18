import pyaudio
import os
import wave
import numpy as np
from datetime import datetime

CHUNK_SIZE = 2**10
baseFile = "turkish-march.wav"

voices = {}
# 既存のオーディオコメンタリーファイルの検索
files = os.listdir("out")
for x in files:
    part = os.path.splitext(x)
    part2 = part[0].split("-")
    fileName = "-".join(part2[:-1])
    frame = int(part2[-1])
    voices.setdefault(fileName, [])
    voices[fileName].append(frame)


p = pyaudio.PyAudio()

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


def playFrames(fileName):
    playFrame = 0 # どこまで再生したか
    filePart = os.path.splitext(os.path.basename(fileName))
    print(filePart)
    # 再生準備
    wf = wave.open(fileName, 'rb')
    playStream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
 
    while True:
        # 再生データの取得
        playData = wf.readframes(CHUNK_SIZE)
        if len(playData) > 0:
          playStream.write(playData)
          playFrame = playFrame + len(playData)
        else:
          break
    
        if voices.get(filePart[0]) and playFrame in voices[filePart[0]]:
            playFrames(os.path.join("out", filePart[0] + "-" + str(playFrame)) + ".wav")

        # 音データの取得
        data = stream.read(chunk)
        # ndarrayに変換
        x = np.frombuffer(data, dtype="int16") / 32768.0
    
        # 閾値以上の場合はファイルに保存
        if False and x.max() > threshold:
            filename = os.path.join("out", filePart[0] +  "-" +  str(playFrame) + ".wav")
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
    playStream.stop_stream()
    playStream.close()

playFrames(baseFile)
stream.close()

playStream.stop_stream()
playStream.close()

p.terminate()

