import drivers
import RPi.GPIO as GPIO
from time import sleep
import Buttons
from CameraStops import sspeed, fstops, isonum, modes
import LightSensor

LCD = drivers.Lcd()

def setISO(iso_index: int):
    current_iso_index = iso_index
    sleep(0.2)
    LCD.lcd_clear()
    LCD.lcd_display_string("ISO " + str(isonum[current_iso_index]), 2)
    while True:
        if GPIO.input(Buttons.setButton) == 0:
            sleep(0.2)
            LCD.lcd_clear()
            return current_iso_index
        if GPIO.input(Buttons.modeButton) == 0:
            current_iso_index -= 1
            if current_iso_index == -1:
                current_iso_index = len(isonum)-1
            LCD.lcd_display_string("ISO       ", 2)
            LCD.lcd_display_string("ISO " + str(isonum[current_iso_index]), 2)
            sleep(0.2)
        elif GPIO.input(Buttons.measureButton) == 0:
            current_iso_index += 1
            if current_iso_index == len(isonum):
                current_iso_index = 0
            LCD.lcd_display_string("ISO       ", 2)
            LCD.lcd_display_string("ISO " + str(isonum[current_iso_index]), 2)
            sleep(0.2)

def setFstop(iso_index: int, fstop_index: int, sspeed_index: int, mode_index: int):
    current_fstop_index = fstop_index
    sleep(0.2)
    LCD.lcd_clear()
    LCD.lcd_display_string("f" + str(fstops[current_fstop_index]), 1)
    while True:
        if GPIO.input(Buttons.setButton) == 0:
            sspeed_index = LightSensor.getExposureIndex(iso_index, sspeed_index, current_fstop_index, mode_index)
            sleep(0.2)
            LCD.lcd_clear()
            LCD.lcd_display_string(str(sspeed[sspeed_index]) + "s f" + str(fstops[current_fstop_index]), 1)
            LCD.lcd_display_string("ISO " + str(isonum[iso_index]) + "   " + modes[mode_index], 2)
            return current_fstop_index
        if GPIO.input(Buttons.modeButton) == 0:
            current_fstop_index += 1
            if current_fstop_index == len(fstops):
                current_fstop_index = 0
            LCD.lcd_display_string("f               ", 1)
            LCD.lcd_display_string("f" + str(fstops[current_fstop_index]), 1)
            sleep(0.2)
        elif GPIO.input(Buttons.measureButton) == 0:
            current_fstop_index -= 1
            if current_fstop_index == -1:
                current_fstop_index = len(fstops)-1
            LCD.lcd_display_string("f               ", 1)
            LCD.lcd_display_string("f" + str(fstops[current_fstop_index]), 1)
            sleep(0.2)

def setSspeed(iso_index: int, fstop_index: int, sspeed_index: int, mode_index: int):
    current_sspeed_index = sspeed_index
    sleep(0.2)
    LCD.lcd_clear()
    LCD.lcd_display_string(str(sspeed[current_sspeed_index]) + "s", 1)
    while True:
        if GPIO.input(Buttons.setButton) == 0:
            fstop_index = LightSensor.getExposureIndex(iso_index, current_sspeed_index, fstop_index, mode_index)
            sleep(0.2)
            LCD.lcd_clear()
            LCD.lcd_display_string(str(sspeed[current_sspeed_index]) + "s f" + str(fstops[fstop_index]), 1)
            LCD.lcd_display_string("ISO " + str(isonum[iso_index]) + "   " + modes[mode_index], 2)
            return current_sspeed_index
        if GPIO.input(Buttons.modeButton) == 0:
            current_sspeed_index += 1
            if current_sspeed_index == len(sspeed):
                current_sspeed_index = 0
            LCD.lcd_clear()
            LCD.lcd_display_string(str(sspeed[current_sspeed_index]) + "s", 1)
            sleep(0.2)
        elif GPIO.input(Buttons.measureButton) == 0:
            current_sspeed_index -= 1
            if current_sspeed_index == 0:
                current_sspeed_index = len(sspeed)-1
            LCD.lcd_clear()
            LCD.lcd_display_string(str(sspeed[current_sspeed_index]) + "s", 1)
            sleep(0.2)

            