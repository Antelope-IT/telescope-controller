# Telescope-Controller
This repository contains the source code for a simple telescope controller for a telescope with basic stepper motor drives. The controller uses an [Adafruit M4 Feather Express](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/overview) microntroller
and the [Adafruit Stepper + DC Motor Feather wing](https://learn.adafruit.com/adafruit-stepper-dc-motor-featherwing) motot drive. It should be possible to use any sbc or microcontroller development board that is capable of running CircuitPython. The software is written in CircuitPython as a simple control loop so is easy to follow and adapt with alternative libraries and languages to suit.

This project came about as a result of me inheriting a telescope with a German Equatorial Mount that was fitted with stepper motors for a motor drive but didn't have the controller box to power and control the stepper motors. 

The aim of this project was to see if it was possible to make the telescope mount work again and at the same time learn about microcontrollers and the Arduino ecosystem.

# Hardware
The image below shows a basic breadboard layout as I built it, the layout is organic (as I added the components) rather than logical. A more logical layout would be to put the microcontroller and motor drive board at either end of the breadboard leaving the space between for the controls and indicators. This would result in shorter runs for the 8 control lines at the expense a slightly longer run for the I2C connection (shown green / white) which runs between the microcontroller and the motor drive board. Alternatively the motor drive and the microcontroller can be stacked which would remove the need for the long off board I2C. 

The four push to make switches control the direction of travel of the telescope and sare connected to microcontroller digital inputs D4,D5,D6,D9. These have internal pull-up circuitry and so pull down to ground when pushed. 

The four leds are used to indicate the direction of travel (its not obvious from the telescope due its speed of motion) these are connected to 4 digital outputs A2,A3,A4,A5 of the microcontroller. The leds are connected to ground via 220Ohm resistors to limit the current flow and therefore the brightness of the leds. It increasing the size of these resistors will reduce the brightness of the leds reducing light pollution in operation and help to preserve night vision.  

The stepper motors (not shown) are connected to the two blocks at either end of the motor drive board. The right ascension stepper stepper motor is connected to the stepper 1 via the M1 and M2 terminals on motor drive and the declination motor is connected to stepper 2 via the M3 and M4 terminals. Looking at the top of the board - as seen in image of the bread board above stepper 1 is at the left hand end of the motor drive board and stepper 2 is at the right hand end.  

A separate power supply for the stepper motors is connected via the 2.1mm barrel connector.

A complete Fritzing breadboard and schematic layout can be found in the file controller.fzz in docs directory (See Health Warning). 

### Breadboard Layout 
![Telescope controller Breadboard Layout](https://github.com/Antelope-IT/telescope-controller/blob/master/docs/Telescope_Controller.png)

## Parts List
The parts lists is split into two sections; essential and optional. Although listed as essential this is only because the code has been written to work with this set of components. All parts can be replaced with compatible components and the code can be modified to use the requisite compatible libraries. 

The optional components are listed with the intention of making the project more portable - i.e. disconnected from the main grid. With this in mind a suitably large usb battery pack with two outputs can be used to power the microcontroller and motor drive boards along with A USB 5v to 6v buck converter to power the stepper motors.* 

In the case of the M4 Express Feather microcontroller a 3.7v LiPo battery can be connected to the microcontroller to power both the microcontroller and the motor drive board (logic only). This leaves the battery power pack free to power just the stepper motors.

### Essential
* Microntroller [Adafruit M4 Feather Express](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/overview)
* Motor Drive board [Adafruit Stepper + DC Motor Feather wing](https://learn.adafruit.com/adafruit-stepper-dc-motor-featherwing)
* 2.1mm Barrel connector (female) - centre positive
* 4 x 3mm leds (red)
* 4 x push to make switches
* 4 x 220 Ohm Resistors or higher for reduced light polution
* 6v 1A+ Power supply with 2.1mm barrel connector (male)
* USB Power supply
### Optional (Improved portability)
* USB Battery Pack
* 3.7v LiPo battery
* Ripcord 5v -> 6v USB voltage booster with 2.1mm barrel connector (male)

> *NB. This assumes that the buck converter is capable of supplying the power and sufficient current to drive the stepper motors. In my case I knew the original motor drive kit was designed to run from a 4 x D Cell battery pack providing a nominal 6v.
>
> The stepper motors are bipolar and by measurement the resistance for each phase was approximately 17-18 Ohms By Ohms law the current draw for each phase is expected to be 0.35A. If all 4 phases (2 x motors x 2 phases) are energised at the same time the current draw would be 1.4A. 
>
> The buck converter I'm using is rated at 2A and the battery power pack is rated at 3A so there should be sufficient headroom and room for error. In practice, in operation the current draw was measured at the output of the battery pack to be 0.9A with both steppers holding.
>
> The Adafruit Stepper + DC Motor Feather is capable of supplying 1.2A per coil/phase at voltages in the range 4.5v to 13.5v so 0.4A at 6v is well within the operating range of the device.

# Software
The code is written in CircuitPython version 5.3.0. The microcontroller will automatically load and run code.py at startup. The code has a setup phase followed by a continuous loop. The code depends on a number of libraries(see below).

In the setup phase the hardware is initialised and timing constants are declared. The timing constants are used to divide the cycle rate of loop so that the stepper motors are advanced at the calculated intervals. Provided that the cycle rate of the loop is sufficiently faster than the rate of stepper motor movement this should be fine.

The defining timing constant is the raDelay constant - the calculation for which is shown below. This value is the delay in seconds between steps of the Right Ascension stepper motor needed to drive the telescope so that it tracks across the sky at the right speed (if I've calculated correctly). The limitations of the stepper motors used means that it can't operate as a goto motor drive - the motors and gearing mean it can't physically move fast enough. To this end RA movement is essentially stop or go, future developments might be to add some means of finer adjustment. The DEC movement is simply for finer adjustment up and down this movement is four times the speed of the RA movement. The value four was selected because its known to give a rate of movement within the operating range of the stepper motors.

The motor step rates are further divided by 8 ( 4 x microsteps per single step / 32 ) to provide a clock rate to drive the indicator leds so that they flash when the motor is moving in indicated direction.

More work could be done to refine and improve this code but it should be remembered that there is no Decimal library for CircuitPython and no Async library (AFAIK) so precision will be limited by the floating precision and the fastest rate at which the processor can traverse the loop of code. It also has to be remembered that not withstanding the limitations inherent in the code, there are also the limitations in the hardware; the stepper motors, gears etc. Hence the health warning regards this isn't a replacement for a consumer grade telescope motor drive.      

## Libraries
The code has the folowing dependencies these are standard Adafruit libraries which can be found in the [CircuitPython libraries and drivers bundel](https://github.com/adafruit/Adafruit_CircuitPython_Bundle). Download the zip, extract it and copy the required libraries to the CircuitPy/lib folder as required.

* Adafruit_Bus_Device
* Adafruit_Register
* Adafruit_PCA9685
* Adafruit SimpleIO
* Adafruit_Motor_Kit
* Adafruit_Motor

An additional dependency is the debouncer library this can be found in the [CircuitPython Community Bundle](https://github.com/adafruit/CircuitPython_Community_Bundle).

* Adafruit_Debouncer 

Add these libraries to the lib folder in CircuitPy directory before running the code.

## Calculations

These calculations serve two purposes: they remind me how I arrived at the figures in the code and for anyone wanting to replicate this project they should serve as a guide on how to adapt the code to their own hardware.

```
  Stepper motor:
    steps / rotation (input shaft) = 48
    gear ratio input shaft : output shaft = 120:1
  
    Steps per rotation = 48 x 120 = 5760 steps per full rotatio of the Stepper motor drive(output) shaft 
    
    The figures of 48 and 120 were found online but could be wrong - no identification markings on the stepper motors so no way to know for sure.
    The figure of 5760 has ben confirmed by experiment (to a good approximation).
    
  Telescope mount:
    By experiment 128 rotations of RA control to turn the telescope head through 360 degrees. (to a good approximation)
    
    Total steps required to turn the telescope head through 360 degrees = 128 x 5760 = _737280_
    
    1 day = 86400 sec 
    
    So to rotate the telescope head at the rate of 1 rotation per day the stepper motor needs to be driven at:
    
    737280 / 86400 steps/sec  = 8.5333 s/s
    
    To achieve this we need a step every 1 / 8.5333s = 0.1171875s <= This gives the RA delay figure 
    
  Refinement:
    The sidereal day - the length of time before the stars are in the same place relative to the earth changes through the year but the mean sidereal day is
    23h 56m 4.0905s. If we take this figure as the length of the day then:
    
    737280 / 86164.0905 steps/sec  = 8.55669 s/s
  
    Which gives a delay of 0.1168675s between steps of the RA stepper motor and this is the figure in the code.
    
    NB. The length of a sidereal day, as given, is only an approximation. Comparing the results of using the two RA Delay figures, after running the mount for a whole day, the difference in pointing angle is just less than 1 degree.
```

# Health Warning
The code and the schematics in this project work for me as I have built them in so far as the mount moves as expected. The project as it is presented here is not a replacement for a consumer level motor drive its not very practical and its not been fully tested and proven to work; I am waiting to collect some other missing parts for the mount before it can be fully assembled with a telescope to test it in the field. 

The expected problems revolve around how effectively the controller can drive the stepper motors at the right speed and the power draw while its doing that. These are points for further experiment, refinement and devlopement. 

Under no circumstances use the contents of the Frizing document directly. It's a long time since I did anything like this and the first time I've done anything with that software and I really didn't have a clue what I was doing.  

The bread board view looks to be an accurate representation of what I have built, if you want to build this project or something based on it, then use the bread board view as a guide and check as you go that the links you are adding make sense. 

The schematics view looks to be technically correct but don't use it as an examplar of how to layout a circuit diagram. 

The pcb schematic should not be used under any circumstance. I have not used it to manufacture from and would recommend that you don't; it was purely a technical exercise to see if I could layout the board without crossing the beams. 

You are welcome to use what you see here and to learn from my mistakes but I make no guarantees regards the quality, functionality or suitability of this project for your application. You are free to use and adapt the information, ideas and designs contained in this project but you do so entirely at your own risk.
