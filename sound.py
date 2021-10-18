### 任意の配列からその配列の音声を再生するコード

import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# 音声を出力するためのストリームを開く
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                frames_per_buffer=1024,
                output=True)

# samplesに好きな配列を入れる -> これが波形になります
samples = np.sin(np.arange(50000) / 20)
plt.plot(samples[0:500])
plt.show()

# sample波を出力
print("play")
print(samples)
stream.write(samples.astype(np.float32).tobytes())
stream.close()
