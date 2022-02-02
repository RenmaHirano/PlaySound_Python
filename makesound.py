# 任意の配列からその配列の音声を再生するコード
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import datetime as dt

RATE = 44100  # 44.1khz
REPEAT_TIMES = 1  # 回心音を鳴らす
WAVE_END_TIME = 1  # 秒の振動になる
                 # ここからは2音に関わるパラメータ
DEFAULT_SECOND_WAVE_SHIFT = 0.3 # 心音が1秒に1回なると仮定した際、1音と2音がなる間の時間(sec)
                     # 普通は大体0.3秒くらいらしい
DEFAULT_SECOND_WAVE_LOUDNESS = 0.3 # 1音に対する音量の比。たとえば0.1なら1/10の音量になります。

GAIN_LIST = [1.0]
GAIN_RATIO_LIST = [0.3, 0.5, 0.7]
ATTENUATION_LIST = [20, 30, 40]
FREQ_LIST = [30, 100, 300]
PHI_LIST = [0.2, 0.3, 0.4]

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
def GenerateHeartbeat(gain :float, gainRatio :float, frequency: float, attenuationRate: float, secondWaveShift: float, saveSoundOption = False):
    time = np.arange(RATE*WAVE_END_TIME) / RATE  # = t
    attenuationArray = np.exp(-1 * attenuationRate * time) # = exp(-Bt)
    basicWave = gain * np.sin(2 * np.pi * frequency * time) * attenuationArray  # = A*sin(2*PIE*f*t)*exp(-Bt)
    firstWave = basicWave
    secondWave = gainRatio * np.roll(basicWave, int(RATE * WAVE_END_TIME * secondWaveShift))
    heartBeatWave = firstWave + secondWave
    
    if saveSoundOption:
        nowTime = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
        out = np.tile(heartBeatWave, REPEAT_TIMES)
        
        freqString = ""
        if frequency == FREQ_LIST[0]:
            freqString = "Low"
        if frequency == FREQ_LIST[1]:
            freqString = "Medium"
        if frequency == FREQ_LIST[2]:
            freqString = "High"

        attenuationString = ""
        if attenuationRate == ATTENUATION_LIST[0]:
            attenuationString = "Low"
        if attenuationRate == ATTENUATION_LIST[1]:
            attenuationString = "Medium"
        if attenuationRate == ATTENUATION_LIST[2]:
            attenuationString = "High"

        phiString = ""
        if secondWaveShift == PHI_LIST[0]:
            phiString = "Low"
        if secondWaveShift == PHI_LIST[1]:
            phiString = "Medium"
        if secondWaveShift == PHI_LIST[2]:
            phiString = "High"
        
        gainRatioString = ""
        if gainRatio == GAIN_RATIO_LIST[0]:
            gainRatioString = "Low"
        if gainRatio == GAIN_RATIO_LIST[1]:
            gainRatioString = "Medium"
        if gainRatio == GAIN_RATIO_LIST[2]:
            gainRatioString = "High"
            
        write(gainRatioString + freqString + attenuationString + phiString + ".wav" , RATE, out.astype(np.float32))
        
    return heartBeatWave

# 図出力部分
def PlotGraph(heartBeatWave):
    plt.title("A="+ str(gain) +", B="+ str(attenuationRate) + ", C=" + str(round(gainRatio,1)) +  ", phi=" + str(phi) + ", f=" + str(frequency), fontsize = 16)
    plt.ylim(-1, 1)
    plt.yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    plt.xlim(0, RATE)
    plt.xticks([0, RATE/4, RATE*2/4, RATE*3/4, RATE])
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
                    for gainRatio in GAIN_RATIO_LIST:
                        wave = GenerateHeartbeat(gain, gainRatio, frequency, attenuationRate, phi, True)
                        ##PlotGraph(wave)
    
    pass

if __name__ == "__main__":
    main()
