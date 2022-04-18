import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal
import soundfile as sf

plt.close('all')

input_file = u"sweep.csv"
data = np.loadtxt(input_file, unpack=True, delimiter=",",usecols = 1)

fs = 1250 # サンプリング周波数
f0,t0,Sxx0 = signal.spectrogram(data, fs, nperseg=256)

plt.figure()
plt.pcolormesh(t0,f0,Sxx0,vmax=1e-6)
plt.xlim([4,37])
plt.xlabel(u"time [sec]")
plt.ylabel(u"frequency [Hz]")
plt.colorbar()
plt.show()


path = '/Users/renmahirano/programming/PlaySound_Python/sweep.wav'
wavTuple = sf.read(path)
wavNumpy = np.array(wavTuple[0])
wavFs = 44100
f1,t1,Sxx1 = signal.spectrogram(wavNumpy, wavFs, nperseg=4096)

plt.figure()
plt.pcolormesh(t1,f1,Sxx1,vmax=1e-6)
plt.xlim([0,30])
plt.ylim([0,800])
plt.colorbar()
plt.show()
