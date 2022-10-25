# 任意の配列からその配列の音声を再生するコード ver.experiment1
from pickle import LIST, TRUE
from telnetlib import GA
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import datetime as dt

RATE = 44100  # 44.1khz
REPEAT_TIMES = 1  # 回心音を鳴らす
DEFAULT_SECOND_WAVE_SHIFT = 0.3 # 心音が1秒に1回なると仮定した際、1音と2音がなる間の時間(sec)
                     # 普通は大体0.3秒くらいらしい
DEFAULT_SECOND_WAVE_LOUDNESS = 0.3 # 1音に対する音量の比。たとえば0.1なら1/10の音量になります。

GAIN_LIST = [1.0, 0.066, 0.095, 0.135, 0.17]
GAIN_RATIO_LIST = [0.3]
ATTENUATION_LIST = [30]
FREQ_LIST = [50, 112.5, 175, 237.5, 300]
WAVE_SHIFT_RATIO_LIST = [0.2, 0.25, 0.3, 0.35, 0.4]
HEART_RATE_LIST = [40, 60, 80, 100, 120]

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

def GenerateHeartbeatWave(gain :float, gainRatio :float, frequency: float, attenuationRate: float, waveShiftRatio: float, heartRate: float, saveSoundOption = False):
    waveEndTime = 60.0 / heartRate
    time = np.arange(RATE*waveEndTime) / RATE  # = t
    attenuationArray = np.exp(-1 * attenuationRate * time) # = exp(-Bt)
    firstWaveShiftRatio = 0.1
    basicWave = gain * np.sin(2 * np.pi * frequency * time) * attenuationArray  # = A*sin(2*PIE*f*t)*exp(-Bt)
    firstWave = np.roll(basicWave, int(RATE * waveEndTime * firstWaveShiftRatio))
    secondWave = gainRatio * np.roll(firstWave, int(RATE * waveEndTime * waveShiftRatio))
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
        if waveShiftRatio == WAVE_SHIFT_RATIO_LIST[0]:
            phiString = "Low"
        if waveShiftRatio == WAVE_SHIFT_RATIO_LIST[1]:
            phiString = "LowerMed"
        if waveShiftRatio == WAVE_SHIFT_RATIO_LIST[2]:
            phiString = "Medium"
        if waveShiftRatio == WAVE_SHIFT_RATIO_LIST[3]:
            phiString = "HigherMed"
        if waveShiftRatio == WAVE_SHIFT_RATIO_LIST[4]:
            phiString = "High"
            
        heartRateString = ""
        if heartRate == HEART_RATE_LIST[0]:
            heartRateString = "Low"
        if heartRate == HEART_RATE_LIST[1]:
            heartRateString = "LowerMed"
        if heartRate == HEART_RATE_LIST[2]:
            heartRateString = "Medium"
        if heartRate == HEART_RATE_LIST[3]:
            heartRateString = "HigherMed"
        if heartRate == HEART_RATE_LIST[4]:
            heartRateString = "High"
            
        outputText = gainRatioString + freqString + attenuationString + phiString + heartRateString + ".wav";
        
        write(outputText , RATE, out.astype(np.float32))
        
    return heartBeatWave

# 図出力部分
def SaveGraph(heartBeatWave, gainRatio :float, frequency: float, attenuationRate: float, heartRate: float, secondWaveShift: float):
    # plt.title("A="+ str(gain) +", B="+ str(attenuationRate) + ", C=" + str(round(gainRatio,1)) +  ", phi=" + str(phi) + ", f=" + str(frequency), fontsize = 16)
    plt.close()
    plt.ylim(-1, 1)
    plt.yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    endTime = RATE * (60.0 / heartRate)
    plt.xlim(0, endTime)
    plt.xticks([0, endTime/4, endTime*2/4, endTime*3/4, endTime])
    plt.plot(heartBeatWave[0:int(endTime)])
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
    if secondWaveShift == WAVE_SHIFT_RATIO_LIST[0]:
        phiString = "Low"
    if secondWaveShift == WAVE_SHIFT_RATIO_LIST[1]:
        phiString = "LowerMed"
    if secondWaveShift == WAVE_SHIFT_RATIO_LIST[2]:
        phiString = "Medium"
    if secondWaveShift == WAVE_SHIFT_RATIO_LIST[3]:
        phiString = "HigherMed"
    if secondWaveShift == WAVE_SHIFT_RATIO_LIST[4]:
        phiString = "High"
        
    heartRateString = ""
    if heartRate == HEART_RATE_LIST[0]:
        heartRateString = "Low"
    if heartRate == HEART_RATE_LIST[1]:
        heartRateString = "LowerMed"
    if heartRate == HEART_RATE_LIST[2]:
        heartRateString = "Medium"
    if heartRate == HEART_RATE_LIST[3]:
        heartRateString = "HigherMed"
    if heartRate == HEART_RATE_LIST[4]:
        heartRateString = "High"
        
    gainRatioString = ""
    if gainRatio == GAIN_RATIO_LIST[0]:
        gainRatioString = "Medium"
    
    plt.savefig(gainRatioString + freqString + attenuationString + phiString + heartRateString +  ".png")
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
        for waveShiftRatio in WAVE_SHIFT_RATIO_LIST:
            for attenuationRate in ATTENUATION_LIST:
                    for gainRatio in GAIN_RATIO_LIST:
                        heartRate = HEART_RATE_LIST[1]
                        wave = GenerateHeartbeatWave(gain, gainRatio, frequency, attenuationRate, waveShiftRatio, heartRate, True)
                        SaveGraph(wave, gainRatio, frequency, attenuationRate, heartRate, waveShiftRatio)
    
    gain = GAIN_LIST[0]
    frequency = FREQ_LIST[0]
    gainRatio = GAIN_RATIO_LIST[0]
    attenuationRate = ATTENUATION_LIST[0]
    waveShiftRatio = WAVE_SHIFT_RATIO_LIST[2]
    for heartRate in HEART_RATE_LIST:
        wave = GenerateHeartbeatWave(gain, gainRatio, frequency, attenuationRate, waveShiftRatio, heartRate, True)
        SaveGraph(wave, gainRatio, frequency, attenuationRate, heartRate, waveShiftRatio)
    
    """
    plt.close()
    plt.ylim(-1, 1)
    plt.yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    plt.xlim(0, RATE)
    plt.xticks([0, RATE/4, RATE*2/4, RATE*3/4, RATE])
    plt.plot(wave[0:RATE])
    plt.show()
    """
    
    pass

if __name__ == "__main__":
    main()
