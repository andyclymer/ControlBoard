

# Control Board

Control Board is a RoboFont extension for communicating with Arduino-compatible devices using the Firmata library. 

It turns physical input events from components connected to the Arduino (pressing buttons, toggling switches, turning knobs) into `ControlBoardInput` event notifications, and turns `ControlBoardOutput` notifications into changes in state of the output components connected to the board (toggling LEDs on and off or changing the color of RGB LEDs, moving motors, etc.)

It makes generous use of the Breakfastserial, pyFirmata and serial Python libraries:
- https://github.com/theycallmeswift/BreakfastSerial
- https://github.com/tino/pyFirmata
- http://pyserial.sourceforge.net


## The state of things

I’m considering this to be a proof of concept for quickly getting simple inputs and ouputs from an Arduino into RoboFont. Currently it doesn’t save any of the settings for which components are attached to a board, and it still requires knowing the names and types of components that other scripts may be looking for.

My plan is to start using this extension as it is to see how I want configurations to be kept: should there be presets for each prototyping board that I attach to the Arduino? Should another extension be able to send a notification to Control Board with a list of component names that it’s looking for, so that the user can quickly get their buttons and LEDs matching up with what another script needs? I’d like to hear more about how others use the extension as well.

The code also makes use of multithreading in Python in a way that might not be entirely safe — it’s definitely possible to crash RoboFont if an action in one thread isn’t able to keep up with one in another thread. This is something I’d like to revisit.

More code examples, shopping lists, and sample circuits will be on their way soon, as well. Otherwise, I think it’s a pretty quick and easy way to get started with making a custom hardware controller for RoboFont, so please give it a try!



## A special Arduino note for Mac OS 10.9 and 10.10 users:

Before you begin, Mac OS 10.9 and 10.10 users will need through a small process of updating the FTDI drivers that came with their computer, in order to be able to communicate with the Arduino.

You can read more about this requirement from the Arduino forum - http://forum.arduino.cc/index.php?topic=198539.0 - or just follow the steps listed below.

1. Start by disabling the FTDI drivers that came with your Mac. In the Terminal, type the following commands 	
	```
	cd /System/Library/Extensions/IOUSBFamily.kext/Contents/PlugIns;
	sudo mv AppleUSBFTDI.kext AppleUSBFTDI.disabled;
	sudo touch /System/Library/Extensions;
	```

2. Restart your computer

3. Install the correct FTDI drivers from http://www.ftdichip.com/Drivers/VCP.htm
    
    You will want to choose either the 32-bit or 64-bit drivers depending on which Mac you have. 
    To find out whether your machine is 32 or 64-bit, have a look here: <https://support.apple.com/en-us/HT3696>

4. After restarting your computer once more for good measure, you will be ready to communicate over USB with your Arduino.


## Arduino Setup:

To use Control Board, you'll need to upload the Standard Firmata library on your Arduino.
 
1, Start by downloading the Arduino IDE software: <http://arduino.cc/en/Main/Software>

2, Plug in your Arduino, and launch the the Arduino application

3, From the menu bar, select File &rarr; Examples &rarr; Firmata &rarr; Standard Firmata

4, From the menu bar, select Tools &rarr; Board &rarr; the Arduino board you're using

5. From the menu bar, select Tools &rarr; Serial Port &rarr; the name of a serial port which contains `USB`

6. At the top of the StandardFirmata window, click the Upload button (it has an up arrow icon)

If all goes well, in a moment your Arduino will have the Standard Firmata library installed on it, and you'll be ready to use Control Board. 
You will only need to set your Arduino up once, it will retain this Standard Firmata library until you upload a new program to it another time.



## Control Board Quick Start

The concept is simple: wire up some basic electronic components to an Arduino's input and output pins, and list what these components are in the Control Board interface. 

The `Input` components (buttons, switches, potentiometers) will broadcast `ControlBoardInput` notifications when their state has changed along with what their current state is. 
Likewise, when you broadcast a `ControlBoardOutput` notification from a separate script to an `Output` component (an LED, motor, etc.) then its state will change.

Control Board will try to connect to the first Arduino it finds connected over USB. 
If the board was plugged in after Control Board was opened, click `Reconnect` to try connecting again.

Once connected, set up your circuit components in the Control Board interface. 
For instance, if you have a button connected to pin #2, add an `Input: Button/Switch` component, choose pin 2, and give the component a name. 
Click `Apply` to send this configuration to your Arduino board.

Now, each time your click the button, `ControlBoardInput` notifications will happen.

The notifications will always have an `info` dictionary. 
The dictionary has a key for the `type` of component (`Button/Switch`, `Sensor`, etc.), a `name` which is the name that you gave the component in the interface, and either a `state` (`up`, `down`) or a `value` (a sensor value between 0 and 1).

To post your own notifications, import the following method from RoboFont's mojo library:
```py
from mojo.events import postEvent
```

Then, post your notification event to the desired component name, with the state the component should take, along with other optional arguments depending on the component. 
For example, you can turn an LED on by posting the following event:

```py
postEvent("ControlBoardOutput", name="My LED", state="on")
```

and then turn it back off by posting this one:

```py
postEvent("ControlBoardOutput", name="My LED", state="off")
```

For a full explanation of all component states and values, check out the sample code in the `/Examples` directory and the table of Component Notifications at the end of this document.

If you're new to the Arduino, a [shopping list](Shopping-List) is coming together on this repo's wiki. More pages will be added with circuit examples as well.


## Component Input/Output Notifications

The incoming notifications tell a lot about how a component's state changed, and an outgoing notification needs to carry the kinds of details about how an output component should change.

See the example code in the `/Examples` directory for a guide to using the notifications documented below.

Here's an overview of the attributes received when observing for a `ControlBoardInput` or sent with a `ControlBoardOutput` notification:

```yaml
- Input: Button/Switch
	"name": string assigned to the component in the Control Board interface. 
	"type": "Button"
	"state": "up", "down", or "hold" when the button is held down for more than one second 

- Input: Rotary Encoder
	"name": string assigned to the component in the Control Board interface. 
	"type": "RotaryEncoder"
	"state": "changed"
	"value": "cw" if it was turned clockwise, or "ccw" if counter-clockwise

- Input: Analog Sensor (Potentiometer, LDR, pressure sensor)
	"name": string assigned to the component in the Control Board interface. 
	"type": "AnalogSensor"
	"state": "changed"
	"value": A float between 0 and 1 of the current sensor value

- Output: LED
	"name": string assigned to the component in the Control Board interface. 
	"state": "on", "off", "toggle", "blink"
	"value": When the state is "on", the value is a float between 0 and 1 to set the brightness of the LED, when state is "blink" the value is the frequency time in milliseconds

- Output: RGB LED
	"name": string assigned to the component in the Control Board interface. 
	"state": "on", "off", "toggle", "blink"
	"value": When the state is "on", the value is either a float between 0 and 1 to set the brightness of all three components, a list of three float values for [R, G, B] between 0 and 1, or the string of the name of a color, such as "red", or "turquoise". When the state is "blink", the value is the value is the frequency time in milliseconds

- Output: Servo Motor
	"name": string assigned to the component in the Control Board interface. 
	"position": The position the motor should turn to, in degrees between 0 and 180.

- Output: DC Motor
	"name": string assigned to the component in the Control Board interface. 
	"state": "on", "off"
	"value": When the state is "on", the value is a float between 0 and 1 of the speed the motor should turn
```

