from vanilla import *
from mojo.events import postEvent

class ProgressBarDemo(object):
        
    def __init__(self):
        
        """
        ControlBoard
            "Progress LED" demo
            
            Starting from Vanilla's Progress Bar demo code, 
            add a few more lines to turn an LED into a progress indicator.
            The LED will sweep through a range of values for hue, 
            and will strobe in the last 80% of the progress.
        
        """
        
        self.w = Window((200, 65))
        self.w.bar = ProgressBar((10, 10, -10, 16))
        self.w.button = Button((10, 35, -10, 20), "Go!", callback=self.showProgress)
        self.w.open()

    def showProgress(self, sender):
        import time
        totalSteps = 100
        self.w.bar.set(0)
        for i in range(totalSteps):
            self.w.bar.increment(1)
            if i/totalSteps < 0.8:
                # The progress is less than 80% of the way through.
                # Use two numbers for the "value", to set the hue and brightness of the LED.
                postEvent("ControlBoardOutput", name="Status Light", state="on", value=(i/totalSteps, 1))
            else:
                # It's within the last 80% of the progress, switch over to blinking at 100/ms
                postEvent("ControlBoardOutput", name="Status Light", state="blink", value=100)
            time.sleep(.05)
        # Progress is done, be sure to turn the LED off!
        postEvent("ControlBoardOutput", name="Status Light", state="off")
            

ProgressBarDemo()

