import wave
import os
baseFile = "turkish-march.wav"
outFile = "convined.wav"
files = os.listdir("out")

CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 2**10
voices = {}

for x in files:
    part = os.path.splitext(x)
    part2 = part[0].split("-")
    fileName = "-".join(part2[:-1])
    frame = int(part2[-1])
    voices.setdefault(fileName, [])
    voices[fileName].append(frame)
print(voices)


of = wave.open(outFile, 'wb')
of.setnchannels(CHANNELS)
of.setsampwidth(2)
of.setframerate(RATE)

def writeFrames(fileName):
  filePart = os.path.splitext(os.path.basename(fileName))
  wf = wave.open(fileName, 'rb')
  playFrame = 0
  print(filePart)
  while True:
      playData = wf.readframes(CHUNK_SIZE)
      if len(playData) == 0:
        break;
      of.writeframes(playData)
      if len(playData) > 0:
        playFrame = playFrame + len(playData)
      if voices.get(filePart[0]) and playFrame in voices[filePart[0]]:
          print("insert " + str(playFrame))
          writeFrames(os.path.join("out", filePart[0] + "-" + str(playFrame)) + ".wav");
          voices[filePart[0]].remove(playFrame)
  wf.close();

writeFrames(baseFile)
of.close();
print("un processing voices")
print(voices)

