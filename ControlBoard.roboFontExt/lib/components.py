import BreakfastSerial as BSer
from mojo.events import addObserver, removeObserver, postEvent
import types
import string
import os
import colorsys


"""

Helper objects to add more functionality to BreakfastSerial components,
and to handle incoming and outgoing "ControlBoardInput" and "ControlBoardOutput" notifications.

"""


# The RGB LED can be set to the color names from the XKCD Color Survey:
# http://xkcd.com/color/rgb/
# Process this text file of color names into a usable format:
extensionPath = os.path.dirname(__file__)
colorFilePath = os.path.join(extensionPath, "rgb.txt")
colorFile = open(colorFilePath, "r")
colorText = colorFile.read()
colorFile.close()
colorNames = {}
for line in string.split(colorText, "\n"):
    if "\t" in line:
        lineSplit = string.split(line, "\t")
        colorName = lineSplit[0]
        hexValue = lineSplit[1][1:7]
        decValue = (int(hexValue[0:2], 16)/255.0, int(hexValue[2:4], 16)/255.0, int(hexValue[4:6], 16)/255.0)
        colorNames[colorName] = decValue
# Change a few color names to more pure values
pureColorNames = {
    "red": (1, 0, 0),       "dark red": (0.15, 0, 0),
    "green": (0, 1, 0),     "dark green": (0, 0.15, 0),
    "blue": (0, 0, 1),      "dark blue": (0, 0, 0.15),
    "yellow": (1, 1, 0),    "dark yellow": (0.15, 0.15, 0),
    "cyan": (0, 1, 1),      "dark cyan": (0, 0.15, 0.15),
    "purple": (1, 0, 1),    "dark purple": (0.15, 0, 0.15),
    "magenta": (1, 0, 1),   "dark magenta": (0.15, 0, 0.15),
    "white": (1, 1, 1),
    "black": (0, 0, 0)}
colorNames.update(pureColorNames)




def fixValue(value, minValue=0, maxValue=1):
    # Keep a value from being less than 0 or greater than 1
    # Optionally scale the value at the same time
    if value <= minValue:
        return minValue
    elif value >= maxValue:
        return maxValue
    else: return value




class ComponentLED(object):
    
    def __init__(self, board, pinList, name):
        
        self.board = board
        self.name = name
        self.pin = pinList[0] 
        # BreakfastSerial component object:
        self.component = BSer.Led(self.board, self.pin)
        # Subscribe to all ControlBoardOutput notifications
        addObserver(self, "outputCallback", "ControlBoardOutput")
        
    def outputCallback(self, info):
        # "info" dictionary always has keys "name", "state", and optionally a "value" which some states need
        
        # Check to see if the notification "name" is the same as this object before proceeding
        if info["name"] == self.name:
            
            # Only change state if "state" came in as a key
            if "state" in info:
            
                # Then, set the state:
                if info["state"] == "on":
                    if not "value" in info:
                        # There's no brightness level, just turn it on
                        self.component.on()
                    elif type(info["value"]) in [types.FloatType, types.IntType]:
                        # Scale the value to be between 0 and 100
                        self.component.brightness(fixValue(info["value"])*100)
                
                elif info["state"] == "off":
                    self.component.off()
                
                elif info["state"] == "toggle":
                    self.component.toggle()
                
                elif info["state"] == "blink":
                    time = 200
                    if "value" in info:
                        time = float(info["value"])
                    self.component.blink(time)
        
    def stop(self):
        self.component.off()
        # Stop watching for notifications
        removeObserver(self, "ControlBoardOutput")
        
        


class ComponentRGBLED(object):
    
    """
    To Do:
        Blink at a specific color value, or at least blink each color component individually?
    """
    
    def __init__(self, board, pinList, name):
        
        self.board = board
        self.name = name
        self.pinRed = pinList[0] 
        self.pinGreen = pinList[1] 
        self.pinBlue = pinList[2] 
        # BreakfastSerial component object:
        self._red = ComponentLED(self.board, [self.pinRed], self.name + "-Red")
        self._green = ComponentLED(self.board, [self.pinGreen], self.name + "-Green")
        self._blue = ComponentLED(self.board, [self.pinBlue], self.name + "-Blue")
        # Subscribe to all ControlBoardOutput notifications
        addObserver(self, "outputCallback", "ControlBoardOutput")
        
    def outputCallback(self, info):
        # "info" dictionary always has keys "name", "state", and optionally a "value" which some states need
        
        # Check to see if the notification "name" is the same as this object before proceeding
        if info["name"] == self.name:
            
            # Only change state if "state" came in as a key
            if "state" in info:
                
                # Default the color value to white
                colorValue = (1, 1, 1)
                
                if "value" in info:
                    # There was a color value
                    value = info["value"]
                    
                    if type(value) == types.StringType:
                        # Color was a name
                        colorName = value.lower()
                        if colorName in colorNames:
                            colorValue = colorNames[colorName]
                    
                    else:
                        if len(value) == 1:
                            # One single value, set all R, G, and B to the same level
                            colorValue = (fixValue(value), fixValue(value), fixValue(value))
                        
                        elif len(value) == 2:
                            # Two values, this is Hue and Level (saturation is always at 100%)
                            colorValue = colorsys.hsv_to_rgb(value[0], 1, value[1])
                            
                        elif len(value) == 3:
                            # Three values: R, G, B
                            colorValue = (fixValue(value[0]), fixValue(value[1]), fixValue(value[2]))

                # Then, set the state:
                if info["state"] == "on":
                    # Scale the values by 100
                    scaledColorValue = [v*100 for v in colorValue]
                    self._red.component.brightness(scaledColorValue[0])
                    self._green.component.brightness(scaledColorValue[1])
                    self._blue.component.brightness(scaledColorValue[2])
                            
                elif info["state"] == "off":
                    self._red.component.off()
                    self._green.component.off()
                    self._blue.component.off()
                
                elif info["state"] == "toggle":
                    self._red.component.toggle()
                    self._green.component.toggle()
                    self._blue.component.toggle()
                
                elif info["state"] == "blink":
                    time = 200
                    if "value" in info:
                        time = float(info["value"])
                    self._red.component.blink(time)
                    self._green.component.blink(time)
                    self._blue.component.blink(time)
                
                elif info["state"] == "fade":
                    # Rainbow fade
                    pass
        
    def stop(self):
        self._red.component.off()
        self._green.component.off()
        self._blue.component.off()
        # Stop watching for notifications
        removeObserver(self, "ControlBoardOutput")




class ComponentServo(BSer.Servo):

    def __init__(self, board, pinList, name):

        self.board = board
        self.name = name
        self.pin = pinList[0]
        self.type = "Servo"
        # BreakfastSerial component object:
        self.component = BSer.Servo(self.board, self.pin)
        self.component.set_position(90)
        # Subscribe to all ControlBoardOutput notifications
        addObserver(self, "outputCallback", "ControlBoardOutput")

    def outputCallback(self, info):
        # "info" dictionary always has keys "name" and "position" for the position in degrees

        # Check to see if the notification "name" is the same as this object before proceeding
        if info["name"] == self.name:

            # Only change state if "position" came in as a key
            if "position" in info:
                if type(info["position"]) in [types.FloatType, types.IntType]:
                    finalPosition = fixValue(info["position"], maxValue=180)
                    self.component.set_position(finalPosition)

    def stop(self):
        # Stop watching for notifications
        removeObserver(self, "ControlBoardOutput")
        



class ComponentMotor(BSer.Motor):

    def __init__(self, board, pinList, name):

        self.board = board
        self.name = name
        self.pin = pinList[0]
        self.type = "Motor"
        # BreakfastSerial component object:
        self.component = BSer.Motor(self.board, self.pin)
        # Subscribe to all ControlBoardOutput notifications
        addObserver(self, "outputCallback", "ControlBoardOutput")

    def outputCallback(self, info):
        # "info" dictionary always has keys "name" and "speed" for the motor speed

        # Check to see if the notification "name" is the same as this object before proceeding
        if info["name"] == self.name:

            # Only change state if "position" came in as a key
            if "state" in info:
                
                if info["state"] in ["stop", "off", False]:
                    self.component.stop()
                elif info["state"] in ["start", "on", True]:
                    speed = 50
                    if "value" in info.keys():
                        if type(info["value"]) in [types.FloatType, types.IntType]:
                            speed = fixValue(info["value"]) * 100
                    self.component.start(speed)

    def stop(self):
        # Stop the motor
        self.component.stop()
        # Stop watching for notifications
        removeObserver(self, "ControlBoardOutput")
        
        
        


class ComponentButton(BSer.Button):
    
    def __init__(self, board, pinList, name):
        
        self.board = board
        self.name = name
        self.pin = pinList[0]
        self.type = "Button"
        # BreakfastSerial component object:
        self.component = BSer.Button(self.board, self.pin)
        # Hold a list of values as the input changes,
        # ...a timer will post an event with the most current value and reset the list
        self.values = []
        # Configure the callbacks for this component object
        self.component.down(self.downCallback)
        self.component.up(self.upCallback)
        self.component.hold(self.holdCallback)
        # Start a timer to call self.reportValueCallback on a regular basis, so that we don't flood RoboFont
        # 16 millis is just over 60 samples per second, drawing the result at 60fps to a window should be plenty fast.
        # This keeps all the sensors from flooding RoboFont with data.
        self._interval = BSer.util.setInterval(self.reportValueCallback, 16)
        
    def downCallback(self):
        self.values += ["down"]
        
    def upCallback(self):
        self.values += ["up"]
        
    def holdCallback(self):
        self.values += ["hold"]
        
    def reportValueCallback(self):
       if self.values:
           postEvent("ControlBoardInput", name=self.name, state=self.values[0], type=self.type)
           self.values = self.values[1:]

    def stop(self):
        pass





class ComponentRotaryEncoder(BSer.RotaryEncoder):
    
    def __init__(self, board, pinList, name):
        
        self.board = board
        self.name = name
        self.pinA = pinList[0]
        self.pinB = pinList[1]
        self.type = "RotaryEncoder"
        # BreakfastSerial component object:
        self.component = BSer.RotaryEncoder(self.board, pinList)
        # Hold a list of values as the input changes,
        # ...a timer will post an event with the most current value and reset the list
        self.values = []
        # Configure the callbacks for this component object
        self.component.cw(self.cwCallback)
        self.component.ccw(self.ccwCallback)
        # Start a timer to call self.reportValueCallback on a regular basis, so that we don't flood RoboFont
        # 16 millis is just over 60 samples per second, drawing the result at 60fps to a window should be plenty fast.
        # This keeps all the sensors from flooding RoboFont with data.
        self._interval = BSer.util.setInterval(self.reportValueCallback, 16)
        
    def cwCallback(self):
        # Encoder was rotated clockwise
        self.values += ["cw"]
        
    def ccwCallback(self):
        # Encoder was rotated counter-clockwise
        self.values += ["ccw"]
        
    def reportValueCallback(self):
       if self.values:
           postEvent("ControlBoardInput", name=self.name, state="changed", value=self.values[0], type=self.type)
           self.values = self.values[1:]

    def stop(self):
        pass





class ComponentSensor(BSer.Sensor):
    
    def __init__(self, board, pinList, name):
        
        self.board = board
        self.name = name
        self.pin = pinList[0]
        self.type = "Sensor"
        # BreakfastSerial component object:
        self.component = BSer.Sensor(self.board, self.pin)
        # Hold a list of values as the input changes,
        # ...a timer will post an event with the most current value and reset the list
        self.values = []
        # Configure the callbacks for this component object
        self.component.change(self.changeCallback)
        # Start a timer to call self.reportValueCallback on a regular basis, so that we don't flood RoboFont
        # 16 millis is just over 60 samples per second, drawing the result at 60fps to a window should be plenty fast.
        # This keeps all the sensors from flooding RoboFont with data.
        self._interval = BSer.util.setInterval(self.reportValueCallback, 16)
        
    def changeCallback(self):
        # Value changed, hold it in the list for now
        value = self.component.value
        self.values.append(value)
    
    def reportValueCallback(self):
        # The setInterval timer will call back to this method at a regular interval.
        # Check to see if there are any new values to report, if there are post the most current value and reset the list
        if self.values:
            postEvent("ControlBoardInput", name=self.name, state="changed", value=self.values[-1], type=self.type)
            del self.values[:]

    def stop(self):
        pass

