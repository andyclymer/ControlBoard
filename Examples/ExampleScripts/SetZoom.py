import vanilla
from mojo.events import addObserver, removeObserver
from mojo.UI import CurrentGlyphWindow

class ZoomWindow:

    def __init__(self):
        
        """
        ControlBoard
            "Set Zoom" demo
            
            Use a potentiometer to set the zoom scale of the CurrentGlyphWindow.
        
        """
        
        self.w = vanilla.Window((100, 100), "Zoom")
        self.w.bind("close", self.windowClosed)
        self.w.open()
        
        # Add an observer to watch for a component's state to change
        addObserver(self, "controlChanged", "ControlBoardInput")
        
        self.controlName = "Zoom"                 
   
    def controlChanged(self, info):
        
        # Check that the control that changed has the name were looking for:
        if info["name"] == self.controlName:
            
            # If there's a glyph window open
            w = CurrentGlyphWindow()
            if w:
                # Set the zoom scale of the window.
                # Scale the incoming "value" of the control to somewhere between 0.15% and 3000%
                scale = (info["value"] * 30) + 0.15
                w.setGlyphViewScale(scale)
    
    def windowClosed(self, sender):
        removeObserver(self, "ControlBoardInput")





ZoomWindow()