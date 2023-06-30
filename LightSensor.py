from CameraStops import fstops, sspeed, isonum, modes
from bh1745 import BH1745
import math
from time import sleep

apertureindex = 0
isoindex = 0
speedindex = 0

evcorrection = 2.5                    # A stop adjustment for EV. Set using greycard and Nikond850
                                     # (additive implies a proportional relationship between brightness and lux, check maths)
calibrationconst=15

# Hardware ################################################################################################
'''
try:
    LIGHTSENSOR = {"sda": 2, "scl": 3}
    I2C = pimoroni_i2c.PimoroniI2C(**LIGHTSENSOR)
    bh1745 = breakout_bh1745.BreakoutBH1745(I2C)
    bh1745.leds(False)
except:
    print("sensor?") # A visual cue that therehas been an issue with the sensor setup
'''
# read the value from the light sensor
def sensorread():
    bh1745 = BH1745()

    bh1745.setup()
    bh1745.set_leds(0)

    sleep(1.0)

    rgbc_raw = bh1745.get_rgbc_raw()
    rgb_clamped = bh1745.get_rgbc_raw()
    brightness=rgbc_raw[3]
    print("Clamped: {}, {}, {}, {}".format(*rgb_clamped))
    print("Bright="+str(brightness))
    try:
        EV = math.log2(brightness/calibrationconst)+evcorrection
        print(EV)
    except:
        EV = -10
    return rgb_clamped[0],rgb_clamped[1],rgb_clamped[2],EV

# Derive the appropriate stop value, based on the reading from the sensor and the chosen mode
def otherindex(index, isoindex, mode, lastmeasure):
    Eiso= lastmeasure + math.log2(float(isonum[isoindex]/100))
    if mode=="Av":
        aperture=fstops[index]
        t= (float(aperture)**2)/(2**Eiso)
        #print(t)
        derivedindex = min(range(len(sspeed)), key=lambda i: abs(eval(sspeed[i])-t))
    elif mode=='Tv':
        speed=sspeed[index]
        #print(eval(speed))
        N = math.sqrt(eval(speed)*2**(Eiso))
        #print(N)
        derivedindex = min(range(len(fstops)), key=lambda i: abs(float(fstops[i])-N))
    print(derivedindex)
    return derivedindex

def getExposureIndex(isoindex, speedindex, apertureindex, modeindex):

    isoindex = isoindex
    speedindex = speedindex
    apertureindex = apertureindex

    mode = modes[modeindex]
    print(mode)
    red, green, blue, lastmeasure=sensorread()

    if mode=="Av":
        return otherindex(apertureindex, isoindex, mode, lastmeasure)
    elif mode=='Tv':
        # Now, derive aperture from shutter speed choice and lastmeasure
        return otherindex(speedindex, isoindex, mode, lastmeasure)
    
    return 0

