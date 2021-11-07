# 任意の配列からその配列の音声を再生するコード
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import datetime as dt

RATE = 44100  # 44.1khz
REPEAT_TIMES = 5  # 回心音を鳴らす
WAVE_END_TIME = 1  # 秒の振動になる
                 # ここからは2音に関わるパラメータ
DEFAULT_SECOND_WAVE_SHIFT = 0.3 # 心音が1秒に1回なると仮定した際、1音と2音がなる間の時間(sec)
                     # 普通は大体0.3秒くらいらしい
SECOND_WAVE_LOUDNESS = 0.3 # 1音に対する音量の比。たとえば0.1なら1/10の音量になります。

GAIN_LIST = [5, 10, 20]
FREQ_LIST = [30, 100, 300]
ATTENUATION_LIST = [10, 30]
PHI_LIST = [0.15, 0.35]

# 音声を出力するためのストリームを開く
def OpenStream():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,   # int32型
                    channels=1,                 # モノラル
                    rate=RATE,                 # 44.1khz
                    frames_per_buffer=1024,     # よくわからないが1024以外にするとエラーが起きる。
                    output=True)                # 録音する時はinput = trueにする
    return stream

# 心音出力関数(gain * sin(2*PIE*frequency*t)*exp(-attenuationRate * t)の減衰正弦波形)
def GenerateHeartbeat(gain :float, frequency: float, attenuationRate: float, secondWaveShift: float, saveSoundOption = False):
    time = np.arange(RATE*WAVE_END_TIME) / RATE  # = t
    attenuationArray = np.exp(-1 * attenuationRate * time) # = exp(-Bt)
    basicWave = gain * np.sin(2 * np.pi * frequency * time) * attenuationArray  # = A*sin(2*PIE*f*t)*exp(-Bt)
    firstWave = basicWave
    secondWave = SECOND_WAVE_LOUDNESS * np.roll(basicWave, int(RATE * WAVE_END_TIME * secondWaveShift))
    heartBeatWave = firstWave + secondWave
    
    if saveSoundOption:
        nowTime = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
        out = np.tile(heartBeatWave, REPEAT_TIMES)
        write("output" + nowTime + "_Gain" + str(gain) + "_Freq" + str(frequency) + "_Atten" + str(attenuationRate) + "_Phi" + str(secondWaveShift) + ".wav" , RATE, out.astype(np.float32))
    
    return heartBeatWave

# 図出力部分
def PlotGraph(heartBeatWave):
    plt.plot(heartBeatWave[0:RATE])
    plt.show()
    
    pass

# 音声を出力
def PlaySound(heartBeatWave, stream):
    print("play sound")
    out = np.tile(heartBeatWave, REPEAT_TIMES)
    stream.write(out.astype(np.float32).tobytes())
    stream.close()
    
    pass

def main():
    for gain in GAIN_LIST:
        for frequency in FREQ_LIST:
            for attenuationRate in ATTENUATION_LIST:
                for phi in PHI_LIST:
                    wave = GenerateHeartbeat(gain, frequency, attenuationRate, phi, True)
    
    pass

if __name__ == "__main__":
    main()
