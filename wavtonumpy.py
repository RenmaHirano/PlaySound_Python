### wavファイル -> numpy array -> plot & play sound(from array)
### 注意：大抵のWAVファイルは2chですが、1chしか出力していません。

import soundfile as sf                      # wavファイルの取り扱いに使用
import numpy as np                          # 配列処理に使用
from matplotlib import pyplot as plt        # グラフ表示に使用
import pyaudio

path = 'Heart001.wav'                       # wavファイルまでのパスを指定（名前はお手持ちのファイル名に変更して下さい）
data, samplerate = sf.read(path)            # wavファイルを読み込む

t = np.arange(0, len(data)) / samplerate    # グラフ表示のための横軸を設定

# 音声を出力するためのストリームを開く
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                frames_per_buffer=1024,
                output=True)
                
print(data[:,0])
stream.write(data[:,0].astype(np.float32).tobytes())
stream.close()

# グラフ表示
plt.plot(t, data[:,0])
plt.show()
plt.close()
