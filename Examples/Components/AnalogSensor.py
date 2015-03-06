import vanilla
from mojo.events import addObserver, removeObserver

class AnalogSensorDemo:
    
    """
    ControlBoard
        "Analog Sensor" component demo
    """
    
    def __init__(self):
    
        self.w = vanilla.Window((200, 150), "Analog Sensor")
        self.w.titleValue = vanilla.TextBox((20, 20, -10, 25), "Sensor value:")
        self.w.slider = vanilla.Slider((20, 40, -20, 25), maxValue=1)
        self.w.titleName = vanilla.TextBox((20, 70, -20, 25), "Compoonent Name:")
        self.w.componentName = vanilla.EditText((20, 100, -20, 25), "My Component")
        self.w.open()
        
        # When the state of any component on your board changes (button pressed, knob turned), a "ControlBoardInput" 
        # notification will be made. Start observing for these notifications and give a method name in this script
        # to be called when the notification comes in, in this case self.controlChanged
        addObserver(self, "controlChanged", "ControlBoardInput")
        
    def controlChanged(self, info):
        # The notification will come in with an "info" dictionary.
        # The dictionary will always have the key "name" with the name of the component that changed.
        
        # Check to see if this notification is coming from the component that was named in this script's window,
        # that's the one we're looking for:
        if info["name"] == self.w.componentName.get():
            
            # The info dictionary will also have the key "type" with the type of component, 
            # if you need to double check that it's the kind of component you were expecting.
            
            # An "Analog Sensor" component will send its new value with the notification that it had changed
            # Set the slider and text box in the interface with this value
            newValue = info["value"]
            self.w.slider.set(newValue)
            self.w.titleValue.set("Sensor value: " + str(newValue))


AnalogSensorDemo()
