import drivers
from time import sleep, time
import RPi.GPIO as GPIO
import UltrasonicSensor
import ButtonActions
import Buttons
from CameraStops import sspeed, fstops, isonum, modes
import LightSensor

Buttons.setupButtons()

LCD = drivers.Lcd()

mode_index = -1
next_mode_index = 0

current_iso_index = 18
current_fstop_index = 35
current_sspeed_index = 21

LCD.lcd_display_string("Dan's Light", 1)
LCD.lcd_display_string("Meter", 2)

try:
    while True:
        button_state_mode = GPIO.input(Buttons.modeButton)
        button_state_set = GPIO.input(Buttons.setButton)
        button_state_measure = GPIO.input(Buttons.measureButton)

        if button_state_measure == 0:
            sleep(0.2)
            
            if mode_index == 0:
                current_sspeed_index = LightSensor.getExposureIndex(current_iso_index, current_sspeed_index, current_fstop_index, mode_index)

                LCD.lcd_clear()
                LCD.lcd_display_string(str(sspeed[current_sspeed_index]) + "s f" + str(fstops[current_fstop_index]), 1)
                LCD.lcd_display_string("ISO " + str(isonum[current_iso_index]) + "   Av", 2)
            elif mode_index == 1:
                current_fstop_index = LightSensor.getExposureIndex(current_iso_index, current_sspeed_index, current_fstop_index, mode_index)

                LCD.lcd_clear()
                LCD.lcd_display_string(str(sspeed[current_sspeed_index]) + "s f" + str(fstops[current_fstop_index]), 1)
                LCD.lcd_display_string("ISO " + str(isonum[current_iso_index]) + "   Tv", 2)

            elif mode_index == 2:
                LCD.lcd_clear() 
                LCD.lcd_display_string("Calculating", 1)
                LCD.lcd_display_string("Distance...", 2)
                distance = UltrasonicSensor.calcuateDistance()
                LCD.lcd_clear()
                LCD.lcd_display_string("Dist: " + str(round(distance / 100, 2)) + " m", 1)
                LCD.lcd_display_string("Set-Refresh Dist.", 2)


        if button_state_set == 0:            

            if mode_index == 0 or 1: #If in Av or Tv
                current_iso_index = ButtonActions.setISO(current_iso_index)

                if mode_index == 0:
                    current_fstop_index = ButtonActions.setFstop(current_iso_index, current_fstop_index, current_sspeed_index, mode_index)

                elif mode_index == 1:
                    current_sspeed_index = ButtonActions.setSspeed(current_iso_index, current_fstop_index, current_sspeed_index, mode_index)


        if button_state_mode == 0:

            if next_mode_index == 0:
                current_sspeed_index = LightSensor.getExposureIndex(current_iso_index, current_sspeed_index, current_fstop_index, next_mode_index)

                LCD.lcd_clear()
                LCD.lcd_display_string(str(sspeed[current_sspeed_index]) + "s f" + str(fstops[current_fstop_index]), 1)
                LCD.lcd_display_string("ISO " + str(isonum[current_iso_index]) + "   Av", 2)

                mode_index = next_mode_index
                next_mode_index = mode_index + 1 
                

            elif next_mode_index == 1:

                current_fstop_index = LightSensor.getExposureIndex(current_iso_index, current_sspeed_index, current_fstop_index, next_mode_index)

                LCD.lcd_clear()
                LCD.lcd_display_string(str(sspeed[current_sspeed_index]) + "s f" + str(fstops[current_fstop_index]), 1)
                LCD.lcd_display_string("ISO " + str(isonum[current_iso_index]) + "   Tv", 2)

                mode_index = next_mode_index
                next_mode_index = mode_index + 1
                

            elif next_mode_index == 2:
                LCD.lcd_clear() 
                LCD.lcd_display_string("Calculating", 1)
                LCD.lcd_display_string("Distance...", 2)
                distance = UltrasonicSensor.calcuateDistance()
                LCD.lcd_clear()
                LCD.lcd_display_string("Dist: " + str(round(distance / 100, 2)) + " m", 1)
                LCD.lcd_display_string("Set-Refresh Dist.", 2)

                mode_index = next_mode_index
                next_mode_index = 0
                
            sleep(0.2)


except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    LCD.lcd_clear()
