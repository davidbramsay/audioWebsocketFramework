import pyaudio
import struct
import math

FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.02
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)


pa = pyaudio.PyAudio()                                 
stream = pa.open(format = FORMAT,                      
         channels = CHANNELS,                          
         rate = RATE,                                  
         input = True,                               
         frames_per_buffer = INPUT_FRAMES_PER_BLOCK)   

def get_rms(block):
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
    # sample is a signed short in +/- 32768. 
    # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

def aweight_block(block):
        
    
    


for i in range(1000):
    try:
        block = stream.read(INPUT_FRAMES_PER_BLOCK)
        amplitude = get_rms(block)
        print amplitude
    except IOError, e:
        print 'error'
