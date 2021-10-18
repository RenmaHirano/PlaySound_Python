### wavファイル -> numpy array -> plot & play sound(from array)
### 注意：大抵のWAVファイルは2chですが、1chしか出力していません。

import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
import pyaudio

# read wav file
path = 'Heart001.wav'
data, samplerate = sf.read(path)

# グラフ表示のための横軸を設定
t = np.arange(0, len(data)) / samplerate

# グラフ表示
plt.plot(t, data[:,0])
plt.show()
plt.close()

# 音声を出力するためのストリームを開く
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                frames_per_buffer=1024,
                output=True)
                
# ch2(data) -> ch1(data[:,0])
print(data[:,0])
stream.write(data[:,0].astype(np.float32).tobytes())
stream.close()
