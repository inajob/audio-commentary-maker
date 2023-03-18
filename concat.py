#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wave
import os
import sys
baseFile = sys.argv[1]
outFile = "convined.wav"

CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 2**10
voices = {}

files = os.listdir("out")

for x in files:
    part = os.path.splitext(x)
    if part[1] == ".wav":
        part2 = part[0].split("-")
        fileName = "-".join(part2[:-1])
        frame = int(part2[-1])
        voices.setdefault(fileName, [])
        voices[fileName].append(frame)

print(voices)

outf = wave.open(outFile, 'wb')
outf.setnchannels(CHANNELS)
outf.setsampwidth(2)
outf.setframerate(RATE)

def writeFrames(fileName):
  filePart = os.path.splitext(os.path.basename(fileName))
  playf = wave.open(fileName, 'rb')
  playFrame = 0
  print(filePart)
  while True:
      playData = playf.readframes(CHUNK_SIZE)
      if len(playData) == 0:
        break;
      outf.writeframes(playData)
      if len(playData) > 0:
        playFrame = playFrame + len(playData)
      if voices.get(filePart[0]) and playFrame in voices[filePart[0]]:
          print("insert " + str(playFrame))
          writeFrames(os.path.join("out", filePart[0] + "-" + str(playFrame)) + ".wav");
          voices[filePart[0]].remove(playFrame)
  playf.close();

writeFrames(baseFile)
outf.close();
print("un processing voices")
print(voices)

