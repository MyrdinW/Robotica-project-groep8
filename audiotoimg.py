import pyaudio #moet geinstalleerd worden
import time
import numpy as np
import pylab as plt #install matplotlib (krijg je numpy automatisch bij)

RATE = 44100
CHUNK = int(RATE/20) # RATE / number of updates per second

def soundtoimg(stream):
    t1=time.time()
    data = np.frombuffer(stream.read(CHUNK),dtype=np.int16)
    plt.plot(data, 'r')
    plt.title(i)
    plt.grid()
    plt.axis([0,len(data),-2**16/2,2**16/2])
    plt.savefig("01.png",dpi=50)
    plt.close('all')
    #print("plotting sound to image took %.02f ms"%((time.time()-t1)*1000))

if __name__=="__main__":
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    for i in range(int(20*RATE/CHUNK)): #do this for 10 seconds
        soundtoimg(stream)
    stream.stop_stream()
    stream.close()
    p.terminate()