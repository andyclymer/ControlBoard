import vanilla
from mojo.events import addObserver, removeObserver

class ButtonDemo:
    
    """
    ControlBoard
        "Button/Switch" component demo
    """
    
    def __init__(self):
    
        self.w = vanilla.Window((200, 150), "Button/Switch")
        self.w.titleState = vanilla.TextBox((20, 20, -10, 25), "Button is: ...")
        self.w.titleName = vanilla.TextBox((20, 70, -20, 25), "Button/Switch Name:")
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
            
            # A "Button/Switch" component will notify you with its current "state",
            # whether it's "up", "down", or if the button is "hold" when it's held down
            if "state" in info.keys():
                currentState = info["state"]
                self.w.titleState.set("Button is: " + currentState)


ButtonDemo()
