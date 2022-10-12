# 任意の配列からその配列の音声を再生するコード
from pickle import LIST, TRUE
from telnetlib import GA
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

GAIN_LIST = [1.0, 0.27, 0.108, 0.72, 0.73]
GAIN_RATIO_LIST = [0.3]
ATTENUATION_LIST = [30]
FREQ_LIST = [50, 112.5, 175, 237.5, 300]
PHI_LIST = [0.2, 0.25, 0.3, 0.35, 0.4]

# 音声を出力するためのストリームを開く
def OpenStream():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,   # float32型
                    channels=1,                 # モノラル
                    rate=RATE,                 # 44.1khz
                    frames_per_buffer=1024,     # よくわからないが1024以外にするとエラーが起きる。
                    output=True)                # 録音する時はinput = trueにする
    return stream

def GenerateSinWave():
    gain = 1.0
    freq = 0
    time = np.arange(RATE*10) / RATE  # = t
    sinWave = gain * np.sin(2 * np.pi * FREQ_LIST[freq] * time)
    
    out = np.tile(sinWave, REPEAT_TIMES)
    write( "freq" + str(freq) + "gain" + str(gain) + ".wav" , RATE, out.astype(np.float32))
    
    return sinWave

def GenerateHeartbeatWave(gain :float, gainRatio :float, frequency: float, attenuationRate: float, secondWaveShift: float, saveSoundOption = False):
    time = np.arange(RATE*WAVE_END_TIME) / RATE  # = t
    attenuationArray = np.exp(-1 * attenuationRate * time) # = exp(-Bt)
    basicalWaveShift = 0.1
    basicWave = gain * np.sin(2 * np.pi * frequency * time) * attenuationArray  # = A*sin(2*PIE*f*t)*exp(-Bt)
    firstWave = np.roll(basicWave, int(RATE * WAVE_END_TIME * basicalWaveShift))
    secondWave = gainRatio * np.roll(firstWave, int(RATE * WAVE_END_TIME * secondWaveShift))
    heartBeatWave = firstWave + secondWave
    
    if saveSoundOption:
        nowTime = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
        out = np.tile(heartBeatWave, REPEAT_TIMES)
        
        gainRatioString = ""
        if gainRatio == GAIN_RATIO_LIST[0]:
            gainRatioString = "Medium"
        
        freqString = ""
        if frequency == FREQ_LIST[0]:
            freqString = "Low"
        if frequency == FREQ_LIST[1]:
            freqString = "LowerMed"
        if frequency == FREQ_LIST[2]:
            freqString = "Medium"
        if frequency == FREQ_LIST[3]:
            freqString = "HigherMed"
        if frequency == FREQ_LIST[4]:
            freqString = "High"
            
        attenuationString = ""
        if attenuationRate == ATTENUATION_LIST[0]:
            attenuationString = "Medium"

        phiString = ""
        if secondWaveShift == PHI_LIST[0]:
            phiString = "Low"
        if secondWaveShift == PHI_LIST[1]:
            phiString = "LowerMed"
        if secondWaveShift == PHI_LIST[2]:
            phiString = "Medium"
        if secondWaveShift == PHI_LIST[3]:
            phiString = "HigherMed"
        if secondWaveShift == PHI_LIST[4]:
            phiString = "High"
            
        outputText = gainRatioString + freqString + attenuationString + phiString + ".wav";
        
        write(outputText , RATE, out.astype(np.float32))
        
    return heartBeatWave

# 図出力部分
def PlotGraph(heartBeatWave, gainRatio :float, frequency: float, attenuationRate: float, secondWaveShift: float):
    # plt.title("A="+ str(gain) +", B="+ str(attenuationRate) + ", C=" + str(round(gainRatio,1)) +  ", phi=" + str(phi) + ", f=" + str(frequency), fontsize = 16)
    plt.close()
    plt.ylim(-1, 1)
    plt.yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    plt.xlim(0, RATE)
    plt.xticks([0, RATE/4, RATE*2/4, RATE*3/4, RATE])
    plt.plot(heartBeatWave[0:RATE])
    freqString = ""
    if frequency == FREQ_LIST[0]:
        freqString = "Low"
    if frequency == FREQ_LIST[1]:
        freqString = "LowerMed"
    if frequency == FREQ_LIST[2]:
        freqString = "Medium"
    if frequency == FREQ_LIST[3]:
        freqString = "HigherMed"
    if frequency == FREQ_LIST[4]:
        freqString = "High"
        
    attenuationString = ""
    if attenuationRate == ATTENUATION_LIST[0]:
        attenuationString = "Medium"

    phiString = ""
    if secondWaveShift == PHI_LIST[0]:
        phiString = "Low"
    if secondWaveShift == PHI_LIST[1]:
        phiString = "LowerMed"
    if secondWaveShift == PHI_LIST[2]:
        phiString = "Medium"
    if secondWaveShift == PHI_LIST[3]:
        phiString = "HigherMed"
    if secondWaveShift == PHI_LIST[4]:
        phiString = "High"
        
    gainRatioString = ""
    if gainRatio == GAIN_RATIO_LIST[0]:
        gainRatioString = "Medium"
    
    plt.savefig(gainRatioString + freqString + attenuationString + phiString +  ".png")
    # plt.show()
    
    pass

# 音声を出力
def PlaySound(heartBeatWave, stream):
    print("play sound")
    out = np.tile(heartBeatWave, REPEAT_TIMES)
    stream.write(out.astype(np.float32).tobytes())
    stream.close()
    
    pass

def main():
    for i in [0, 1, 2, 3, 4]:
        gain = GAIN_LIST[i]
        frequency = FREQ_LIST[i]
        for phi in PHI_LIST:
            for attenuationRate in ATTENUATION_LIST:
                    for gainRatio in GAIN_RATIO_LIST:
                        wave = GenerateHeartbeatWave(gain, gainRatio, frequency, attenuationRate, phi, True)
                        PlotGraph(wave, gainRatio, frequency, attenuationRate, phi)


    
    plt.close()
    plt.ylim(-1, 1)
    plt.yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    plt.xlim(0, RATE)
    plt.xticks([0, RATE/4, RATE*2/4, RATE*3/4, RATE])
    plt.plot(wave[0:RATE])
    # plt.show()
    
    
    pass

if __name__ == "__main__":
    main()
