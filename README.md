# Telescope-Controller
This repository contains the source code for a simple telescope controller for a telescope with basic stepper motor drives. The controller uses an [Adafruit M4 Feather Express](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/overview) microntroller
and the [Adafruit Stepper + DC Motor Feather wing](https://learn.adafruit.com/adafruit-stepper-dc-motor-featherwing) motot drive. It should be possible to use any sbc or microcontroller development board that is capable of running CircuitPython. The software is written in CircuitPython as a simple control loop so is easy to follow and adapt with alternative libraries and languages to suit.

This project came about as a result of me inheriting a telescope with a German Equatorial Mount that was fitted with stepper motors for a motor drive but didn't have the controller box to power and control the stepper motors. 

The aim of this project was to see if it was possible to make the telescope mount work again and at the same time learn about microcontrollers and similar development boards. 

# Health Warning
The code and the schematics in this project work for me as I have built them in so far as the mount moves as expected. The project as it is presented here is not a replacement for consumer level motor drive its not very practical and its not been fully tested and proven to work; I am waiting to collect some other missing parts for the mount before it can be fully assembled with a telescope to test it in the field. 

The expected problems revolve around how effectively the controller can drive the stepper motors at the right speed and the power draw while its doing that. These are points for further experiment and refinement and devlopement. 

Under no circumstances use the contents of the Frizing document directly. It's a long time since I did anything like this and the first time I've done anything with that software and I really didn't have a clue what I was doing.  

The bread board view looks to be an accurate representation of what I have built, in front of me, if you want to build this project or something based on it, then use the bread board view as a guide and check as you go that the links you are adding make sense. 

The schematics view looks to be technically correct but don't use it as an examplar of how to layout a circuit diagram. 

The pcb schematic should not be used under any circumstance. I have not used it to manufacture from and would recommend that you don't; it was purely a technical exercise to see if I could layout the board without crossing the beams. 

You are welcome to use what you see here and to learn from my mistakes but I make no guarantees regards the quality, functionality or suitability of this project for your application. You can use and adapt the information,ideas and designs contained in this project but you do so entirely at your own risk.

# Hardware
### Breadboard Layout 
![Telescope controller Breadboard Layout](https://github.com/Antelope-IT/telescope-controller/blob/master/docs/Telescope_Controller.png)

## Parts List
The part lists is split into two sections; essential and optional. Although listed as essential this is only because the code has been written to work with this combination of components. It is entirely possible to replace any of the parts with compatible components or indeed similarly functioning components and then adapt the code and libraries to suit the new component. 

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
> The stepper motors are bipolar and by measurement the resistance for each phase was approximately 17-18 Ohms By Ohms law current draw for each phase is expected to be 0.35A. If all 4 phases (2 x motors x 2 phases) are energised at the same time the current draw would be 1.4A. 
>
> The buck converter I'm using is rated at 2A and the battery power pack is rated at 3A so there should be sufficient headroom and room for error. In practice, in operation current draw was measured at the output of the battery pack to be 0.9A with both steppers holding.
>
> The Adafruit Stepper + DC Motor Feather is capable of supplying 1.2A per coil/phase at voltages in the range 4.5v to 13.5v so for this application everything would appear to be within specification.

# Software
## Libraries
## Calculations

**_To be completed..._**
