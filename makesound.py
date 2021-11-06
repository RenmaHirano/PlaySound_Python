# 任意の配列からその配列の音声を再生するコード

import pyaudio
import numpy as np
import matplotlib.pyplot as plt

RATE = 44100  # 44.1khz
REPEAT_TIMES = 5  # 回心音を鳴らす

gain = 20  # 初期振幅
frequency = 40  # (Hz)
attenuationRate = 30  # 減衰率
waveEndTime = 1  # 秒の振動になる
# ここからは2音に関わるパラメータ
secondWaveShit = 0.3 # 心音が1秒に1回なると仮定した際、1音と2音がなる間の時間(sec)
                     # 普通は大体0.3秒くらいらしい
secondWaveLoundness = 0.3 # 1音に対する音量の比。たとえば0.1なら1/10の音量になります。

# 音声を出力するためのストリームを開く
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,   # int32型
                channels=1,                 # モノラル
                rate=RATE,                 # 44.1khz
                frames_per_buffer=1024,     # よくわからないが1024以外にするとエラーが起きる。
                output=True)                # 録音する時はinput = trueにする

# 心音計算部分(A*sin(2*PIE*f*t)*exp(-Bt)の減衰正弦波形)
time = np.arange(RATE*waveEndTime) / RATE  # = t
attenuationArray = np.exp(-1 * attenuationRate * time) # = exp(-Bt)
basicWave = np.sin(2 * np.pi * frequency * time) * attenuationArray  # = A*sin(2*PIE*f*t)*exp(-Bt)
firstWave = basicWave
secondWave = secondWaveLoundness * np.roll(basicWave, int(RATE * waveEndTime * secondWaveShit))
heatBeatWave = firstWave + secondWave

# 図出力部分
plt.plot(heatBeatWave[0:RATE])
plt.show()

# 音声を出力
print("play")
out = np.tile(heatBeatWave, REPEAT_TIMES)
stream.write(out.astype(np.float32).tobytes())
stream.close()
