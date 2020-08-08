# Telescope-Controller
This repository contains the source code for a simple telescope controller for a telescope with basic stepper motor drives. The controller uses an [Adafruit M4 Feather Express](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/overview) 
and the [Adafruit Stepper + DC Motor Feather wing](https://learn.adafruit.com/adafruit-stepper-dc-motor-featherwing) although it should be possible to use any sbc or microcontroller 
development board that is capable of running CircuitPython. The software is written in CircuitPython and is fairly simple so should be amenable for translation to your language of choice. 

This project came about as a result of me inheriting a telescope with a German Equatorial Mount tripod that was fitted with stepper motor drives but didn't have the controller box to power and control the stepper motors. 

The aim of this project was to see if it was possible to make the telescope mount work again and at the same time learn about Arduino compatible development boards. 

# Health Warning
The code and the schematics in this project work for me as I have built them in so far as the mount moves as expected. The project as it is presented here is not a replacement for consumer level motor drive its not very practical and its not been fully tested and proven to work; I am
waiting to collect some other missing parts for my mount before I can fully assemble the tripod with a telescope and the drive controller and test it in the field. As stated, it does work expected problems revolve around how effectively the controller can drive the
stepper motors at the right speed and the power draw while its doing that. These are points for further experiment and refinement. You are welcome to use what you see here and to learn from my mistakes but I make no guarantees regards the quality or the functionality of contents of this project. You can use and adapt the information,
ideas and designs contained in this project but you do so at your own risk.

Under no circumstances use the contents of the Frizing document directly. Its the first time I've done anything with that software and I really didn't have a clue what I was doing. 

The bread board view looks to be an accurate representation of what I have built in front of me, if you want to build this project or something based on it, for yourself then use the bread board view as a guide and check as you go that the links you are adding make sense. 

The schematics view looks to be technically correct but don't use it as an examplar of how to layout a circuit diagram. 

The pcb schematic should not be used to manufacture from; I haven't. It was purely a technical exercise to see if I could layout the board without crossing the beams. I've succeeded in that but its not suitable for manufacture. 

More to come, Work in progress... 
