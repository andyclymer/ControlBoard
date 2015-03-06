from mojo.events import addObserver, removeObserver, postEvent
import vanilla

class ServoDemo:
    
    """
    ControlBoard
        "Servo" component demo
        
        Set a servo motor to the angle of a potentiometer.
    """

    def __init__(self):
        
        # The name of the sensor (the potentiometer) and the servo:
        self.sensorName = "Knob"
        self.servoName = "Servo"
        
        self.w = vanilla.Window((200, 100), "Servo Demo")
        self.w.titleValue = vanilla.TextBox((20, 20, -10, 25), "Current value and angle:")
        self.w.knobValue = vanilla.TextBox((20, 40, -10, 25), "0.0, 0" + chr(176))
        self.w.bind("close", self.windowClosed)
        self.w.open()
        
        addObserver(self, "controlChanged", "ControlBoardInput")

    def controlChanged(self, info):
            
        if info["name"] == self.sensorName:
            
            # Turn the value into a position in degrees between 0 and 180
            pos = info["value"] * 180
            # Update the interface
            newText = str(info["value"]) + ", " + str(pos) + chr(176)
            self.w.knobValue.set(newText)
            # Make the servo motor move to this position by sending it a notification
            postEvent("RoboControlOutput", name="Servo", position=pos)
            
            
    def windowClosed(self, sender):
        removeObserver(self, "ControlBoardInput")
            
            
            

ServoDemo()