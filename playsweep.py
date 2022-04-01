# 任意の配列からその配列の音声を再生するコード
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import datetime as dt
from scipy.signal import chirp, spectrogram

RATE = 44100  # 44.1khz
WAVE_END_TIME = 30  # 秒の振動になる
                 # ここからは2音に関わるパラメータ

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
def GenerateHeartbeat(saveSoundOption = False):
    time = np.arange(RATE*WAVE_END_TIME) / RATE  # = t
    sweepWave = chirp(time, f0=20, f1=500, t1=WAVE_END_TIME, method='linear')
    
    if saveSoundOption:
        nowTime = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
        out = np.tile(sweepWave, 1)
            
        write("sweep.wav" , RATE, out.astype(np.float32))
        
    return sweepWave

# 図出力部分
def PlotGraph(sweepWave):
    plt.ylim(-1, 1)
    plt.yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    plt.xlim(0, RATE)
    plt.xticks([0, RATE/4, RATE*2/4, RATE*3/4, RATE])
    plt.plot(sweepWave[0:RATE])
    plt.show()
    
    pass

# 音声を出力
def PlaySound(sweepWave, stream):
    print("play sound")
    out = np.tile(sweepWave, REPEAT_TIMES)
    stream.write(out.astype(np.float32).tobytes())
    stream.close()
    
    pass

def main():
    wave = GenerateHeartbeat(True)
    PlotGraph(wave)
    
    pass

if __name__ == "__main__":
    main()
