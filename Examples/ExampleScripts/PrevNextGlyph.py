from mojo.UI import CurrentGlyphWindow
from mojo.events import addObserver, removeObserver
import vanilla


class PrevNextGlyph:
    
    """
    ControlBoard
        "PrevNextGlyph" demo
        
        Use a Rotary Encoder component to swtich the Current Glyph Window to the previous or next glyphs.
        After removing the code for the sample window, this script could be used as a Startup Script
    
    """
    
    def __init__(self):
        
        self.w = vanilla.Window((100, 100), "Previous/Next Glyph")
        self.w.bind("close", self.windowClosed)
        self.w.open()
        
        # When the state of any component on your board changes (button pressed, knob turned), a "ControlBoardInput" 
        # notification will be made. Start observing for these notifications and give a method name in this script
        # to be called when the notification comes in, in this case self.controlChanged
        addObserver(self, "controlChanged", "ControlBoardInput")
        self.controlName = "Rotary"
        
    def controlChanged(self, info):
        
        # Make sure the RoboControlInput notificaiton is for the desired control name:
        if info["name"] == self.controlName:
            
            # Figure out some info about the current glyph, and current glyph window
            glyph = CurrentGlyph()
            font = CurrentFont()
            glyphOrder = []
            if font:
                glyphOrder = font.lib["public.glyphOrder"]
            
            # If there's a glyph window open:
            w = CurrentGlyphWindow()
            if w:
                # Find this glyph's index in the glyphOrder
                thisGlyphIndex = glyphOrder.index(glyph.name)
                prevGlyphIndex = thisGlyphIndex - 1
                nextGlyphIndex = thisGlyphIndex + 1
                if nextGlyphIndex == len(glyphOrder):
                    nextGlyphIndex = 0
                elif prevGlyphIndex < 0:
                    prevGlyphIndex = len(glyphOrder) - 1
                # Then, find the previous/next glyph names
                prevGlyphName = glyphOrder[prevGlyphIndex]
                nextGlyphName = glyphOrder[nextGlyphIndex]
                
                # Now that we know something about the current glyph and its neighbors:
                if info["value"] == "cw":
                    # Move clockwise, next glypyh
                    w.setGlyphByName(nextGlyphName)
                elif info["value"] == "ccw":
                    # Counter-clockwise, prev glyph
                    w.setGlyphByName(prevGlyphName)
                    
    def windowClosed(self, sender):
        removeObserver(self, "ControlBoardInput")
                    
PrevNextGlyph()
                    
                    